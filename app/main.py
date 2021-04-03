#!/usr/bin/env python
import argparse


def start_mode():
    from webapi import create_app

    app = create_app()
    app.run(host='0.0.0.0', port='50000')


def accuracy_mode():
    # FIXME
    pass


if __name__ == '__main__':
    # options
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start',
                        help='start app',
                        action='store_true')
    parser.add_argument('-a', '--accuracy',
                        help='measure accuracy',
                        action='store_true')
    args = parser.parse_args()

    if args.start:
        start_mode()
    if args.accuracy:
        accuracy_mode()
