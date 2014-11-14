import salt.utils.event
import salt.client
import salt.config

__opts__ = {}
event = salt.utils.event.MasterEvent('/var/run/salt/master')
# global repeat_count
# repeat_count = 5


def rerun():
    client = salt.client.LocalClient('/etc/salt/minion')
    for data in event.iter_events(tag='rerun', full=True):
    # for data in event.iter_events(tag=''):
        print (data)
        target = data['data']['id']
        # print target
        fun = data['data']['data']['fun']
        # print command
        fun_args = data['data']['data']['fun_args']
        # print args
        minions = client.cmd(target, fun, fun_args, ret='rerun')

print "starting..."
rerun()
