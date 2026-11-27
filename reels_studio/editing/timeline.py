"""Cut plan: where to cut, how long each clip lasts, which zoom to apply."""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass


@dataclass
class Segment:
    start: float
    end: float
    zoom: str            # punch | slow_in | slow_out | shake | still
    source: str = "main"  # main | stock keyword


ZOOM_CYCLE = ["slow_in", "punch", "slow_out", "still", "punch", "shake", "slow_in"]


def plan_cuts(duration: float, beats: list[float], min_len: float = 1.2,
              max_len: float = 4.0, seed: int = 7) -> list[Segment]:
    """Cut on beats; keep segments between min_len and max_len."""
    rng = random.Random(seed)
    points = [0.0]
    candidates = [b for b in beats if min_len < b < duration - 0.3]
    last = 0.0
    for b in candidates:
        if b - last >= max_len or (b - last >= min_len and rng.random() < 0.5):
            points.append(b)
            last = b
    points.append(duration)

    zooms = itertools.cycle(ZOOM_CYCLE)
    segments = []
    for a, b in zip(points, points[1:]):
        if b - a < 0.2:
            continue
        segments.append(Segment(start=a, end=b, zoom=next(zooms)))
    return segments
