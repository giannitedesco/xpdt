/*#- macro entry_name(struct) -#*/
/*{namespace.name}*/_/*{struct.name}*/
/*#- endmacro #*/

/*#- macro stream() -#*/
/*{namespace.name}*/_xostream
/*#- endmacro #*/

/*#- macro cdecls(struct) -#*/
/*{struct.non_reserved_members
	| map(attribute="const_cdecl")
	| join(",\n\t\t")}*/
/*#- endmacro -#*/

/*#- macro memb_names(struct) -#*/
/*{struct.non_reserved_members
	| map(attribute="name")
	| join(",\n\t\t")}*/
/*#- endmacro -#*/

/*#- macro wr_wrapped(struct) -#*/
/*{struct.name}*/__write_wrapped
/*#- endmacro -#*/


/* Generated by xpdt
 * xpdt is written by Gianni Tedesco
 * https://github.com/giannitedesco/xpdt
 */

/*# for hdr in headers #*/
#include /*{hdr.path_spec}*/
/*# endfor #*/

extern struct xostream /*{stream()}*/;
/*#- for struct in namespace #*/


void /*{entry_name(struct)}*/(/*{cdecls(struct)}*/)
{
	/*{wr_wrapped(struct)}*/(&/*{stream()}*/,
		/*{memb_names(struct)}*/);
}
/*#- endfor #*/
