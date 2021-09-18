import unittest

from xpdt import NameSpace, StructDecl, MemberDecl, BaseType

class Test_Stringy(unittest.TestCase):
    def setUp(self):
        self.code = NameSpace.from_decls(
            (
                StructDecl(
                    struct_name='Item',
                    members=[
                        MemberDecl('id', 'u32'),
                        MemberDecl('name', 'intstack16'),
                        MemberDecl('_pad0', 'u32'),
                        MemberDecl('_pad1', 'bytes'),
                    ],
                ),
                StructDecl(
                    struct_name='Entity',
                    members=[
                        MemberDecl('id', 'u32'),
                        MemberDecl('a', 'Item'),
                        MemberDecl('b', 'Item'),
                        MemberDecl('_pad0', 'u32'),
                        MemberDecl('_pad1', 'bytes'),
                        MemberDecl('_pad2', 'Item'),
                    ],
                ),
            ),
            name=None,
        ).gen_dynamic_python()

    def test_entity(self):
        obj_a = self.code.Item(1, (1, 2, 3, 4))
        obj_b = self.code.Item(2, (2, 4, 6, 8))
        orig = self.code.Entity(0xdeadbeef, obj_a, obj_b)
        b = bytes(orig)
        clone = orig._frombytes(b)
        self.assertEqual(orig, clone)

    def notest_entity_list(self):
        obj_a = self.code.Item(1, (1, 2, 3, 4))
        obj_b = self.code.Item(2, (1, 4, 6, 8))
        obj_c = self.code.Item(3, (3, 6, 9))
        ent_a = self.code.Entity(0xdeadbeef, obj_a, obj_b)
        ent_b = self.code.Entity(0xfeedface, obj_c, obj_b)

        orig = [ent_a, ent_b]

        clone = b''.join((bytes(ent) for ent in orig))
        view = memoryview(clone)

        tot_len = len(clone)
        decoded = []
        off = 0
        while off < tot_len:
            item_len, ent = self.code.Entity._frombuf(view, off)
            off += item_len
            decoded.append(ent)

        self.assertListEqual(orig, decoded)
