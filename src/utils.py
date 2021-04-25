#!/usr/bin/env python3

"""
utils.py
@amritrau

Holds global utilities.
"""

import datetime
import hashlib
import frontmatter
import pathlib
import re
import unicodedata


def slugify(value):
    """From StackOverflow #5574042"""
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def get_zk_prefix(filename: pathlib.Path, mode='ctime'):
    """Get an 8-digit Zettelkasten-style prefix from a filepath"""
    if mode == 'ctime':
        dt = filename.stat().st_ctime
    elif mode == 'mtime':
        dt = filename.stat().st_ctime
    else:
        raise ValueError(f"Mode not recognized: {mode}")

    return datetime.datetime.fromtimestamp(dt).strftime("%Y%m%d")


def hash_note(filename: pathlib.Path, n=12):
    """Get a unique n-hexdigit hash of the note's contents"""
    note = frontmatter.load(filename)
    sha = hashlib.sha256()
    sha.update(str(note.content).encode())
    sha.update(str(get_zk_prefix(filename)).encode())
    return str(sha.hexdigest())[:n]


def flush(note: frontmatter.Post, filename):
    """Write a modified note object back to a file"""
    with open(filename, 'w') as f:
        f.write(frontmatter.dumps(note))