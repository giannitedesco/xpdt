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

#include <stddef.h>
#include <stdint.h>

struct xbuf_iter {
	const uint8_t *it_ptr;
	const uint8_t *it_end;
};

#define XBUF_ITER_INIT(_ptr, _end) \
	((struct xbuf_iter){.it_ptr = _ptr, .it_end = _end})

#define XBUF_ITER_NIL \
	XBUF_ITER_INIT(NULL, NULL)

static inline struct xbuf_iter xbuf_iter_new(const size_t len;
					const uint8_t buf[static const len],
					const size_t len)
{
	return XBUF_ITER_INIT(buf, buf + len);
}

static bool xbuf_iter_eof(const struct xbuf_iter it)
{
	return (it.it_ptr >= it.it_end);
}

static inline struct xbuf_iter xbuf_iter_nil(void)
{
	return XBUF_ITER_NIL;
}

static inline const void *xbuf_iter_read(struct xbuf_iter *it, const size_t len)
{
	const uint8_t * const ret = it->it_ptr;
	const uint8_t * const end = it->it_ptr + len;

	if (__builtin_expect(end > it->it_end, false))
		return NULL;

	it->it_ptr = end;
	return ret;
}

/* WARNING: This is unchecked, it's an optimization */
static inline void xbuf_iter_advance(struct xbuf_iter *it, const size_t len)
{
	it->it_ptr += len;
}

static inline size_t xbuf_iter_count_items_unchecked(const struct xbuf_iter it,
							const size_t len)
{
	const size_t sz = it.it_end - it.it_ptr;

	return sz / len;
}

static inline size_t xbuf_iter_count_items(const struct xbuf_iter it, const size_t len)
{
	if (xbuf_iter_eof(it)) {
		return 0;
	}

	return xbuf_iter_count_items_unchecked(it, len);
}

static inline size_t xbuf_iter_bytes_remaining(const struct xbuf_iter it)
{
	ptrdiff_t ret;

	ret = it.it_end - it.it_ptr;
	if (ret <= 0)
		return 0;

	return ret;
}
