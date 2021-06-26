from .type import XpdtType
from .integraltype import IntegralType

__all__ = (
    'BufType',
)


class BufType(XpdtType):
    __slots__ = (
        '_off_type',
    )

    def __init__(self) -> None:
        self._off_type = IntegralType(32, False)

    @property
    def struct_fmt(self) -> str:
        return self._off_type.struct_fmt

    @property
    def pytype(self) -> str:
        return 'bytes'

    @property
    def ctype(self) -> str:
        return 'struct xbuf'

    @property
    def size(self) -> int:
        return self._off_type.size

    @property
    def needs_vbuf(self) -> bool:
        return True

    def read_func(self, s: str) -> str:
        return s

    def write_func(self, s: str) -> str:
        return s
