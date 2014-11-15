import salt.utils.event
import salt.client
import salt.config

__opts__ = {}
event = salt.utils.event.MasterEvent('/var/run/salt/master')
repeat_count = 0

def rerun():
    global repeat_count
    client = salt.client.LocalClient('/etc/salt/minion')
    for data in event.iter_events(tag='rerun', full=True):
    # for data in event.iter_events(tag=''):
    #     print (data)
        target = data['data']['id']
        # print target
        fun = data['data']['data']['fun']
        # print fun
        fun_args = data['data']['data']['fun_args']
        # print fun_args
        if fun == 'test.arg':
            if fun_args[0].lower() == 'abort':
                print "\"abort\" received, now terminating runner..."
                print "command repeated {0} times".format(repeat_count)
                break
            elif fun_args[0].lower() == 'stop':
                print "stop"
            elif fun_args[0].lower() == 'pause':
                print "pause"
            elif fun_args[0].lower() == 'stats':
                print "repeat_count = ", (repeat_count)
        else:
            repeat_count += 1
            minions = client.cmd(target, fun, fun_args, ret='rerun')

print "starting..."
rerun()
