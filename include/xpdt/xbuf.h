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

#define XBUF_INIT(_ptr, _len) \
	((struct xbuf){.ptr = _ptr, .len = _len})

#define XBUF_NIL \
	XBUF_INIT(NULL, 0)

static inline struct xbuf xbuf(const size_t len;
				const uint8_t buf[static const len],
				const size_t len)
{
	return XBUF_INIT(buf, len);
}

static inline struct xbuf xbuf_str(const size_t len;
				const char buf[static const len],
				const size_t len)
{
	return XBUF_INIT((uint8_t *)buf, len);
}

static inline struct xbuf xbuf_nil(void)
{
	return XBUF_NIL;
}

static inline struct xbuf xbuf_cstring(const char *str)
{
	return xbuf_str(str, strlen(str));
}

static inline bool xbuf_is_set(const struct xbuf *str)
{
	return str->len;
}

static inline bool xbuf_is_nil(const struct xbuf *str)
{
	return !str->len;
}
