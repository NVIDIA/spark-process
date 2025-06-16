RSL_FILES = $(wildcard *.rsl) ../../steps.rsl
TRLC_FILES = $(wildcard *.trlc)
INC_TARGETS := $(addsuffix .inc, $(basename $(TRLC_FILES)))
TOP := ../../../..

all: $(INC_TARGETS)
	trlc --verify ../../steps.rsl .
	cat *.sections | sort | uniq > all_sections.txt

%.inc: %.trlc $(RSL_FILES)
	$(TOP)/util/iso_tracing.py $^ --out $@
