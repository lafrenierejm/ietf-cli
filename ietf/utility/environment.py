#!/usr/bin/env python3
from xdg import BaseDirectory
import os
import sys


def get_app_dir(sub_dir='') -> str:
    """Return the path to the XDG dir or exit 1."""
    xdg_dir = BaseDirectory.save_data_path('ietf')
    want_dir = os.path.join(xdg_dir, sub_dir)
    # Ensure that the directory exists
    if not os.path.isdir(want_dir):
        print("'{}' is not a directory.  "
              "Run the `mirror` subcommand to create it."
              .format(want_dir))
        sys.exit(1)
    return want_dir


def get_db_path(no_warn=False) -> str:
    """Return the path to the database."""
    xdg_dir = BaseDirectory.save_data_path('ietf')
    db_path = os.path.join(xdg_dir, 'rfc-index.sqlite3')
    # Ensure that the file exists
    if (not os.path.isfile(db_path)) and (not no_warn):
        print("The database at '{}' does not exist.  "
              "Run the `mirror` subcommand to create it."
              .format(db_path))
        sys.exit(1)
    return db_path


def get_pager():
    """Return $PAGER if it exists or exit 2."""
    pager = os.environ.get('PAGER', -1)
    if isinstance(pager, int):
        print('No value for $PAGER found in environment. '
              'Export PAGER then rerun.')
        sys.exit(2)
    pager_cmd = pager.split()  # Split the returned string into a list
    return pager_cmd


def get_editor():
    """Return $EDITOR if it exists or exit 2."""
    editor = os.environ.get('EDITOR', -1)
    if isinstance(editor, int):
        print('No value for $EDITOR found in environment. '
              'Export EDITOR then rerun.')
        sys.exit(2)
    editor_cmd = editor.split()  # Split the returned string into a list
    return editor_cmd
