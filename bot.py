#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
import yt_dlp
import requests
from ShazamAPI import Shazam
import subprocess
import tempfile
from dotenv import load_dotenv
import librosa

# .env faylini yuklash
load_dotenv()

# Logging sozlamasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram bot token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")

# Vaqtinchalik fayllar uchun papka
TEMP_DIR = Path(tempfile.gettempdir()) / "instagram_bot"
TEMP_DIR.mkdir(exist_ok=True)

# Yuklab olingan videolar papkasi
DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

# Video hajmi limiti (30MB)
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 30MB in bytes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot boshlash komandasi"""
    welcome_text = """
🎵 **Video Music Bot** 🎵

Salom! Men videolardan musiqani yuklab olaman va qoshiq nomini aytaman.

**Qabul qiladigan manbalar:**
📱 Instagram (reel, post)
🎥 YouTube (video, short)
📌 Pinterest (video)

**Qanday ishlash kerak:**
1️⃣ Video linkini jo'nating
2️⃣ Bot videoni MP4 qilib yuklab oladi
3️⃣ Audio qismini analiz qilib qoshiq nomini topadi
4️⃣ Video va qoshiq nomini sizga jo'natadi

**🎵 Qoshiq Yuklab Olish:**
- Qoshiq nomini yuborsangiz, YouTube dan topib MP3 faylda jo'natib qo'yaman
- Misal: "Bohemian Rhapsody" yoki "Bohemian Rhapsody Queen"

**Komandalar:**
/start - Bu xabar
/help - Yordam
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yordam komandasi"""
    help_text = """
**📱 Video Yuklab Olish:**

1️⃣ Instagram, YouTube yoki Pinterest video linkini jo'nating
2️⃣ Bot videoni yuklab oladi (30MB gacha)
3️⃣ Audio qismini Shazam orqali analiz qiladi
4️⃣ Qoshiq nomini va artistni aytadi

**🎵 Qoshiq Yuklab Olish:**

Qoshiq nomini yuborsangiz, YouTube dan topib MP3 faylda jo'natib qo'yaman.

Misal: "Bohemian Rhapsody"

**Qabul qiladigan linklar:**
- Instagram: https://www.instagram.com/reel/...
- YouTube: https://www.youtube.com/watch?v=...
- Pinterest: https://www.pinterest.com/pin/...

**Cheklovlar:**
- Video hajmi: 30MB gacha
- Audio sifati: Yaxshi bo'lishi kerak
- Qoshiq: Shazam bazasida bo'lishi kerak

**Savol-javoblar:**
Q: Videoning hajmi qancha bo'lishi kerak?
J: 30MB gacha

Q: Qancha vaqt oladi?
J: Odatda 1-3 minut

Q: Qoshiq topilmasa?
J: Bot "Topilmadi" deb aytadi
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


def get_video_source(url: str) -> str:
    """Video manbasi aniqlash"""
    if 'instagram.com' in url:
        return 'instagram'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'pinterest.com' in url:
        return 'pinterest'
    else:
        return 'unknown'


def download_video(url: str, output_path: Path) -> tuple[bool, str]:
    """Videoni yuklab olish"""
    try:
        logger.info(f"Videoni yuklab olish: {url}")
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': str(output_path / '%(id)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 30,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = output_path / f"{info['id']}.mp4"
            
            if video_file.exists():
                file_size = video_file.stat().st_size
                
                # Hajmni tekshirish
                if file_size > MAX_VIDEO_SIZE:
                    video_file.unlink()
                    return False, f"Video hajmi juda katta ({file_size / (1024*1024):.1f}MB). 30MB gacha bo'lishi kerak."
                
                logger.info(f"Video muvaffaqiyatli yuklab olindi: {video_file}")
                return True, str(video_file)
            else:
                return False, "Video faylini topib bo'lmadi"
                
    except Exception as e:
        logger.error(f"Video yuklab olishda xato: {str(e)}")
        return False, f"Xato: {str(e)[:100]}"


def download_song_as_mp3(song_name: str, output_path: Path) -> tuple[bool, str]:
    """YouTube dan qoshiqni MP3 qilib yuklab olish"""
    try:
        logger.info(f"Qoshiqni yuklab olish: {song_name}")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 30,
        }
        
        search_url = f"ytsearch:{song_name}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=True)
            
            if info and 'entries' in info and len(info['entries']) > 0:
                first_result = info['entries'][0]
                mp3_file = output_path / f"{first_result['title']}.mp3"
                
                if mp3_file.exists():
                    logger.info(f"Qoshiq muvaffaqiyatli yuklab olindi: {mp3_file}")
                    return True, str(mp3_file)
        
        return False, "Qoshiq topilmadi"
        
    except Exception as e:
        logger.error(f"Qoshiq yuklab olishda xato: {str(e)}")
        return False, f"Xato: {str(e)[:100]}"


def extract_audio_from_video(video_path: Path, audio_path: Path) -> bool:
    """Videodagi audioni ajratib olish"""
    try:
        logger.info(f"Audio ajratib olish: {video_path}")
        
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-q:a', '9',
            '-n',
            str(audio_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if audio_path.exists() and audio_path.stat().st_size > 0:
            logger.info(f"Audio muvaffaqiyatli ajratildi: {audio_path}")
            return True
        else:
            logger.error("Audio ajratishda xato")
            return False
            
    except Exception as e:
        logger.error(f"Audio ajratishda xato: {str(e)}")
        return False


def recognize_song(audio_path: Path) -> dict:
    """Shazam orqali qoshiq nomini aniqlash"""
    try:
        logger.info(f"Qoshiq aniqlash: {audio_path}")
        
        # Audiofaylni o'qish
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        
        # Shazam API orqali aniqlash
        shazam = Shazam(audio_data)
        recognize_generator = shazam.recognizeSong()
        
        # Natijani olish
        for result in recognize_generator:
            if result and 'matches' in result and len(result['matches']) > 0:
                match = result['matches'][0]
                song_info = {
                    'title': match.get('title', 'Noma\'lum'),
                    'artist': match.get('subtitle', 'Noma\'lum artist'),
                    'cover': match.get('images', {}).get('coverart', ''),
                }
                logger.info(f"Qoshiq topildi: {song_info['title']} - {song_info['artist']}")
                return song_info
        
        return None
        
    except Exception as e:
        logger.error(f"Qoshiq aniqlashda xato: {str(e)}")
        return None


def is_video_link(text: str) -> bool:
    """Matn video link ekanligini tekshirish"""
    video_sources = ['instagram.com', 'youtube.com', 'youtu.be', 'pinterest.com']
    return any(source in text for source in video_sources)


def is_song_query(text: str) -> bool:
    """Matn qoshiq nomini tekshirish"""
    # Qoshiq nomini tekshirish: hech qanday URL bo'lmasa va 2 ta so'zdan ko'p bo'lsa
    if 'http' in text or 'www' in text:
        return False
    
    # Kamida 2 ta harif bo'lsa, qoshiq nomi deb hisoblash
    return len(text.strip()) >= 2


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xabarni qayta ishlash"""
    
    message_text = update.message.text.strip()
    
    # Video linkini tekshirish
    if is_video_link(message_text):
        await handle_video_link(update, message_text)
    
    # Qoshiq nomini tekshirish
    elif is_song_query(message_text):
        await handle_song_query(update, message_text)
    
    else:
        await update.message.reply_text(
            "❌ Iltimos, video linkini yoki qoshiq nomini jo'nating!\n\n"
            "**Video linklar:**\n"
            "📱 Instagram\n"
            "🎥 YouTube\n"
            "📌 Pinterest\n\n"
            "**Qoshiq nomini yuborsangiz, MP3 qilib jo'natib qo'yaman**\n"
            "Misal: `Bohemian Rhapsody`",
            parse_mode='Markdown'
        )


async def handle_video_link(update: Update, url: str) -> None:
    """Video linkini qayta ishlash"""
    
    # Jarayonni boshlash
    await update.message.chat.send_action(ChatAction.TYPING)
    processing_msg = await update.message.reply_text("⏳ Videoni yuklab olayotgan bo'lman...")
    
    try:
        # Vaqtinchalik papka yaratish
        session_dir = TEMP_DIR / f"session_{update.message.chat_id}"
        session_dir.mkdir(exist_ok=True)
        
        # 1. Videoni yuklab olish
        await processing_msg.edit_text("📥 Videoni yuklab olayotgan bo'lman...")
        
        success, result = download_video(url, session_dir)
        
        if not success:
            await processing_msg.edit_text(f"❌ {result}")
            return
        
        video_path = Path(result)
        
        # 2. Audioni ajratib olish
        await processing_msg.edit_text("🎵 Audio ajratib olayotgan bo'lman...")
        
        audio_path = session_dir / "audio.mp3"
        if not extract_audio_from_video(video_path, audio_path):
            await processing_msg.edit_text("❌ Audio ajratishda xato yuz berdi.")
            return
        
        # 3. Qoshiq nomini aniqlash
        await processing_msg.edit_text("🔍 Qoshiq nomini aniqlayotgan bo'lman...")
        
        song_info = recognize_song(audio_path)
        
        # 4. Natijani jo'natish
        await processing_msg.delete()
        
        if song_info:
            result_text = (
                f"✅ **Qoshiq topildi!**\n\n"
                f"🎵 **Nomi:** {song_info['title']}\n"
                f"🎤 **Artist:** {song_info['artist']}\n\n"
                f"💡 **Qoshiqni MP3 qilib olish uchun:** `{song_info['title']}`"
            )
        else:
            result_text = (
                "⚠️ Qoshiq topilmadi. Video audiosi musiqasiz yoki Shazam topib bo'lmadi.\n\n"
                "💡 Qoshiq nomini o'zingiz aytib, MP3 qilib olishingiz mumkin."
            )
        
        # Videoni jo'natish
        await update.message.chat.send_action(ChatAction.UPLOAD_VIDEO)
        
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=result_text,
                parse_mode='Markdown'
            )
        
        logger.info(f"Video jo'natildi: {update.message.chat_id}")
        
    except Exception as e:
        logger.error(f"Xato: {str(e)}")
        await processing_msg.edit_text(
            f"❌ Xato yuz berdi: {str(e)[:100]}\n\n"
            "Iltimos, qayta urinib ko'ring yoki /help ni bosing."
        )
    
    finally:
        # Vaqtinchalik fayllarni tozalash
        try:
            session_dir = TEMP_DIR / f"session_{update.message.chat_id}"
            if session_dir.exists():
                import shutil
                shutil.rmtree(session_dir)
        except Exception as e:
            logger.warning(f"Fayllarni tozalashda xato: {str(e)}")


async def handle_song_query(update: Update, song_name: str) -> None:
    """Qoshiq nomini qayta ishlash"""
    
    await update.message.chat.send_action(ChatAction.TYPING)
    processing_msg = await update.message.reply_text(f"🔍 '{song_name}' qidirmoqda...")
    
    try:
        # Vaqtinchalik papka yaratish
        session_dir = TEMP_DIR / f"session_{update.message.chat_id}"
        session_dir.mkdir(exist_ok=True)
        
        # Qoshiqni YouTube dan MP3 qilib yuklab olish
        await processing_msg.edit_text(f"📥 '{song_name}' yuklab olayotgan bo'lman...")
        
        success, result = download_song_as_mp3(song_name, session_dir)
        
        if not success:
            await processing_msg.edit_text(f"❌ {result}")
            return
        
        mp3_path = Path(result)
        
        # MP3 faylni jo'natish
        await processing_msg.delete()
        await update.message.chat.send_action(ChatAction.UPLOAD_AUDIO)
        
        with open(mp3_path, 'rb') as audio_file:
            await update.message.reply_audio(
                audio=audio_file,
                title=song_name,
                caption=f"✅ **Qoshiq:** {song_name}"
            )
        
        logger.info(f"Qoshiq jo'natildi: {update.message.chat_id}")
        
    except Exception as e:
        logger.error(f"Xato: {str(e)}")
        await processing_msg.edit_text(
            f"❌ Xato yuz berdi: {str(e)[:100]}\n\n"
            "Iltimos, qayta urinib ko'ring yoki /help ni bosing."
        )
    
    finally:
        # Vaqtinchalik fayllarni tozalash
        try:
            session_dir = TEMP_DIR / f"session_{update.message.chat_id}"
            if session_dir.exists():
                import shutil
                shutil.rmtree(session_dir)
        except Exception as e:
            logger.warning(f"Fayllarni tozalashda xato: {str(e)}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xatolarni qayta ishlash"""
    logger.error(f"Xato: {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ Xato yuz berdi. Iltimos, qayta urinib ko'ring.\n"
            "/help ni bosing."
        )


def main() -> None:
    """Bot asosiy funksiyasi"""
    
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Komanda handlerlari
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Xabar handleri
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Xato handleri
    application.add_error_handler(error_handler)
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushirilmoqda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
