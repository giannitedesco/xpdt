import unittest

from xpdt import NameSpace, StructDef, MemberDef, BaseType

class Test_RoundTrips(unittest.TestCase):
    def setUp(self):
        self.code = NameSpace(
            structs=(
                StructDef(
                    name='Point',
                    members=(
                        MemberDef('x', BaseType.s32),
                        MemberDef('y', BaseType.s32),
                        MemberDef('z', BaseType.s32),
                    ),
                ),
                StructDef(
                    name='Item',
                    members=(
                        MemberDef('id', BaseType.u32),
                        MemberDef('first_name', BaseType.blob),
                        MemberDef('surname', BaseType.blob),
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
        orig = self.code.Item(0xdeadbeef, b'Malkovich', b'')
        b = bytes(orig)
        clone = orig._frombytes(b)
        self.assertEqual(orig, clone)
