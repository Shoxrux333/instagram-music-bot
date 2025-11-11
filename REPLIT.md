# 🚀 Replit da Bot Deploy Qilish

Replit eng oson va tez usuli. Quyidagi bosqichlarni bajaring.

## 📋 Bosqichlar

### 1️⃣ Replit.com ga kirish

- https://replit.com ga kirish
- GitHub akkaunt orqali ro'yxatdan o'tish yoki kirish

### 2️⃣ Yangi Repl yaratish

1. **"Create"** tugmasini bosing
2. **"Import from GitHub"** ni tanlang
3. GitHub repositoriyasini ulang:
   - URL: `https://github.com/Shoxrux333/instagram-music-bot`
4. **"Import"** tugmasini bosing

Replit avtomatik ravishda repositoriyani klonlaydi.

### 3️⃣ Environment Variable o'rnatish

1. Replit sahifasida chap tarafda **"Secrets"** (kilt belgisi) ni bosing
2. **"New Secret"** ni bosing
3. Quyidagilarni kiritish:
   - **Key:** `TELEGRAM_BOT_TOKEN`
   - **Value:** `8595539202:AAHNkg-oExRsd6RdQXpEao-KfU6zhfOO4SY`
4. **"Add Secret"** tugmasini bosing

### 4️⃣ Bot ishga tushirish

1. Replit sahifasida yuqori o'ng burchakda **"Run"** tugmasini bosing
2. Replit avtomatik ravishda:
   - FFmpeg o'rnatadi
   - Python kutubxonalarini o'rnatadi
   - Bot kodini ishga tushiradi

### 5️⃣ Bot tekshirish

1. Telegram da **@lumi** botga `/start` ni bosing
2. Bot javob bersa ✅ - Tayyor!
3. Video linkini yoki qoshiq nomini jo'nating

## 🎯 Replit Features

✅ **24/7 Ishlash** - Always-on mode (Replit Pro)
✅ **Bepul** - Hech qanday to'lov kerak emas
✅ **Oson** - GitHub integrations
✅ **Logs** - Xatolarni ko'rish mumkin

## ⚙️ Replit Sozlamalari

### Always-on Mode (Ixtiyoriy)

Bot 24/7 ishlashi uchun:

1. Replit sahifasida **"Secrets"** ni bosing
2. **"New Secret"** ni bosing:
   - **Key:** `REPLIT_ALWAYS_ON`
   - **Value:** `true`

Lekin bu Replit Pro kerak (pullik).

### Bepul Variant

Replit bepul variantida bot:
- 1 soat faol bo'lsa, ishlaydi
- 1 soat faol bo'lmasa, to'xtaydi
- Siz yoki boshqalar uni ishga tushirganda, qayta ishga tushadi

## 🐛 Muammolarni hal qilish

### Bot ishlamayotgan bo'lsa

1. **Logs ni tekshirish:**
   - Replit sahifasida **"Console"** ni bosing
   - Xato xabarlarini ko'ring

2. **Token tekshirish:**
   - Secrets da token to'g'ri kiritilganligini tekshiring
   - Token yangi bo'lishi kerak (eski token regenerate qilingan bo'lsa)

3. **Kutubxonalarni qayta o'rnatish:**
   ```bash
   pip install -r requirements.txt
   ```

### "ModuleNotFoundError" xatosi

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### FFmpeg xatosi

```bash
apt-get update
apt-get install -y ffmpeg
```

## 📱 Bot Funksionalligi

### Video Yuklab Olish

```
User: https://www.instagram.com/reel/ABC123/
Bot: Video yuklab oladi → Qoshiq nomini aytadi
```

### Qoshiq Yuklab Olish (MP3)

```
User: Bohemian Rhapsody
Bot: YouTube dan topadi → MP3 qilib jo'natadi
```

## 💡 Maslahatlar

1. **Replit URL** - Replit sizga public URL beradi. Bu URL bot uchun kerak emas (polling ishlatiladi).

2. **Logs** - Har doim logs ni tekshiring. Xatolar ko'rinadi.

3. **Restart** - Bot muammoli bo'lsa, **"Run"** tugmasini qayta bosing.

4. **Updates** - Kodni yangilasangiz, Replit avtomatik restart qiladi.

## 🎉 Tayyor!

Bot Replit da 24/7 ishlaydi! 

Telegram da `/start` ni bosib, test qiling! 🚀

---

**Savollar bo'lsa:** Bot muallifi bilan bog'laning.
