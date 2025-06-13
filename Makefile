# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= -n -W
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
SPARK_SOURCE  ?= ~/open_source/spark2014

html:
	make -C source
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp source/process/checklist/Checklist_Template_*.md \
	   build/html/process/checklist

pdf:
	make -C source
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

linkcheck:
	make -C source
	@$(SPHINXBUILD) -M linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

extract_assumptions:
	util/extract-spark-assumptions.py $(SPARK_SOURCE)

fix_unicode:
	find . -type f -name "*.md" -exec util/unicode_fix.py '{}' ';'
	find . -type f -name "*.rst" -exec util/unicode_fix.py '{}' ';'
	find . -type f -name "*.rsl" -exec util/unicode_fix.py '{}' ';'
	find . -type f -name "*.trlc" -exec util/unicode_fix.py '{}' ';'
	find . -type f -name "*.csv" -exec util/unicode_fix.py --csv '{}' ';'
