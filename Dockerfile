FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg fonts-hosny-amiri fontconfig curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN bash scripts/download_assets.sh \
    && mkdir -p /usr/local/share/fonts/reels && cp assets/fonts/*.ttf /usr/local/share/fonts/reels/ && fc-cache -f \
    && fc-list | grep -qi cairo && fc-list | grep -qi amiri

EXPOSE 7860
CMD ["python", "-m", "reels_studio.app"]
