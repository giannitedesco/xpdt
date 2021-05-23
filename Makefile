MAKEFLAGS += --no-builtin-rules
.SUFFIXES:

TARGET: all

.PHONY: all
all:
	./setup.py build

.PHONY: clean
clean:
	./setup.py clean
	rm -rf build dist *.egg-info
	rm -rf .coverage htmlcov/
	find . -regex '^.*\(__pycache__\|\.py[co]\)$$' -delete


COV_FLAGS := \
	--include="${PWD}/xpdt/*" \
	--omit="${PWD}/xpdt/templates/*"
.PHONY: cov
cov:
	rm -rf .coverage htmlcov/
	coverage run -m unittest discover
	coverage html $(COV_FLAGS)
	coverage report $(COV_FLAGS)
