from typing import NamedTuple, List

__all__ = (
    'MemberDecl',
    'StructDecl',
)


class MemberDecl(NamedTuple):
    member_name: str
    type_name: str


class StructDecl(NamedTuple):
    struct_name: str
    members: List[MemberDecl]

    def prefix(self, pfx: str) -> 'StructDecl':
        new_name = f'{pfx}_{self.struct_name}'
        return self._replace(struct_name=new_name)
