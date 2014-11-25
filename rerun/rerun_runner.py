import salt.utils.event
import salt.client
import salt.config

from mapper import mapper

__opts__ = {}
event = salt.utils.event.MasterEvent('/var/run/salt/master')

def rerun():
    repeat_count = 0
    m = None
    client = salt.client.LocalClient('/etc/salt/minion')
    for data in event.iter_events(tag='rerun', full=True):
        # this is the inner event loop...
        #
        print 'data =', (data)
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
                print "\"abort\" received, now terminating runner..."
                return False
            elif command == 'reset':
                print "\"reset\" received, now restarting..."
                return True
            elif command == 'run':
                print "run"
                RERUN_IT = True
            elif command == 'stop':
                print "stop"
            elif command == 'pause':
                print "pause"
            elif command == 'stats':
                print "repeat_count = ", (repeat_count)
                print "results = ", (m.statit())
            elif command == 'mapit':
                print "mapit"
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
            m.reducer(data['data']['data']['return'])
            try:
                mod
            except:
                RERUN_IT = False
                # This is NOT a MR enabled salt execution module so don't rerun it


        if RERUN_IT:
            try:
                fun = m.module_name
                fun_args = repeat.next()
                minions = client.cmd_async(target, fun, fun_args, ret='rerun')
                repeat_count += 1
                print 'repeat =', (repeat_count)
            except StopIteration:
                print "done."
                pass

print "starting..."
while rerun():
    pass

