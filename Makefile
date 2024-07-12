ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL := /bin/bash
TOX_DIR := .tox
VIRTUALENV_DIR ?= virtualenv
ST2_VIRTUALENV_DIR ?= st2/virtualenv

# Sphinx docs options
SPHINXBUILD := sphinx-build
DOC_SOURCE_DIR := docs/source
DOC_BUILD_DIR := docs/build

BINARIES := bin

PYTHON_VERSION := python3.8

# All components are prefixed by st2
COMPONENTS := $(wildcard st2*)
COMPONENTS_RUNNERS := $(wildcard st2/contrib/runners/*)

# Components that implement a component-controlled test-runner. These components provide an
# in-component Makefile. (Temporary fix until I can generalize the pecan unittest setup. -mar)
# Note: We also want to ignore egg-info dir created during build
COMPONENT_SPECIFIC_TESTS := st2tests st2client.egg-info

# nasty hack to get a space into a variable
space_char :=
space_char +=
comma := ,
COMPONENT_PYTHONPATH = $(subst $(space_char),:,$(realpath $(COMPONENTS)))

REQUIREMENTS := requirements.txt st2/requirements.txt
DOCS_VERSION := $(shell cat version.txt | cut -d '.' -f 1,2)
ST2_BRANCH := v$(DOCS_VERSION)
ifneq (,$(findstring dev,$(ST2_BRANCH)))
	ST2_BRANCH := master
endif

PIP_VERSION := $(shell curl --silent https://raw.githubusercontent.com/StackStorm/st2/$(ST2_BRANCH)/Makefile | grep 'PIP_VERSION ?= ' | awk '{ print $$3 }')
PIP_OPTIONS := $(ST2_PIP_OPTIONS)

ifndef PIP_OPTIONS
	PIP_OPTIONS := -U -q
endif

.PHONY: all
all: docs

.PHONY: docs
docs: requirements orquesta .docs

# This isn't a dependency of st2, but it needs to be installed in the st2 virtualenv
# so that the generate-runner-parameters-documentation.py script can write out the
# RST table
$(ST2_VIRTUALENV_DIR)/lib/$(PYTHON_VERSION)/site-packages/pytablewriter: $(ST2_VIRTUALENV_DIR)/done
	. $(ST2_VIRTUALENV_DIR)/bin/activate; pip install pytablewriter
	touch $@

.PHONY: .docs
.docs: $(VIRTUALENV_DIR)/installed $(ST2_VIRTUALENV_DIR)/lib/$(PYTHON_VERSION)/site-packages/pytablewriter
	@echo
	@echo "========================== DOCS ========================="
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
.livedocs: $(VIRTUALENV_DIR)/installed
	@echo
	@echo "==========================================================="
	@echo "                       RUNNING DOCS"
	@echo "==========================================================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; sphinx-autobuild --host 0.0.0.0 -b html $(DOC_SOURCE_DIR) $(DOC_BUILD_DIR)/html
	@echo

.PHONY: .cleandocs
.cleandocs:
	@echo "Removing generated documentation"
	rm -rf $(DOC_BUILD_DIR)

.PHONY: .clean-orquesta
.clean-orquesta:
	@echo
	@echo "================= .clean-orquesta ================="
	@echo
	rm -rf orquesta

.PHONY: .clean-st2
.clean-st2:
	@echo
	@echo "==================== .clean-st2 ==================="
	@echo
	rm -rf st2

.PHONY: .clean
.clean: .cleandocs

.PHONY: clean
clean: .clean

.PHONY: distclean
distclean: .clean .clean-orquesta .clean-st2
	@echo
	@echo "==================== distclean ===================="
	@echo
	rm -rf $(VIRTUALENV_DIR)

.PHONY: requirements
requirements: $(VIRTUALENV_DIR)/installed

$(VIRTUALENV_DIR)/installed: requirements.txt $(VIRTUALENV_DIR)/done st2
	@echo
	@echo "==================== st2docs requirements ===================="
	@echo

	# Use same pip version as st2
	$(VIRTUALENV_DIR)/bin/pip install --upgrade "pip==$(PIP_VERSION)"

	# Install requirements
	#
	for req in $(REQUIREMENTS); do \
			echo "Installing $$req..." ; \
			$(VIRTUALENV_DIR)/bin/pip install $(PIP_OPTIONS) -r $$req ; \
	done
	touch $@

$(VIRTUALENV_DIR): $(VIRTUALENV_DIR)/done

$(VIRTUALENV_DIR)/done: $(VIRTUALENV_DIR)/bin/activate
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
	touch $@

$(VIRTUALENV_DIR)/bin/activate:
	@echo
	@echo "==================== st2docs virtualenv ===================="
	@echo
	virtualenv --python=$(PYTHON_VERSION) $(VIRTUALENV_DIR)
	touch $@

$(ST2_VIRTUALENV_DIR)/installed_runners: $(ST2_VIRTUALENV_DIR)/done
	@echo ""
	@echo "================== install runners ===================="
	@echo ""
	@for component in $(COMPONENTS_RUNNERS); do \
		echo "==========================================================="; \
		echo "Installing runner:" $$component; \
		echo "==========================================================="; \
        (. $(ST2_VIRTUALENV_DIR)/bin/activate; cd $$component; $(PYTHON_VERSION) setup.py develop); \
	done
	touch $@

st2:
	@echo
	@echo "==================== cloning st2 ===================="
	@echo
	./scripts/clone-st2.sh
	touch $@

$(ST2_VIRTUALENV_DIR): st2
	@echo
	@echo "==================== st2 virtualenv ===================="
	@echo
	cd st2; make virtualenv

$(ST2_VIRTUALENV_DIR)/done: $(ST2_VIRTUALENV_DIR)
	cd ./st2; make requirements
	touch $@

orquesta:
	@echo
	@echo "==================== cloning orquesta ===================="
	@echo
	./scripts/clone-orquesta.sh

.PHONY: docker
docker: docker-build docker-run

.PHONY: docker-build
docker-build:
	@echo
	@echo "==================== Building st2docs Docker ===================="
	@echo
	docker build -t st2/st2docs -f Dockerfile .

.PHONY: docker-run
docker-run:
	@echo
	@echo "==================== Running st2docs in Docker ===================="
	@echo
	docker run --rm -it -v ${PWD}/docs/source:/st2docs/docs/source -p 127.0.0.1:8000:8000 st2/st2docs
