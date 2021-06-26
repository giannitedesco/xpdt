from .buftype import BufType

__all__ = (
    'Utf8Type',
)


class Utf8Type(BufType):
    __slots__ = ()

    @property
    def pytype(self) -> str:
        return 'str'

    def read_func(self, s: str) -> str:
        return f'{s}.decode()'

    def write_func(self, s: str) -> str:
        return f'{s}.encode()'
