from typing import Iterable
from collections import Counter


__all__ = (
    'dupes',
)


def dupes[T](s: Iterable[T]) -> list[T]:
    return [x for x, y in Counter(s).items() if y > 1]
