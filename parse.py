#!/usr/bin/env python
from pyparsing import *
tests = '''
m[mi++]="06.01.13 12:05:00|2489;2602;7093;52;10|2309;2407;5625;52;11|893;33;-2;0.8;2726"
m[mi++]="06.01.13 12:00:00|2502;2617;6881;52;10|2323;2418;5428;52;11|897;33;-3;0.0;2653"
m[mi++]="06.01.13 11:55:00|2329;2433;6672;52;10|2148;2254;5233;52;11|836;33;-2;0.0;2581"
m[mi++]="06.01.13 11:50:00|2501;2620;6474;52;9|2326;2418;5050;52;10|908;33;-3;0.5;2514"
m[mi++]="06.01.13 11:45:00|2468;2571;6261;52;9|2262;2350;4853;52;10|892;30;-3;0.4;2440"'''.splitlines()

tests.remove('')

print tests

point = Literal(".")
#num = Optional(point + Word(nums))

# +6.7 or -89.678 or 5 or 892892
num = Combine(Word("+-" + nums, nums) + Optional(point + Optional(Word(nums))))

delimiter = oneOf(". : ; |")

start_trash = Suppress(Literal("m[mi++]="))
quote = Suppress(Literal("\""))
date = num + '.' + num + '.' + num
time = num + ':' + num + ':' + num
delimiter = Suppress(Literal("|"))
inv1 = num + ';' + num + ';' + num + ';' + num + ';' + num
inv2 = num + ';' + num + ';' + num + ';' + num + ';' + num
# Plan for possible negative temperatures
env = num + ';' + num + ';' + Optional('-') + num + ';' + num + ';' + num

interval = start_trash + quote + date + time + delimiter + inv1 + delimiter + \
    inv2 + delimiter + env + quote

for test in tests:
    stats = interval.parseString(test)
    print stats.asList()
