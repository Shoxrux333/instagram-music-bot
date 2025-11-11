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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot boshlash komandasi"""
    welcome_text = """
🎵 **Instagram Music Bot** 🎵

Salom! Men Instagram videolaridan musiqani yuklab olaman va qoshiq nomini aytaman.

**Qanday ishlash kerak:**
1. Instagram video linkini menga jo'nating
2. Bot videoni MP4 qilib yuklab oladi
3. Audio qismini analiz qilib qoshiq nomini topadi
4. Video va qoshiq nomini sizga jo'natadi

**Misal:**
`https://www.instagram.com/reel/ABC123DEF/`

**Komandalar:**
/start - Bu xabar
/help - Yordam
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yordam komandasi"""
    help_text = """
**Qanday ishlash kerak:**

1️⃣ Instagram reel yoki post linkini jo'nating
2️⃣ Bot videoni yuklab oladi (MP4)
3️⃣ Audio qismini Shazam orqali analiz qiladi
4️⃣ Qoshiq nomini va artistni aytadi

**Qabul qiladigan linklar:**
- Instagram reels: https://www.instagram.com/reel/...
- Instagram posts: https://www.instagram.com/p/...
- Instagram stories (agar saqlanib qolgan bo'lsa)

**Masalalar:**
- Private akkauntdan video bo'lsa, ishlaydi
- Juda uzun videolar vaqt olishi mumkin
- Audio qismida musiqasi bo'lmasa, topilmaydi

**Savol-javoblar:**
Q: Videoning hajmi qancha bo'lishi kerak?
J: 50MB gacha

Q: Qancha vaqt oladi?
J: Odatda 1-3 minut

Q: Qoshiq topilmasa?
J: Bot "Topilmadi" deb aytadi
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


def download_instagram_video(url: str, output_path: Path) -> bool:
    """Instagram videoni yuklab olish"""
    try:
        logger.info(f"Instagram videoni yuklab olish: {url}")
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': str(output_path / '%(id)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = output_path / f"{info['id']}.mp4"
            
            if video_file.exists():
                logger.info(f"Video muvaffaqiyatli yuklab olindi: {video_file}")
                return True
            else:
                logger.error("Video faylini topib bo'lmadi")
                return False
                
    except Exception as e:
        logger.error(f"Video yuklab olishda xato: {str(e)}")
        return False


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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Instagram linkini qabul qilish va qayta ishlash"""
    
    message_text = update.message.text
    
    # Instagram linkini tekshirish
    if 'instagram.com' not in message_text:
        await update.message.reply_text(
            "❌ Iltimos, Instagram linkini jo'nating!\n\n"
            "Misal: https://www.instagram.com/reel/ABC123DEF/"
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
        await processing_msg.edit_text("📥 Instagram videoni yuklab olayotgan bo'lman...")
        
        if not download_instagram_video(message_text, session_dir):
            await processing_msg.edit_text(
                "❌ Videoni yuklab bo'lmadi. Iltimos, linkni tekshiring va qayta urinib ko'ring."
            )
            return
        
        # Yuklab olingan videofaylni topish
        video_files = list(session_dir.glob('*.mp4'))
        if not video_files:
            await processing_msg.edit_text("❌ Video faylini topib bo'lmadi.")
            return
        
        video_path = video_files[0]
        
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
                f"🎤 **Artist:** {song_info['artist']}"
            )
        else:
            result_text = "⚠️ Qoshiq topilmadi. Video audiosi musiqasiz yoki Shazam topib bo'lmadi."
        
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
