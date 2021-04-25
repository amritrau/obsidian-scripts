#!/usr/bin/env python3

"""
index.py
@amritrau

Usage: index.py VAULT
Options:
  --help            Show this message and exit.

In all subdirectories that contain at least one Markdown file, add an 
00000000-*.md file with outbound links to each file.
"""

import click
import frontmatter
import logging
import os
import pathlib

from constants import INDEX_PREFIX
from utils import slugify

logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument('vault')
def main(vault):
    # Collect a set of all directories with Markdown files
    filenames = list(pathlib.Path(vault).rglob("*.md"))
    directories = {filename.parent.absolute() for filename in filenames}
    n_indexes = 0

    for d in directories:
        # Retrieve each of the Markdown files in this directory
        filenames = sorted(
            filter(
                lambda f: not os.path.basename(f).startswith(INDEX_PREFIX), 
                d.glob("*.md")),
            reverse=True
        )

        if len(filenames) > 0:
            def make_entry(filename):
                # Construct the index entry
                basename = os.path.basename(filename)
                note = frontmatter.load(filename)
                title = note['title']
                return f"[[{basename}|{title}]]"
            
            # Collect index entries and add a heading
            entries = list(map(make_entry, filenames))
            dir_basename = os.path.basename(d)
            entries = [f"* {e}\n" for e in entries]  # f.writelines doesn't add \n
            entries = [f"# {dir_basename}\n"] + entries  # add H1

            # Overwrite the index file
            index_basename = f"{INDEX_PREFIX}-{slugify(dir_basename)}.md"
            with open(d / index_basename, 'w') as f:
                f.writelines(entries)
            n_indexes += 1

    logging.info(f"Created {n_indexes} indexes.")


if __name__ == "__main__":
    main()
