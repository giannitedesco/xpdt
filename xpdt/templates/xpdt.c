// import 'macros.c' as macros
#pragma once

/* Generated by xpdt
 * xpdt is written by Gianni Tedesco
 * https://www.scaramanga.co.uk
*/

#include <stdlib.h>

#include /*{xpdt_hdr.path_spec}*/

/* ==== structs ==== */

/*#- for struct in namespace #*/

/*{macros.struct_decl(struct)}*/
/*# if struct.needs_vbuf #*/

/*{macros.serialized_struct_decl(struct)}*/

/*{macros.blob_struct_decl(struct)}*/
/*# endif #*/
/*#- endfor -#*/

/*# for struct in namespace #*/


/* ==== /*{struct.name}*/ ==== */
/*{macros.ctors(struct)}*/
/*{macros.writers(struct)}*/
/*{macros.readers(struct)}*/
/*#- endfor -#*/