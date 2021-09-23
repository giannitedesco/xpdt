"""
xpdt: eXPeditious Data Transfer
"""

from .__version__ import \
    __title__, \
    __description__, \
    __url__, \
    __author__, \
    __author_email__, \
    __copyright__, \
    __license__, \
    __version__  # noqa: F401

from .type import XpdtType
from .typedef import TypeDef
from .basetypes import BaseType, base_types
from .member import MemberDef
from .struct import StructDef
from .decl import MemberDecl, StructDecl
from .namespace import NameSpace
from .parse import parse, parse_file
from .shiftreduce import ParseError
from .load import load

__all__ = (
    'XpdtType',

    'TypeDef',
    'BaseType',
    'base_types',

    'MemberDecl',
    'StructDecl',

    'MemberDef',
    'StructDef',

    'NameSpace',

    'parse',
    'parse_file',

    'ParseError',

    'load',
)
