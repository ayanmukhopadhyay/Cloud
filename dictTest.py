__author__ = 'ayanmukhopadhyay'
from itertools import cycle

testDictionary = {"ayan":[1,2,3]}
testDictionary["ayan"].append(4)
print testDictionary

list = [1,2,3]
a = cycle(list)
print next(a)
print next(a)
print next(a)
list.append(4)
print next(a)
print next(a)
print next(a)
print next(a)