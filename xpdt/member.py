from typing import NamedTuple

from .type import XpdtType
from .typedef import TypeDef


__all__ = (
    'MemberDef',
)


class MemberDef(NamedTuple):
    name: str
    typedef: TypeDef

    @property
    def needs_vbuf(self) -> bool:
        return self.typedef.type.needs_vbuf

    @property
    def cdecl(self) -> str:
        return f'{self.typedef.type.ctype} {self.name}'

    @property
    def const_cdecl(self) -> str:
        return f'const {self.cdecl}'

    @property
    def type(self) -> XpdtType:
        return self.typedef.type

    @property
    def is_scalar(self) -> bool:
        return self.typedef.type.is_scalar

    @property
    def is_reserved(self) -> bool:
        return self.name.startswith('_')
