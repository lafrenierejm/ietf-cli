#!/usr/bin/env python3
import argparse
import os

from mirror import mirror
from xdg import BaseDirectory


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand',
                                       help='subcommand help')
    subparsers.required = True  # Require a subcommand

    # Create the parser for the mirror subcommand
    parser_mirror = subparsers.add_parser(
        'mirror',
        help='update a local mirror')
    parser_mirror.add_argument(
        '-d', '--dir',
        type=str,
        nargs=1,  # exactly 1 argument
        default=BaseDirectory.save_data_path('ietf-cli'),
        help='top-level destination of local mirror')
    parser_mirror.add_argument(
        '--flat',
        action='store_true',
        help='do not create a subdirectory for each document type')
    parser_mirror.add_argument(
        '-t', '--type',
        type=str,
        nargs='+',  # 1 or more arguments
        choices=['draft',
                 'iana',
                 'iesg',
                 'charter',
                 'conflict',
                 'status',
                 'rfc'],
        default=None,
        help='type of documents to download')
    parser_mirror.set_defaults(func=mirror)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
