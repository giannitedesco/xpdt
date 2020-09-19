from typing import Iterable, TypeVar, List
from collections import Counter


__all__ = (
    'dupes',
)


_T = TypeVar('_T')


def dupes(s: Iterable[_T]) -> List[_T]:
    return [x for x, y in Counter(s).items() if y > 1]
