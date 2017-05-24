#!/usr/bin/env python3
import argparse

cli_parser = argparse.ArgumentParser()
cli_subparsers = cli_parser.add_subparsers(help='sub-command help')

# Create the parser for the `mirror` command
cli_parser_mirror = cli_subparsers.add_parser('mirror',
                                              help='update a local mirror')
cli_parser_mirror.add_argument('-d', '--dir',
                               type=str,
                               nargs=1,
                               default=None,
                               help='directory to download to')
cli_parser_mirror.add_argument('-t', '--type',
                               type=str,
                               nargs='+',
                               choices=['draft',
                                        'iana',
                                        'iesg',
                                        'charter',
                                        'status',
                                        'rfc'],
                               default='everything',
                               help='type(s) of files to download')

cli_args = cli_parser.parse_args()
