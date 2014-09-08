#!/usr/bin/env python
from pyparsing import Combine, Literal, Optional, Suppress, Word, nums
from pyparsing import *
import argparse
import datetime


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
    #print logs

    # Only whole number strings
    #num = Word(nums).setParseAction(lambda t:int(t[0]))
    #num = Word(nums).setParseAction( lambda s,l,t: [ int(t[0]) ] )
    num = Word(nums)
    # Float number - +6.7 or -89.678 or 5 or 892892
    point = Literal(".")
    fnum = Combine(Word("+-" + nums, nums) +
                   Optional(point + Optional(Word(nums))))

    start_trash = Suppress(Literal("m[mi++]="))
    quote = Suppress(Literal("\""))
    dot = Suppress(Literal("."))
    colon = Suppress(Literal(":"))
    #date = num + dot + num + dot + num
    day = num
    month = num
    year = num
    hour = num
    min = num
    sec = num
    #timestamp = datetime.datetime(year, month, day, hour, min, sec)

    date = day.setResultsName("day") + dot + month + dot + year.setResultsName("year")
    time = hour + colon + min + colon + sec
    delimiter = Suppress(Literal("|"))
    inv1 = num + ';' + num + ';' + num + ';' + num + ';' + num
    inv2 = num + ';' + num + ';' + num + ';' + num + ';' + num
    # Plan for possible negative temperatures
    env = num + ';' + num + ';' + fnum + ';' + fnum + ';' + num

    interval = (start_trash + quote +  date + time + delimiter + inv1 +
                delimiter + inv2 + delimiter + env + quote)

    for log in logs:
        stats = interval.parseString(log)
        #timestamp = datetime.datetime(int(year))
        print "Year: " + stats.year
        print "Timestamp: " + datetime.datetime(int(stats.year), \
                                                int(stats.month), \
                                                int()
        #print stats.asList()


if __name__ == "__main__":
    main()
