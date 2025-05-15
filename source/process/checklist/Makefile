RST_SOURCES := $(shell find .. -name "*.rst")
RST_TARGETS := $(addsuffix .rst, $(basename $(wildcard *.trlc)))

TOP := ../../..

TRLC_VERIFY := --verify $(if $(OS),--use-cvc5-binary $(TOP)/cvc5.exe)

all: $(RST_TARGETS)
	trlc $(TRLC_VERIFY) ../steps.rsl .

%.rst: %.trlc
	$(TOP)/util/checklist-generator.py $<
