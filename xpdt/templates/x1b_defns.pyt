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
    def _frombuf(cls,
                 buf: bytes,
                 off: int = 0,
                 ) -> _Tuple[int, '$$ struct.name $$']:
        (
## for var in struct.python_var_names
            $$var$$,
## endfor
        ) = cls._unpack_from(buf, off)
        ret = cls(
## for e in struct.construct_recursive()
$$e.indent('    ', 3)$$$$construct_object(e)$$
## endfor
        )
        return cls._bin_size, ret
#%- endmacro -%#
