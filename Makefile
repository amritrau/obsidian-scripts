.PHONY: alias

PY=python
BIN=.bin
VAULT=amritrau

index: alias
	$(PY) $(BIN)/index.py $(VAULT)

alias:
	$(PY) $(BIN)/alias.py --overwrite $(VAULT)
