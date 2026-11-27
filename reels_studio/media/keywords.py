"""Pull b-roll search keywords out of an Arabic transcript."""
from __future__ import annotations

from ..transcribe import Word

AR_STOPWORDS = set("""في من على إلى عن أن إن كان كانت هو هي هذا هذه ذلك التي الذي
مع أو لا لم لن ما مما عند بعد قبل كل بين حتى إذا كيف لماذا لكن ثم قد لقد و يا
the a an of to and or in on for with""".split())


def extract_keywords(words: list[Word], per_window: int = 12) -> list[tuple[float, str]]:
    """Return (time, keyword) pairs: one visual keyword per speech window."""
    pairs: list[tuple[float, str]] = []
    for i in range(0, len(words), per_window):
        window = words[i:i + per_window]
        candidates = [w for w in window
                      if len(w.text) > 3 and w.text not in AR_STOPWORDS]
        if candidates:
            pick = max(candidates, key=lambda w: len(w.text))
            pairs.append((window[0].start, pick.text))
    return pairs
