#!/usr/bin/env python3
import argparse
import os

from xdg import BaseDirectory


def mirror(args):
    # The URIs for the document types
    uris = {'charter': 'ietf.org::everything-ftp/ietf/',
            'conflict': 'rsync.ietf.org::everything-ftp/conflict-reviews/',
            'draft': 'rsync.ietf.org::internet-drafts',
            'iana': 'rsync.ietf.org::everything-ftp/iana/',
            'iesg': 'rsync.ietf.org::iesg-minutes/',
            'rfc': 'ftp.rfc-editor.org::everything-ftp/in-notes/',
            'status': 'rsync.ietf.org::everything-ftp/status-changes/'}
    # Strings to be passed to rsync as arguments to `--exclude`
    excludes = {'charter': [],
                'conflict': [],
                'draft': ['*.xml', '*.pdf'],
                'iana': [],
                'iesg': [],
                'rfc': ['tar*', 'search*', 'PDF-RFC*', 'tst/', 'pdfrfc/',
                        'internet-drafts/', 'ien/'],
                'status': []}

    # Set the top-level mirror directory
    if args.dir is not None:
        top_dir = args.dir[0]
    else:
        top_dir = BaseDirectory.save_data_path('ietf-cli')
    # Attempt to create directory
    try:
        os.mkdir(top_dir)
    except FileExistsError:
        pass  # Directory already exists


def main():
    cli_parser = argparse.ArgumentParser()
    cli_subparsers = cli_parser.add_subparsers(dest='subcommand',
                                               help='subcommand help')
    cli_subparsers.required = True  # Require a subcommand

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


if __name__ == '__main__':
    main()
