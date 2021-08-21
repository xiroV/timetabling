#!/bin/bash

# Executes N tests on each of the specified solvers on
# the given data file

NAME=$1
N=3
SOLVERS='gecode yuck chuffed ortools oscar'

for s in $SOLVERS; do
    i=0
    while [ $i -lt $N ]; do
        echo "Running test $i of $N with solver $s on $NAME"
        ( exec test-util/run_test.sh $s $NAME $i )
        i=$(($i+1))
    done
done
