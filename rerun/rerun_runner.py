import salt.utils.event
import salt.client
import salt.config

__opts__ = {}
event = salt.utils.event.MasterEvent('/var/run/salt/master')
repeat_count = 0
repeat = 0


def rerun():
    global repeat_count
    global repeat
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
        if fun == 'test.arg':
            command = fun_args[0].lower()
            if command == 'abort':
                print "\"abort\" received, now terminating runner..."
                print "command repeated {0} times".format(repeat_count)
                break
            elif command == 'load':
                print "load..."
                print 'fun_args =', fun_args
            elif command == 'start':
                print "start"
            elif command == 'config':
                print "config"
                limit = fun_args[-1]['limit']
                repeat = iter(xrange(1, limit))
            elif command == 'stop':
                print "stop"
            elif command == 'pause':
                print "pause"
            elif command == 'stats':
                print "repeat_count = ", (repeat_count)
            elif command == 'add':
                print "add"
                try:
                    repeat.next()
                    minions = client.cmd(target, fun_args[1], [fun_args[2]], ret='rerun')
                except StopIteration:
                    print "limit exceeded"
                    pass
        else:
            repeat_count += 1
            print 'repeat =', (repeat_count)
            try:
                repeat.next()
                minions = client.cmd(target, fun, fun_args, ret='rerun')
            except StopIteration:
                print "done."
                pass

print "starting..."
rerun()
