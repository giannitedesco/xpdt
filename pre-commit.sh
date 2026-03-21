#!/bin/sh

set -euo pipefail

exec 1>&2

pkgname='xpdt'
scripts=

mypy \
	--strict \
	--install-types \
	--non-interactive \
	${pkgname} ${scripts}

bandit \
	${pkgname} ${scripts}

flake8 ${pkgname}

green
