from .type import XpdtType

__all__ = (
    'UuidType',
)


class UuidType(XpdtType):
    __slots__ = ()

    pytype = 'bytes'

    @property
    def ctype(self) -> str:
        return 'xu128_t'

    @property
    def struct_fmt(self) -> str:
        return '16s'

    @property
    def size(self) -> int:
        return 16

    @property
    def needs_vbuf(self) -> bool:
        return False
