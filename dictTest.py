__author__ = 'ayanmukhopadhyay'
from itertools import cycle
import datetime
import numpy as np

testDictionary = {"ayan":[[1,2,3],[4]]}
testDictionary["ayan"][0].append(4)
testDictionary["ayan"][1].append(4)

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
print a

latency = np.empty((len()))
latency = [[1,2,3,4,5,6],[datetime.datetime(2009,1,1),datetime.datetime(2009,1,1),datetime.datetime(2009,1,1),datetime.datetime(2009,1,1),datetime.datetime(2009,1,1),datetime.datetime(2009,1,1)]]
latency = np.array(latency)
latencies = latency[np.argsort(latency[:,1])]