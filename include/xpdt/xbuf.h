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

#include <string.h>
#include <stdlib.h>

struct xbuf {
	const uint8_t *ptr;
	size_t len;
};

#define XBUF_INIT(_len, _ptr) \
	(struct xbuf){.len = _len, .ptr = _ptr}

#define XBUF_NIL \
	XBUF_INIT(0, NULL)

static inline struct xbuf xbuf(size_t len,
				const uint8_t buf[static len])
{
	return XBUF_INIT(len, buf);
}

static inline struct xbuf xbuf_str(size_t len,
				const char buf[static len])
{
	return XBUF_INIT(len, (uint8_t *)buf);
}

static inline struct xbuf xbuf_nil(void)
{
	return XBUF_NIL;
}

static inline struct xbuf xbuf_cstring(const char *str)
{
	return XBUF_INIT(strlen(str), (uint8_t *)str);
}

static inline bool xbuf_isset(const struct xbuf *str)
{
	return str->len;
}
