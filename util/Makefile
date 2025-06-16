.PHONY: lint style

lint: style
	@python3 -m pylint --rcfile=pylint3.cfg \
		--reports=no \
		*.py

style:
	@python3 -m pycodestyle *.py
