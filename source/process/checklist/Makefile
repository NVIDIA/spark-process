RST_SOURCES := $(shell find .. -name "*.rst")
RST_TARGETS := $(addsuffix .rst, $(basename $(wildcard *.trlc)))
CHECKLIST := \
	Checklist_Template_Low.md \
	Checklist_Template_Medium.md \
	Checklist_Template_High.md

TOP := ../../..

all: $(RST_TARGETS) $(CHECKLIST)
	trlc --verify ../steps.rsl .

%.rst: %.trlc
	$(TOP)/util/checklist_generator.py --min-priority ALL $<

Checklist_Template_%.md: $(wildcard *.trlc) $(wildcard *.rsl)
	$(TOP)/util/checklist_template_generator.py --min-priority $*
