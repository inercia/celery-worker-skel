
TOP=.

# the system python we will use for bootstrapping
SYS_PYTHON=python2.7

# Buildout
BUILDOUT=$(TOP)/bin/buildout
BUILDOUT_ARGS=-t 120

# the boostrap file
BOOTSTRAP_PY_URL=http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py
BOOTSTRAP_FILE=$(TOP)/buildout/bootstrap.py
BOOTSTRAP_ARGS=-c $(BUILDOUT_DEV_CONF)

# directories we need for running the server but are not automatically created
RUN_DIRS=\
         logs \
         run  \
         var  var/lib

# cleanup some things after building...
POST_BUILD_CLEANUPS=\
        doc  man *~

# RPM creation
RPM_TAR=$(TOP)/pkg.tar
RPM_FILES=README.rst
RPM_DIRS=\
         $(RUN_DIRS) \
         bin conf include lib sbin share \
         html  html/static \
         share/doc \
         scripts
RPM_BUILD_ROOT=/tmp/XXXX-buildroot

STATICS_DIR=$(TOP)/html/static

# where the sources are and how to build them
SOURCES_DIR=$(TOP)/sources
PLUGINS_DIR=$(TOP)/plugins
SETUP_PY=$(SOURCES_DIR)/setup.py

# the admin script
ADMIN_SCRIPT=$(TOP)/bin/XXXX

# API docs dir
API_GEN=$(TOP)/bin/sphinx-apidoc
API_DOCS_DIR=$(TOP)/docs/api/
API_DOCS_OUTPUT_DIR=$(TOP)/docs/api/build

COVERAGE_DOCS_OUTPUT_DIR=$(TOP)/docs/coverage

# nose arguments
NOSE_ARGS=--with-xunit  --all-modules

BUILDOUT_CONF=$(TOP)/buildout.cfg
BUILDOUT_DEV_CONF=$(TOP)/buildout.devel.cfg
BUILDOUT_DEPLOY_CONF=$(TOP)/buildout.deploy.cfg

####################################################################################################

all: devel


$(BUILDOUT): $(BOOTSTRAP_FILE)
	@echo ">>> Bootstraping..."
	@[ -d downloads ] || mkdir downloads
	$(SYS_PYTHON) $(BOOTSTRAP_FILE) $(BOOTSTRAP_ARGS)
	@echo ">>> Bootstrapping SUCCESSFUL!"

00-common:
	@echo ">>> Running buildout for DEVELOPMENT..."
	PATH=$(TOP)/bin:$$PATH $(BUILDOUT) -N $(BUILDOUT_ARGS) -c $(BUILDOUT_DEV_CONF)
	@echo ">>> Checking dirs..."
	@for i in $(RUN_DIRS) ; do mkdir -p $$i ; done
	@rm -rf $(POST_BUILD_CLEANUPS)
	@echo


XXXX: $(BUILDOUT) 00-common

00-deploy:
	@echo ">>> Running buildout for DEPLOYMENT..."
	PATH=$(TOP)/bin:$$PATH $(BUILDOUT) -N $(BUILDOUT_ARGS) -c $(BUILDOUT_DEPLOY_CONF) -v
	@echo ">>> Build SUCCESSFUL !!"
	@echo ">>> You can now 'make docs', 'make coverage'..."

.PHONY: XXXX-deploy
deploy:          $(BUILDOUT)   00-deploy
.PHONY: deploy-fast
deploy-fast:                   00-deploy



devel: $(BUILDOUT)
	@echo ">>> Running buildout for DEVELOPMENT..."
	PATH=$(TOP)/bin:$$PATH $(BUILDOUT) -N $(BUILDOUT_ARGS) -c $(BUILDOUT_DEV_CONF) -v
	@echo ">>> Build SUCCESSFUL !!"
	@echo ">>> You can now 'make docs', 'make coverage'..."

fast: $(BUILDOUT)
	@echo ">>> Running FAST buildout. I hope we have all dependencies installed..."
	PATH=$(TOP)/bin:$$PATH $(BUILDOUT) -N $(BUILDOUT_ARGS) -o  -c $(BUILDOUT_DEV_CONF)
	@rm -rf $(POST_BUILD_CLEANUPS) $(TOP)/pip-*
	@echo ">>> Fast-build SUCCESSFUL !!"
	@echo ">>> You can now 'make docs', 'make coverage'..."

$(BOOTSTRAP_FILE):
	@echo ">>> Getting boostrap.py..."
	@wget -q -O $(BOOTSTRAP_FILE)   $(BOOTSTRAP_PY_URL)
	@echo ">>> We got the bootstrap file !!"


####################################################################################################
# cleanup



clean-pyc: 
	@echo ">>> Cleaning pyc..."
	rm -f     `find $(SOURCES_DIR) $(PLUGINS_DIR) -name '*.pyc'`
	rm -f     `find $(SOURCES_DIR) $(PLUGINS_DIR) -name '*.pyo'`

clean-dcache:
	rm -rf    $(TOP)/downloads

clean: clean-pyc
	@echo ">>> Cleaning stuff..."
	rm -rf    $(TOP)/bin $(TOP)/doc $(TOP)/dist $(TOP)/var
	rm -rf    $(TOP)/conf/*.conf  $(TOP)/conf/*/*.conf
	rm -rf    $(TOP)/*.spec $(TOP)/buildout/packaging/*.spec
	rm -rf    $(TOP)/plugins/*/*.egg-info
	rm -rf    $(TOP)/develop-eggs $(TOP)/eggs $(TOP)/html
	rm -rf    $(TOP)/include $(TOP)/man $(TOP)/local $(TOP)/lib $(TOP)/logs $(TOP)/parts
	rm -rf    $(TOP)/run $(TOP)/share $(TOP)/sbin
	rm -rf    $(TOP)/doc $(TOP)/docs/coverage/*
	rm -rf    $(TOP)/build $(TOP)/local $(TOP)/temp $(TOP)/*_temp $(TOP)/*~  $(TOP)/pip-*
	rm -rf    $(TOP)/*.egg-info  $(TOP)/*/*.egg-info   $(TOP)/nosetests.xml
	rm -rf    $(TOP)/*__tmp  $(TOP)/*log.txt  $(TOP)/test.py*  $(TOP)/*.log  $(TOP)/log
	rm -rf    $(TOP)/.installed.cfg $(TOP)/depends-log.txt
	rm -rf    $(TOP)/*packages-log.txt $(TOP)/profile.* $(TOP)/*.log
	rm -rf    $(TOP)/nosetests.xml  $(TOP)/nosetests.log
	rm -rf    $(TOP)/*.rpm $(TOP)/*.deb $(TOP)/*.tgz $(TOP)/*.pdf $(TOP)/*.dump
	rm -rf    $(TOP)/.Python
	rm -rf    $(RPM_TAR)
	@echo ">>> Everything bright and clean!!"
	@echo ">>> You can now 'make'..."

distclean: clean-docs clean

run-cleanup:
	@echo ">>> Cleaning up things..."
	@[ -d logs ] || mkdir logs
	@[ -d logs ] && rm -rf logs/*
	@[ -d run ] || mkdir run
	@[ -d run ] && rm -rf run/*
	@echo ">>> Checking dirs..."
	@for i in $(RUN_DIRS) ; do mkdir -p $$i ; done

####################################################################################################
# packaging

00-rpm:
	@echo ">>> Packaging..."
	PATH=$(TOP)/bin:$$PATH $(BUILDOUT) -N $(BUILDOUT_ARGS) -c $(BUILDOUT_DEPLOY_CONF) -v install rpm
	@echo ">>> Packaging SUCCESSFUL !!"

.PHONY: rpm
rpm:                           $(BUILDOUT) run-cleanup   deploy  00-rpm
.PHONY: rpm-fast
rpm-fast:                                                        00-rpm
rpm-clean: distclean rpm

####################################################################################################
# run

run: run-cleanup
	@echo ">>> Running the XXXX CC..."
	@PYTHONPATH=$(SOURCES_DIR):$$PYTHONPATH \
		LD_LIBRARY_PATH=$(TOP)/lib:$$LD_LIBRARY_PATH       \
		DYLD_LIBRARY_PATH=$(TOP)/lib:$$DYLD_LIBRARY_PATH   \
		$(ADMIN_SCRIPT) --config=$(TOP)/conf/XXXX.conf

####################################################################################################
# documentation

# note: on Mac OS X, set "LC_ALL=en_US.UTF-8" and "LANG=en_US.UTF-8" for docs generation

clean-docs:
	@echo ">>> Cleaning docs..."
	rm -rf    $(API_DOCS_OUTPUT_DIR)

$(TOP)/bin/sphinx-build: $(BUILDOUT)
	@echo ">>> Creating docs builder..."
	@[ -d $(API_DOCS_OUTPUT_DIR) ] || mkdir -p $(API_DOCS_OUTPUT_DIR)

docs-api:
	@echo ">>> Creating API docs..."
	rm -f $(API_DOCS_DIR)/XXXX.*.rst
	ABS_SOURCES_DIR=`pwd`/$(SOURCES_DIR) ; \
	    $(API_GEN) --force -o $(API_DOCS_DIR) -d 8 -s rst  $$ABS_SOURCES_DIR  \
	    `find $$ABS_SOURCES_DIR -name tests`

.PHONY: 00-docs-run
00-docs-run: docs-api
	@echo ">>> Creating development docs..."
	@PYTHONPATH=$(SOURCES_DIR):$$PYTHONPATH \
	    XXXX_PREFIX=$(TOP) \
	    XXXX_CONF=$(TOP)/conf/XXXX.conf \
	    LD_LIBRARY_PATH=$(TOP)/lib:$$LD_LIBRARY_PATH   \
	    DYLD_LIBRARY_PATH=$(TOP)/lib:$$DYLD_LIBRARY_PATH   \
		    $(TOP)/bin/sphinx-build -q -b html  $(API_DOCS_DIR)  $(API_DOCS_OUTPUT_DIR)
	@echo ">>> Documentation left at $(API_DOCS_OUTPUT_DIR)"

.PHONY: docs
docs:              clean-docs all $(TOP)/bin/sphinx-build   00-docs-run
.PHONY: docs-fast
docs-fast:         clean-docs                                00-docs-run

.PHONY: 00-docs-pdf-run
00-docs-pdf-run: docs-api
	@echo ">>> Creating development docs (PDF)..."
	@PYTHONPATH=$(SOURCES_DIR):$$PYTHONPATH \
	    XXXX_PREFIX=$(TOP) \
	    XXXX_CONF=$(TOP)/conf/XXXX.conf \
	    LD_LIBRARY_PATH=$(TOP)/lib:$$LD_LIBRARY_PATH   \
	    DYLD_LIBRARY_PATH=$(TOP)/lib:$$DYLD_LIBRARY_PATH   \
		    $(TOP)/bin/sphinx-build -q -b latex  \
		        $(API_DOCS_DIR)  $(API_DOCS_OUTPUT_DIR)/latex
	make -C  $(API_DOCS_OUTPUT_DIR)/latex   all-pdf
	@echo ">>> PDF documentation at $(API_DOCS_OUTPUT_DIR)/latex"
	@cp $(API_DOCS_OUTPUT_DIR)/latex/*.pdf   $(TOP)/  && echo ">>> PDFs also copied at $(TOP)"


.PHONY: docs-pdf
docs-pdf:          clean-docs all $(TOP)/bin/sphinx-build   00-docs-pdf-run
.PHONY: docs-pdf-fast
docs-pdf-fast:     clean-docs                                00-docs-pdf-run


####################################################################################################
# test & coverage

.PHONY: 00-test-run
00-test-run:
	@echo ">>> Running unit tests FAST..."
	$(TOP)/bin/XXXX-tess
	@echo ">>> done!"

.PHONY: test
test:               $(ADMIN_SCRIPT) 00-test-run
.PHONY: test-fast
test-fast:                     00-test-run

00-coverage-run:
	@echo ">>> Creating coverage report for the node..."
	@[ -d $(COVERAGE_DOCS_OUTPUT_DIR) ] || mkdir $(COVERAGE_DOCS_OUTPUT_DIR)
	@rm -rf $(COVERAGE_DOCS_OUTPUT_DIR)/*
	$(TOP)/bin/XXXX-tests --node \
	    --with-xcoverage --xcoverage-file=coverage.xml --cover-package=XXXX --cover-erase && \
	[ $$? -eq 0 ] && $(TOP)/bin/coverage html -d $(COVERAGE_DOCS_OUTPUT_DIR)
	@echo ">>> Documentation left at $(COVERAGE_DOCS_OUTPUT_DIR)"

.PHONY: coverage
coverage:              $(ADMIN_SCRIPT)  00-coverage-run
.PHONY: coverage-fast
coverage-fast:                     00-coverage-run


00-pylint-run:
	@echo ">>> Creating pylint report..."
	@PYTHONPATH=$(SOURCES_DIR):$$PYTHONPATH \
	$(TOP)/bin/pylint --rcfile=$(TOP)/buildout/pylintrc $(SOURCES_DIR)
	@echo ">>> done!"

.PHONY: pylint
pylint:              $(ADMIN_SCRIPT)  00-pylint-run
.PHONY: pylint-fast
pylint-fast:                     00-pylint-run



