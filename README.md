# obsidian-scripts
Be sure to make a backup of your vault before attempting to run these scripts. This repository is unstable.

## Setup
1. Add this repository as a submodule at the top level of your Obsidian vault repository.
```bash
git submodule add git@github.com:amritrau/obsidian-scripts.git .bin
```

2. Copy `Makefile` into the root directory of your Obsidian vault repository.
```bash
cd .bin
cp Makefile path/to/vaults/root/Makefile
```

3. Install the necessary requirements. (Consider using a [virtualenv](https://docs.python.org/3/tutorial/venv.html).)
```bash
pip install -r requirements.txt
```

## Usage
From the root directory of your Obsidian vault repository, run
```bash
make
```
