"""Zoom/movement presets as ffmpeg zoompan expressions."""
from __future__ import annotations

FPS_DEFAULT = 30


def zoom_filter(kind: str, frames: int, fps: int = FPS_DEFAULT) -> str:
    """Return a zoompan filter string for one segment of *frames* frames."""
    z = {
        # punch: fast zoom 1.0 -> 1.25 in first 8 frames, holds
        "punch": "zoompan=z='min(1.0+0.25*min(on/8\\,1),1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s=1080x1920:fps={fps}",
        # slow in: gentle 1.0 -> 1.15 over the whole segment
        "slow_in": "zoompan=z='1.0+0.15*on/{d}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s=1080x1920:fps={fps}",
        # slow out: 1.15 -> 1.0
        "slow_out": "zoompan=z='1.15-0.15*on/{d}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s=1080x1920:fps={fps}",
        # shake: static zoom + sinusoidal shake
        "shake": "zoompan=z='1.12':x='iw/2-(iw/zoom/2)+8*sin(on*1.5)':y='ih/2-(ih/zoom/2)+6*cos(on*1.2)':d={d}:s=1080x1920:fps={fps}",
        # still: just reframe
        "still": "zoompan=z='1.0':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s=1080x1920:fps={fps}",
    }[kind]
    return z.format(d=max(1, frames), fps=fps)
