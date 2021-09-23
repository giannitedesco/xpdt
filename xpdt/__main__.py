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


def gen_c(ns: NameSpace, base: Path, module_name: str) -> None:
    p = base / f'{module_name}.h'
    _log.info('Writing code: %s', p)
    with p.open('w') as f:
        ns.gen_c(f)


def gen_py(ns: NameSpace, base: Path, module_name: str) -> None:
    p = base / f'{module_name}.py'
    _log.info('Writing code: %s', p)
    with p.open('w') as f:
        ns.gen_python(f)


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

    name = ns.name
    assert name is not None

    backends = {
        'c': gen_c,
        'py': gen_py,
        'python': gen_py,
    }

    try:
        fn = backends[args.language]
    except KeyError:
        print(f'Unknown language: "{args.language}"')
        raise SystemExit(1)

    args.out.mkdir(exist_ok=True)

    fn(ns, args.out, name)


if __name__ == '__main__':
    main()
