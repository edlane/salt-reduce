# -*- coding: utf-8 -*-
'''
Module for running arbitrary tests
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

__proxyenabled__ = ['*']

try:
    # ...a hack used to ignore this class when used as a salt
    # execution module
    # TODO: implement this using decorator:
    # http://docs.saltstack.com/en/latest/ref/modules/#useful-decorators-for-modules
    #
    from mylib.mapper import *

    class _mapper(mapper):

        sum = 0

        class partializer():
            part_size = 100000

            def __init__(self, upper):
                self.upper = upper[0]
                self.x = 0

            def next(self):
                ret = self.x
                if ret >= self.upper:
                    raise StopIteration
                remain = self.upper - ret
                if remain >= self.part_size:
                    remain = self.part_size
                self.x += remain
                return [ret, remain]


        def reducer(self, n):
            self.sum += n
            return self.sum

        def statit(self):
            return self.sum

except:
    pass


def echo(*args):
    # return args
    return 5000


def fib(num):
    '''
    Return a Fibonacci sequence up to the passed number, and the
    timeit took to compute in seconds. Used for performance tests

    CLI Example:

    .. code-block:: bash

        salt '*' test.fib 3
    '''
    num = int(num)
    start = time.time()
    fib_a, fib_b = 0, 1
    ret = [0]
    while fib_b < num:
        ret.append(fib_b)
        fib_a, fib_b = fib_b, fib_a + fib_b
    return ret, time.time() - start


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
    lower = int(lower)
    num = lower
    sum = num

    for a in xrange(0, count-1):
        num += 1
        sum += num

    return sum

def sleep20(*args):
    '''
    Instruct the minion to initiate a process that will sleep for a given
    period of time.

    CLI Example:

    .. code-block:: bash

        salt '*' mapit.sleep20 1 2
    '''
    time.sleep(20)
    return 20


