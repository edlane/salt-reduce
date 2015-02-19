#!/bin/bash
#ID_GRAIN=`salt-call --local grains.item id --output=txt`
#regex="local: \{'id': '(.*)'\}"
#[[ $ID_GRAIN =~ $regex ]]
#MINION=${BASH_REMATCH[1]}
#echo $MINION
set -v
echo Demo time...
salt-run rerun_runner.run verbose=True &
read
salt-call test.arg mapit test.sleep 15 --return=rerun
read
salt \* test.arg run 20 --return=rerun
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
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun
read
salt \* test.arg run --return=rerun

