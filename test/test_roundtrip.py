import unittest

from xpdt import NameSpace, StructDef, MemberDef, BaseType

class Test_RoundTrips(unittest.TestCase):
    def setUp(self):
        self.code = NameSpace(
            structs=(
                StructDef(
                    name='Point',
                    members=(
                        MemberDef('x', BaseType.i32),
                        MemberDef('y', BaseType.i32),
                        MemberDef('z', BaseType.i32),
                        MemberDef('_pad0', BaseType.i32),
                        MemberDef('_pad1', BaseType.bytes),
                    ),
                ),
                StructDef(
                    name='Item',
                    members=(
                        MemberDef('uuid', BaseType.uuid),
                        MemberDef('id', BaseType.u32),
                        MemberDef('first_name', BaseType.utf8),
                        MemberDef('surname', BaseType.utf8),
                        MemberDef('data', BaseType.bytes),
                        MemberDef('_pad0', BaseType.i32),
                        MemberDef('_pad1', BaseType.bytes),
                    ),
                ),
            ),
            name=None,
        ).gen_dynamic_python()

    def test_point(self):
        orig = self.code.Point(1, -2, 3)
        b = bytes(orig)
        clone = orig._frombytes(b)
        self.assertEqual(orig, clone)


    def test_item(self):
        orig = self.code.Item(b'\x00' * 16, 0xdeadbeef, 'Malkovich', '', b'\x12\x34')
        b = bytes(orig)
        clone = orig._frombytes(b)
        self.assertEqual(orig, clone)
