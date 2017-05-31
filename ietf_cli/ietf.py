#!/usr/bin/env python3
import argparse
import os

from xdg import BaseDirectory


def mirror(args):
    # Define the URIs
    uri = {'draft': 'rsync.ietf.org::internet-drafts',
           'iana': 'rsync.ietf.org::everything-ftp/iana/',
           'iesg': 'rsync.ietf.org::iesg-minutes/',
           'charter': 'ietf.org::everything-ftp/ietf/',
           'conflict': 'rsync.ietf.org::everything-ftp/conflict-reviews/',
           'status': 'rsync.ietf.org::everything-ftp/status-changes/',
           'rfc': 'ftp.rfc-editor.org::everything-ftp/in-notes/'}

    # Set the top-level mirror directory
    if args.dir is not None:
        mirror_dir = args.dir[0]
    else:
        mirror_dir = BaseDirectory.save_data_path('ietf-cli')

    if os.access(mirror_dir, os.W_OK | os.X_OK):
        print('{} is writable'.format(mirror_dir))
    else:
        print('{} is not writable'.format(mirror_dir))


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
