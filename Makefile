.PHONY: index
.PHONY: alias

PY=python
BIN=.bin

index: alias
	$(PY) $(BIN)/index.py $(VAULT)

alias:
	$(PY) $(BIN)/alias.py --overwrite $(VAULT)
