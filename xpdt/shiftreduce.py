from __future__ import annotations
from typing import Optional, Callable, Any, cast
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


class State[T]:
    __slots__ = ()

    def on(self: T, *args: str) -> Callable[..., StateFunc[T]]:
        raise NotImplementedError

    def default(self: T) -> Callable[..., StateFunc[T]]:
        raise NotImplementedError

    def __call__(self: T, tok: Token) -> NextState[T]:
        raise NotImplementedError


type NextState[T] = Optional[State[T]]
type StateFunc[T] = Callable[[T, Token], NextState[T]]


def state[T](func: Callable[[T], None]) -> State[T]:
    registry: dict[Any, StateFunc[T]] = {}
    dfl: Optional[StateFunc[T]] = None

    def on(*args: str) -> Callable[..., StateFunc[T]]:
        def decorator(func: StateFunc[T]) -> StateFunc[T]:
            for tok_type in args:
                registry[tok_type] = func
            return func
        return decorator

    def default() -> Callable[..., StateFunc[T]]:
        def decorator(func: StateFunc[T]) -> StateFunc[T]:
            nonlocal dfl
            dfl = func
            return func

        return decorator

    @wraps(func)
    def wrapper(self: T, tok: Token) -> NextState[T]:
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

    return cast(State[T], wrapper)
