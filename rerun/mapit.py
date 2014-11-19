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

class testme():

    sum = 0
    iterit = None

    def iterateit(self):
        iterit = iter(xrange(0, 10, 2))
        return iterit

    def reduceit(self, n):
        self.sum += n
        return self.sum

    def statit(self):
        print "sum = " + self.sum


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
    return sum, time.time() - start


def sum_nums_partial(lower, upper):
    '''
    Return the sum of the sequence of numbers in the range [lower, upper], and the
    time it took to compute in seconds. Useful for validating the mapreduce runner

    CLI Example:

    .. code-block:: bash

        salt '*' mapreduce.sum_nums_partial 10 20

    '''
    lower = int(lower)
    upper = int(upper)
    start = time.time()
    num = lower
    sum = num

    while num < upper:
        num += 1
        sum += num

    return sum, time.time() - start



