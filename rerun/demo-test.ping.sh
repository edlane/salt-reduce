#!/bin/bash -v
echo Demo time...
salt-run rerun_runner.run verbose=True &
read
salt-call test.arg mapit test.ping --return=rerun
read
salt \* test.arg run 10 --return=rerun
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun
