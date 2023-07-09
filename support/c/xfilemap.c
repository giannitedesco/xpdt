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

#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>
#include <stdio.h>
#include <stdint.h>

#include <xpdt/xfilemap.h>

#ifndef likely
#define likely(x) __builtin_expect((bool)(x), false)
#endif
#ifndef unlikely
#define unlikely(x) __builtin_expect((bool)(x), false)
#endif

bool xfilemap__map(struct xfilemap *xf, const int fd, bool prefault)
{
	const int flags = (prefault) ? (MAP_SHARED | MAP_POPULATE) : (MAP_SHARED);
	struct stat st;
	const uint8_t *m_map;
	size_t m_len;

	if (unlikely(fstat(fd, &st))) {
		return false;
	}

	m_len = st.st_size;
	if (!m_len) {
		*xf = MAPFILE_NIL;
		return true;
	}

	m_map = mmap(NULL,
			st.st_size,
			PROT_READ,
			flags,
			fd,
			0);
	if (unlikely(m_map == MAP_FAILED)) {
		*xf = MAPFILE_NIL;
		return false;
	}

	*xf = xfilemap_new(m_map, m_len);

	return true;
}

bool xfilemap__open(struct xfilemap *xf, const char *fn, bool prefault)
{
	const int fd = open(fn, O_RDONLY);

	if (unlikely(fd < 0)) {
		return false;
	}

	if (unlikely(!xfilemap__map(xf, fd, prefault))) {
		const int saved_errno = errno;

		close(fd);

		errno = saved_errno;
		return false;
	}

	close(fd);
	return true;
}

void xfilemap_close(const struct xfilemap xf)
{
	if (xf.m_len) {
		munmap((void *)xf.m_map, xf.m_len);
	}
}
