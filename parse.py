#!/usr/bin/env python
from pyparsing import Combine, Literal, Optional, Suppress, Word, nums
import argparse


def main():
    parser = argparse.ArgumentParser(description='Parse data from the Solar\
                                     Log JS log files')
    parser.add_argument('logfile', help='A single Solar Log log file')
    args = parser.parse_args()
    logfile = args.logfile

    # Parse logfile into a list
    with open(logfile) as f:
        logs = f.readlines()

    # Debug
    print logs

    # Only whole number strings
    num = Word(nums)
    # Float number - +6.7 or -89.678 or 5 or 892892
    point = Literal(".")
    fnum = Combine(Word("+-" + nums, nums) +
                   Optional(point + Optional(Word(nums))))

    start_trash = Suppress(Literal("m[mi++]="))
    quote = Suppress(Literal("\""))
    date = num + '.' + num + '.' + num
    time = num + ':' + num + ':' + num
    delimiter = Suppress(Literal("|"))
    inv1 = num + ';' + num + ';' + num + ';' + num + ';' + num
    inv2 = num + ';' + num + ';' + num + ';' + num + ';' + num
    # Plan for possible negative temperatures
    env = num + ';' + num + ';' + fnum + ';' + fnum + ';' + num

    interval = (start_trash + quote + date + time + delimiter + inv1 +
                delimiter + inv2 + delimiter + env + quote)

    for log in logs:
        stats = interval.parseString(log)
        print stats.asList()


if __name__ == "__main__":
    main()
