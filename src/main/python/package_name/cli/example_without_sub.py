import argparse
import sys
import cmd

example_without_sub_parser = argparse.ArgumentParser()
@cmd(example_without_sub_parser)
def _execute(args):
    """example without subcommand"""
    print "example without subcommand"
