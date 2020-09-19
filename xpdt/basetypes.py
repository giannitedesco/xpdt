from typing import Dict
from enum import Enum

from .integraltype import IntegralType
from .buftype import BufType
from .uuidtype import UuidType
from .typedef import TypeDef

__all__ = (
    'BaseType',
    'base_types',
)

Blob = BufType()
xu128 = UuidType()
UnsignedInt8 = IntegralType(8, False)
SignedInt8 = IntegralType(8, True)
UnsignedInt16 = IntegralType(16, False)
SignedInt16 = IntegralType(16, True)
UnsignedInt32 = IntegralType(32, False)
SignedInt32 = IntegralType(32, True)
UnsignedInt64 = IntegralType(64, False)
SignedInt64 = IntegralType(64, True)


class BaseType(TypeDef, Enum):
    __slots__ = ()

    blob = 'blob', Blob
    u8 = 'u8', UnsignedInt8
    s8 = 's8', SignedInt8
    u16 = 'u16', UnsignedInt16
    s16 = 's16', SignedInt16
    u32 = 'u32', UnsignedInt32
    s32 = 's32', SignedInt32
    u64 = 'u64', UnsignedInt64
    s64 = 's64', SignedInt64
    u128 = 'u128', xu128
    uuid = 'uuid', xu128


def base_types() -> Dict[str, TypeDef]:
    return {t.name: t.value for t in BaseType}
