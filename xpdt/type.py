from __future__ import annotations

from typing import NamedTuple, Generator, Tuple, TYPE_CHECKING
from enum import Enum
from abc import ABC, abstractmethod
from struct import calcsize


if TYPE_CHECKING:
    from .member import MemberDef  # pragma: no cover


__all__ = (
    'ConstructAction',
    'ConstructElement',
    'XpdtType',
)


class ConstructAction(Enum):
    AGG_PUSH = 'agg_push'
    AGG_POP = 'agg_pop'
    MEMBER = 'member'


class ConstructElement(NamedTuple):
    action: ConstructAction
    member: MemberDef
    path: Tuple[MemberDef, ...] = ()

    def indent(self, pat: str = '\t', base: int = 0) -> str:
        return pat * (base + len(self.path))

    @property
    def path_names(self) -> Tuple[str, ...]:
        return tuple((x.name for x in self.path))

    @property
    def full_path(self) -> Tuple[MemberDef, ...]:
        return self.path + (self.member, )

    @property
    def full_path_names(self) -> Tuple[str, ...]:
        return tuple((x.name for x in self.full_path))

    @property
    def c_named_initializer(self) -> str:
        return '.'.join(self.full_path_names)

    @property
    def python_var_name(self) -> str:
        # FIXME: this is not prefix-free
        return f'_{"_".join(self.full_path_names)}'

    @property
    def is_reserved(self) -> bool:
        return self.member.is_reserved


class XpdtType(ABC):
    @property
    @abstractmethod
    def struct_fmt(self) -> str: ...

    @property
    @abstractmethod
    def ctype(self) -> str: ...

    @property
    @abstractmethod
    def pytype(self) -> str: ...

    @property
    @abstractmethod
    def needs_vbuf(self) -> bool: ...

    @property
    @abstractmethod
    def needs_decode(self) -> bool: ...

    @property
    def size(self) -> int:
        return calcsize(self.struct_fmt)

    @property
    def is_scalar(self) -> bool:
        return True

    @property
    def struct_name(self) -> str:
        # Only relevant for aggregate types
        raise NotImplementedError

    def construct_recursive(self,
                            path: Tuple[MemberDef, ...] = (),
                            include_reserved: bool = True,
                            ) -> Generator[ConstructElement, None, None]:
        # Only relevant for aggregate types
        raise NotImplementedError

    @property
    def scalar_members(self) -> Generator[ConstructElement, None, None]:
        raise NotImplementedError
