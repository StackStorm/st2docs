ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL := /bin/bash
TOX_DIR := .tox
VIRTUALENV_DIR ?= virtualenv
ST2_VIRTUALENV_DIR = st2/virtualenv

# Sphinx docs options
SPHINXBUILD := sphinx-build
DOC_SOURCE_DIR := docs/source
DOC_BUILD_DIR := docs/build

BINARIES := bin

# All components are prefixed by st2
COMPONENTS := $(wildcard st2*)

# Components that implement a component-controlled test-runner. These components provide an
# in-component Makefile. (Temporary fix until I can generalize the pecan unittest setup. -mar)
# Note: We also want to ignore egg-info dir created during build
COMPONENT_SPECIFIC_TESTS := st2tests st2client.egg-info

# nasty hack to get a space into a variable
space_char :=
space_char +=
comma := ,
COMPONENT_PYTHONPATH = $(subst $(space_char),:,$(realpath $(COMPONENTS)))
COMPONENTS_TEST := $(foreach component,$(filter-out $(COMPONENT_SPECIFIC_TESTS),$(COMPONENTS)),$(component))
COMPONENTS_TEST_COMMA := $(subst $(space_char),$(comma),$(COMPONENTS_TEST))

PYTHON_TARGET := 2.7

REQUIREMENTS := requirements.txt st2/requirements.txt
PIP_OPTIONS := $(ST2_PIP_OPTIONS)

ifndef PIP_OPTIONS
	PIP_OPTIONS := -U -q
endif

.PHONY: all
all: requirements check tests docs

.PHONY: docs
docs: .clone-st2 requirements .requirements-st2 .docs

.PHONY: .docs
.docs:
	@echo
	@echo "==================== docs ===================="
	@echo
	. $(ST2_VIRTUALENV_DIR)/bin/activate; ./scripts/generate-runner-parameters-documentation.py
	. $(ST2_VIRTUALENV_DIR)/bin/activate; ./scripts/generate-internal-triggers-table.py
	. $(ST2_VIRTUALENV_DIR)/bin/activate; ./scripts/generate-available-permission-types-table.py
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; $(SPHINXBUILD) -W -b html $(DOC_SOURCE_DIR) $(DOC_BUILD_DIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(DOC_BUILD_DIR)/html."

.PHONY: livedocs
livedocs: docs .livedocs

.PHONY: .livedocs
.livedocs:
	@echo
	@echo "==========================================================="
	@echo "                       RUNNING DOCS"
	@echo "==========================================================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; sphinx-autobuild -H 0.0.0.0 -b html $(DOC_SOURCE_DIR) $(DOC_BUILD_DIR)/html
	@echo

.PHONY: bwcdocs
bwcdocs: .clone-st2 .clone-ipfabric requirements .requirements-st2 .bwcdocs .docs

.PHONY: .bwcdocs
.bwcdocs:
	@echo
	@echo "=========================================================="
	@echo "                     PATCHING BWC DOCS"
	@echo "=========================================================="
	@echo
	cp -R ipfabric/* docs/source/

.PHONY: bwclivedocs
livedocs: bwcdocs .livedocs

.PHONY: .cleandocs
.cleandocs:
	@echo "Removing generated documentation"
	rm -rf $(DOC_BUILD_DIR)

.PHONY: distclean
distclean: clean
	@echo
	@echo "==================== distclean ===================="
	@echo
	rm -rf $(VIRTUALENV_DIR)

.PHONY: requirements
requirements: virtualenv
	@echo
	@echo "==================== st2docs requirements ===================="
	@echo

	# Make sure we use latest version of pip
	$(VIRTUALENV_DIR)/bin/pip install --upgrade "pip<8.0.0"

	# Install requirements
	#
	for req in $(REQUIREMENTS); do \
			echo "Installing $$req..." ; \
			$(VIRTUALENV_DIR)/bin/pip install $(PIP_OPTIONS) -r $$req ; \
	done

.PHONY: virtualenv
virtualenv: $(VIRTUALENV_DIR)/bin/activate
$(VIRTUALENV_DIR)/bin/activate:
	@echo
	@echo "==================== st2docs virtualenv ===================="
	@echo
	test -d $(VIRTUALENV_DIR) || virtualenv --no-site-packages $(VIRTUALENV_DIR)

	# Setup PYTHONPATH in bash activate script...
	echo '' >> $(VIRTUALENV_DIR)/bin/activate
	echo '_OLD_PYTHONPATH=$$PYTHONPATH' >> $(VIRTUALENV_DIR)/bin/activate
	echo 'PYTHONPATH=$$_OLD_PYTHONPATH:$(COMPONENT_PYTHONPATH)' >> $(VIRTUALENV_DIR)/bin/activate
	echo 'export PYTHONPATH' >> $(VIRTUALENV_DIR)/bin/activate
	touch $(VIRTUALENV_DIR)/bin/activate

	# Setup PYTHONPATH in fish activate script...
	echo '' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo 'set -gx _OLD_PYTHONPATH $$PYTHONPATH' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo 'set -gx PYTHONPATH $$_OLD_PYTHONPATH $(COMPONENT_PYTHONPATH)' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo 'functions -c deactivate old_deactivate' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo 'function deactivate' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo '  if test -n $$_OLD_PYTHONPATH' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo '    set -gx PYTHONPATH $$_OLD_PYTHONPATH' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo '    set -e _OLD_PYTHONPATH' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo '  end' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo '  old_deactivate' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo '  functions -e old_deactivate' >> $(VIRTUALENV_DIR)/bin/activate.fish
	echo 'end' >> $(VIRTUALENV_DIR)/bin/activate.fish
	touch $(VIRTUALENV_DIR)/bin/activate.fish

.PHONY: .clone-st2
.clone-st2:
	@echo
	@echo "==================== cloning st2 ===================="
	@echo
	./scripts/clone-st2.sh

.PHONY: .clone-ipfabric
.clone-ipfabric:
	@echo
	@echo "==================== cloning ipfabric docs ===================="
	@echo
	./scripts/clone-ipfabric.sh

PHONY: .virtualenv-st2
.virtualenv-st2: .clone-st2
	@echo
	@echo "==================== st2 virtualenv ===================="
	@echo
	cd st2; make virtualenv

PHONY: .requirements-st2
.requirements-st2: .clone-st2
	@echo
	@echo "==================== st2 requirements ===================="
	@echo
	cd st2; make requirements
