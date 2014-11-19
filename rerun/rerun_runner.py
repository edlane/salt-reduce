import salt.utils.event
import salt.client
import salt.config
import ast

import mapit

__opts__ = {}
event = salt.utils.event.MasterEvent('/var/run/salt/master')
repeat_count = 0
template = None
rerun_dict = {}


class mapper():

    def partializer(self, limit):
        return iter(xrange(0, limit))

    def reducer(self, partial_results):
        pass

m = mapper()
repeat = m.partializer(10)

def rerun():
    global repeat_count
    global repeat
    global template
    client = salt.client.LocalClient('/etc/salt/minion')
    for data in event.iter_events(tag='rerun', full=True):
    # for data in event.iter_events(tag=''):
        print 'data =', (data)
        target = data['data']['id']
        print 'target', target
        fun = data['data']['data']['fun']
        # print fun
        fun_args = data['data']['data']['fun_args']
        # print fun_args
        RERUN_IT = True
        REDUCER_CALLBACK = True
        if fun == 'test.arg':
            RERUN_IT = False    # don't rerun control commands
            REDUCER_CALLBACK = False    # don't callback results from control commands
            command = fun_args[0].lower()
            if command == 'abort':
                print "\"abort\" received, now terminating runner..."
                break
            elif command == 'load':
                print "load..."
                print 'fun_args =', fun_args
            elif command == 'start':
                print "start"
            elif command == 'config':
                print "config"
                limit = fun_args[-1]['limit']
                repeat = iter(xrange(1, limit+1))
            elif command == 'stop':
                print "stop"
            elif command == 'pause':
                print "pause"
            elif command == 'stats':
                print "repeat_count = ", (repeat_count)
            elif command == 'iterator':
                print 'iterator'
                iterator = eval(fun_args[1])
            elif command == 'template':
                print 'template'
                template = {}
                template['fun'] = fun_args[1]
                template['fun_args'] = fun_args[2]
            elif command == 'mapit':
                print "mapit"
                template = {}
                template['fun'] = fun_args[1]
                template['fun_args'] = fun_args[2]
                RERUN_IT = True     # insert the initial "partializer" command to be run

        if RERUN_IT:
            if REDUCER_CALLBACK:
                # only callback the reducer if we got "real" results from a "partialize" command
                m.reducer(data['data']['data']['return'])
            try:
                rerun_dict['next'] = str(repeat.next())
                if template:
                    stringit = template['fun_args'].format(**rerun_dict)
                    fun_args = [ast.literal_eval("'" + stringit + "'")]
                    fun = template['fun']
                minions = client.cmd(target, fun, fun_args, ret='rerun')
                repeat_count += 1
                print 'repeat =', (repeat_count)
            except StopIteration:
                print "done."
                repeat_count = 0
                pass

print "starting..."
rerun()
