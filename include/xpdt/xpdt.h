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
#include <string.h>
#include <stdbool.h>

#define xpdt_likely(x) __builtin_expect((bool)(x), true)
#define xpdt_unlikely(x) __builtin_expect((bool)(x), false)

#include "xu128.h"
#include "xbuf.h"
#include "xbuf_iter.h"
#include "xfilemap.h"

typedef uint32_t xpdt_reclen_t;
typedef uint32_t xpdt_buflen_t;
typedef uint32_t xpdt_discriminant_t;
typedef uint64_t xpdt_timestamp_t;

struct xpdt_sized {
	xpdt_buflen_t rec_len;
} __attribute__((packed));

struct xpdt_enum {
	xpdt_buflen_t rec_len;
	xpdt_discriminant_t discr;
	xpdt_timestamp_t timestamp;
} __attribute__((packed));

typedef struct xostream *xostream_t;
uint8_t *xostream_prepare(xostream_t, size_t);
bool xostream_commit(xostream_t, size_t);
xpdt_timestamp_t xostream_get_timestamp(void);
