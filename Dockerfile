# Resmi optimize edilmiş hafif Python 3.12 imajı
FROM python:3.12-slim

# Sistem bağımlılıklarını kur (C derleyicileri ve grafik kütüphaneleri)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Gradio portunu dışarı aç
EXPOSE 7860

# Çevre değişkeni ayarları
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Uygulamayı başlat
CMD ["python", "app.py"]