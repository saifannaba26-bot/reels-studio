"""Command line entry: python -m reels_studio.cli ..."""
from __future__ import annotations

import argparse

from .config import Config
from .captions.styles import STYLE_ORDER
from .pipeline import make_reel


def main() -> None:
    p = argparse.ArgumentParser(prog="reels-studio",
                                description="استوديو ريلز - مونتاج تلقائي للريلز العربية")
    p.add_argument("input", help="ملف الفيديو أو الصوت الأساسي")
    p.add_argument("-o", "--out", default="output/reel.mp4", help="مسار الناتج")
    p.add_argument("--music", help="موسيقى خلفية (القطع هيتزامن مع الإيقاع)")
    p.add_argument("--script", help="نص التعليق الصوتي (يستبدل صوت الفيديو)")
    p.add_argument("--style", default=None, choices=STYLE_ORDER,
                   help="ستايل الكابشن")
    p.add_argument("--config", help="ملف إعدادات YAML")
    args = p.parse_args()

    cfg = Config.load(args.config)
    make_reel(args.input, out_path=args.out, music=args.music,
              script=args.script, caption_style=args.style, config=cfg)


if __name__ == "__main__":
    main()
