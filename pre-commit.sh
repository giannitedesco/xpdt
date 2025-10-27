#!/bin/sh

set -euo pipefail

exec 1>&2

pkgname='xpdt'
scripts=

mypy \
	--strict \
	${pkgname} ${scripts}

bandit \
	${pkgname} ${scripts}

flake8 ${pkgname}

green
