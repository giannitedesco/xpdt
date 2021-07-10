from typing import NamedTuple, List, Optional

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
    discriminant: Optional[int] = None

    def with_prefix(self, pfx: str) -> 'StructDecl':
        new_name = f'{pfx}_{self.struct_name}'
        return self._replace(struct_name=new_name)

    def with_discriminant(self, d: int) -> 'StructDecl':
        assert self.discriminant is None
        return self._replace(discriminant=d)
