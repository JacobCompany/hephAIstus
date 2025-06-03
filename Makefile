.PHONY: ruff

PYMODULE:=src

ruff:
	ruff check --fix $(PYMODULE)
	ruff format $(PYMODULE)