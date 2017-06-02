#!/usr/bin/env python3
import os

import typing
from typing import List

from xdg import BaseDirectory
from subprocess import Popen

URI_DICT = {'charter': 'ietf.org::everything-ftp/ietf/',
            'conflict': 'rsync.ietf.org::everything-ftp/conflict-reviews/',
            'draft': 'rsync.ietf.org::internet-drafts',
            'iana': 'rsync.ietf.org::everything-ftp/iana/',
            'iesg': 'rsync.ietf.org::iesg-minutes/',
            'rfc': 'ftp.rfc-editor.org::everything-ftp/in-notes/',
            'status': 'rsync.ietf.org::everything-ftp/status-changes/'}

EXCLUDE_DICT = {'charter': [],
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


def assemble_rsync(doc_type: str, top_dir: int, flat: bool) -> List[str]:
    # Add the rsync boilerplate
    command = ['rsync', '-az', '--delete-during']

    # Add any relevant `--exclude` strings
    for exclude in EXCLUDE_DICT[doc_type]:
        command.append("--exclude='{}'".format(exclude))

    # Add the type's corresponding URI
    command.append(URI_DICT[doc_type])

    # Specify the output directory
    if not flat:
        dest_dir = top_dir + '/' + doc_type
        _create_dir(dest_dir)
        command.append(dest_dir)
    else:
        command.append(top_dir)

    return command


def mirror(args):
    # Set the top-level mirror directory
    top_dir = _expand_path(args.dir[0])
    # Attempt to create directory
    _create_dir(top_dir)

    # Dictionary to hold the commands
    commands = {}
    # No document type passed as an argument
    if args.type is None:
        for doc_type, _ in URI_DICT.items():
            commands[doc_type] = assemble_rsync(doc_type, top_dir, args.flat)
    # One or multiple document types passed as arguments
    else:
        for doc_type in args.type:
            commands[doc_type] = assemble_rsync(doc_type, top_dir, args.flat)

    # List to hold the spawned processes' IDs
    processes = []
    for doc_type, command in commands.items():
        # Start the rsync process and add its PID to processes
        process = Popen(command)
        processes.append(process)

    # Wait for each rsync process to complete
    exitcodes = [p.wait() for p in processes]
