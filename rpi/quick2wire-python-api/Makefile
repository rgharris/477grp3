
# Which version of python are we using?
ifndef python
python=3.2
endif

# Which devices are connected and configured for loopback testing?
ifndef devices
devices=mcp23017 gpio mcp23008
endif


ARCHITECTURE:=$(shell uname -m)

PYTHON_ENV=$(PWD)/python$(python)-$(ARCHITECTURE)
PYTHON_EXE=$(PYTHON_ENV)/bin/python
PIP=$(PYTHON_ENV)/bin/pip

PROJECT:=$(shell $(PYTHON_EXE) setup.py --name)
VERSION:=$(shell $(PYTHON_EXE) setup.py --version)


all: check dist
.PHONY: all

env: env-base env-libs
.PHONY: env

env-base:
	mkdir -p $(dir $(PYTHON_ENV))
	tools/virtualenv --python=python$(python) $(PYTHON_ENV)
	rm -f distribute-*.tar.gz
.PHONY: env-base

env-libs:
	$(PIP) install -r requirements.txt
.PHONY: env-libs

env-clean:
	rm -rf $(PYTHON_ENV)/
.PHONY: env-clean

env-again: env-clean env
.PHONY: env-again

check:
	$(PYTHON_EXE) setup.py test
.PHONY: check

check-install: TESTENV=$(abspath build/test-python$(python)-$(ARCHITECTURE))
check-install: dist
	$(MAKE) PYTHON_ENV=$(TESTENV) env-again
	mkdir -p build/
	cd build/ && tar xzf ../dist/$(PROJECT)-$(VERSION).tar.gz
	cd build/$(PROJECT)-$(VERSION) && $(TESTENV)/bin/python setup.py install
	$(TESTENV)/bin/python setup.py test
.PHONY: check-install

dist/$(PROJECT)-$(VERSION).tar.gz: setup.py Makefile README.rst
	$(PYTHON_EXE) setup.py sdist

README.rst: README.md
	pandoc --from=markdown --to=rst $^ > $@

dist: dist/$(PROJECT)-$(VERSION).tar.gz
.PHONY: dist

clean:
	rm -rf output/ dist/ build/ MANIFEST README.rst quick2wire_api.egg-info README.rst
	find . -name '*.pyc' -o -name '*~' | xargs -r rm -f
.PHONY: clean

again: clean all
.PHONY: again


SCANNED_FILES=$(shell find src/ -type d) $(shell find test/ -type d) Makefile setup.py

.PHONY: continually
continually:
	@while true; do \
	  clear; \
	  if not make check; \
	  then \
	      notify-send --icon=error --category=build --expire-time=250 "$(PROJECT) build broken"; \
	  fi; \
	  date; \
	  inotifywait -r -qq -e modify -e delete $(SCANNED_FILES); \
	done
