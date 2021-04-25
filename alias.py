#!/usr/bin/env python3

"""
alias.py
@amritrau

Usage: alias.py [OPTIONS] VAULT
Options:
  --overwrite TEXT  Overwrite existing aliases.  [default: False]
  --help            Show this message and exit.

Sets the top-level heading as the note's `title` and `alias` in its YAML front 
matter.
"""

import click
import frontmatter
import logging
import os
import pathlib
import re

from constants import INDEX_PREFIX

logging.basicConfig(level=logging.INFO)


def flush(note, filename):
    with open(filename, 'w') as f:
        f.write(frontmatter.dumps(note))


@click.command()
@click.option('--overwrite/--no-overwrite', help='Overwrite existing aliases.',
                default=False, show_default=True)
@click.argument('vault')
def main(overwrite, vault):
    filenames = list(filter(
        lambda f: not os.path.basename(f).startswith(INDEX_PREFIX),
        pathlib.Path(vault).rglob("*.md")
    ))
    n_files, n_modified = len(filenames), 0

    for filename in filenames:
        logging.debug(f"Processing {filename}")
    
        # Extract the first line of the file
        note = frontmatter.load(filename)
        heading = note.content.split('\n')[0]

        # Ensure that it's a top-level heading
        match = re.match(r"^# (.*)$", heading)
        if match:
            # Always update title attribute
            note['title'] = match.group(1)
            flush(note, filename)

            # Add to existing aliases if requested
            aliases = [match.group(1)]
            existing = note.get('aliases', [])
            if not overwrite:
                if existing and isinstance(existing, list):
                    aliases += existing

            # Only write back if we changed something
            if len(set(aliases) & set(existing)) != len(set(aliases)) or \
                len(set(aliases)) != len(set(existing)):
                new_aliases = list(set(aliases))
                logging.debug(f"Setting aliases {new_aliases}")
                note['aliases'] = new_aliases
                flush(note, filename)
                n_modified += 1

    logging.info(f"Updated aliases for {n_modified} of {n_files} files.")

if __name__ == "__main__":
    main()
