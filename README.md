# 🎵 Instagram Music Bot

Instagram videolaridan musiqani yuklab olish va qoshiq nomini aniqlash uchun Telegram bot.

## ✨ Funksionalliq

- 📥 Instagram videolarini MP4 qilib yuklab olish
- 🎵 Videodagi musiqani Shazam API orqali aniqlash
- 🎤 Qoshiq nomi va artistni ko'rsatish
- ⚡ Tez va sod interfeys

## 📋 Talablar

- Python 3.8+
- FFmpeg
- Instagram akkaunt (private bo'lsa ham ishlaydi)
- Telegram Bot Token

## 🚀 O'rnatish

### 1. Lokal o'rnatish

```bash
# Loyihani klonlash yoki papkaga kirish
cd instagram_music_bot

# Virtual muhit yaratish
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# FFmpeg o'rnatish (agar bo'lmasa)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# https://ffmpeg.org/download.html dan oling
```

### 2. Telegram Bot Token olish

1. Telegram da [@BotFather](https://t.me/botfather) ga yozing
2. `/newbot` komandasi bilan yangi bot yaratish
3. Bot nomini va username ni kiriting
4. Token ni olish

### 3. .env faylini sozlash

```bash
# .env.example ni .env ga nusxalash
cp .env.example .env

# .env faylini ochib, token ni kiritish
nano .env
# yoki
code .env
```

`.env` faylida:
```
TELEGRAM_BOT_TOKEN=your_token_here
```

### 4. Botni ishga tushirish

```bash
python3 bot.py
```

## 💻 Serverga yuklash (24/7 ishlashi uchun)

### Variant 1: Heroku (Bepul)

```bash
# Heroku CLI o'rnatish
# https://devcenter.heroku.com/articles/heroku-cli

# Heroku ga kirish
heroku login

# Yangi app yaratish
heroku create your-app-name

# Procfile yaratish
echo "worker: python3 bot.py" > Procfile

# Git orqali yuklash
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Environment variable o'rnatish
heroku config:set TELEGRAM_BOT_TOKEN=your_token_here

# Loglarni ko'rish
heroku logs --tail
```

### Variant 2: VPS (Masalan, DigitalOcean, AWS)

```bash
# VPS ga SSH orqali kirish
ssh root@your_server_ip

# Python va FFmpeg o'rnatish
sudo apt-get update
sudo apt-get install python3 python3-pip ffmpeg

# Loyihani yuklash
git clone your_repo_url
cd instagram_music_bot

# Virtual muhit yaratish
python3 -m venv venv
source venv/bin/activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# Systemd service yaratish
sudo nano /etc/systemd/system/instagram-bot.service
```

`instagram-bot.service` faylida:
```ini
[Unit]
Description=Instagram Music Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/instagram_music_bot
Environment="PATH=/home/ubuntu/instagram_music_bot/venv/bin"
ExecStart=/home/ubuntu/instagram_music_bot/venv/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Service ni ishga tushirish
sudo systemctl enable instagram-bot
sudo systemctl start instagram-bot

# Status tekshirish
sudo systemctl status instagram-bot

# Loglarni ko'rish
sudo journalctl -u instagram-bot -f
```

### Variant 3: Docker (Tavsiya qilinadi)

```bash
# Dockerfile yaratish
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
EOF

# Docker image yaratish
docker build -t instagram-bot .

# Container ishga tushirish
docker run -d \
  --name instagram-bot \
  -e TELEGRAM_BOT_TOKEN=your_token_here \
  instagram-bot
```

## 📱 Botni ishlatish

1. Telegram da botni topib, `/start` ni bosing
2. Instagram video linkini jo'nating
3. Bot videoni yuklab oladi va qoshiq nomini aytadi

**Misal linklar:**
- `https://www.instagram.com/reel/ABC123DEF/`
- `https://www.instagram.com/p/XYZ789ABC/`

## ⚙️ Sozlamalar

### Maksimal video hajmi
`bot.py` da `MAX_VIDEO_SIZE` ni o'zgartirib, maksimal hajmni belgilash mumkin.

### Timeout vaqti
`download_instagram_video()` funksiyasida timeout vaqtini o'zgartirib, yuklab olish vaqtini oshirish mumkin.

## 🐛 Masalalarni hal qilish

### "Videoni yuklab bo'lmadi" xatosi
- Instagram linkini tekshiring
- Private akkaunt bo'lsa, bot akkauntiga follow qiling
- yt-dlp ni yangilang: `pip install --upgrade yt-dlp`

### "Qoshiq topilmadi" xatosi
- Videoda musiqasi bo'lishi kerak
- Audio sifati yaxshi bo'lishi kerak
- Shazam bazasida qoshiq bo'lishi kerak

### FFmpeg xatosi
- FFmpeg o'rnatilganligini tekshiring: `ffmpeg -version`
- Ubuntu: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

## 📄 Litsenziya

MIT License

## 👨‍💻 Muallif

Instagram Music Bot

## 🤝 Yordam

Savollar yoki muammolar bo'lsa, issue ochib qo'ying.

---

**Eslatma:** Bot Instagram shartlariga rioya qilish uchun faqat shaxsiy maqsadda ishlatilishi kerak.
