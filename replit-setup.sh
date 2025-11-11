#!/bin/bash

echo "🎵 Instagram Music Bot - Replit Setup"
echo "======================================"

# FFmpeg o'rnatish
echo "📦 FFmpeg o'rnatilmoqda..."
apt-get update -qq
apt-get install -y ffmpeg > /dev/null 2>&1

# Python kutubxonalarini o'rnatish
echo "📚 Python kutubxonalari o'rnatilmoqda..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup tugallandi!"
echo ""
echo "🚀 Bot ishga tushirish uchun:"
echo "   python3 bot.py"
echo ""
echo "📝 .env faylini sozlashni unutmang!"
echo "   TELEGRAM_BOT_TOKEN=your_token_here"
