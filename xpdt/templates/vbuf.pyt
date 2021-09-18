#%- macro buf_slice(vbuf_var) -%#
buf[off_$$vbuf_var.value$$:off_$$vbuf_var.value + 1$$]
#%- endmacro -%#

#%- macro decoded_buf(elem, vbuf_var) -%#
$$elem.member.type.read_func(buf_slice(vbuf_var))$$
#%- endmacro -%#

#%- macro decoded_scalar(elem) -%#
$$elem.member.type.read_func(elem.python_var_name)$$
#%- endmacro -%#

#%- macro construct_object(elem, vbuf_var) -%#
##- if elem.action.value == 'agg_push'
$$elem.member.type.struct_name$$(
##- elif elem.action.value == 'agg_pop'
),
##- else:
##-   if elem.member.type.needs_vbuf
$$decoded_buf(elem, vbuf_var)$$,
##-     set vbuf_var.value = vbuf_var.value + 1
##-   elif elem.member.type.needs_decode
$$decoded_scalar(elem)$$,
##-   else
$$elem.python_var_name$$,
##-   endif
##- endif
#%- endmacro -%#

#%- macro get_member(full_path_names) -%#
self.$$ ".".join(full_path_names) $$
#%- endmacro -%#

#%- macro encoded_var(elem) -%#
$$elem.member.type.write_func(get_member(elem.full_path_names))$$
#%- endmacro -%#

#% macro write_methods(struct) %#

    def __bytes__(self) -> bytes:
## for e in struct.all_vbuf_members
        $$e.python_var_name$$_buf = $$encoded_var(e)$$
        $$e.python_var_name$$_len = len($$e.python_var_name$$_buf)
## endfor

        return b''.join((
            self._pack(
## for e in struct.all_members
##   if e.member.type.needs_vbuf
                $$e.python_var_name$$_len,
##   elif e.member.type.needs_decode
                $$encoded_var(e)$$,
##   else
                self.$$ ".".join(e.full_path_names) $$,
##   endif
## endfor
            ),
## for e in struct.all_vbuf_members | rejectattr("member.is_reserved")
            $$e.python_var_name$$_buf,
## endfor
        ))

    @classmethod
    def _frombuf(cls: _Typ[_T],
                 buf: memoryview,
                 off: int = 0,
                 unp: _F[[memoryview, int], _Tup[int, ...]] = _unpack_from,
                 fmt_size: int = _fmt_size,
                 tobytes: _F[[memoryview], bytes] = memoryview.tobytes,
                 tostr: _F[[bytes], str] = bytes.decode,
                 ) -> _T:
        (
## for var in struct.python_var_names
            $$var$$,
## endfor
        ) = unp(buf, off)

        off_0 = off + fmt_size
## for var in struct.python_vbuf_names
        off_$$loop.index0 + 1$$ = off_$$loop.index0$$ + $$var$$
## endfor
        ret = cls(
## set vbuf_var = namespace(value=0)
## for e in struct.construct_recursive(include_reserved=False)
$$e.indent('    ', 3)$$$$construct_object(e, vbuf_var)$$
## endfor
        )
        return ret

    def _write(self,
               _p: _F[[int], bytes] = _vlen_pack,
               ) -> bytes:
        buf = bytes(self)
        tot_len = _p(len(buf))
        return tot_len + buf

    @classmethod
    def _read(cls: _Typ[_T],
              buf: memoryview,
              off: int = 0,
              _unp: _F[[bytes, int], _Tup[int, ...]] = _vlen_unpack_from,
              _hdr_len: int = _vlen_size,
              _frombuf: _F[[_Typ[_T], memoryview], _T] = (
                  getattr(_frombuf, '__func__')
              )) -> _T:
        tot_len, = _unp(buf, off)
        off += _hdr_len
        payload = buf[off:off + tot_len]
        return _frombuf(cls, payload)

    @classmethod
    def _read_many(cls: _Typ[_T],
                   buf: memoryview,
                   _unp: _F[[bytes, int], _Tup[int, ...]] = _vlen_unpack_from,
                   _hdr_len: int = _vlen_size,
                   _frombuf: _F[[_Typ[_T], memoryview, int], _T] = (
                       getattr(_frombuf, '__func__')
                   )) -> _G[_T, None, None]:
        tot_len = len(buf)

        off = 0
        while off < tot_len:
            rec_len, = _unp(buf, off)
            off += _hdr_len
            yield _frombuf(cls, buf, off)
            off += rec_len

    @classmethod
    def _from_file(cls: _Typ[_T],
                   p: _Path,
                   ) -> _G[_T, None, None]:
        with p.open('rb') as f:
            content = _mmap(f.fileno(), 0, access=_PROT_READ)
            yield from cls._read_many(memoryview(content))
#%- endmacro -%#
