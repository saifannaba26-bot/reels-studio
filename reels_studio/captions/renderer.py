"""Render word groups into a styled .ass subtitle file."""
from __future__ import annotations

import re
from pathlib import Path

from ..transcribe import Word, group_words
from .styles import CaptionStyle, STYLES

_ARABIC_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def _ass_time(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _emphasize_numbers(text: str) -> str:
    """Make any number huge (used by the 'numbers' style)."""
    def repl(m: re.Match) -> str:
        return r"{\fs160\b1}" + m.group(0) + r"{\fs80\b1}"
    return re.sub(r"[0-9٠-٩]+", repl, text)


def build_ass(groups: list[list[Word]], style: CaptionStyle,
              width: int = 1080, height: int = 1920) -> str:
    bold = -1 if style.bold else 0
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
ScaledBorderAndShadow: yes
WrapStyle: 0
RTL: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{style.font},{style.font_size},{style.primary},{style.highlight},{style.outline},&H64000000,{bold},0,0,0,100,100,0,0,1,{style.outline_w},{style.shadow},{style.alignment},40,40,{style.margin_v},178

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines: list[str] = []
    for g in groups:
        start, end = g[0].start, g[-1].end
        text = " ".join(w.text for w in g)
        text = text.translate(_ARABIC_DIGITS)
        tags = ""
        if style.karaoke:
            # word-by-word sweep highlight
            parts = []
            for w in g:
                cs = max(1, int((w.end - w.start) * 100))
                parts.append(r"{\kf%d}%s" % (cs, w.text.translate(_ARABIC_DIGITS)))
            text = " ".join(parts)
        if style.pop_in:
            tags += r"{\fscx30\fscy30\t(0,150,\fscx100\fscy100)}"
        if style.key == "motion3d":
            tags += r"{\frz-4\t(0,200,\frz0)\fscx40\fscy40\t(0,200,\fscx100\fscy100)}"
        if style.numbers_mode:
            text = _emphasize_numbers(text)
        if tags and style.karaoke:
            # karaoke override tags are inline; wrap group-level tags separately
            text = tags + text if not text.startswith("{") else text.replace("{", tags + "{", 1) if False else tags + text
        elif tags:
            text = tags + text
        lines.append(f"Dialogue: 0,{_ass_time(start)},{_ass_time(end)},Cap,,0,0,0,,{text}")
    return header + "\n".join(lines) + "\n"


def write_captions(words: list[Word], style_key: str, out_path: str | Path,
                   width: int = 1080, height: int = 1920) -> Path:
    style = STYLES[style_key]
    groups = group_words(words)
    ass = build_ass(groups, style, width, height)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ass, encoding="utf-8")
    return out
