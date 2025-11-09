# 🚀 Serverga Yuklash Ko'rsatmalari

Instagram Music Bot ni 24/7 ishlashi uchun serverga yuklash uchun quyidagi variantlardan birini tanlang.

---

## 📌 Variant 1: Render.com (Tavsiya qilinadi - Bepul)

Render.com eng oson va bepul variantdir. Heroku dan farqli o'laroq, hozir ham bepul bo'lib qolgan.

### Bosqichlar:

1. **Render.com ga ro'yxatdan o'tish**
   - https://render.com ga kirish
   - GitHub akkaunt orqali ro'yxatdan o'tish

2. **GitHub repositoriyani yaratish**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/instagram-music-bot.git
   git push -u origin main
   ```

3. **Render.com da yangi Web Service yaratish**
   - "New +" tugmasini bosing
   - "Web Service" ni tanlang
   - GitHub repositoriyani ulang
   - Quyidagi sozlamalarni kiriting:
     - **Name:** instagram-music-bot
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python3 bot.py`
     - **Plan:** Free

4. **Environment Variables o'rnatish**
   - Settings → Environment ni ochish
   - Quyidagini qo'shish:
     ```
     TELEGRAM_BOT_TOKEN=your_token_here
     ```

5. **Deploy qilish**
   - "Deploy" tugmasini bosing
   - Kutish (2-3 minut)
   - Bot ishga tushadi!

---

## 📌 Variant 2: Railway.app (Bepul kredit)

Railway.app har oyda $5 bepul kredit beradi.

### Bosqichlar:

1. **Railway.app ga ro'yxatdan o'tish**
   - https://railway.app ga kirish
   - GitHub orqali kirish

2. **Yangi proyekt yaratish**
   - "New Project" tugmasini bosing
   - "Deploy from GitHub repo" ni tanlang
   - Repositoriyani ulang

3. **Environment Variables**
   - Variables bo'limiga kirish
   - `TELEGRAM_BOT_TOKEN` qo'shish

4. **Deploy**
   - Avtomatik deploy bo'ladi
   - Logs bo'limida ko'rish mumkin

---

## 📌 Variant 3: DigitalOcean Droplet (Arzon - $5/oy)

VPS orqali to'liq nazorat qilish uchun.

### Bosqichlar:

1. **Droplet yaratish**
   - DigitalOcean.com ga kirish
   - "Create" → "Droplets"
   - Ubuntu 22.04 tanlash
   - Eng arzon plan ($5/oy) tanlash

2. **SSH orqali ulanish**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Paketlarni yangilash**
   ```bash
   apt-get update
   apt-get upgrade -y
   apt-get install -y python3 python3-pip python3-venv ffmpeg git
   ```

4. **Proyektni yuklash**
   ```bash
   git clone https://github.com/YOUR_USERNAME/instagram-music-bot.git
   cd instagram-music-bot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Environment sozlamasi**
   ```bash
   nano .env
   # TELEGRAM_BOT_TOKEN=your_token_here
   # Ctrl+X, Y, Enter
   ```

6. **Systemd Service yaratish**
   ```bash
   sudo nano /etc/systemd/system/instagram-bot.service
   ```

   Quyidagini kiritish:
   ```ini
   [Unit]
   Description=Instagram Music Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/instagram-music-bot
   Environment="PATH=/root/instagram-music-bot/venv/bin"
   ExecStart=/root/instagram-music-bot/venv/bin/python3 bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

7. **Service ishga tushirish**
   ```bash
   systemctl daemon-reload
   systemctl enable instagram-bot
   systemctl start instagram-bot
   systemctl status instagram-bot
   ```

8. **Loglarni ko'rish**
   ```bash
   journalctl -u instagram-bot -f
   ```

---

## 📌 Variant 4: Docker + Any Cloud (AWS, GCP, Azure)

### Docker Image yaratish va yuklash:

1. **Docker Hub da ro'yxatdan o'tish**
   - https://hub.docker.com

2. **Image yaratish va yuklash**
   ```bash
   docker build -t YOUR_USERNAME/instagram-music-bot:latest .
   docker login
   docker push YOUR_USERNAME/instagram-music-bot:latest
   ```

3. **AWS ECS, GCP Cloud Run yoki Azure Container Instances da ishlatish**
   - Image URI: `YOUR_USERNAME/instagram-music-bot:latest`
   - Environment variable: `TELEGRAM_BOT_TOKEN`

---

## 🔒 Xavfsizlik Masalalari

1. **Token xavfsizligi**
   - Token ni hech qachon GitHub da commit qilmang
   - `.env` faylini `.gitignore` ga qo'shish:
     ```
     .env
     venv/
     downloads/
     __pycache__/
     *.pyc
     ```

2. **Rate Limiting**
   - Instagram API rate limitini tekshirish
   - Shazam API limitini tekshirish

3. **Disk Space**
   - Yuklab olingan videolarni muntazam tozalash
   - Cron job orqali avtomatik tozalash:
     ```bash
     0 0 * * * find /path/to/downloads -type f -mtime +7 -delete
     ```

---

## 🐛 Muammolarni hal qilish

### Bot ishlamayotgan bo'lsa:

1. **Loglarni tekshirish**
   ```bash
   # Render.com
   # Logs bo'limiga kirish
   
   # DigitalOcean
   journalctl -u instagram-bot -f
   ```

2. **Token tekshirish**
   - Token to'g'ri kiritilganligini tekshirish
   - @BotFather dan yangi token olish

3. **FFmpeg tekshirish**
   ```bash
   ffmpeg -version
   ```

4. **Internet ulanishini tekshirish**
   ```bash
   curl https://www.instagram.com
   ```

---

## 💡 Maslahatlar

1. **Monitoring qo'shish**
   - Render.com yoki Railway.app avtomatik monitoring qiladi
   - DigitalOcean uchun Uptime Robot ishlatish

2. **Backup qilish**
   - GitHub repositoriyani private qilish
   - Environment variables ni xavfsiz saqlash

3. **Updates**
   - Muntazam kutubxonalarni yangilash
   - `pip list --outdated` orqali tekshirish

---

## 📞 Yordam

Savollar bo'lsa, GitHub issues ochib qo'ying yoki bot muallifi bilan bog'laning.

---

**Eslatma:** Bot Instagram shartlariga rioya qilish uchun faqat shaxsiy maqsadda ishlatilishi kerak.
