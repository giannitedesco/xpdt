from pathlib import Path
from xpdt.registry import Registry


def test_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "registry.toml"

    r = Registry.empty()
    assert r.module_id("foo") == 0
    assert r.struct_id("foo", "Bar") == 0
    assert r.struct_id("foo", "Baz") == 1
    assert r.module_id("quux") == 1
    assert r.dirty
    r.save(p)

    r2 = Registry.from_file(p)
    assert not r2.corrupt
    assert not r2.dirty                       # nothing was (re)allocated on load

    # Looking up known names must NOT mark dirty -> they came from disk.
    assert r2.module_id("foo") == 0
    assert r2.struct_id("foo", "Bar") == 0
    assert r2.struct_id("foo", "Baz") == 1
    assert r2.module_id("quux") == 1
    assert not r2.dirty                       # still clean -> no allocation happened

    # A brand-new name must allocate the *next* id, proving the loaded
    # state included the previous ones.
    assert r2.module_id("new_mod") == 2       # 0 and 1 already taken
    assert r2.struct_id("foo", "Qux") == 2    # Bar=0, Baz=1 already taken
    assert r2.dirty
    