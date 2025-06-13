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
	$(TOP)/util/checklist-generator.py --min-priority ALL $<

Checklist_Template_%.md: $(wildcard *.trlc) $(wildcard *.rsl)
	$(TOP)/util/checklist-template-generator.py --min-priority $*
