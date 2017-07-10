#!/usr/bin/env python3
import argparse
import cmd.mirror as mirror


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand',
                                       help='subcommand help')
    subparsers.required = True  # Require a subcommand
    mirror.add_subparser(subparsers)  # Add parser for `mirror` subcommand
    args = parser.parse_args()  # Parse the supplied arguments
    args.func(args)  # Run the specified (sub)command


if __name__ == '__main__':
    main()
