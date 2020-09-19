#pragma once

/* Copyright (c) 2020 Gianni Tedesco
 * https://www.scaramanga.co.uk
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
*/

#include <stdlib.h>

#include <stdint.h>

struct _xu128_s {
	union {
#ifdef __SIZEOF_INT128__
		unsigned __int128 u128;
#endif
		struct {
			uint64_t lo;
			uint64_t hi;
		};
		uint8_t bytes[16];
	};
} __attribute__((packed));

typedef struct _xu128_s xu128_t;

#define XU128_INIT(_hi, _lo) \
	(struct _xu128_s){ \
		.lo = _lo, \
		.hi = _hi, \
	}

#define XU128_NIL XU128_INIT(0, 0)

static inline xu128_t xu128(uint64_t hi, uint64_t lo)
{
	return XU128_INIT(hi, lo);
}
