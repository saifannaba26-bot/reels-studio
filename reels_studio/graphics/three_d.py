"""3D-look graphics: perspective tilt, parallax layers, rotating accent cards.

True 3D rendering is out of scope for an ffmpeg pipeline; these filters fake
depth with perspective transforms and layered motion, which reads as 3D on
mobile feeds.
"""
from __future__ import annotations


def perspective_tilt(start: float, dur: float = 1.5) -> str:
    """Quick perspective 'card flip' accent, enabled for a window of time."""
    end = start + dur
    return (
        "perspective=x0='if(between(t,{s},{e}),W*0.08*sin((t-{s})/{d}*PI),0)'"
        ":y0=0:x1='if(between(t,{s},{e}),W*(1-0.08*sin((t-{s})/{d}*PI)),W)'"
        ":y1=0:x2='if(between(t,{s},{e}),W*(1-0.08*sin((t-{s})/{d}*PI)),W)'"
        ":y2=H:x3='if(between(t,{s},{e}),W*0.08*sin((t-{s})/{d}*PI),0)':y3=H"
    ).format(s=start, e=end, d=dur)


def parallax_caption_plane() -> str:
    """Placeholder docstring for the parallax layer: captions render on their
    own ASS layer, which already sits 'in front' of the video; combining that
    with the behind-person mask gives a real depth stack:
    background video -> caption layer -> person mask."""
    return ""
