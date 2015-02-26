import salt.utils.event
import salt.client
import salt.config
import logging

# from mapper import mapper

import sys
sys.path.append('/srv/salt/_runners')
sys.path.append('/srv/salt/_modules')

from lib.mapper import mapper
from resource import getrusage as resource_usage, RUSAGE_SELF
from time import time as timestamp

__opts__ = {}
event = salt.utils.event.MasterEvent('/var/run/salt/master')
log = logging.getLogger(__name__)
verbose = False

def rerun():
    inflight = {}   # a dictionary for jobs with pending returned results
    repeat_count = 0
    m = None
    client = salt.client.LocalClient('/etc/salt/minion')
    for data in event.iter_events(tag='rerun', full=True):
        # this is the inner event loop...
        #
        if verbose: print >> sys.stderr, 'data =', (data)
        target = data['data']['id']
        fun = data['data']['data']['fun']
        fun_args = data['data']['data']['fun_args']
        RERUN_IT = True
        REDUCER_CALLBACK = True
        if fun == 'test.arg':
            # Interactive commands for controlling the mapper enter here...
            # We repurpose the existing salt test.arg command
            #
            # >>> salt "test.arg <command> <args> <kwargs> --return=rerun"
            #
            # to control the runner
            #
            RERUN_IT = False
                # ...don't rerun control commands
            REDUCER_CALLBACK = False    # don't callback results from control commands
            command = fun_args[0].lower()
            if command == 'abort':
                if verbose: print >> sys.stderr, "\"abort\" received, now terminating runner..."
                return False
            elif command == 'reset':
                if verbose: print >> sys.stderr, "\"reset\" received, now restarting..."
                return True
            elif command == 'run':
                if verbose: print >> sys.stderr, "run"
                try:
                    run_done = fun_args[1]
                except IndexError:
                    pass # no count passed to run command, ignore it
                RERUN_IT = True
                # start timers
                start_time, start_resources = timestamp(), resource_usage(RUSAGE_SELF)
            elif command == 'stop':
                if verbose: print >> sys.stderr, "stop", "not implemented"
            elif command == 'pause':
                if verbose: print >> sys.stderr, "pause", "not implemented"
            elif command == 'stats':
                print >> sys.stderr, "repeat_count = ", (repeat_count)
                print >> sys.stderr, "results = ", (m.statit())
            elif command == 'mapit':
                if verbose: print >> sys.stderr, "mapit"
                if not m:
                    # run this only once...
                    try:
                        module_name = fun_args[1].split('.')[0]
                        # from module_name import _mapper
                        mod = __import__(module_name)
                        mod = getattr(mod, '_mapper')
                        # this module has a "_mapper" class so use it...
                        m = mod(fun_args[1])
                        repeat = m.partializer(fun_args[2:])
                    except:
                        # not a map-reduce style module, so use base mapper class
                        m = mapper(fun_args[1])
                        repeat = m.partializer(fun_args[2:])
                # RERUN_IT = True
                # # ...causes the initial "partializer" command to be run

        if REDUCER_CALLBACK:
            # only callback the reducer if we got "real" results from a salt
            # execution module
            if inflight[data['data']['data']['jid']]:
                # TODO: This should not happen. Investigate why and prevent it
                m.reducer(data['data']['data']['return'])
                inflight.pop(data['data']['data']['jid'])
                try:
                    mod
                except:
                    RERUN_IT = False
                    # This is NOT a MR enabled salt execution module so don't rerun it
            else:
                RERUN_IT = False    # ...ignore this spurious event


        if RERUN_IT:
            try:
                try:
                    # use "run_done" to stop all subsequent salt module calls
                    if run_done <= repeat_count:
                        raise StopIteration
                except NameError:
                    pass
                my_fun = m.module_name
                my_fun_args = repeat.next()
                if verbose: print >> sys.stderr, "my_fun_args = ", (my_fun_args)
                minions = client.cmd_async(target, my_fun, my_fun_args, ret='rerun')
                inflight[minions] = True
                if verbose: print >> sys.stderr, "sending...", (my_fun), (my_fun_args), (minions)
                repeat_count += 1
                if verbose: print >> sys.stderr, 'repeat =', (repeat_count)

            except StopIteration:
                print >> sys.stderr, "done."
                if len(inflight) == 0:
                    # all the results in, ok to terminate
                    end_resources, end_time = resource_usage(RUSAGE_SELF), timestamp()
                    runner_stats = {'real': end_time - start_time,
                                    'sys': end_resources.ru_stime - start_resources.ru_stime,
                                    'user': end_resources.ru_utime - start_resources.ru_utime}
                    exit({'result': m.statit(), 'runner stats': runner_stats})

def run(*args, **kwargs):
    global verbose
    if 'verbose' in kwargs:
        verbose = kwargs['verbose']

    if verbose: print >> sys.stderr, "starting..."
    while rerun():
        pass


if __name__ == '__main__':
    exec (''.join(['run'] + sys.argv[1:]))
    # run()
