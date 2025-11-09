#!/bin/bash

# Ranglar
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎵 Instagram Music Bot - O'rnatish${NC}\n"

# Python versiyasini tekshirish
echo -e "${YELLOW}Python versiyasini tekshirish...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 o'rnatilmagan. Iltimos, Python3 o'rnating.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 topildi: $(python3 --version)${NC}\n"

# FFmpeg ni tekshirish
echo -e "${YELLOW}FFmpeg ni tekshirish...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}⚠️  FFmpeg o'rnatilmagan. O'rnatish...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    else
        echo -e "${RED}❌ Avtomatik o'rnatish mumkin emas. Qo'lda FFmpeg o'rnating.${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}✓ FFmpeg topildi: $(ffmpeg -version | head -n 1)${NC}\n"

# Virtual muhit yaratish
echo -e "${YELLOW}Virtual muhit yaratish...${NC}"
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}✓ Virtual muhit yaratildi${NC}\n"

# Kutubxonalarni o'rnatish
echo -e "${YELLOW}Kutubxonalarni o'rnatish...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Kutubxonalar o'rnatildi${NC}\n"

# .env faylini yaratish
echo -e "${YELLOW}.env faylini sozlash...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env faylini yaratildi${NC}"
    echo -e "${YELLOW}⚠️  .env faylini ochib, TELEGRAM_BOT_TOKEN ni kiritish kerak!${NC}"
    echo -e "${YELLOW}   nano .env yoki code .env${NC}\n"
else
    echo -e "${GREEN}✓ .env fayli allaqachon mavjud${NC}\n"
fi

# Papkalarni yaratish
echo -e "${YELLOW}Papkalarni yaratish...${NC}"
mkdir -p downloads logs
echo -e "${GREEN}✓ Papkalar yaratildi${NC}\n"

echo -e "${GREEN}✅ O'rnatish tugallandi!${NC}\n"
echo -e "${YELLOW}Keyingi qadam:${NC}"
echo -e "1. .env faylini ochib, TELEGRAM_BOT_TOKEN ni kiritish:"
echo -e "   ${GREEN}nano .env${NC}"
echo -e ""
echo -e "2. Botni ishga tushirish:"
echo -e "   ${GREEN}python3 bot.py${NC}"
echo -e ""
echo -e "3. Telegram da botni topib, /start ni bosing"
echo -e ""
echo -e "${YELLOW}Serverga yuklash uchun README.md ni o'qing.${NC}"
