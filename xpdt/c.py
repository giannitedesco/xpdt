from pathlib import PurePosixPath

__all__ = (
    'Include',
    'SysInclude',
    'RelInclude',
)


class Include(PurePosixPath):
    @property
    def path_spec(self) -> str:
        raise NotImplementedError

    @property
    def include(self) -> str:
        return f'#include {self.path_spec}'


class SysInclude(Include):
    @property
    def path_spec(self) -> str:
        return f'<{self}>'


class RelInclude(Include):
    @property
    def path_spec(self) -> str:
        return f'"{self}"'
