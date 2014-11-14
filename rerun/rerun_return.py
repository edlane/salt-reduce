# -*- coding: utf-8 -*-
'''
The rerun returner is used to repeated execute the same salt module which
originally invoked it.
It simply sends the return data to the "rerun_runner" on the salt-master
which re-targets this minion with identical salt module/ arguments.

  To use the rerun returner, append '--return rerun' to the salt command. ex:

    salt '*' test.sleep  10 --return rerun
'''


# Define the module's virtual namel
__virtualname__ = 'rerun'

def __virtual__():
    return __virtualname__

def returner(ret):
    '''
        # reissue the same command which brought us here from the salt-master
    '''

    try:
        sock_dir = '/var/run/salt/minion'
        out = __salt__['event.fire_master'](ret, "rerun")

    except Exception, e:
        print (e)
