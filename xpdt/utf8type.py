from .buftype import BufType

__all__ = (
    'Utf8Type',
)


class Utf8Type(BufType):
    __slots__ = ()

    def read_func(self, s: str) -> str:
        return f'{s}.decode()'

    def write_func(self, s: str) -> str:
        return f'{s}.encode()'
