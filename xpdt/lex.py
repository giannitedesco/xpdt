from typing import NamedTuple, Generator, FrozenSet, Pattern
import re

from .shiftreduce import ParseError


__all__ = (
    'lex',
    'Lexeme',
)


_re = re.compile('|'.join((
    r'(?P<kw_struct>\bstruct\b)',
    r'(?P<identifier>[a-zA-Z_][a-zA-Z0-9_]*)',
    r'(?P<num>[0-9][0-9]*)',
    r'(?P<lbrace>\{)',
    r'(?P<rbrace>\})',
    r'(?P<semicolon>;)',
    r'(?P<comment>#.*?(?=\n))',          # up to but not including newline
    r'(?P<whitespace>[^\S\n][^\S\n]*)',  # non-newline whitespace
    r'(?P<newline>\n)',
)))
_ignore_toks = frozenset({'whitespace', 'comment', 'newline'})


class Lexeme(NamedTuple):
    tok_type: str
    val: str
    file: str
    line: int


def lex(s: str,
        file: str = '<string>',
        line: int = 1,
        eof: bool = True,
        _ignored: FrozenSet[str] = _ignore_toks,
        _dfa: Pattern[str] = _re,
        ) -> Generator[Lexeme, None, None]:
    pos = 0

    while True:
        m = _dfa.match(s, pos)
        if not m:
            break
        grp = m.lastgroup
        begin, end = m.span()
        pos = end
        if grp not in _ignored:
            assert(grp is not None)
            yield Lexeme(grp, s[begin:end], file, line)
        elif grp == 'newline':
            line += 1

    if pos < len(s):
        bad = s[pos:]
        if len(bad) > 32:
            bad = bad[:29] + '...'
        tok = Lexeme('unknown', bad, file, line)
        raise ParseError('Lex error', tok)

    if eof:
        yield Lexeme('eof', '$', file, line)
