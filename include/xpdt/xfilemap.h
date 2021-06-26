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
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

#include "xbuf_iter.h"

struct xfilemap {
	size_t m_len;
	const uint8_t *m_map;
};

#define MAPFILE_INIT(_len, _map) \
	(struct xfilemap){.m_len = _len, .m_map = _map}

#define MAPFILE_NIL \
	MAPFILE_INIT(0, NULL)

static inline struct xfilemap xfilemap_new(size_t len,
					const uint8_t map[static len])
{
	return MAPFILE_INIT(len, map);
}

static inline size_t xfilemap_count_items(const struct xfilemap *xf, size_t len)
{
	return xf->m_len / len;
}

bool xfilemap_open(struct xfilemap *xf, const char *fn);
void xfilemap_close(struct xfilemap *xf);

static inline struct xbuf_iter xfilemap_iter(const struct xfilemap *xf)
{
	return xbuf_iter_new(xf->m_len, xf->m_map);
}

static inline struct xbuf_iter xfilemap_iter_slice(const struct xfilemap *xf,
							size_t from,
							size_t len)
{
	assert(xf->m_len <= (from + len));
	return xbuf_iter_new(len, xf->m_map + from);
}

static inline struct xbuf_iter xfilemap_iter_items(const struct xfilemap *xf,
							size_t item_size)
{
	size_t trailer = xf->m_len % item_size;
	return xbuf_iter_new(xf->m_len - trailer, xf->m_map);
}

static inline struct xbuf_iter xfilemap_iter_unrolled(const struct xfilemap *xf,
							unsigned int burst_size,
							size_t item_size,
							unsigned int *trailer)
{
	size_t nr_items = xf->m_len / item_size;
	*trailer = nr_items % burst_size;
	return xfilemap_iter_items(xf, burst_size * item_size);
}
