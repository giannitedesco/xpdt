from .type import XpdtType
from .integraltype import IntegralType

__all__ = (
    'BufType',
    'Utf8Type',
    'ByteArrayType',
)


class BufBase(XpdtType):
    __slots__ = (
        '_off_type',
    )

    def __init__(self) -> None:
        self._off_type = IntegralType(32, False)

    @property
    def size(self) -> int:
        return self._off_type.size

    @property
    def struct_fmt(self) -> str:
        return self._off_type.struct_fmt

    @property
    def ctype(self) -> str:
        return 'struct xbuf'

    @property
    def needs_vbuf(self) -> bool:
        return True


class BufType(BufBase):
    __slots__ = ()

    @property
    def pytype(self) -> str:
        return 'bytes'

    def read_func(self, s: str) -> str:
        return f'tobytes({s})'

    def write_func(self, s: str) -> str:
        return s


class Utf8Type(BufBase):
    __slots__ = ()

    @property
    def pytype(self) -> str:
        return 'str'

    def read_func(self, s: str) -> str:
        return f'tostr(tobytes({s}))'

    def write_func(self, s: str) -> str:
        return f'{s}.encode()'


class ByteArrayType(BufBase):
    __slots__ = ()

    @property
    def pytype(self) -> str:
        return '_Tup[int]'

    def read_func(self, s: str) -> str:
        return f'tuple({s})'

    def write_func(self, s: str) -> str:
        return f'bytes({s})'