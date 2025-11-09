FROM python:3.11-slim

# FFmpeg va boshqa zarur paketlarni o'rnatish
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Ishchi papka
WORKDIR /app

# Requirements o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodni nusxalash
COPY . .

# Bot ishga tushirish
CMD ["python3", "bot.py"]
