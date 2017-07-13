#!/usr/bin/env python3
from ietf.sql.base import Base
from ietf.sql.rfc import Rfc
from ietf.utility.environment import get_app_dir, get_editor, get_pager
from ietf.utility.query import get_db_session, query_rfc_by_id
from subprocess import run
import argparse
import os
import sys
import typing


def view(args):
    """View the passed RFC numbers in args.number."""
    # Get the directory containing the RFCs
    rfc_dir = get_app_dir('rfc')
    # Get the command to use to view
    if args.editor:
        cmd = get_editor()
    else:
        cmd = get_pager()

    # Determine the validity of each passed number
    dne = []  # List to hold arguments lacking a corresponding file
    files = []  # List to hold files to view
    for number in args.number:
        # See if the specific RFC exists
        rfc_file = os.path.join(rfc_dir, 'rfc{}.txt'.format(number))
        if not os.path.isfile(rfc_file):
            dne.append(number)
        else:
            files.append(rfc_file)

    # Run pager_cmd on found files
    if files:  # Not empty
        cmd.extend(files)
        run(cmd)

    # Print a list of files not found
    if dne:  # Not empty
        print("No files were found for the following RFCs in '{}':"
              .format(rfc_dir))
        for number in dne:
            print(number)

    # Exit successfully
    sys.exit(0)


def print_meta(args):
    # Get a DB session
    session = get_db_session()
    # Query for the passed RFC numbers
    for number in args.number:
        row = query_rfc_by_id(session, number)
        if row is None:
            print("RFC {} does not exist.".format(number))
        else:
            print(row)
        print()

    # Exit successfully
    sys.exit(0)


def add_subparser(parent_parser: argparse._SubParsersAction):
    """Create the parser for the `rfc` subcommand."""
    parser = parent_parser.add_parser(
        'rfc',
        help='view information about RFCs',
    )
    subparsers = parser.add_subparsers(dest='rfc subcommand')
    subparsers.required = True

    # Add `view` parser
    view_parser = subparsers.add_parser(
        'view',
        help='open RFC for viewing',
    )
    view_parser.add_argument(
        '-e', '--editor',
        action='store_true',
        help='open RFCs in $EDITOR rather than $PAGER',
    )
    view_parser.add_argument(
        'number',
        type=int,
        nargs='+',  # 1 or more arguments
        help='RFC to view',
    )
    view_parser.set_defaults(func=view)

    # Add `meta` parser
    meta_parser = subparsers.add_parser(
        'meta',
        help='print RFC metadata',
    )
    meta_parser.add_argument(
        'number',
        type=int,
        nargs='+',  # 1 or more arguments
        help='RFC to view',
    )
    meta_parser.set_defaults(func=print_meta)
