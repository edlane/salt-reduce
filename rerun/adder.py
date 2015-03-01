# -*- coding: utf-8 -*-
'''
Module for demonstating salt-reduce
'''

# Import Python libs
import os
import sys
import time
import traceback
import random

# Import Salt libs
import salt
import salt.version
import salt.loader

# __proxyenabled__ = ['*']

from resource import getrusage as resource_usage, RUSAGE_SELF
from time import time as timestamp

try:
    # ...a hack used to ignore this class when used as a salt
    # execution module
    # TODO: implement this using decorator:
    # http://docs.saltstack.com/en/latest/ref/modules/#useful-decorators-for-modules
    #
    from lib.mapper import *

    class _mapper(mapper):

        sum = 0
        times = {}

        def __init__(self, module_name=None):
            if module_name == 'adder.add':
                # redirect "map" method to "partial_result"
                self.module_name = 'adder.partial_result'
            # self.module_name = module_name

        class partializer():
            part_size = 10000000

            def __init__(self, upper):
                self.upper = int(upper[0]) # need to cast this to int because "salt-call" does not
                self.x = 0

            def next(self):
                ret = self.x
                if ret >= self.upper:
                    raise StopIteration
                remainder = self.upper - ret
                if remainder >= self.part_size:
                    remainder = self.part_size
                self.x += remainder
                return [ret, remainder]

        def reducer(self, n):
            self.sum += n[0]
            for k, v in n[1].iteritems():
                try:
                    self.times[k] += v
                except KeyError:
                    self.times[k] = 0

            return self.sum

        def statit(self):
            return self.sum, self.times

except:
    pass



def sum_nums(upper):
    '''
    Return the sum of the sequence of numbers from 1 to [upper], and the
    time it took to compute in seconds. Useful for validating the mapreduce runner

    CLI Example:

    .. code-block:: bash

        salt '*' mapit.sum_nums 10

    '''

    upper = int(upper)
    start = time.time()
    num = 0
    sum = 0

    while num < upper:
        num += 1
        sum += num
    print "sum = " + str(sum)
    return sum


def partial_result(lower, count):
    '''
    Return the sum of the sequence of numbers in the range [lower, upper], and the
    time it took to compute in seconds. Useful for validating the mapreduce runner

    CLI Example:

    .. code-block:: bash

        salt '*' mapit.sum_nums_partial 10 20

    '''
    start_time, start_resources = timestamp(), resource_usage(RUSAGE_SELF)
    lower = int(lower)
    num = lower
    sum = num

    for a in xrange(0, count-1):
        num += 1
        sum += num

    end_resources, end_time = resource_usage(RUSAGE_SELF), timestamp()

    return sum, {'real': end_time - start_time,
                 'sys': end_resources.ru_stime - start_resources.ru_stime,
                 'user': end_resources.ru_utime - start_resources.ru_utime}



