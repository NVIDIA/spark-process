RST_SOURCES := $(shell find .. -name "*.rst")
RST_TARGETS := $(addsuffix .rst, $(basename $(wildcard *.trlc)))

TOP := ../../..

all: $(RST_TARGETS)
	trlc --verify ../steps.rsl .

%.rst: %.trlc
	$(TOP)/util/checklist-generator.py $<
