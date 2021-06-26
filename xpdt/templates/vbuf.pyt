#%- macro construct_object(elem, vbuf_var) -%#
##- if elem.action.value == 'agg_push'
$$elem.member.type.struct_name$$(
##- elif elem.action.value == 'agg_pop'
),
##- else:
##-   if elem.member.type.needs_vbuf
buf[off_$$vbuf_var.value$$:off_$$vbuf_var.value + 1$$],
##-     set vbuf_var.value = vbuf_var.value + 1
##-   else
$$elem.python_var_name$$,
##-   endif
##- endif
#%- endmacro -%#

#% macro write_methods(struct) %#

    def __bytes__(self) -> bytes:
## for e in struct.all_vbuf_members
        $$e.python_var_name$$_buf = self.$$ ".".join(e.full_path_names) $$
        $$e.python_var_name$$_len = len($$e.python_var_name$$_buf)
## endfor
        tot_len = sum((
            self._fmt_size,
## for var in struct.python_vbuf_names
            $$var$$_len,
## endfor
        ))

        return b''.join((
            self._pack(
                tot_len,
## for e in struct.all_members
##   if e.member.type.needs_vbuf
                $$e.python_var_name$$_len,
##   else
                self.$$ ".".join(e.full_path_names) $$,
##   endif
## endfor
            ),
## for e in struct.all_vbuf_members
            $$e.python_var_name$$_buf,
## endfor
        ))

    @classmethod
    def _frombuf(cls,
                 buf: bytes,
                 off: int = 0,
                 ) -> _Tuple[int, '$$struct.name$$']:
        (
            tot_len,
## for var in struct.python_var_names
            $$var$$,
## endfor
        ) = cls._unpack_from(buf, off)

        off_0 = off + cls._fmt_size
## for var in struct.python_vbuf_names
        off_$$loop.index0 + 1$$ = off_$$loop.index0$$ + $$var$$
## endfor
        ret = cls(
## set vbuf_var = namespace(value=0)
## for e in struct.construct_recursive()
$$e.indent('    ', 3)$$$$construct_object(e, vbuf_var)$$
## endfor
        )
        return tot_len, ret
#%- endmacro -%#
