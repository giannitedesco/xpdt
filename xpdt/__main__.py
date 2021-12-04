from typing import ClassVar, TextIO, Optional
from argparse import ArgumentParser
from pathlib import Path
from sys import stdout
import logging

from xpdt import NameSpace, load

_fmt = logging.Formatter('%(message)s')
_stdio_handler = logging.StreamHandler(stream=stdout)
_stdio_handler.setFormatter(_fmt)
_log = logging.getLogger('xpdt')
_log.addHandler(_stdio_handler)


class BackendDef:
    suffix: ClassVar[str]

    __slots__ = (
        '_p',
        '_ns',
        '_inc_prefix',
    )

    _p: Path
    _ns: NameSpace
    _inc_prefix: Optional[str]

    def _name(self, base: Path, name: str) -> Path:
        return base / (name + self.suffix)

    def __init__(self, ns: NameSpace, base: Path,
                 inc_prefix: Optional[str] = None) -> None:
        self._ns = ns
        name = ns.name
        assert name is not None
        self._p = self._name(base, name)
        self._inc_prefix = inc_prefix

    def _gen(self, f: TextIO) -> None:
        raise NotImplementedError

    def gen(self) -> None:
        _log.info('Writing code: %s', self._p)
        with self._p.open('w') as f:
            return self._gen(f)


class OutputC(BackendDef):
    suffix = '_impl.h'
    __slots__ = ()

    def _gen(self, f: TextIO) -> None:
        self._ns.gen_c(f)


class OutputCAPI(BackendDef):
    suffix = '.c'
    __slots__ = ()

    def _gen(self, f: TextIO) -> None:
        self._ns.gen_c_api_entries(f, self._inc_prefix)


class OutputCHdr(BackendDef):
    suffix = '_api.h'
    __slots__ = ()

    def _gen(self, f: TextIO) -> None:
        self._ns.gen_c_api_hdr(f)


class OutputPy(BackendDef):
    suffix = '.py'
    __slots__ = ()

    def _gen(self, f: TextIO) -> None:
        self._ns.gen_python(f)


def main() -> None:
    opts = ArgumentParser(description='xpdt: eXPeditious Data Transfer')
    opts.add_argument('--verbose', '-v',
                      action='count',
                      default=0,
                      help='Be more talkative')
    opts.add_argument('--registry', '-r',
                      default=None,
                      type=Path,
                      help='Path to registry.toml')
    opts.add_argument('--module-name', '-n',
                      default=None,
                      type=str,
                      help='Name of module (output file)')
    opts.add_argument('--language', '-l',
                      default='c',
                      type=str,
                      help='Output language')
    opts.add_argument('--out', '-o',
                      default=Path(),
                      type=Path,
                      help='Output dir')
    opts.add_argument('-I',
                      dest='inc_prefix',
                      help='Include path (for C headers)')
    opts.add_argument('file',
                      type=Path,
                      nargs='+',
                      help='xpdt schema files')

    args = opts.parse_args()
    if args.verbose:
        _log.setLevel(logging.DEBUG)
    else:
        _log.setLevel(logging.INFO)

    ns = load(
        args.file,
        registry=args.registry,
        module_name=args.module_name,
    )

    if ns.name is None:
        ns.name = 'xpdt'

    backends = {
        'c': OutputC,
        'capi': OutputCAPI,
        'chdr': OutputCHdr,
        'py': OutputPy,
        'python': OutputPy,
    }

    try:
        cls = backends[args.language]
    except KeyError:
        print(f'Unknown language: "{args.language}"')
        raise SystemExit(1)

    args.out.mkdir(exist_ok=True)
    backend = cls(ns, args.out, args.inc_prefix)
    backend.gen()


if __name__ == '__main__':
    main()
