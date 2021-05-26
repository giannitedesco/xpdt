from __future__ import annotations
from typing import NamedTuple, Dict, Generator, List, Optional, Union
from pathlib import Path

from .decl import StructDecl, MemberDecl
from .shiftreduce import state, State, ParseError
from .lex import lex, Lexeme

__all__ = (
    'parse',
    'parse_file',
)


class MemberTypeItem(NamedTuple):
    member_type: str


class MemberNameItem(NamedTuple):
    member_name: str


class NamespaceItem(NamedTuple):
    ns: Dict[str, StructDecl]


# These are the stack items for the for LR parser stack
Item = Union[
    MemberTypeItem,
    MemberNameItem,
    NamespaceItem,
    StructDecl,
]


class Parser:
    __slots__ = (
        '_tokens',
        '_stack',
    )

    _stack: List[Item]

    def __init__(self, toks: Generator[Lexeme, None, None]):
        self._tokens = toks
        self._stack = list()

    def push(self, item: Item) -> None:
        self._stack.append(item)

    def pop(self) -> Item:
        return self._stack.pop()

    def stacktop(self) -> Item:
        return self._stack[-1]

    def __iter__(self) -> Generator[StructDecl, None, None]:
        self._stack.clear()
        self.push(NamespaceItem({}))

        gen = self._tokens
        st: Optional[State[Parser]] = self._initial

        while st is not None:
            try:
                tok = next(gen)
            except StopIteration:
                raise ParseError('Unexpected end of token-stream')

            st = st(tok)

        ns_item = self.pop()
        assert isinstance(ns_item, NamespaceItem)

        yield from ns_item.ns.values()

    @classmethod
    def fromstring(cls, s: str, file: str = '<string>') -> Parser:
        return cls(lex(s, file=file))

    @classmethod
    def fromfile(cls, p: Path) -> Parser:
        """
        Loads the file, line at a time.
        """

        def gen() -> Generator[Lexeme, None, None]:
            file = str(p)
            with p.open() as f:
                lno = 1
                for line in f:
                    yield from lex(line, file, lno, False)
                    lno += 1
            yield Lexeme('eof', '$', file, lno)
        return cls(gen())

    # Define our states
    @state
    def _initial(self) -> None: ...

    @state
    def _struct_name(self) -> None: ...

    @state
    def _type_start(self) -> None: ...

    @state
    def _member_type(self) -> None: ...

    @state
    def _member_name(self) -> None: ...

    @state
    def _member_end(self) -> None: ...

    # These methods encode what would be the contents of the ACTION/GOTO tables
    # if this were a generated table-based parser.
    #  - The return values define the result of the GOTO table lookup
    #  - The method body either performs a shift or a reduction. Some shifts
    #    are omitted if they are irrelevant to the semantic analysis

    @_initial.on('semicolon')
    def _initial_semi(self, tok: Lexeme) -> Optional[State[Parser]]:
        # reduce
        return self._initial

    @_initial.on('eof')
    def _initial_eof(self, tok: Lexeme) -> Optional[State[Parser]]:
        # accept
        return None

    @_initial.on('kw_struct')
    def _initial_struct_keyword(self, tok: Lexeme) -> Optional[State[Parser]]:
        # shift
        return self._struct_name

    @_type_start.on('lbrace')
    def _type_start_lbrace(self, tok: Lexeme) -> Optional[State[Parser]]:
        # shift
        return self._member_type

    @_struct_name.on('identifier')
    def _struct_name_identifier(self, tok: Lexeme) -> Optional[State[Parser]]:
        # shift
        self.push(StructDecl(tok.val, list()))
        return self._type_start

    @_member_type.on('identifier')
    def _member_type_identifier(self, tok: Lexeme) -> Optional[State[Parser]]:
        # shift
        self.push(MemberTypeItem(tok.val))
        return self._member_name

    @_member_name.on('identifier')
    def _member_name_identifier(self, tok: Lexeme) -> Optional[State[Parser]]:
        # shift
        self.push(MemberNameItem(tok.val))
        return self._member_end

    @_member_end.on('semicolon')
    def _member_end_semicolon(self, tok: Lexeme) -> Optional[State[Parser]]:
        # reduce MemberDecl
        name_item = self.pop()
        type_item = self.pop()

        assert isinstance(name_item, MemberNameItem)
        assert isinstance(type_item, MemberTypeItem)

        member_name = name_item.member_name
        member_type = type_item.member_type

        t = self.stacktop()
        assert isinstance(t, StructDecl)

        t.members.append(MemberDecl(member_name, member_type))
        return self._member_type

    @_member_type.on('rbrace')
    def _member_type_rbrace(self, tok: Lexeme) -> Optional[State[Parser]]:
        # reduce StructDef
        t = self.pop()
        ns = self.stacktop()

        assert isinstance(t, StructDecl)
        assert isinstance(ns, NamespaceItem)

        ns.ns[t.struct_name] = t
        return self._initial


def parse(s: str, file: str = '<string>') -> Generator[StructDecl, None, None]:
    yield from Parser.fromstring(s, file)


def parse_file(p: Path) -> Generator[StructDecl, None, None]:
    yield from Parser.fromfile(p)
