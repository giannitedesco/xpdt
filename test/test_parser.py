import unittest

from io import StringIO

from xpdt import NameSpace, parse, ParseError


_all_fixed = '''
struct fixed {
    u128 u128;
    u64 u64;
    i64 i64;
    u32 u32;
    i32 i32;
    u16 u16;
    i16 i16;
    u8 u8;
    i8 i8;
};
'''

_all_types = '''
struct fixed {
    bytes bytes;
    u128 u128;
    u64 u64;
    i64 i64;
    u32 u32;
    i32 i32;
    u16 u16;
    i16 i16;
    u8 u8;
    i8 i8;
};
'''

class Test_Parser(unittest.TestCase):
    def test_parse_error(self):
        with self.assertRaises(ParseError):
            decls = list(parse('flibble'))

    def test_parse_error_message(self):
        try:
            decls = list(parse('struct x {\nflibble', file='flibble'))
        except ParseError as e:
            buf = str(e)
            self.assertTrue('flibble:2' in buf)

    def test_parse_error_fields(self):
        try:
            decls = list(parse('struct x {\nflibble', file='flibble'))
        except ParseError as e:
            self.assertEqual(e.tok.file, 'flibble')
            self.assertEqual(e.tok.line, 2)

    def test_parse_all_fixed(self):
        decls = parse(_all_fixed)
        ns = NameSpace.from_decls(decls, name=None)
        self.assertEqual(ns.name, None)
        self.assertEqual(len(ns), 1)

    def test_parse_all_types(self):
        decls = parse(_all_types)
        ns = NameSpace.from_decls(decls, name=None)
        self.assertEqual(ns.name, None)
        self.assertEqual(len(ns), 1)

    def test_gen_c_fixed(self):
        decls = parse(_all_fixed)
        ns = NameSpace.from_decls(decls, name=None)
        buf = StringIO()
        ns.gen_c(buf)
        c_prog = buf.getvalue()

    def test_gen_c_vbuf(self):
        decls = parse(_all_types)
        ns = NameSpace.from_decls(decls, name=None)
        buf = StringIO()
        ns.gen_c(buf)
        c_prog = buf.getvalue()

    def test_gen_python_fixed(self):
        decls = parse(_all_fixed)
        ns = NameSpace.from_decls(decls, name=None)
        buf = StringIO()
        ns.gen_python(buf)
        c_prog = buf.getvalue()

    def test_gen_python_vbuf(self):
        decls = parse(_all_types)
        ns = NameSpace.from_decls(decls, name=None)
        buf = StringIO()
        ns.gen_python(buf)
        c_prog = buf.getvalue()
