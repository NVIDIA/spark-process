RST_SOURCES := $(wildcard *.rst) $(wildcard process/*.rst)

generated: steps.rsl
	make -C checklist
	make -C tracing
	make -C switches

steps.rsl: $(RST_SOURCES)
	echo "package Steps" > $@
	echo "" >> $@
	echo "enum ID {" >> $@
	egrep -h "Step ID: (.+)" $^ | \
		sed "s/Step ID: /   /" | sort >> $@
	echo "   ALL" >> $@
	echo "   VARIOUS" >> $@
	echo "}" >> $@
