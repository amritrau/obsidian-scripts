.PHONY: index
.PHONY: alias
.PHONY: rename

PY=python
BIN=.bin

index: alias
	$(PY) $(BIN)/index.py $(VAULT)

alias: rename
	$(PY) $(BIN)/alias.py --overwrite $(VAULT)

rename: 
	$(PY) $(BIN)/rename.py $(VAULT)
