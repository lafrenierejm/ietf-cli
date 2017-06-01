#!/usr/bin/env python3
import argparse
import os

from xdg import BaseDirectory
from subprocess import Popen


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
        top_dir = os.path.expandvars(os.path.expanduser(args.dir[0]))
    else:
        top_dir = BaseDirectory.save_data_path('ietf-cli')
    top_dir = os.path.abspath(top_dir)
    # Attempt to create directory
    try:
        os.makedirs(top_dir)
    except FileExistsError:
        pass  # Directory already exists

    # Run rsync with no document type passed as an argument
    if args.type is None:
        # Generate a dict of command arrays from the above dicts
        commands = {}
        for doc_type, uri in uris.items():
            command = ['rsync', '-az', '--delete-during']
            for exclude in excludes[doc_type]:
                command.append("--exclude='{}'".format(exclude))
            command.append('{}'.format(uri))
            command.append('{}'.format(top_dir + '/' + doc_type))
            print(command)
            commands[doc_type] = command
        processes = []
        for doc_type, command in commands.items():
            # Create subdirectory for the document type
            try:
                os.makedirs(top_dir + '/' + doc_type)
            except FileExistsError:  # Directory already exists
                pass
            # Start the rsync process and add its PID to processes
            process = Popen(command)
            processes.append(process)
        # Wait for each rsync process to complete
        exitcodes = [p.wait() for p in processes]
    # rsync only the specified document type
    else:
        command = ['rsync', '-az', '--delete-during']
        for exclude in excludes[args.type[0]]:
            command.append("--exclude='{}'".format(exclude))
        command.append('{}'.format(uris[args.type[0]]))
        command.append('{}'.format(top_dir))
        print(command)
        process = Popen(command)
        process.wait()


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
        default=None,
        help='manually specify a directory to download to')
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
