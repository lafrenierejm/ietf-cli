#!/usr/bin/env python3


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
