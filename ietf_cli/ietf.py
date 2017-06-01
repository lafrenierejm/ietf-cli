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

    # Create the parser for the `mirror` command
    parser_mirror = subparsers.add_parser(
        'mirror',
        help='update a local mirror')
    parser_mirror.add_argument(
        '-d', '--dir',
        type=str,
        nargs=1,  # exactly 1 argument
        default=BaseDirectory.save_data_path('ietf-cli'),
        help='where to download local mirror')
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
        help='type(s) of files to download')
    parser_mirror.set_defaults(func=mirror)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
