#!/usr/bin/env python3
from ietf.utility.environment import (get_editor, get_file, get_pager)
from ietf.utility.query import (get_db_session, query_rfc,
                                query_rfc_by_updates, query_rfc_by_obsoletes,
                                query_rfc_by_is_also, query_rfc_by_see_also,)
from subprocess import run
import sys


def get_docs(args):
    """Get documents from the passed list and display them."""
    db_session = get_db_session()
    numbers = sort_preserve_order(args.number)  # Remove duplicate arguments
    docs = []
    dne = []
    if args.updates:
        for number in numbers:
            doc = query_rfc_by_updates(db_session, number)
            if doc is not None:
                docs.append(doc)
            else:
                dne.append("RFC {} does not exist.".format(number))
    elif args.obsoletes:
        for number in numbers:
            rfc = query_rfc_by_obsoletes(db_session, number)
            if rfc is not None:
                docs.append(rfc)
            else:
                dne.append("RFC {} does not exist.".format(number))
    elif args.is_also:
        for number in numbers:
            rfc = query_rfc(db_session, number)
            if rfc is None:
                dne.append("RFC {} does not exist.".format(number))
            else:
                aliases = query_rfc_by_is_also(db_session, number)
                docs.extend(aliases)
    elif args.see_also:
        for number in numbers:
            reference = query_rfc_by_see_also(db_session, number)
            if reference is not None:
                docs.append(reference)
            else:
                dne.append("RFC {} does not exist.".format(number))
    else:
        for number in numbers:
            rfc = query_rfc(db_session, number)
            if rfc is not None:
                docs.append(rfc)
            else:
                dne.append("RFC {} does not exist.".format(number))

    # Display found documents
    show_docs(sort_preserve_order(docs), args.editor, args.pager)
    # Display messages about nonexistent documents
    for msg in dne:
        print(msg)

    # Exit successfully
    sys.exit(0)


def sort_preserve_order(sequence):
    """Return a set with the original order of elements preserved.

    credit: https://www.peterbe.com/plog/uniqifiers-benchmark
    """
    seen = set()  # Create an empty set
    seen_add = seen.add  # Resolve once instead of per-iteration
    return [x for x in sequence if not (x in seen or seen_add(x))]


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
    """Create the parser for the `rfc` subcommand."""
    parser = parent_parser.add_parser(
        'rfc',
        help='view information about RFCs',
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

    # Add mutually exclusive group for lookups
    lookup_group = parser.add_mutually_exclusive_group()
    lookup_group.add_argument(
        '-u', '--updates',
        action='store_true',
        help='lookup documents that update the specified RFCs',
    )
    lookup_group.add_argument(
        '-o', '--obsoletes',
        action='store_true',
        help='lookup documents that obsolete the specified RFCs',
    )
    lookup_group.add_argument(
        '-i', '--is_also',
        action='store_true',
        help='lookup documents that are aliases for the specified RFCs',
    )
    lookup_group.add_argument(
        '-s', '--see_also',
        action='store_true',
        help='lookup documents referenced by the specified RFCs',
    )

    # Add RFC number as a required argument
    parser.add_argument(
        'number',
        type=int,
        nargs='+',  # 1 or more arguments
        help='RFC ID number',
    )

    # Pass arguments to `collect_ids()`
    parser.set_defaults(func=get_docs)
