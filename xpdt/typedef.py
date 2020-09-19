from typing import NamedTuple

from .type import XpdtType

__all__ = (
    'TypeDef',
)


class TypeDef(NamedTuple):
    name: str
    type: XpdtType
