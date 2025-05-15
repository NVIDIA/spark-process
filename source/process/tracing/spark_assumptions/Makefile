TOP := ../../../..
TRLC_VERIFY := --verify $(if $(OS),--use-cvc5-binary $(TOP)/cvc5.exe)

all:
	trlc $(TRLC_VERIFY) ../../steps.rsl .
	$(TOP)/util/assumption-tracing.py --source-dir=../../
