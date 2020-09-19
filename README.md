# xpdt: eXPeditious Data Transfer

<div align="center">
  <img src="https://img.shields.io/pypi/v/xpdt?label=pypi" alt="PyPI version">
</div>

## About
xpdt is (yet another) language for defining data-types and generating code for
serializing and deserializing them. It aims to produce code with little or no
overhead and is based on fixed-length representations which allows for
zero-copy deserialization and (at-most-)one-copy writes (source to buffer).

The generated C code, in particular, is highly optimized and often permits the
elimination of data-copying for writes and enables optimizations such as
loop-unrolling for fixed-length objects. This can lead to read speeds in
excess of 500 million objects per second (~1.8 nsec per object).

## Examples
The xpdt source language looks similar to C struct definitions:

```
type timestamp {
	u32	tv_sec;
	u32	tv_nsec;
};

type point {
	s32	x;
	s32	y;
	s32	z;
};

type line {
	timestamp	time;
	point		line_start;
	point		line_end;
	blob		comment;
};
```

Fixed width integer types from 8 to 128 bit are supported, along with the
`blob` type, which is a variable-length sequence of bytes.

## Target Languages
The following target languages are currently supported:
- C
- Python

The C code is very highly optimized, and the Python code is fairly well
optimized, it uses typed `NamedTuple` for objects and uses `struct.Struct` for
packing/unpacking. Performance of the pure Python code is comparable to a JSON
library implemented in C or Rust.

For better performance in Python, it may be desirable to develop a Cython
target.

Target languages are implemented purely as `jinja2` templates.

## Serialization format
The serialization format for fixed-length objects is simly a packed C struct.

For any object which contains `blob` type fields:
- a 32bit unsigned record length is prepended to the struct
- all `blob` type fields are converted to `u32` and contain the length of the blob
- all blob contents are appended after the struct in the order in which they appear

For example, following the example above, the serialization would be:

```
u32 tot_len # = 41
u32 time.tv_sec
u32 time.tv_usec
s32 line_start.x
s32 line_start.y
s32 line_start.z
s32 line_end.x
s32 line_end.y
s32 line_end.z
u32 comment # = 5
u8 'H'
u8 'e'
u8 'l'
u8 'l'
u8 'o'
```

## Features
The feature-set is, as of now, pretty slim.

There are no array / sequence / map types, and no keyed unions.

Support for such things may be added in future provided that suitable
implementations exist. An implementation is suitable if:
- It admits a zero (or close to zero) overhead implementation
- it causes no overhead when the feature isn't being used

# License
The compiler is released under the GPLv3.

The C support code/headers are released under the MIT license.

The generated code is yours.
