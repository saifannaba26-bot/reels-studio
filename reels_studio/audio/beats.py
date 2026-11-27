"""Beat detection: cut points land on the music's beat."""
from __future__ import annotations


def detect_beats(music_path: str, min_gap: float = 0.8) -> list[float]:
    """Return beat times (seconds) for a music track, thinned to >= min_gap apart."""
    import librosa

    y, sr = librosa.load(music_path, sr=22050, mono=True)
    tempo, frames = librosa.beat.beat_track(y=y, sr=sr)
    times = librosa.frames_to_time(frames, sr=sr).tolist()

    thinned: list[float] = []
    for t in times:
        if not thinned or t - thinned[-1] >= min_gap:
            thinned.append(round(float(t), 3))
    return thinned


def snap_to_beats(times: list[float], beats: list[float]) -> list[float]:
    """Snap each cut time to the nearest beat."""
    if not beats:
        return times
    snapped = []
    for t in times:
        nearest = min(beats, key=lambda b: abs(b - t))
        snapped.append(nearest)
    return sorted(set(snapped))
