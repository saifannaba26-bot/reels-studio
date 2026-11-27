"""Motion graphics: animated lower thirds, progress bar, accent shapes."""
from __future__ import annotations


def lower_third(text: str, start: float, dur: float = 3.0,
                width: int = 1080, height: int = 1920) -> str:
    """ffmpeg drawbox+drawtext chain for an animated lower-third banner.

    Slides up from the bottom, holds, slides away. Arabic text must be passed
    through drawtext with a font that supports it (Cairo/Amiri) - libfreetype
    shapes it via HarfBuzz in modern ffmpeg builds.
    """
    y = int(height * 0.78)
    end = start + dur
    box = (
        f"drawbox=x=0:y='if(lt(t\\,{start})\\,{height}\\,"
        f"max({y}\\,{height}-({height}-{y})*(t-{start})/0.4))'"
        f":w={width}:h=140:color=black@0.55:t=fill"
        f":enable='between(t,{start},{end})'"
    )
    txt = (
        f"drawtext=text='{text}':fontfile=assets/fonts/Cairo-Bold.ttf"
        f":fontsize=52:fontcolor=white:x=(w-text_w)/2"
        f":y='if(lt(t\\,{start})\\,{height}\\,max({y}+35\\,{height}-({height}-{y}-35)*(t-{start})/0.4))'"
        f":enable='between(t,{start},{end})'"
    )
    return f"{box},{txt}"


def progress_bar(width: int = 1080, height: int = 1920, color: str = "0xFFD700") -> str:
    """Thin progress bar pinned to the top of the frame."""
    return (f"drawbox=x=0:y=12:w='(t/DUR)*{width}':h=8:color={color}@0.9:t=fill"
            .replace("DUR", "DUR_PLACEHOLDER"))
