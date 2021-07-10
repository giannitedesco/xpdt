from typing import Tuple, Type, TypeVar, NamedTuple, Generator
from enum import Enum

import re


class Case(Enum):
    DASHY = 'dashy'
    SNAKE = 'snake'
    SCREAMING_SNAKE = 'screaming-snake'
    PASCAL = 'pascal'
    CAMEL = 'camel'


T = TypeVar('T', bound='Symbol')


_camel_re = re.compile('(?<=[a-z])(?=[A-Z])')


class Symbol(NamedTuple):
    components: Tuple[str, ...]

    @property
    def dashy(self) -> str:
        return '-'.join(self.components)

    @property
    def snake(self) -> str:
        return '_'.join(self.components)

    @property
    def screaming_snake(self) -> str:
        return '_'.join((c.upper() for c in self.components))

    @property
    def pascal(self) -> str:
        return ''.join((c.title() for c in self.components))

    @property
    def camel(self) -> str:
        p = self.components

        def gen() -> Generator[str, None, None]:
            yield p[0]
            yield from (c.title() for c in p[1:])

        return ''.join(gen())

    @classmethod
    def from_dashy(cls: Type[T], s: str) -> T:
        # TODO: Validate
        return cls(tuple((c.lower() for c in s.split('-'))))

    @classmethod
    def from_snake(cls: Type[T], s: str) -> T:
        # TODO: Validate
        return cls(tuple((c.lower() for c in s.split('_'))))

    @classmethod
    def from_screaming_snake(cls: Type[T], s: str) -> T:
        # TODO: Validate
        return cls(tuple((c.lower() for c in s.split('_'))))

    @classmethod
    def from_pascal(cls: Type[T], s: str) -> T:
        # TODO: Validate
        return cls(tuple((c.lower() for c in _camel_re.split(s))))

    @classmethod
    def from_camel(cls: Type[T], s: str) -> T:
        # TODO: Validate
        return cls(tuple((c.lower() for c in _camel_re.split(s))))

    @classmethod
    def detect(cls: Type[T], s: str) -> T:
        if not s:
            raise ValueError('Cannot have an empty symbol')

        used = frozenset(s)

        begins_lower = s[0].islower()
        has_upper = any(x.isupper() for x in used)
        has_lower = any(x.islower() for x in used)
        has_unders = '_' in used
        has_dashes = '-' in used

        if has_dashes:
            return cls.from_dashy(s)
        elif has_unders:
            if has_upper:
                return cls.from_screaming_snake(s)
            else:
                return cls.from_snake(s)
        elif has_upper and has_lower:
            if begins_lower:
                return cls.from_camel(s)
            else:
                return cls.from_pascal(s)
        elif has_lower:
            return cls.from_snake(s)
        elif has_upper:
            return cls.from_screaming_snake(s)
        else:
            raise ValueError('cannot recognize')


def main() -> None:
    examples = (
        'foo-bar',
        'foo_bar',
        'FOO_BAR',
        'FooBar',
        'fooBar',
        'foo',
        'FOO',
        'Foo',
    )

    for x in examples:
        s = Symbol.detect(x)
        print(s.dashy, s.snake, s.screaming_snake, s.pascal, s.camel)


if __name__ == '__main__':
    main()
