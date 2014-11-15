Here is a reworked example of a "rerun" salt returner and associated runner

1. place "rerun_return.py" in the /srv/salt/_returners directory:

lane@ubuntu:~$ cp rerun_return.py /srv/salt/_returners

2. copy "rerun_return.py" to all minions:

lane@ubuntu:~$ salt "*" saltutil.sync_returners

3. start up the "rerun_runner.py" on the salt-master:

lane@ubuntu:~$ python rerun_runner.py

4. running the "rerun" returner: ( only run once! )

lane@ubuntu:~$ salt ubuntu test.sleep 10 --return rerun


