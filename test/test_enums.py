import unittest

from xpdt import NameSpace, StructDef, MemberDef, BaseType

class Test_RoundTrips(unittest.TestCase):
    def setUp(self):
        self.code = NameSpace(
            structs=(
                StructDef(
                    name='Item',
                    members=(
                        MemberDef('b', BaseType.bytes),
                        MemberDef('s', BaseType.utf8),
                    ),
                    discriminant=0xfacebeef,
                ),
            ),
            name='test',
        ).gen_dynamic_python()

    def test_item(self):
        orig = self.code.Item(b'\x00' * 4, 'Malkovich')
        b = orig._enum_wrap(ts)
        clone, = self.code.Test.read_many(memoryview(b))
        self.assertEqual((ts, orig), clone)

    def test_item(self):
        bad_utf = b'\xc3\x28'
        ts = 0

        orig = self.code.Item(b'\xff', 'AA')

        a = orig._enum_wrap(ts)
        a = a[:-len(bad_utf)] + bad_utf

        b = orig._enum_wrap(ts)

        first, second = list(self.code.Test.read_many(memoryview(a + b)))
        self.assertIsInstance(first, UnicodeDecodeError)
        self.assertEqual(second, (ts, orig))
