from typing import Tuple, Generator, Iterator

from .dupes import dupes

from .type import XpdtType, ConstructAction, ConstructElement
from .member import MemberDef


__all__ = (
    'StructDef',
    'StructType',
)


class StructDef:
    __slots__ = (
        '_name',
        '_membs',
        '_vmembs',
    )

    def __init__(self, name: str, members: Tuple[MemberDef, ...]):
        d = dupes((m.name for m in members))
        if d:
            raise ValueError(f'{name}: Duplicated member name: '
                             ", ".join(d))
        self._name = name
        self._membs = {m.name: m for m in members}
        self._vmembs = tuple((m for m in members
                              if m.needs_vbuf))

    @property
    def name(self) -> str:
        return self._name

    @property
    def ctype(self) -> str:
        return f'struct {self._name}'

    @property
    def tag(self) -> str:
        return self._name

    @property
    def member_types(self) -> Generator[XpdtType, None, None]:
        yield from (m.typedef.type for m in self)

    @property
    def vbuf_members(self) -> Tuple[MemberDef, ...]:
        return self._vmembs

    @property
    def needs_vbuf(self) -> bool:
        return any((t.needs_vbuf for t in self.member_types))

    @property
    def all_members_scalar(self) -> bool:
        return all((t.is_scalar for t in self.member_types))

    @property
    def all_members(self) -> Generator[ConstructElement, None, None]:
        return (elem for elem in
                self.construct_recursive()
                if elem.action == ConstructAction.MEMBER)

    @property
    def all_vbuf_members(self) -> Generator[ConstructElement, None, None]:
        return (elem for elem in
                self.construct_recursive()
                if elem.action == ConstructAction.MEMBER
                and elem.member.type.needs_vbuf)

    @property
    def scalar_members(self) -> Generator[Tuple[str, ...], None, None]:
        return (elem.full_path_names for elem in
                self.construct_recursive()
                if elem.action == ConstructAction.MEMBER)

    @property
    def python_var_names(self) -> Generator[str, None, None]:
        return (elem.python_var_name for elem in
                self.construct_recursive()
                if elem.action == ConstructAction.MEMBER)

    @property
    def c_named_initializers(self) -> Generator[str, None, None]:
        return (elem.c_named_initializer for elem in
                self.construct_recursive()
                if elem.action == ConstructAction.MEMBER)

    @property
    def c_named_initializers_x1v(self) -> Generator[str, None, None]:
        return (elem.c_named_initializer for elem in
                self.construct_recursive()
                if elem.action == ConstructAction.MEMBER
                and elem.member.type.needs_vbuf)

    @property
    def python_vbuf_names(self) -> Generator[str, None, None]:
        return (elem.python_var_name for elem in
                self.construct_recursive()
                if elem.action == ConstructAction.MEMBER
                and elem.member.type.needs_vbuf)

    def construct_recursive(self,
                            path: Tuple[MemberDef, ...] = (),
                            ) -> Generator[ConstructElement, None, None]:
        for m in self:
            if m.is_scalar:
                yield ConstructElement(ConstructAction.MEMBER, m, path)
            else:
                stype = m.type
                new_path = path + (m,)
                yield ConstructElement(ConstructAction.AGG_PUSH, m, path)
                yield from stype.construct_recursive(new_path)
                yield ConstructElement(ConstructAction.AGG_POP, m, path)

    @property
    def struct_fmt(self) -> str:
        return ''.join((t.struct_fmt for t in self.member_types))

    def __getitem__(self, k: str) -> MemberDef:
        return self._membs[k]

    def __iter__(self) -> Iterator[MemberDef]:
        return iter(self._membs.values())

    def __len__(self) -> int:
        return len(self._membs)


class StructType(XpdtType):
    __slots__ = (
        '_struct',
    )

    _struct: StructDef

    def __init__(self, struct: StructDef):
        self._struct = struct

    @property
    def _members(self) -> Generator[MemberDef, None, None]:
        yield from self._struct

    @property
    def _member_types(self) -> Generator[XpdtType, None, None]:
        yield from (m.typedef.type for m in self._struct)

    @property
    def struct_fmt(self) -> str:
        return self._struct.struct_fmt

    @property
    def struct_tag(self) -> str:
        return self._struct.tag

    @property
    def struct(self) -> StructDef:
        return self._struct

    @property
    def ctype(self) -> str:
        return self._struct.ctype

    @property
    def needs_vbuf(self) -> bool:
        return any((t.needs_vbuf for t in self._member_types))

    @property
    def pytype(self) -> str:
        return self._struct.name

    @property
    def is_scalar(self) -> bool:
        return False

    @property
    def struct_name(self) -> str:
        # Allow the possibility for typedef and struct name to differ
        return self._struct.name

    def construct_recursive(self,
                            path: Tuple[MemberDef, ...] = (),
                            ) -> Generator[ConstructElement, None, None]:
        yield from self._struct.construct_recursive(path)

    @property
    def scalar_members(self) -> Generator[Tuple[str, ...], None, None]:
        yield from self._struct.scalar_members
