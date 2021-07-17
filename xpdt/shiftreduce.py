from __future__ import annotations
from typing import Dict, Optional, Callable, Any, TypeVar, Generic, cast
from typing_extensions import Protocol
from functools import wraps

"""
Helpers for shift/reduce parsing
"""

__all__ = (
    'ParseError',
    'state',
)


class Token(Protocol):
    @property
    def tok_type(self) -> Any: ...

    @property
    def val(self) -> str: ...

    @property
    def file(self) -> str: ...

    @property
    def line(self) -> int: ...


class ParseError(Exception):
    tok: Optional[Token]

    def __init__(self,
                 msg: str,
                 /,
                 tok: Optional[Token] = None,
                 ) -> None:
        super().__init__(msg)
        self.tok = tok

    def __str__(self) -> str:
        s = super().__str__()
        tok = self.tok
        if tok is None:
            return s
        return f'{tok.file}:{tok.line}: at "{tok.val}": {s}'


_T = TypeVar('_T')


class State(Generic[_T]):
    __slots__ = ()

    def on(self: _T, *args: str) -> Callable[..., StateFunc[_T]]: ...
    def default(self: _T) -> Callable[..., StateFunc[_T]]: ...
    def __call__(self: _T, tok: Token) -> NextState[_T]: ...


NextState = Optional[State[_T]]
StateFunc = Callable[[_T, Token], NextState[_T]]


def state(func: Callable[[_T], None]) -> State[_T]:
    registry: Dict[Any, StateFunc[_T]] = {}
    dfl: Optional[StateFunc[_T]] = None

    def on(*args: str) -> Callable[..., StateFunc[_T]]:
        def decorator(func: StateFunc[_T]) -> StateFunc[_T]:
            for tok_type in args:
                registry[tok_type] = func
            return func
        return decorator

    def default() -> Callable[..., StateFunc[_T]]:
        nonlocal dfl

        def decorator(func: StateFunc[_T]) -> StateFunc[_T]:
            nonlocal dfl
            dfl = func
            return func

        return decorator

    @wraps(func)
    def wrapper(self: _T, tok: Token) -> NextState[_T]:
        nonlocal dfl

        tok_type = tok.tok_type
        try:
            f = registry[tok_type]
        except KeyError:
            if dfl is not None:
                return dfl(self, tok)

            expected = ', '.join(sorted(registry.keys()))
            raise ParseError(
                f'{tok_type} unexpected, looking for {expected}',
                tok=tok,
            )
        return f(self, tok)

    wrapper.on = on  # type: ignore
    wrapper.default = default  # type: ignore

    return cast(State[_T], wrapper)
