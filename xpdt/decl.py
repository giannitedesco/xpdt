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
