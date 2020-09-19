#!/bin/sh

set -euo pipefail

exec 1>&2

pkgname='xpdt'
scripts=

mypy \
	--strict \
	${pkgname} ${scripts}

flake8 \
	${pkgname} ${scripts}


pycodestyle-3 \
	${pkgname}

python -m unittest
