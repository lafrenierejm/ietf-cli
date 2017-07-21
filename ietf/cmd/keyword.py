#!/usr/bin/env python3
from ietf.sql.rfc import Rfc
from ietf.utility.environment import (
    get_db_session,
    get_editor,
    get_file,
    get_pager,
)
from ietf.utility.query_keyword import query_rfc_by_keyword
from subprocess import run
import sys


def get_rfcs(args):
    """Get RFCs containing passed keywords."""
    # Create an all-inclusive query to intersect with
    Session = get_db_session()
    # Add argument queries
    query = query_rfc_by_keyword(Session, args.keyword)
    # Run the assembled query
    rfcs = query.order_by(Rfc.id).all()
    show_docs(rfcs, args.editor, args.pager)  # Display found documents
    # Exit successfully
    sys.exit(0)


def show_docs(docs, edit, page):
    """Display the passed documents."""
    # Get the command to run (if any)
    if edit:
        cmd = get_editor()
    elif page:
        cmd = get_pager()
    # Run `cmd` on the passed docs if `cmd` exists.
    if 'cmd' in vars():
        added_to_cmd = False  # To see if any files actually exist
        for doc in docs:
            file_path = get_file(doc)  # Get the doc's plaintext file
            if file_path:
                added_to_cmd = True  # We have a reason to run `cmd`
                cmd.append(file_path)  # Add the path as an argument to `cmd`
        if added_to_cmd:
            run(cmd)  # Block while running external process
    # Otherwise print to stdout
    else:
        for doc in docs:
            print(doc)
            print()  # newline


def add_subparser(parent_parser):
    """Create the parser for the `keyword` subcommand."""
    parser = parent_parser.add_parser(
        'keyword',
        help='query RFCs by keyword',
    )

    # Add mutually exclusive group for pager and editor
    view_group = parser.add_mutually_exclusive_group()
    view_group.add_argument(
        '-e', '--editor',
        action='store_true',
        help='open RFC files in $EDITOR',
    )
    view_group.add_argument(
        '-p', '--pager',
        action='store_true',
        help='open RFC files in $PAGER',
    )

    # Required keyword argument
    parser.add_argument(
        'keyword',
        type=str,
        nargs='+',
        help='keyword to query',
    )

    # Pass arguments to `get_rfcs()`
    parser.set_defaults(func=get_rfcs)
