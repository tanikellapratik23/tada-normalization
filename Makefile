PYTHON ?= python3
.PHONY: demo test fixtures validate
fixtures:
	$(PYTHON) -m tada generate
validate:
	$(PYTHON) -m tada validate fixtures/synthetic.json
test:
	$(PYTHON) -m unittest discover -s tests -v
demo:
	$(PYTHON) -m tada ingest fixtures/synthetic.json
	$(PYTHON) -m tada serve
