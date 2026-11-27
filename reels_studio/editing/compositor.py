"""Assemble the final reel with ffmpeg.

Multi-step render (robust > clever):
  1. Cut + zoom each segment to a temp clip.
  2. Concat segments with xfade transitions.
  3. Overlay stock b-roll where the speech calls for it.
  4. Burn styled Arabic captions (.ass via libass).
  5. Mix voice/music/sfx.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from ..audio.sfx import SfxEvent
from ..utils import ffmpeg as ff
from .timeline import Segment
from .zoom import zoom_filter

XFADE = "fade"


def _render_segment(src: str, seg: Segment, out: Path, fps: int) -> None:
    frames = int((seg.end - seg.start) * fps)
    vf = (
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,{zoom_filter(seg.zoom, frames, fps)},setsar=1"
    )
    ff.run(["ffmpeg", "-y", "-ss", f"{seg.start:.3f}", "-i", src,
            "-t", f"{seg.end - seg.start:.3f}", "-vf", vf,
            "-an", "-r", str(fps), "-c:v", "libx264", "-preset", "fast",
            "-crf", "20", str(out)])


def _concat(parts: list[Path], out: Path, fps: int) -> None:
    if len(parts) == 1:
        out.write_bytes(parts[0].read_bytes())
        return
    inputs: list[str] = []
    for p in parts:
        inputs += ["-i", str(p)]
    # xfade chain (video only; audio handled later from original source)
    chain = ""
    prev = "0:v"
    offset = 0.0
    durs = [ff.duration(p) for p in parts]
    for i in range(1, len(parts)):
        offset += durs[i - 1] - (0.25 if i > 1 else 0)
        lbl = f"x{i}"
        chain += f"[{prev}][{i}:v]xfade=transition={XFADE}:duration=0.25:offset={max(0.0, offset):.3f}[{lbl}];"
        prev = lbl
    ff.run(["ffmpeg", "-y", *inputs, "-filter_complex", chain.rstrip(";"),
            "-map", f"[{prev}]", "-r", str(fps), "-c:v", "libx264",
            "-preset", "fast", "-crf", "20", str(out)])


def _overlay_stock(base: Path, overlays: list[tuple[Path, float, float]],
                   out: Path, fps: int) -> Path:
    """Overlay stock clips (path, at, duration) fullscreen over the base video."""
    if not overlays:
        return base
    inputs = ["-i", str(base)]
    for p, _, _ in overlays:
        inputs += ["-i", str(p)]
    chain = ""
    prev = "0:v"
    for i, (_, at, dur) in enumerate(overlays, start=1):
        lbl = f"ov{i}"
        chain += (f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
                  f"crop=1080:1920,setsar=1,setpts=PTS-STARTPTS+{at:.3f}/TB[s{i}];"
                  f"[{prev}][s{i}]overlay=eof_action=pass:enable='between(t,{at:.3f},{at + dur:.3f})'[{lbl}];")
        prev = lbl
    ff.run(["ffmpeg", "-y", *inputs, "-filter_complex", chain.rstrip(";"),
            "-map", f"[{prev}]", "-r", str(fps), "-c:v", "libx264",
            "-preset", "fast", "-crf", "20", str(out)])
    return out


def _burn_captions(video: Path, ass: Path, out: Path, fps: int) -> None:
    vf = f"ass='{ass}'"
    ff.run(["ffmpeg", "-y", "-i", str(video), "-vf", vf,
            "-r", str(fps), "-c:v", "libx264", "-preset", "fast",
            "-crf", "19", "-pix_fmt", "yuv420p", str(out)])


def _mix_audio(video: Path, source_media: str, music: str | None,
               sfx_events: list[SfxEvent], music_volume: float,
               sfx_volume: float, out: Path, voiceover: str | None = None) -> None:
    inputs = ["-i", str(video)]
    tracks: list[tuple[int, str, float, float]] = []  # (input_idx, kind, volume, delay)
    idx = 1
    if voiceover:
        inputs += ["-i", voiceover]
        tracks.append((idx, "voice", 1.0, 0.0))
        idx += 1
    elif ff.has_audio(source_media):
        inputs += ["-i", source_media]
        tracks.append((idx, "voice", 1.0, 0.0))
        idx += 1
    if music:
        inputs += ["-i", music]
        tracks.append((idx, "music", music_volume, 0.0))
        idx += 1
    for ev in sfx_events:
        inputs += ["-i", ev.file]
        tracks.append((idx, "sfx", ev.volume * sfx_volume / 0.5, ev.at))
        idx += 1

    if not tracks:
        ff.run(["ffmpeg", "-y", *inputs, "-c", "copy", str(out)])
        return

    chain_parts = []
    mix_inputs = ""
    for n, (src_idx, kind, vol, delay) in enumerate(tracks):
        part = f"[{src_idx}:a]volume={vol}"
        if delay > 0:
            ms = int(delay * 1000)
            part += f",adelay={ms}|{ms}"
        part += f"[a{n}]"
        chain_parts.append(part)
        mix_inputs += f"[a{n}]"
    chain = ";".join(chain_parts) + (
        f";{mix_inputs}amix=inputs={len(tracks)}:duration=first:dropout_transition=0,"
        f"alimiter=limit=0.95[aout]")
    ff.run(["ffmpeg", "-y", *inputs, "-filter_complex", chain,
            "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)])


def compose(source: str, segments: list[Segment], out_path: str,
            captions_ass: Path | None = None,
            stock_overlays: list[tuple[Path, float, float]] | None = None,
            music: str | None = None, voiceover: str | None = None,
            sfx_events: list[SfxEvent] | None = None,
            music_volume: float = 0.18, fps: int = 30) -> Path:
    work = Path(tempfile.mkdtemp(prefix="reels_"))
    parts = []
    for i, seg in enumerate(segments):
        part = work / f"seg_{i:03d}.mp4"
        _render_segment(source, seg, part, fps)
        parts.append(part)

    body = work / "body.mp4"
    _concat(parts, body, fps)

    if stock_overlays:
        ov = work / "overlaid.mp4"
        body = _overlay_stock(body, stock_overlays, ov, fps)

    if captions_ass:
        capped = work / "capped.mp4"
        _burn_captions(body, captions_ass, capped, fps)
        body = capped

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    _mix_audio(body, source, music, sfx_events or [], music_volume, 0.5, out,
               voiceover=voiceover)
    return out
