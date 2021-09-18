from .type import XpdtType

__all__ = (
    'IntegralType',
)


class IntegralType(XpdtType):
    __slots__ = (
        '_width',
        '_signed',
        '_fmt',
        '_size',
        '_ctype',
    )

    _struct_map = {
        8: 'b',
        16: 'h',
        32: 'i',
        64: 'q',
    }

    def __init__(self, width: int, signed: bool):
        self._width = width
        self._signed = signed
        fmt = self._struct_map[self._width]
        if signed:
            self._ctype = f'int{width}_t'
            fmt = fmt.lower()
        else:
            self._ctype = f'uint{width}_t'
            fmt = fmt.upper()
        self._fmt = fmt
        self._size = super().size

    @property
    def ctype(self) -> str:
        return self._ctype

    @property
    def pytype(self) -> str:
        return 'int'

    @property
    def struct_fmt(self) -> str:
        return self._fmt

    @property
    def size(self) -> int:
        return self._size

    @property
    def needs_vbuf(self) -> bool:
        return False

    @property
    def needs_decode(self) -> bool:
        return False
