import argparse
import cmd

example_parser = argparse.ArgumentParser()
example_parser.add_argument('date', type=str, help='YYYYMMDD')
example_parser.add_argument('data', type=str, nargs='+', help='plain texts')
example_parser.add_argument('--max', default='999999', type=str, help='maximum data range to list keys')
example_parser.add_argument('id', type=int, help='integer id')
example_parser.add_argument('-b', '--bits', type=int, default=512, help='[int]')
example_parser.add_argument('-p', '--phone', action='store_true', help='Message or PhoneNumber')
@cmd(example_parser)
def example(args): # TODO args list print
    """example message"""
    print args.date
    print args.data
    print args.max
    print args.id
    print args.bits
    print args.phone

