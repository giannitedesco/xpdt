from typing import (
    Optional, Tuple, Dict, NamedTuple, Type, TextIO, Iterable, Iterator, Any
)
from types import SimpleNamespace

from .dupes import dupes
from .decl import StructDecl, MemberDecl
from .typedef import TypeDef
from .basetypes import base_types
from .member import MemberDef
from .struct import StructDef, StructType
from .jinja import ctemplate, pytemplate
from .c import SysInclude

__all__ = (
    'NameSpace',
)


class NameSpace:
    __slots__ = (
        '_name',
        '_structs',
    )

    _name: Optional[str]
    _structs: Dict[str, StructDef]

    x1b_c = ctemplate.get_template('x1b.c')
    x1b_python = pytemplate.get_template('x1b.pyt')

    def __init__(self,
                 structs: Tuple[StructDef, ...],
                 name: Optional[str] = None):

        d = dupes((s.name for s in structs))
        if d:
            raise ValueError(f'{name}: Duplicated struct name: '
                             ", ".join(d))

        self._name = name

        # TODO: Allow sub-structs
        self._structs = {s.name: s for s in structs}

    @property
    def name(self) -> Optional[str]:
        return self._name

    def __iter__(self) -> Iterator[StructDef]:
        yield from self._structs.values()

    def __len__(self) -> int:
        return len(self._structs)

    def _gen_dynamic_clsname(self, s: StructDef) -> str:
        if self._name:
            return f'{self._name}.{s.name}'
        else:
            return s.name

    def _gen_storage_class(self, s: StructDef) -> Type[NamedTuple]:
        sig = [(m.name, m.typedef.type.pytype) for m in s]

        # This class is a tuple for storing the data in each instance
        # mypy insists on literals, but sorry, no can do...
        return NamedTuple(s.name, sig)  # type: ignore

    @property
    def python_code(self) -> str:
        return self.x1b_python.render(namespace=self)

    def gen_dynamic_python(self) -> SimpleNamespace:
        names = {s.name for s in self}
        g: Dict[str, Any] = {}
        exec(self.python_code, g, g)
        return SimpleNamespace(**{x: g[x] for x in names})

    def gen_python(self, f: TextIO) -> None:
        f.write(self.python_code)

    def gen_c(self, f: TextIO) -> None:
        x1b_hdr = SysInclude('xpdt/x1b.h')
        headers = (
            SysInclude('stdint.h'),
            SysInclude('stdbool.h'),
            SysInclude('string.h'),
        )

        code = self.x1b_c.render(
            headers=headers,
            namespace=self,
            x1b_hdr=x1b_hdr,
        )
        f.write(code)

    @classmethod
    def from_decls(cls,
                   decls: Iterable[StructDecl],
                   name: Optional[str] = None) -> 'NameSpace':

        typemap = base_types()

        def define_member(decl: MemberDecl) -> MemberDef:
            type_name = decl.type_name
            try:
                member_type = typemap[type_name]
            except KeyError:
                raise KeyError(f'Type "{type_name}" not known')
            return MemberDef(
                decl.member_name,
                member_type,
            )

        def define_struct(decl: StructDecl) -> StructDef:
            name = decl.struct_name
            struct = StructDef(
                name,
                tuple((define_member(m) for m in decl.members)),
            )
            if name in typemap:
                raise ValueError(f'Type {name} already defined')
            typemap[name] = TypeDef(name, StructType(struct))
            return struct

        defns = tuple((define_struct(decl) for decl in decls))

        return cls(defns, name)
