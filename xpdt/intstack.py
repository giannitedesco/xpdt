from .integraltype import IntegralType

__all__ = (
    'IntStackType',
)


class IntStackType(IntegralType):
    __slots__ = (
        '_width',
    )

    _struct_map = {
        8: 'b',
        16: 'h',
        32: 'i',
        64: 'q',
    }

    def __init__(self, width: int):
        super().__init__(64, False)
        self._width = width

    @property
    def _mask(self) -> int:
        return (1 << self._width) - 1

    @property
    def pytype(self) -> str:
        return '_Tup[int]'

    def read_func(self, s: str) -> str:
        return f'_decode_intstack({s}, 0x{self._mask:x}, {self._width})'

    def write_func(self, s: str) -> str:
        return f'_encode_intstack({s}, 0x{self._mask:x}, {self._width})'

    @property
    def needs_decode(self) -> bool:
        return True
