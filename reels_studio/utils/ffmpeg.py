"""Thin ffmpeg/ffprobe helpers. All heavy lifting is done by ffmpeg itself."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


class FFmpegError(RuntimeError):
    pass


def run(cmd: list[str]) -> None:
    """Run a command, raising with stderr on failure."""
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise FFmpegError(f"command failed: {' '.join(cmd[:6])}...\n{proc.stderr[-2000:]}")


def probe(path: str | Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


def duration(path: str | Path) -> float:
    info = probe(path)
    return float(info["format"]["duration"])


def has_audio(path: str | Path) -> bool:
    info = probe(path)
    return any(s["codec_type"] == "audio" for s in info["streams"])
