from typing import Any, ClassVar, Optional, TypeVar
from pathlib import Path

import logging
import toml

_log = logging.getLogger(__package__)


__all__ = (
    'Registry',
)


_R = TypeVar('_R', bound='Registry')


class Registry:
    MAX_MOD_ID: ClassVar[int] = 0xffff
    MAX_STRUCT_ID: ClassVar[int] = 0xffff

    __slots__ = (
        '_reg',
        '_dirty',
        '_corrupt',
        '_meta',
        '_modules',
        '_module',
    )

    _reg: dict[str, Any]
    _corrupt: bool
    _dirty: bool

    def __init__(self, reg: dict[str, Any]) -> None:
        self._reg = reg
        self._corrupt = False
        self._dirty = False

        self._meta = self._top_level_table('meta')
        self._modules = self._top_level_table('modules')
        self._module = self._top_level_table('module')

    @property
    def corrupt(self) -> bool:
        return self._corrupt

    @property
    def dirty(self) -> bool:
        return self._dirty

    def _create_toplevel(self, table: str) -> dict[str, Any]:
        ret: dict[str, Any] = dict()
        self._reg[table] = ret
        return ret

    def _top_level_table(self, table: str) -> dict[str, Any]:
        """
        Fetch a top-level table from the registry. If it doesn't exist or is
        not a table, then return an empty dict.
        """
        tab = self._reg.get(table)

        if tab is None:
            return self._create_toplevel(table)

        if not isinstance(tab, dict):
            _log.warn('registry.toml: "%s" is not a table', table)
            self._corrupt = True
            return self._create_toplevel(table)

        return tab

    @property
    def name(self) -> Optional[str]:
        meta = self._meta
        name = meta.get('name')
        if not isinstance(name, str):
            return None
        return name

    def _alloc_module_id(self) -> int:
        all_ids = [x for x in self._modules.values()
                   if isinstance(x, int)]
        if not all_ids:
            return 0

        ret = max(all_ids) + 1

        if ret > self.MAX_MOD_ID:
            _log.warn('registry.toml: module ID "%d" is beyond max allowable',
                      ret)
            self._corrupt = True

        return ret

    def _new_module_id(self, module_name: str) -> int:
        mod_id = self._alloc_module_id()
        self._modules[module_name] = mod_id
        self._dirty = True
        return mod_id

    def module_id(self, module_name: str) -> int:
        modules = self._modules
        mod_id = modules.get(module_name)

        if mod_id is None:
            return self._new_module_id(module_name)

        if not isinstance(mod_id, int):
            _log.warn('registry.toml: "modules.%s" is not an int', module_name)
            self._corrupt = True
            return self._new_module_id(module_name)

        return mod_id

    def _new_module_tab(self, module_name: str) -> dict[str, Any]:
        ret: dict[str, Any] = dict()
        self._module[module_name] = ret
        self._dirty = True
        return ret

    def _get_module_tab(self, module_name: str) -> dict[str, Any]:
        module = self._module
        mod_tab = module.get(module_name)
        if mod_tab is None:
            return self._new_module_tab(module_name)

        if not isinstance(mod_tab, dict):
            _log.warn('registry.toml: "module.%s" is not a table', module_name)
            self._corrupt = True
            return self._new_module_tab(module_name)

        return mod_tab

    def _alloc_struct_id(self, mod_tab: dict[str, Any]) -> int:
        all_ids = [x for x in mod_tab.values()
                   if isinstance(x, int)]
        if not all_ids:
            return 0
        ret = max(all_ids) + 1

        if ret > self.MAX_STRUCT_ID:
            _log.warn('registry.toml: struct ID "%d" is beyond max allowable',
                      ret)
            self._corrupt = True
        return ret

    def _new_struct_id(self, mod_tab: dict[str, Any], struct_name: str) -> int:
        struct_id = self._alloc_struct_id(mod_tab)
        mod_tab[struct_name] = struct_id
        self._dirty = True
        return struct_id

    def struct_id(self, module_name: str, struct_name: str) -> int:
        mod_tab = self._get_module_tab(module_name)
        ret = mod_tab.get(struct_name)

        if ret is None:
            return self._new_struct_id(mod_tab, struct_name)

        if not isinstance(ret, int):
            _log.warn('registry.toml: "module.%s.%s" is not an int',
                      module_name, struct_name)
            self._corrupt = True
            return self._new_struct_id(mod_tab, struct_name)

        return ret

    @classmethod
    def empty(cls: type[_R]) -> _R:
        return cls({})

    @classmethod
    def from_file(cls: type[_R], p: Path) -> _R:
        return cls(toml.load(p))

    def save(self, p: Path) -> None:
        if self._dirty:
            with p.open('w') as f:
                toml.dump(self._reg, f)
            self._dirty = False
