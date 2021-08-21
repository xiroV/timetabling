#!/bin/bash

# Run like this:
# ./mzn-test.sh test_name 

SOLVERS='gecode yuck oscar'
NAME=$1
TIMELIMIT=3700 # Timelimit in seconds
TIMELIMIT_MS=$((TIMELIMIT * 1000))
PYTHON=python3

$PYTHON src/preprocess.py -f data/$NAME.xml -o dzn/$NAME.dzn

for SOLVER in $SOLVERS; do
    if [ $SOLVER == "gecode" ]; then
        minizinc --statistics --output-objective --output-time --time-limit $TIMELIMIT_MS --solver gecode -o output/mzn-$NAME-gecode.out -d dzn/$NAME.dzn mzn/base.mzn 
    elif [ $SOLVER == "yuck" ]; then
        minizinc --statistics --output-objective --output-time --time-limit $TIMELIMIT_MS --solver yuck -o output/mzn-$NAME-yuck.out -d dzn/$NAME.dzn mzn/base.mzn 
    elif [ $SOLVER == "chuffed" ]; then
        minizinc --statistics --output-objective --output-time --time-limit $TIMELIMIT_MS -a --solver chuffed -o output/mzn-$NAME-chuffed.out -d dzn/$NAME.dzn mzn/base.mzn 
    elif [ $SOLVER == "ortools" ]; then
        minizinc --statistics --output-objective --output-time --time-limit $TIMELIMIT -a --solver ortools -o output/mzn-$NAME-ortools.out -d dzn/$NAME.dzn mzn/base.mzn
    elif [ $SOLVER == "oscar" ]; then
        minizinc --statistics --output-objective --output-time --time-limit $TIMELIMIT_MS -a --solver oscar -o output/mzn-$NAME-oscar.out -d  dzn/$NAME.dzn mzn/base.mzn
    else
        echo "Solver '$SOLVER' not found"
    fi

    # Do postprocess
	$PYTHON src/postprocess.py -n $NAME -i data/$NAME.xml -o output/mzn-$NAME-$SOLVER.out -r solutions/mzn-$NAME-$SOLVER.xml
done


