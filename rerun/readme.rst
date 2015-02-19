Here is a reworked example of a "rerun" salt returner and associated runner

1. deploy the code:

lane@ubuntu:~$ ./deploy2test.sh


2. start up the "rerun_runner.py" on the salt-master:

lane@ubuntu:~$ salt-run rerun_runner.py


3. prime the runner: ( run only once! )

lane@ubuntu:~$ salt-call test.arg mapit adder.add 1000000 --return=rerun


4. run "adder.add" on all the targeted minions (in this example, "\*")

lane@ubuntu:~$ salt \* test.arg run --return=rerun

