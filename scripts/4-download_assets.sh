#!/usr/bin/env bash
# Fonts (Cairo + Amiri) and starter SFX pack.
set -e
cd "$(dirname "$0")/.."

FONT_DIR=assets/fonts
SFX_DIR=assets/sfx
mkdir -p "$FONT_DIR" "$SFX_DIR"

is_font() {  # TrueType / OpenType magic bytes, so an HTML error page is rejected
  case "$(head -c4 "$1" 2>/dev/null | od -An -tx1 | tr -d ' \n')" in
    00010000|4f54544f|74727565) return 0 ;; *) return 1 ;;
  esac
}
fetch_font() {  # name url
  if [ -s "$FONT_DIR/$1" ] && is_font "$FONT_DIR/$1"; then return 0; fi
  rm -f "$FONT_DIR/$1"
  curl -fsSL --retry 3 -o "$FONT_DIR/$1" "$2"
  is_font "$FONT_DIR/$1" || { echo "ERROR: $1 is not a valid font file" >&2; exit 1; }
}
fetch_font Cairo-Bold.ttf "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo%5Bslnt%2Cwght%5D.ttf"
fetch_font Amiri-Regular.ttf "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"

# Starter SFX: synthesize simple whoosh/impact/pop/ding with ffmpeg so the
# pipeline works out of the box; replace with your own pack anytime.
gen() { [ -f "$SFX_DIR/$1" ] || ffmpeg -y -v error -f lavfi -i "$2" -t "$3" "$SFX_DIR/$1"; }
gen whoosh.wav "anoisesrc=color=pink:amplitude=0.4,lowpass=f=3000,volume='t/0.4':eval=frame" 0.4
gen impact.wav "sine=frequency=60,volume='(1-t/0.5)^2*2':eval=frame" 0.5
gen riser.wav "aevalsrc='sin(2*PI*(200*t+400*t*t/1.2))*0.4':s=44100:d=1.2" 1.2
gen pop.wav    "sine=frequency=800,volume='(1-t/0.15)^3*1.5':eval=frame" 0.15
gen ding.wav   "sine=frequency=1567,volume='(1-t/0.8)^2':eval=frame" 0.8
echo "assets ready"
