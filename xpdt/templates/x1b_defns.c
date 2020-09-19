/*#- macro init_macro_name(struct) -#*/
/*{struct.name.upper()}*/_INIT
/*#- endmacro #*/


/*#- macro ctor(struct) -#*/
/*{struct.name}*/_new
/*#- endmacro -#*/


/*#- macro xrec_ctor(struct) -#*/
/*{struct.name}*/_xrec
/*#- endmacro -#*/


/*#- macro xptrs_ctor(struct) -#*/
/*{struct.name}*/_xptrs
/*#- endmacro -#*/


/*#- macro raw_write(struct) -#*/
/*{struct.name}*/_raw_write
/*#- endmacro -#*/


/*#- macro bufreq(struct) -#*/
/*{struct.name}*/_bufreq
/*#- endmacro -#*/


/*#- macro construct(struct) -#*/
/*{struct.name}*/_construct
/*#- endmacro -#*/


/*#- macro cdecls(struct) -#*/
/*{struct
	| map(attribute="const_cdecl")
	| join(",\n\t\t")}*/
/*#- endmacro -#*/


/*#- macro vbuf_cdecls(struct) -#*/
/*{struct.vbuf_members
	| map(attribute="const_cdecl")
	| join(",\n\t\t")}*/
/*#- endmacro -#*/


/*#- macro memb_names(struct) -#*/
/*{struct
	| map(attribute="name")
	| join(",\n\t\t")}*/
/*#- endmacro -#*/


/*#- macro _memb_names(struct) -#*/
/*{struct
	| map(attribute="name")
	| map("prefix", "_")
	| join(",\n\t\t") }*/
/*#- endmacro -#*/


/*#- macro buf_lens(struct) -#*/
/*{struct.c_named_initializers_x1v
	| map("wrap", "obj.", ".len")
	| join("\n\t\t+ ")}*/
/*#- endmacro -#*/


/*#- macro naturally_packed(struct) -#*/
/*#- if struct.needs_vbuf -#*/
__attribute__((packed))
/*#- endif -#*/
/*#- endmacro -#*/


/*#- macro struct_xrec(struct) -#*/
struct /*{struct.name}*/_xrec
/*#- endmacro -#*/


/*#- macro struct_envelope(struct) -#*/
struct /*{struct.name}*/_xrec_envelope
/*#- endmacro -#*/


/*#- macro struct_xptrs(struct) -#*/
struct /*{struct.name}*/_xptrs
/*#- endmacro -#*/


/*#- macro struct_decl(struct) -#*/

struct /*{struct.tag}*/ {
// for member in struct
	/*{member.cdecl}*/;
// endfor
} /*{naturally_packed(struct)}*/;
/*#- endmacro -#*/


/*#- macro serialized_struct_decl(struct) -#*/

/*{struct_xrec(struct)}*/ {
// for member in struct
// if member.needs_vbuf
// if member.is_scalar
	x1b_strlen_t /*{member.name}*/;
// else
	/*{struct_xrec(member.type.struct)}*/ /*{member.name}*/;
// endif
// else
	/*{member.cdecl}*/;
// endif
// endfor
} __attribute__((packed));

/*{struct_envelope(struct)}*/ {
	x1b_strlen_t tot_len;
	/*{struct_xrec(struct)}*/ fixed;
	uint8_t buffer[0];
} __attribute__((packed));
/*#- endmacro -#*/



/*#- macro blob_struct_decl(struct) -#*/

/*{struct_xptrs(struct)}*/ {
// for member in struct.vbuf_members
// if member.type.is_scalar
	const uint8_t * /*{-member.name}*/;
// else
	/*{struct_xptrs(member.type.struct)}*/ /*{member.name}*/;
// endif
// endfor
};
/*#- endmacro -#*/


/*#- macro fixed_ctor_defn(struct) #*/
#define /*{init_macro_name(struct)}*/( \
		/*{_memb_names(struct)|macro}*/) \
	(/*{struct.ctype}*/){ \
// for member in struct
		./*{member.name}*/ = _/*{member.name}*/, \
// endfor
	}

static inline
/*{struct.ctype}*/
/*{ctor(struct)}*/(/*{cdecls(struct)}*/)
{
	return /*{init_macro_name(struct)}*/(
		/*{memb_names(struct)}*/);
}
/*#- endmacro -#*/


/*#- macro vbuf_ctor_defn(struct) #*/

static inline
/*{struct_xrec(struct)}*/
/*{xrec_ctor(struct)}*/(struct /*{struct.tag}*/ obj)
{
	return (/*{struct_xrec(struct)}*/){
// for member in struct
// if member.needs_vbuf
// if member.is_scalar
		./*{member.name}*/ = obj./*{member.name}*/.len,
// else
		./*{member.name}*/ = /*{xrec_ctor(member.type.struct)}*/(obj./*{member.name}*/),
// endif
// else
		./*{member.name}*/ = obj./*{member.name}*/,
// endif
// endfor
	};
}

static inline
/*{struct_xptrs(struct)}*/
/*{xptrs_ctor(struct)}*/(struct /*{struct.tag}*/ obj)
{
	return (/*{struct_xptrs(struct)}*/){
// for path in struct.c_named_initializers_x1v
		./*{path}*/ = obj./*{path}*/.ptr,
// endfor
	};
}
/*#- endmacro -#*/


// macro ctors(struct)
/*{fixed_ctor_defn(struct)}*/
// if struct.needs_vbuf
/*{vbuf_ctor_defn(struct)}*/
// endif
// endmacro


/*# macro raw_write_fixed_func(struct) #*/
static inline
bool /*{raw_write(struct)}*/(xostream_t out, const /*{struct.ctype}*/ obj)
{
	/*{struct.ctype}*/ *ptr;

	ptr = (/*{struct.ctype}*/ *)xostream_prepare(out, sizeof(obj));
	if (x1b_unlikely(ptr == NULL)) {
		return false;
	}

	*ptr = obj;

	return xostream_commit(out, sizeof(obj));
}
/*# endmacro #*/


/*# macro raw_write_variable_func(struct) #*/
static inline
size_t /*{bufreq(struct)}*/(const /*{struct.ctype}*/ obj)
{
	return /*{buf_lens(struct)}*/;
}

static inline
bool /*{raw_write(struct)}*/(xostream_t out, const /*{struct.ctype}*/ obj)
{
	/*{struct_envelope(struct)}*/ *ptr;
	const size_t tot_len = sizeof(*ptr) + /*{bufreq(struct)}*/(obj);
	x1b_strlen_t str_len;
	uint8_t *buf;

	ptr = (/*{struct_envelope(struct)}*/ *)xostream_prepare(out, tot_len);
	if (x1b_unlikely(ptr == NULL)) {
		return false;
	}

	ptr->tot_len = tot_len;
	ptr->fixed = /*{xrec_ctor(struct)}*/(obj);

	buf = ptr->buffer;
/*# for path in struct.c_named_initializers_x1v #*/

	str_len = obj./*{path}*/.len;
	memcpy(buf, obj./*{path}*/.ptr, str_len);
	buf += str_len;
/*# endfor #*/

	return xostream_commit(out, tot_len);
}
/*# endmacro #*/

/*#- macro writers(struct) -#*/
// if struct.needs_vbuf
/*{raw_write_variable_func(struct)}*/
// else
/*{raw_write_fixed_func(struct)}*/
// endif

static inline
bool /*{struct.name}*/_write(xostream_t out,
		/*{cdecls(struct)}*/)
{
	return /*{raw_write(struct)}*/(out, /*{ctor(struct)}*/(
		/*{memb_names(struct)}*/));
}
/*#- endmacro -#*/


/*#- macro readers(struct) #*/

static inline
const /*{struct_xrec(struct)}*/ * /*{-struct.name}*/_read_fixed(struct xbuf_iter *it)
{
	const /*{struct_envelope(struct)}*/ *e;
	const uint8_t *ptr, *end;

	ptr = it->it_ptr;
	end = it->it_end;

	e = (/*{struct_envelope(struct)}*/ *)ptr;
	if (x1b_unlikely((uint8_t *)&e->fixed > end))
		return NULL;

	ptr += e->tot_len;
	if (x1b_unlikely(ptr > end))
		return NULL;

	it->it_ptr = ptr;
	return &e->fixed;
}

static inline
const /*{struct_xrec(struct)}*/ * /*{-struct.name}*/_read(struct xbuf_iter *it, /*{struct_xptrs(struct)}*/ *ptrs)
{
	const /*{struct_envelope(struct)}*/ *e;
	const uint8_t *buf, *ptr, *end;

	ptr = it->it_ptr;
	end = it->it_end;

	e = (/*{struct_envelope(struct)}*/ *)ptr;
	buf = e->buffer;
	if (x1b_unlikely((uint8_t *)&e->fixed > end))
		return NULL;

	ptr += e->tot_len;
	if (x1b_unlikely(ptr > end))
		return NULL;
/*# for path in struct.c_named_initializers_x1v #*/

	ptrs->/*{path}*/ = buf;
	buf += e->fixed./*{path}*/;
/*# endfor #*/

	it->it_ptr = ptr;
	return &e->fixed;
}

static inline
/*{struct.ctype}*/ /*{construct(struct)}*/(const /*{struct_xrec(struct)}*/ *rec, const /*{struct_xptrs(struct)}*/ *ptrs)
{
	return (/*{struct.ctype}*/){
// for member in struct
// if member.needs_vbuf
// if member.is_scalar
		./*{member.name}*/ = xbuf(rec->/*{member.name}*/, ptrs->/*{member.name}*/),
// else
		./*{member.name}*/ = /*{member.type.struct.name}*/_construct(&rec->/*{member.name}*/, &ptrs->/*{member.name}*/),
// endif
// else
		./*{member.name}*/ = rec->/*{member.name}*/,
// endif
// endfor
	};
}
/*#- endmacro -#*/
