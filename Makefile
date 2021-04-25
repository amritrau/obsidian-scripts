.PHONY: index
.PHONY: alias
.PHONY: rename

PY=python
BIN=.bin

index: alias
	$(PY) $(BIN)/src/index.py $(VAULT)

alias: rename
	$(PY) $(BIN)/src/alias.py --overwrite $(VAULT)

rename: 
	$(PY) $(BIN)/src/rename.py $(VAULT)
