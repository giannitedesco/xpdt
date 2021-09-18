from typing import Dict
from enum import Enum

from .integraltype import IntegralType
from .buftypes import BufType, Utf8Type, ByteArrayType, StringArrayType
from .uuidtype import UuidType
from .intstack import IntStackType
from .typedef import TypeDef

__all__ = (
    'BaseType',
    'base_types',
)

Bytes = BufType()
Utf8 = Utf8Type()
ByteArray = ByteArrayType()
StringArray = StringArrayType()

UnsignedInt8 = IntegralType(8, False)
SignedInt8 = IntegralType(8, True)
UnsignedInt16 = IntegralType(16, False)
SignedInt16 = IntegralType(16, True)
UnsignedInt32 = IntegralType(32, False)
SignedInt32 = IntegralType(32, True)
UnsignedInt64 = IntegralType(64, False)
SignedInt64 = IntegralType(64, True)

Uuid = UuidType()

IntStack8 = IntStackType(8)
IntStack16 = IntStackType(16)
IntStack32 = IntStackType(32)


class BaseType(TypeDef, Enum):
    __slots__ = ()

    bytes = 'bytes', Bytes
    utf8 = 'utf8', Utf8
    bytearray = 'bytearray', ByteArray
    stringarray = 'stringarray', StringArray

    u8 = 'u8', UnsignedInt8
    i8 = 'i8', SignedInt8
    u16 = 'u16', UnsignedInt16
    i16 = 'i16', SignedInt16
    u32 = 'u32', UnsignedInt32
    i32 = 'i32', SignedInt32
    u64 = 'u64', UnsignedInt64
    i64 = 'i64', SignedInt64

    u128 = 'u128', Uuid
    uuid = 'uuid', Uuid

    intstack8 = 'intstack8', IntStack8
    intstack16 = 'intstack16', IntStack16
    intstack32 = 'intstack32', IntStack32


def base_types() -> Dict[str, TypeDef]:
    return {t.name: t.value for t in BaseType}
