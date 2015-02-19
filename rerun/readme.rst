Here is a reworked example of a "rerun" salt returner and associated runner

1. place "rerun_return.py" in the /srv/salt/_returners directory:

lane@ubuntu:~$ cp rerun_return.py /srv/salt/_returners


2. copy "rerun_return.py" to all minions:

lane@ubuntu:~$ salt "*" saltutil.sync_returners


3. start up the "rerun_runner.py" on the salt-master:

lane@ubuntu:~$ salt-run rerun_runner.py


4. prime the runner: ( run only once! )

lane@ubuntu:~$ salt \* test.arg mapit adder.add 1000000 --return=rerun


5. run "mapit.partial" on all the targeted minions (in this example, "\*")

lane@ubuntu:~$ salt \* test.arg run --return=rerun

