# 🚀 Render.com ga Bot Deploy Qilish - Batafsil Ko'rsatmalar

Quyidagi bosqichlarni aniq bajaring. Bot 24/7 ishlashi uchun.

---

## 📋 Bosqichlar

### 1️⃣ Render.com ga kirish

1. **https://render.com** ga kirish
2. Agar akkaunt bo'lmasa:
   - **"Sign Up"** ni bosing
   - GitHub akkaunt orqali ro'yxatdan o'tish (tavsiya qilinadi)
3. Agar akkaunt bo'lsa:
   - **"Sign In"** ni bosing
   - GitHub orqali kirish

---

### 2️⃣ Yangi Web Service yaratish

1. Render.com dashboard da **"New +"** tugmasini bosing
2. **"Web Service"** ni tanlang
3. **"Connect a repository"** ni bosing

#### GitHub ulanish (agar birinchi marta bo'lsa):
- **"Connect GitHub"** ni bosing
- GitHub da ruxsat berish
- **"Shoxrux333/instagram-music-bot"** repositoriyasini tanlang
- **"Connect"** ni bosing

---

### 3️⃣ Deploy sozlamalari

Quyidagi sozlamalarni aniq kiritish:

| Sozlama | Qiymat | Izoh |
|---------|--------|------|
| **Name** | `instagram-music-bot` | Har qanday nom bo'lishi mumkin |
| **Environment** | `Python 3` | Avtomatik tanlangan bo'ladi |
| **Region** | `Ohio (us-east-1)` | Eng yaqin region tanlang |
| **Branch** | `main` | GitHub branch |
| **Build Command** | `pip install -r requirements.txt` | Kutubxonalarni o'rnatish |
| **Start Command** | `python3 bot.py` | Bot ishga tushirish |
| **Plan** | `Free` | Bepul plan |

---

### 4️⃣ Environment Variables o'rnatish

1. **"Environment"** bo'limiga scroll qilish
2. **"Add Environment Variable"** ni bosing
3. Quyidagilarni kiritish:

```
Key: TELEGRAM_BOT_TOKEN
Value: 8595539202:AAHNkg-oExRsd6RdQXpEao-KfU6zhfOO4SY
```

4. **"Save"** ni bosing

---

### 5️⃣ Deploy qilish

1. Yuqori o'ng burchakda **"Create Web Service"** tugmasini bosing
2. Render.com deploy qilishni boshlaydi:
   - GitHub dan kodni klonlash
   - Kutubxonalarni o'rnatish
   - Bot kodini ishga tushirish

**Kutish vaqti:** 3-5 minut

---

### 6️⃣ Deploy statusini tekshirish

1. Render.com dashboard da yangi service ko'rinadi
2. **"Logs"** bo'limida deploy jarayonini ko'rish mumkin
3. Agar **"Service is live"** yozilsa ✅ - Tayyor!

---

## 🔍 Logs ni tekshirish

Agar xato bo'lsa, logs da ko'rinadi:

1. Service sahifasida **"Logs"** tugmasini bosing
2. Oxirgi xabarlarni o'qish
3. Xato bo'lsa, menga aytib qo'ying

**Xatolar:**
- `ModuleNotFoundError` - Kutubxona o'rnatilmadi
- `TELEGRAM_BOT_TOKEN not set` - Environment variable kerak
- `Connection timeout` - Internet muammosi

---

## ✅ Bot tekshirish

1. Telegram da **@lumi** botga kirish
2. **/start** ni bosing
3. Bot javob bersa ✅ - Tayyor!

**Test qilish:**
- Instagram video linkini jo'nating
- Qoshiq nomini jo'nating (masalan: "Bohemian Rhapsody")

---

## 🔄 Bot qayta ishga tushirish

Agar bot to'xtab qolsa:

1. Render.com dashboard da service ni tanlang
2. Yuqori o'ng burchakda **"..."** (menu) ni bosing
3. **"Restart"** ni tanlang

---

## 🐛 Muammolarni hal qilish

### Bot ishlamayotgan bo'lsa

**1. Token tekshirish:**
```
Settings → Environment → TELEGRAM_BOT_TOKEN
```
Token to'g'ri kiritilganligini tekshiring.

**2. Logs tekshirish:**
```
Logs bo'limida xato xabarlarini o'qish
```

**3. Bot qayta ishga tushirish:**
```
"Restart" tugmasini bosing
```

### "Service is live" lekin bot javob bermayotgan bo'lsa

1. Bot token yangi bo'lishi kerak
2. @BotFather dan token regenerate qiling
3. Render.com da environment variable o'zgartiring
4. Service ni restart qiling

---

## 💡 Maslahatlar

1. **Logs ni muntazam tekshiring** - Xatolarni erta topish uchun
2. **Bot token xavfsiz saqlang** - GitHub da commit qilmang
3. **Har hafta tekshiring** - Bot 24/7 ishlayotganini tekshirish
4. **Uptime Robot ishlating** - Bot to'xtab qolsa, xabar olish uchun

---

## 📞 Savollar

Agar muammoga duch kelsangiz:

1. Logs ni o'qing
2. Xato xabarini menga aytib qo'ying
3. Men tuzatib beraman

---

## 🎉 Tayyor!

Bot Render.com da 24/7 ishlaydi!

Telegram da `/start` ni bosib, test qiling! 🚀

---

**Eslatma:** Bot Instagram shartlariga rioya qilish uchun faqat shaxsiy maqsadda ishlatilishi kerak.
