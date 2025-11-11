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
MAX_VIDEO_SIZE = 30 * 1024 * 1024  # 30MB in bytes


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

**Qoshiq qidirish:**
- Qoshiq nomini yuborsangiz, YouTube dan topib linkini berib qo'yaman
- Misal: "Bohemian Rhapsody" yoki "Bohemian Rhapsody Queen"

**Komandalar:**
/start - Bu xabar
/help - Yordam
/search - Qoshiq qidirish
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

**🎵 Qoshiq Qidirish:**

/search Qoshiq Nomi - YouTube dan qoshiq qidirish
Misal: `/search Bohemian Rhapsody`

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


def search_song_on_youtube(song_name: str) -> str:
    """YouTube dan qoshiq qidirish"""
    try:
        logger.info(f"YouTube dan qoshiq qidirish: {song_name}")
        
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        search_url = f"ytsearch:{song_name}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
            
            if info and 'entries' in info and len(info['entries']) > 0:
                first_result = info['entries'][0]
                video_url = f"https://www.youtube.com/watch?v={first_result['id']}"
                logger.info(f"Qoshiq topildi: {video_url}")
                return video_url
        
        return None
        
    except Exception as e:
        logger.error(f"YouTube qidirish xatosi: {str(e)}")
        return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xabarni qayta ishlash"""
    
    message_text = update.message.text
    
    # Qoshiq qidirish komandasi
    if message_text.startswith('/search '):
        song_name = message_text.replace('/search ', '').strip()
        
        if not song_name:
            await update.message.reply_text("❌ Qoshiq nomini kiritib qo'ying!\n\nMisal: `/search Bohemian Rhapsody`", parse_mode='Markdown')
            return
        
        await update.message.chat.send_action(ChatAction.TYPING)
        searching_msg = await update.message.reply_text(f"🔍 '{song_name}' qidirmoqda...")
        
        try:
            youtube_url = search_song_on_youtube(song_name)
            
            if youtube_url:
                await searching_msg.edit_text(
                    f"✅ **Qoshiq topildi!**\n\n"
                    f"🎵 **Nomi:** {song_name}\n"
                    f"🎥 **YouTube:** {youtube_url}",
                    parse_mode='Markdown'
                )
            else:
                await searching_msg.edit_text(f"❌ '{song_name}' YouTube da topilmadi.")
        
        except Exception as e:
            logger.error(f"Qoshiq qidirish xatosi: {str(e)}")
            await searching_msg.edit_text(f"❌ Xato: {str(e)[:100]}")
        
        return
    
    # Video linkini tekshirish
    if not any(source in message_text for source in ['instagram.com', 'youtube.com', 'youtu.be', 'pinterest.com']):
        await update.message.reply_text(
            "❌ Iltimos, video linkini jo'nating!\n\n"
            "Qabul qiladigan manbalar:\n"
            "📱 Instagram\n"
            "🎥 YouTube\n"
            "📌 Pinterest\n\n"
            "Yoki qoshiq qidirish uchun: `/search Qoshiq Nomi`",
            parse_mode='Markdown'
        )
        return
    
    # Jarayonni boshlash
    await update.message.chat.send_action(ChatAction.TYPING)
    processing_msg = await update.message.reply_text("⏳ Videoni yuklab olayotgan bo'lman...")
    
    try:
        # Vaqtinchalik papka yaratish
        session_dir = TEMP_DIR / f"session_{update.message.chat_id}"
        session_dir.mkdir(exist_ok=True)
        
        # 1. Videoni yuklab olish
        await processing_msg.edit_text("📥 Videoni yuklab olayotgan bo'lman...")
        
        success, result = download_video(message_text, session_dir)
        
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
                f"💡 **Qoshiq qidirish:** `/search {song_info['title']}`"
            )
        else:
            result_text = (
                "⚠️ Qoshiq topilmadi. Video audiosi musiqasiz yoki Shazam topib bo'lmadi.\n\n"
                "💡 Qoshiq nomini o'zingiz aytib, qidirish uchun: `/search Qoshiq Nomi`"
            )
        
        # Videoni jo'natish
        await update.message.chat.send_action(ChatAction.UPLOAD_VIDEO)
        
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=result_text,
                parse_mode='Markdown'
            )
        
        logger.info(f"Natija jo'natildi: {update.message.chat_id}")
        
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
