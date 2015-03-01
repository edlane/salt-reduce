#!/bin/bash
#ID_GRAIN=`salt-call --local grains.item id --output=txt`
#regex="local: \{'id': '(.*)'\}"
#[[ $ID_GRAIN =~ $regex ]]
#MINION=${BASH_REMATCH[1]}
#echo $MINION
#set -v
echo Demo time...
salt-run rerun_runner.run &
echo install salt module "test.sleep" ...
salt-call test.arg mapit test.sleep 15 --return=rerun

echo "run ""test.sleep"" 40 times --- 40 * (15 seconds) = 10 minutes worth of sleep"
echo startup a total of 40 workers ...
read

salt \* test.arg run 40 --return=rerun

salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun

salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun

salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun
salt \* test.arg run --return=rerun

read
