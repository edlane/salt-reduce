#!/bin/bash -v
echo Demo time...
salt-run rerun_runner.run verbose=True &
read
salt-call test.arg mapit mapit.map 1000000 --return=rerun
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun
