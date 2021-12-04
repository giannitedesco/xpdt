/*#- macro init_macro_name(struct) -#*/
/*{struct.name.upper()}*/_INIT
/*#- endmacro #*/


/*#- macro ctor(struct) -#*/
/*{struct.name}*/__new
/*#- endmacro -#*/


/*#- macro fixed_ctor(struct) -#*/
/*{struct.name}*/__fixed
/*#- endmacro -#*/


/*#- macro ptrs_ctor(struct) -#*/
/*{struct.name}*/__ptrs
/*#- endmacro -#*/


/*#- macro rd(struct) -#*/
/*{struct.name}*/__read
/*#- endmacro -#*/


/*#- macro rd_fixed(struct) -#*/
/*{struct.name}*/__read_fixed
/*#- endmacro -#*/


/*#- macro rd_sized(struct) -#*/
/*{struct.name}*/__read_sized
/*#- endmacro -#*/


/*#- macro wr_fixed(struct) -#*/
/*{struct.name}*/__wr_fixed
/*#- endmacro -#*/


/*#- macro wr_sized(struct) -#*/
/*{struct.name}*/__wr_sized
/*#- endmacro -#*/


/*#- macro wr_wrapped(struct) -#*/
/*{struct.name}*/__wr_wrapped
/*#- endmacro -#*/


/*#- macro wr(struct) -#*/
/*{struct.name}*/__wr
/*#- endmacro -#*/


/*#- macro write_fixed(struct) -#*/
/*{struct.name}*/__write_fixed
/*#- endmacro -#*/


/*#- macro write_sized(struct) -#*/
/*{struct.name}*/__write_sized
/*#- endmacro -#*/


/*#- macro write_wrapped(struct) -#*/
/*{struct.name}*/__write_wrapped
/*#- endmacro -#*/


/*#- macro bufreq(struct) -#*/
/*{struct.name}*/__vbuf_size
/*#- endmacro -#*/


/*#- macro construct(struct) -#*/
/*{struct.name}*/__construct
/*#- endmacro -#*/


/*#- macro write(struct) -#*/
/*{struct.name}*/__write
/*#- endmacro -#*/


/*#- macro cdecls(struct) -#*/
/*{struct.non_reserved_members
	| map(attribute="const_cdecl")
	| join(",\n\t\t")}*/
/*#- endmacro -#*/


/*#- macro vbuf_cdecls(struct) -#*/
/*{struct.non_reserved_vbuf_members
	| map(attribute="const_cdecl")
	| join(",\n\t\t")}*/
/*#- endmacro -#*/


/*#- macro memb_names(struct) -#*/
/*{struct.non_reserved_members
	| map(attribute="name")
	| join(",\n\t\t")}*/
/*#- endmacro -#*/


/*#- macro _memb_names(struct) -#*/
/*{struct.non_reserved_members
	| map(attribute="name")
	| map("prefix", "_")
	| join(",\n\t\t") }*/
/*#- endmacro -#*/


/*#- macro buf_lens(struct) -#*/
/*{struct.c_named_initializers_x1v
	| map("wrap", "obj.", ".len")
	| join("\n\t\t+ ")}*/
/*#- endmacro -#*/


/*#- macro naturally_packed(struct) #*/
 __attribute__((packed))
/*#- endmacro -#*/


/*#- macro fixed(struct) -#*/
struct /*{struct.name}*/__fixed
/*#- endmacro -#*/


/*#- macro struct_fixed(struct) -#*/
/*# if struct.needs_vbuf #*/
/*{fixed(struct)}*/
/*#- else #*/
struct /*{struct.name}*/
/*#- endif #*/
/*#- endmacro -#*/


/*#- macro sized(struct) -#*/
struct /*{struct.name}*/__sized
/*#- endmacro -#*/


/*#- macro wrapped(struct) -#*/
struct /*{struct.name}*/__wrapped
/*#- endmacro -#*/


/*#- macro ptrs_struct(struct) -#*/
struct /*{struct.name}*/__ptrs
/*#- endmacro -#*/


/*#- macro api_struct_decl(struct) -#*/

struct /*{struct.name}*/ {
// for member in struct
	/*{member.cdecl}*/;
// endfor
}/*{naturally_packed(struct)}*/;
/*#- endmacro -#*/


################################################################################
/*# macro fixed_struct_decl(struct) #*/

/*{fixed(struct)}*/ {
// for member in struct
// if member.needs_vbuf
// if member.is_scalar
	xpdt_buflen_t /*{member.name}*/;
// else
	/*{struct_fixed(member.type.struct)}*/ /*{member.name}*/;
// endif
// else
	/*{member.cdecl}*/;
// endif
// endfor
} __attribute__((packed));
/*#- endmacro -#*/


################################################################################
/*# macro len_wrapped_struct_decl(struct) #*/

/*{sized(struct)}*/ {
	struct xpdt_sized hdr;
	/*{struct_fixed(struct)}*/ fixed;
// if struct.needs_vbuf
	uint8_t vbuf[0];
// endif
} __attribute__((packed));

/*{wrapped(struct)}*/ {
	struct xpdt_enum hdr;
	/*{struct_fixed(struct)}*/ fixed;
// if struct.needs_vbuf
	uint8_t vbuf[0];
// endif
} __attribute__((packed));
/*#- endmacro -#*/


################################################################################
/*# macro vbuf_struct_decl(struct) #*/

/*{ptrs_struct(struct)}*/ {
// for member in struct.vbuf_members
// if member.type.is_scalar
	const uint8_t * /*{-member.name}*/;
// else
	/*{ptrs_struct(member.type.struct)}*/ /*{member.name}*/;
// endif
// endfor
};
/*#- endmacro -#*/


################################################################################
/*#- macro ctor_defn(struct) #*/
#define /*{init_macro_name(struct)}*/( \
		/*{_memb_names(struct)|macro}*/) \
	(/*{struct.ctype}*/){ \
// for member in struct.non_reserved_members
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


################################################################################
/*#- macro fixed_ctor_defn(struct) #*/

/* Convert /*{struct.name}*/ in to its serialized format, without strings */
static inline
/*{struct_fixed(struct)}*/
/*{fixed_ctor(struct)}*/(const struct /*{struct.name}*/ obj)
{
	return (/*{struct_fixed(struct)}*/){
// for member in struct.non_reserved_members
// if member.needs_vbuf
// if member.is_scalar
		./*{member.name}*/ = obj./*{member.name}*/.len,
// else
		./*{member.name}*/ = /*{fixed_ctor(member.type.struct)}*/(obj./*{member.name}*/),
// endif
// else
		./*{member.name}*/ = obj./*{member.name}*/,
// endif
// endfor
	};
}
/*#- endmacro -#*/


################################################################################
/*#- macro ptrs_ctor_defn(struct) #*/

/* Get pointers to all the variable length fields of a /*{struct.name}*/ object */
static inline
/*{ptrs_struct(struct)}*/
/*{ptrs_ctor(struct)}*/(const struct /*{struct.name}*/ obj)
{
	return (/*{ptrs_struct(struct)}*/){
// for path in struct.c_named_initializers_x1v
		./*{path}*/ = obj./*{path}*/.ptr,
// endfor
	};
}
/*#- endmacro -#*/


################################################################################
/*# macro write_fixed_func(struct) #*/

/* Write an /*{struct.name}*/ object */
static inline
bool /*{wr_fixed(struct)}*/(xostream_t out, const /*{struct.ctype}*/ obj)
{
	/*{struct.ctype}*/ *ptr;

	ptr = (/*{struct.ctype}*/ *)xostream_prepare(out, sizeof(obj));
	if (xpdt_unlikely(ptr == NULL)) {
		return false;
	}

	*ptr = obj;

	return xostream_commit(out, sizeof(obj));
}

/* Create an object and then write it */
static inline
bool /*{write_fixed(struct)}*/(xostream_t out,
		/*{cdecls(struct)}*/)
{
	return /*{wr_fixed(struct)}*/(out, /*{ctor(struct)}*/(
		/*{memb_names(struct)}*/));
}
/*#- endmacro -#*/


################################################################################
/*# macro write_bufreq_func(struct) #*/

/* Calculate the amount of space needed for the vbuf */
static inline
size_t /*{bufreq(struct)}*/(const /*{struct.ctype}*/ obj)
{
	return /*{buf_lens(struct)}*/;
}
/*#- endmacro -#*/


################################################################################
/*# macro write_sized_func(struct) #*/

/* Write an /*{struct.name}*/ object */
static inline
bool /*{wr_sized(struct)}*/(xostream_t out, const /*{struct.ctype}*/ obj)
{
	/*{sized(struct)}*/ *ptr;
// if struct.needs_vbuf
	const size_t rec_len = sizeof(ptr->fixed) + /*{bufreq(struct)}*/(obj);
	xpdt_buflen_t str_len;
	uint8_t *buf;
// else
	const size_t rec_len = sizeof(ptr->fixed);
// endif
	const size_t tot_len = rec_len + sizeof(ptr->hdr);

	ptr = (/*{sized(struct)}*/ *)xostream_prepare(out, tot_len);
	if (xpdt_unlikely(ptr == NULL)) {
		return false;
	}

	ptr->hdr.rec_len = rec_len;
// if struct.needs_vbuf
	ptr->fixed = /*{fixed_ctor(struct)}*/(obj);
// else
	ptr->fixed = obj;
// endif

// if struct.needs_vbuf
	buf = ptr->vbuf;
/*# for path in struct.c_named_initializers_x1v #*/

	str_len = obj./*{path}*/.len;
	memcpy(buf, obj./*{path}*/.ptr, str_len);
	buf += str_len;
/*# endfor #*/
// endif

	return xostream_commit(out, tot_len);
}

/* Create an object and then write it */
static inline
bool /*{write_sized(struct)}*/(xostream_t out,
		/*{cdecls(struct)}*/)
{
	return /*{wr_sized(struct)}*/(out, /*{ctor(struct)}*/(
		/*{memb_names(struct)}*/));
}
/*#- endmacro -#*/


################################################################################
/*# macro write_wrapped_func(struct) #*/

/* Write an /*{struct.name}*/ object */
static inline
bool /*{wr_wrapped(struct)}*/(xostream_t out, const /*{struct.ctype}*/ obj)
{
	/*{wrapped(struct)}*/ *ptr;
// if struct.needs_vbuf
	const size_t rec_len = sizeof(ptr->fixed) + /*{bufreq(struct)}*/(obj);
	xpdt_buflen_t str_len;
	uint8_t *buf;
// else
	const size_t rec_len = sizeof(ptr->fixed);
// endif
	const size_t tot_len = rec_len + sizeof(ptr->hdr);

	ptr = (/*{wrapped(struct)}*/ *)xostream_prepare(out, tot_len);
	if (xpdt_unlikely(ptr == NULL)) {
		return false;
	}

	ptr->hdr.rec_len = rec_len;
	ptr->hdr.discr = 0x/*{struct.discriminant|hex32}*/;
	ptr->hdr.timestamp = xostream_get_timestamp();
// if struct.needs_vbuf
	ptr->fixed = /*{fixed_ctor(struct)}*/(obj);
// else
	ptr->fixed = obj;
// endif

// if struct.needs_vbuf
	buf = ptr->vbuf;
/*# for path in struct.c_named_initializers_x1v #*/

	str_len = obj./*{path}*/.len;
	memcpy(buf, obj./*{path}*/.ptr, str_len);
	buf += str_len;
/*# endfor #*/
// endif

	return xostream_commit(out, tot_len);
}

/* Create an object and then write it */
static inline
bool /*{write_wrapped(struct)}*/(xostream_t out,
		/*{cdecls(struct)}*/)
{
	return /*{wr_wrapped(struct)}*/(out, /*{ctor(struct)}*/(
		/*{memb_names(struct)}*/));
}
/*#- endmacro -#*/


################################################################################
/*# macro readers(struct) #*/

static inline
const /*{struct_fixed(struct)}*/ *
/*# if struct.needs_vbuf #*/
/*{rd_fixed(struct)}*/(struct xbuf_iter *it, /*{ptrs_struct(struct)}*/ *ptrs)
/*# else #*/
/*{rd_fixed(struct)}*/(struct xbuf_iter *it)
/*# endif #*/
{
	const /*{struct_fixed(struct)}*/ *f;
	const uint8_t *ptr, *end;

	ptr = it->it_ptr;
	end = it->it_end;

	f = (/*{struct_fixed(struct)}*/ *)ptr;
	ptr += sizeof(*f);
	if (xpdt_unlikely(ptr > end))
		return NULL;
/*# if struct.needs_vbuf #*/
/*# for path in struct.c_named_initializers_x1v #*/

	ptrs->/*{path}*/ = ptr;
	ptr += f->/*{path}*/;
/*# endfor #*/

	if (xpdt_unlikely(ptr > end))
		return NULL;
/*# endif #*/

	it->it_ptr = ptr;
	return f;
}

static inline
const /*{struct_fixed(struct)}*/ *
/*# if struct.needs_vbuf #*/
/*{rd_sized(struct)}*/(struct xbuf_iter *it, /*{ptrs_struct(struct)}*/ *ptrs)
/*# else #*/
/*{rd_sized(struct)}*/(struct xbuf_iter *it)
/*# endif #*/
{
	const /*{sized(struct)}*/ *e;
	const uint8_t *ptr, *end;
/*# if struct.needs_vbuf #*/
	const uint8_t *buf;
/*# endif #*/

	ptr = it->it_ptr;
	end = it->it_end;

	e = (/*{sized(struct)}*/ *)ptr;
/*# if struct.needs_vbuf #*/
	buf = e->vbuf;
/*# endif #*/
	if (xpdt_unlikely((uint8_t *)&e->fixed > end))
		return NULL;

	ptr += e->hdr.rec_len;
	if (xpdt_unlikely(ptr > end))
		return NULL;
/*# for path in struct.c_named_initializers_x1v #*/

	ptrs->/*{path}*/ = buf;
	buf += e->fixed./*{path}*/;
/*# endfor #*/

	it->it_ptr = ptr;
	return &e->fixed;
}
/*#- endmacro -#*/


################################################################################
/*# macro obj_ptrs_ctor_defn(struct) #*/

/* Reconstruct a /*{struct.name}*/ object from it's serialized representation and buffers */
static inline
/*{struct.ctype}*/
/*{construct(struct)}*/(const /*{struct_fixed(struct)}*/ *rec, const /*{ptrs_struct(struct)}*/ *ptrs)
{
	return (/*{struct.ctype}*/){
// for member in struct.non_reserved_members
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
