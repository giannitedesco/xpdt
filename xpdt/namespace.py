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
from .c import Include, SysInclude, RelInclude

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
    chdr = ctemplate.get_template('apihdr.c')
    capi = ctemplate.get_template('api.c')
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

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

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

    @property
    def python_type_name(self) -> str:
        name = self._name
        if name is None:
            return 'XpdtBase'
        return f'{name.title()}Type'

    @property
    def python_enum_name(self) -> str:
        name = self._name
        assert name is not None
        return name.title()

    def gen_dynamic_python(self) -> SimpleNamespace:
        names = {s.name for s in self}
        names.add(self.python_type_name)
        if self._name is not None:
            names.add(self.python_enum_name)

        g: Dict[str, Any] = {}
        exec(self.python_code, g, g)
        return SimpleNamespace(**{x: g[x] for x in names})

    def gen_python(self, f: TextIO) -> None:
        f.write(self.python_code)

    def gen_c(self, f: TextIO) -> None:
        headers = (
            SysInclude('stdlib.h'),
            SysInclude('xpdt/xpdt.h'),
        )

        code = self.c.render(
            headers=headers,
            namespace=self,
        )
        f.write(code)

    def gen_c_api_entries(self, f: TextIO,
                          inc_prefix: Optional[str] = None,
                          ) -> None:
        api_hdr: Include
        if not inc_prefix:
            api_hdr = RelInclude(f'{self.name}_api.h')
        else:
            api_hdr = SysInclude(f'{inc_prefix}/{self.name}_api.h')

        headers = (
            api_hdr,
            RelInclude(f'{self.name}_impl.h'),
        )

        code = self.capi.render(
            headers=headers,
            namespace=self,
        )
        f.write(code)

    def gen_c_api_hdr(self, f: TextIO) -> None:
        headers = (
            SysInclude('xpdt/xpdt.h'),
        )
        code = self.chdr.render(
            headers=headers,
            namespace=self,
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
