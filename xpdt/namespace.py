from typing import (
    Optional, Tuple, Dict, TextIO, Iterable, Iterator, Any
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

    c = ctemplate.get_template('xpdt.c')
    python = pytemplate.get_template('xpdt.pyt')

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

    @property
    def has_name(self) -> bool:
        return self._name is not None

    def __iter__(self) -> Iterator[StructDef]:
        yield from self._structs.values()

    def __len__(self) -> int:
        return len(self._structs)

    @property
    def python_code(self) -> str:
        return self.python.render(namespace=self)

    def gen_dynamic_python(self) -> SimpleNamespace:
        names = {s.name for s in self}
        g: Dict[str, Any] = {}
        exec(self.python_code, g, g)
        return SimpleNamespace(**{x: g[x] for x in names})

    def gen_python(self, f: TextIO) -> None:
        f.write(self.python_code)

    def gen_c(self, f: TextIO) -> None:
        xpdt_hdr = SysInclude('xpdt/xpdt.h')
        headers = (
        )

        code = self.c.render(
            headers=headers,
            namespace=self,
            xpdt_hdr=xpdt_hdr,
        )
        f.write(code)

    @classmethod
    def from_decls(cls,
                   decls: Iterable[StructDecl],
                   name: Optional[str] = None) -> 'NameSpace':
        this = name if name is not None else '<anon>'

        typemap = base_types()

        def define_member(decl: MemberDecl) -> MemberDef:
            type_name = decl.type_name
            try:
                member_type = typemap[type_name]
            except KeyError:
                raise KeyError(f'{this}: Type {type_name!r} not known')
            return MemberDef(
                decl.member_name,
                member_type,
            )

        def define_struct(decl: StructDecl) -> StructDef:
            name = decl.struct_name
            struct = StructDef(
                name,
                tuple((define_member(m) for m in decl.members)),
                discriminant=decl.discriminant,
            )
            if name in typemap:
                raise ValueError(f'{this}: Type {name!r} already defined')
            typemap[name] = TypeDef(name, StructType(struct))
            return struct

        defns = tuple((define_struct(decl) for decl in decls))

        return cls(defns, name)
