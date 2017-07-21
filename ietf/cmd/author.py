#!/usr/bin/env python3
from ietf.sql.rfc import Rfc
from ietf.utility.environment import (get_editor, get_file, get_pager)
from ietf.utility.query_author import (query_author_by_name,
                                       query_author_by_title)
from ietf.utility.query_doc import (get_db_session)
from subprocess import run
import sys


def get_rfcs(args):
    """Get RFCs written by the passed authors."""
    # Create an all-inclusive query to intersect with
    Session = get_db_session()
    query = Session.query(Rfc)
    # Add argument queries
    if args.name:
        query = query.intersect(query_author_by_name(Session, args.name))
    if args.title:
        query = query.intersect(query_author_by_title(Session, args.title))
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
    """Create the parser for the `author` subcommand."""
    parser = parent_parser.add_parser(
        'author',
        help='query RFCs by author',
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

    # Query by authors' names
    parser.add_argument(
        '-n', '--name',
        type=str,
        nargs='+',
        help='query by author.name',
    )

    # Query by authors' titles
    parser.add_argument(
        '-t', '--title',
        type=str,
        nargs='+',
        metavar=('TITLE'),
        help='query by author.title',
    )

    # Pass arguments to `get_rfcs()`
    parser.set_defaults(func=get_rfcs)
