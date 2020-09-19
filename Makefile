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
	find . -regex '^.*\(__pycache__\|\.py[co]\)$$' -delete
