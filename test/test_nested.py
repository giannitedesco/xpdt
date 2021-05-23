import unittest

from xpdt import NameSpace, StructDecl, MemberDecl, BaseType

class Test_Nested(unittest.TestCase):
    def setUp(self):
        self.code = NameSpace.from_decls(
            (
                StructDecl(
                    struct_name='Point',
                    members=[
                        MemberDecl('x', 's32'),
                        MemberDecl('y', 's32'),
                        MemberDecl('z', 's32'),
                    ],
                ),
                StructDecl(
                    struct_name='Entity',
                    members=[
                        MemberDecl('id', 'u32'),
                        MemberDecl('pos', 'Point'),
                    ],
                ),
            ),
            name=None,
        ).gen_dynamic_python()

    def test_point(self):
        point = self.code.Point(1, 2, 3)
        orig = self.code.Entity(0xdeadbeef, point)
        b = bytes(orig)
        clone = orig._frombytes(b)
        self.assertEqual(orig, clone)
