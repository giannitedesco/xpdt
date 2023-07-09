from typing import Iterable, Optional, Generator
from itertools import chain
from pathlib import Path

import logging

from .namespace import NameSpace
from .decl import StructDecl
from .parse import parse_file
from .registry import Registry
from .shiftreduce import ParseError

_log = logging.getLogger(__package__)


__all__ = (
    'load',
)


def load(files: Iterable[Path],
         registry: Optional[Path] = None,
         module_name: Optional[str] = None,
         ) -> NameSpace:
    file_set = list(files)
    single = len(file_set) == 1

    if registry is not None:
        reg = Registry.from_file(registry)
    else:
        reg = Registry.empty()

    if module_name:
        module_name = module_name
    elif meta_name := reg.name:
        module_name = meta_name
    elif single:
        in_path, = file_set
        module_name = in_path.stem

    def parse(p: Path) -> Generator[StructDecl, None, None]:
        try:
            yield from parse_file(p)
        except ParseError as e:
            _log.exception(e)
            raise SystemExit(1)

    def parse_with_prefix(p: Path) -> Generator[StructDecl, None, None]:
        name = p.stem

        if registry:
            module_id = reg.module_id(name)
        else:
            module_id = 0

        assert 0 <= module_id <= 0xffff

        for s in parse(p):
            decl = s.with_prefix(name)

            if registry:
                struct_name = s.struct_name
                struct_id = reg.struct_id(name, struct_name)

                assert 0 <= struct_id <= 0xffff

                discriminant = (module_id << 16) | struct_id
                decl = decl.with_discriminant(discriminant)

            yield decl

    if single:
        in_file, = file_set
        decls = tuple(parse(in_file))
    else:
        decls = tuple(chain(*map(parse_with_prefix, file_set)))

    if registry:
        if reg.corrupt:
            _log.error('Registry file is corrupted, refusing to write')
            raise SystemExit(1)
        reg.save(registry)

    return NameSpace.from_decls(decls, name=module_name)
