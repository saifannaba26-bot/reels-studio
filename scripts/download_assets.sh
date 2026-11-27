#!/usr/bin/env bash
# Fonts (Cairo + Amiri) and starter SFX pack.
set -e
cd "$(dirname "$0")/.."

FONT_DIR=assets/fonts
SFX_DIR=assets/sfx
mkdir -p "$FONT_DIR" "$SFX_DIR"

if [ ! -f "$FONT_DIR/Cairo-Bold.ttf" ]; then
  curl -sL -o /tmp/cairo.zip "https://fonts.google.com/download?family=Cairo" \
    && unzip -o /tmp/cairo.zip -d "$FONT_DIR" || \
  curl -sL -o "$FONT_DIR/Cairo-Bold.ttf" \
    "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo%5Bslnt%2Cwght%5D.ttf"
fi
if [ ! -f "$FONT_DIR/Amiri-Regular.ttf" ]; then
  curl -sL -o "$FONT_DIR/Amiri-Regular.ttf" \
    "https://github.com/aliftype/amiri/raw/master/fonts/Amiri-Regular.ttf" || true
fi

# Starter SFX: synthesize simple whoosh/impact/pop/ding with ffmpeg so the
# pipeline works out of the box; replace with your own pack anytime.
gen() { [ -f "$SFX_DIR/$1" ] || ffmpeg -y -v error -f lavfi -i "$2" -t "$3" "$SFX_DIR/$1"; }
gen whoosh.wav "anoisesrc=color=pink:amplitude=0.4,lowpass=f=3000,volume='t/0.4':eval=frame" 0.4
gen impact.wav "sine=frequency=60,volume='(1-t/0.5)^2*2':eval=frame" 0.5
gen riser.wav "aevalsrc='sin(2*PI*(200*t+400*t*t/1.2))*0.4':s=44100:d=1.2" 1.2
gen pop.wav    "sine=frequency=800,volume='(1-t/0.15)^3*1.5':eval=frame" 0.15
gen ding.wav   "sine=frequency=1567,volume='(1-t/0.8)^2':eval=frame" 0.8
echo "assets ready"
