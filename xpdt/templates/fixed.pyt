#%- macro construct_object(elem) -%#
##- if elem.action.value == 'agg_push'
$$elem.member.type.struct_name$$(
##- elif elem.action.value == 'agg_pop'
),
##- else:
$$elem.python_var_name$$,
##- endif
#%- endmacro -%#

#% macro write_methods(struct) %#

    def __bytes__(self) -> bytes:
        # FIXME: This can be more efficient
        return self._pack(
## for member in struct.scalar_members
            self.$$ ".".join(member) $$,
## endfor
        )

    @classmethod
    def _frombuf(cls: _Typ[_T],
                 buf: memoryview,
                 off: int = 0,
                 unp: _F[[memoryview, int], _Tup[int, ...]] = _unpack_from,
                 ) -> _T:
        (
## for var in struct.python_var_names
            $$var$$,
## endfor
        ) = unp(buf, off)
        ret = cls(
## for e in struct.construct_recursive(include_reserved=False)
$$e.indent('    ', 3)$$$$construct_object(e)$$
## endfor
        )
        return ret

    _write = __bytes__
    _read = _frombuf

    @classmethod
    def _read_many(cls: _Typ[_T],
                   buf: memoryview,
                   rec_len: int = _fmt_size,
                   frombuf: _F[[_Typ[_T], memoryview, int], _T] = (
                       getattr(_frombuf, '__func__')
                   )) -> _G[_T, None, None]:
        off = 0
        tot_len = len(buf)
        while off < tot_len:
            yield frombuf(cls, buf, off)
            off += rec_len

    @classmethod
    def _from_file(cls: _Typ[_T],
                   p: _Path,
                   ) -> _G[_T, None, None]:
        with p.open('rb') as f:
            content = _mmap(f.fileno(), 0, access=_PROT_READ)
            yield from cls._read_many(memoryview(content))
#%- endmacro -%#
