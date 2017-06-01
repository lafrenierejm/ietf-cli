#!/usr/bin/env python3
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
    top_dir = os.path.abspath(
        os.path.expandvars(
            os.path.expanduser(
                args.dir[0])))
    # Attempt to create directory
    try:
        os.makedirs(top_dir)
    except FileExistsError:
        pass  # Directory already exists

    # No document type passed as an argument
    if args.type is None:
        # Generate a dict of command arrays from the above dicts
        commands = {}
        for doc_type, uri in uris.items():
            command = ['rsync', '-az', '--delete-during']
            for exclude in excludes[doc_type]:
                command.append("--exclude='{}'".format(exclude))
            command.append(uri)
            command.append(top_dir + '/' + doc_type)
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
    # One or multiple document types passed as arguments
    else:
        # Generate a dict of command arrays
        commands = {}
        for doc_type in args.type:
            command = ['rsync', '-az', '--delete-during']
            for exclude in excludes[doc_type]:
                command.append("--exclude='{}'".format(exclude))
            command.append(uris[doc_type])
            command.append(top_dir + '/' + doc_type)
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
