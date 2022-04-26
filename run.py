#!/usr/bin/python

import sys

sys.path.insert(0, "src/")


from subs_src import get_subs
from get_subs import GetSub


def main(args):
    if len(args) != 2:
        sys.exit("usage: 'Give video file as input' 'specify language'")

    gs = GetSub(3, 30, 300)
    gs.download(args[0], args[1])


if __name__ == "__main__":

    main(sys.argv[1:])
