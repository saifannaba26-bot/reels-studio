"""Sound effects: whoosh on cuts, impacts on zooms, risers before drops."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class SfxEvent:
    file: str
    at: float          # seconds in the output timeline
    volume: float = 0.5


SFX_LIBRARY = {
    "whoosh": "whoosh.wav",
    "impact": "impact.wav",
    "riser": "riser.wav",
    "pop": "pop.wav",
    "ding": "ding.wav",
}


def plan_sfx(cut_times: list[float], zoom_kinds: list[str], sfx_dir: str | Path) -> list[SfxEvent]:
    """Place a whoosh on every cut and an impact on punch-zooms."""
    events: list[SfxEvent] = []
    sfx_dir = Path(sfx_dir)
    for i, t in enumerate(cut_times[1:], start=1):  # skip t=0
        kind = zoom_kinds[i - 1] if i - 1 < len(zoom_kinds) else "cut"
        name = "impact" if kind == "punch" else "whoosh"
        f = sfx_dir / SFX_LIBRARY[name]
        if f.exists():
            events.append(SfxEvent(file=str(f), at=t))
    return events
