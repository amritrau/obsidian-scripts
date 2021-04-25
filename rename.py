#!/usr/bin/env python3

"""
rename.py
@amritrau

Usage: rename.py VAULT
Options:
  --help            Show this message and exit.

Rename all Markdown files that don't follow the `YYYYMMDD-note-title.md`
naming convention. Do not modify filenames that already match the pattern
(even if their title is out of date).
"""

import click
import frontmatter
import logging
import os
import pathlib
import re

from constants import INDEX_PREFIX
from utils import slugify, get_zk_prefix, hash_note, flush

logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument('vault')
def main(vault):
    filenames = list(pathlib.Path(vault).rglob("*.md"))
    n_files, n_renamed = len(filenames), 0
    pattern = r"^\d{8}-(.*)\.md$"  # YYYYMMDD-note-title.md

    for filename in filenames:
        basename = os.path.basename(filename)
        if not re.match(pattern, basename):
            prefix = get_zk_prefix(filename)
            
            # Extract the title from the first line of the file
            note = frontmatter.load(filename)
            heading = note.content.split('\n')[0]
            match = re.match(r"^# (.*)$", heading)
            if match:
                slug = slugify(match.group(1))
            else:
                # Generate a unique title based on the note's contents
                slug = f"untitled-{hash_note(filename)}"

                # Add a heading to the top of the file and write back
                lines = note.content.split('\n').insert(0, f"# {slug}\n")
                note.content = '\n'.join(lines)
                flush(note, filename)
            
            new_name = f"{prefix}-{slug}.md"
            
            # Rename file
            new_filename = str(filename).replace(basename, new_name)
            os.rename(filename, new_filename)
            n_renamed +=1

    logging.info(f"Renamed {n_renamed} of {n_files} files.")


if __name__ == "__main__":
    main()
