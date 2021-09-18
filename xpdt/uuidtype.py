from .type import XpdtType

__all__ = (
    'UuidType',
)


class UuidType(XpdtType):
    __slots__ = ()

    @property
    def ctype(self) -> str:
        return 'xu128_t'

    @property
    def pytype(self) -> str:
        return 'bytes'

    @property
    def struct_fmt(self) -> str:
        return '16s'

    @property
    def size(self) -> int:
        return 16

    @property
    def needs_vbuf(self) -> bool:
        return False

    @property
    def needs_decode(self) -> bool:
        return False
