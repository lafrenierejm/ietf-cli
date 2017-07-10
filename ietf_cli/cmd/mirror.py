#!/usr/bin/env python3
import os
import argparse
import typing
from typing import List, Tuple

from xdg import BaseDirectory
from subprocess import Popen

__URI_DICT__ = {'charter': 'ietf.org::everything-ftp/ietf/',
                'conflict': 'rsync.ietf.org::everything-ftp/conflict-reviews/',
                'draft': 'rsync.ietf.org::internet-drafts',
                'iana': 'rsync.ietf.org::everything-ftp/iana/',
                'iesg': 'rsync.ietf.org::iesg-minutes/',
                'rfc': 'ftp.rfc-editor.org::everything-ftp/in-notes/',
                'status': 'rsync.ietf.org::everything-ftp/status-changes/'}

__EXCLUDE_DICT__ = {'charter': [],
                    'conflict': [],
                    'draft': ['*.xml', '*.pdf'],
                    'iana': [],
                    'iesg': [],
                    'rfc': ['tar*', 'search*', 'PDF-RFC*', 'tst/', 'pdfrfc/',
                            'internet-drafts/', 'ien/'],
                    'status': []}


def _expand_path(path: int) -> str:
    return os.path.expandvars(os.path.expanduser(path))


def _create_dir(path: str):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


RsyncInfo = Tuple[List[str], str]
def assemble_rsync(doc_type: str, top_dir: int, flat: bool) -> RsyncInfo:
    # Add the rsync boilerplate
    command = ['rsync', '-az', '--delete-during']

    # Add any relevant `--exclude` strings
    for exclude in __EXCLUDE_DICT__[doc_type]:
        command.append("--exclude='{}'".format(exclude))

    # Add the type's corresponding URI
    command.append(__URI_DICT__[doc_type])

    # Specify the output directory
    if not flat:
        dest_dir = top_dir + '/' + doc_type
    else:
        dest_dir = top_dir
    command.append(dest_dir)

    return command, dest_dir


def mirror(args):
    # Set the top-level mirror directory
    top_dir = _expand_path(args.dir[0])
    # Attempt to create directory
    _create_dir(top_dir)

    # Dictionary to hold the commands
    commands = {}
    # No document type passed as an argument
    if args.type is None:
        for doc_type, _ in __URI_DICT__.items():
            commands[doc_type], dest_dir = assemble_rsync(
                doc_type, top_dir, args.flat)
            _create_dir(dest_dir)
    # One or multiple document types passed as arguments
    else:
        for doc_type in args.type:
            commands[doc_type], dest_dir = assemble_rsync(
                doc_type, top_dir, args.flat)
            _create_dir(dest_dir)

    # List to hold the spawned processes' IDs
    processes = []
    for doc_type, command in commands.items():
        # Start the rsync process and add its PID to processes
        process = Popen(command)
        processes.append(process)

    # Wait for each rsync process to complete
    exitcodes = [p.wait() for p in processes]


def add_subparser(subparsers: argparse._SubParsersAction):
    """Create the parser for the `mirror` subcommand."""
    parser = subparsers.add_parser(
        'mirror',
        help='update a local mirror')
    parser.add_argument(
        '-d', '--dir',
        type=str,
        nargs=1,  # exactly 1 argument
        default=BaseDirectory.save_data_path('ietf-cli'),
        help='top-level destination of local mirror')
    parser.add_argument(
        '--flat',
        action='store_true',
        help='do not create a subdirectory for invidivual document types')
    parser.add_argument(
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
    parser.set_defaults(func=mirror)
