#!/bin/bash

# Run like this:
# ./run_test.sh solver test_name 

SOLVER=$1
NAME=$2
ID=$3
TIMELIMIT=3700 # Timelimit in seconds
TIMELIMIT_MS=$((TIMELIMIT * 1000))
PYTHON=python3

GECODE_CMD="fzn-gecode -s 1 -n 0 -a 1 -time $TIMELIMIT_MS fzn/$NAME.fzn > output/$NAME-gecode-$TIMELIMIT-$ID.out"
YUCK_CMD="yuck -J-Xmx12g -v --runtime-limit $TIMELIMIT fzn/$NAME.fzn > output/$NAME-yuck-$TIMELIMIT-$ID.out"
CHUFFED_CMD="fzn-chuffed -a -v -t $TIMELIMIT_MS fzn/$NAME.fzn > output/$NAME-chuffed-$TIMELIMIT-$ID.out"
ORTOOLS_CMD="fzn-or-tools -statistics=true -all_solutions=true -time_limit=$TIMELIMIT_MS fzn/$NAME.fzn > output/$NAME-ortools-$TIMELIMIT-$ID.out"
OSCAR_CMD="fzn-oscar-cbls -a -t $TIMELIMIT fzn/$NAME.fzn > output/$NAME-oscar-$TIMELIMIT-$ID.out"


if [ $SOLVER == "gecode" ]; then
    SOLVER_CMD=$GECODE_CMD
elif [ $SOLVER == "yuck" ]; then
    SOLVER_CMD=$YUCK_CMD
elif [ $SOLVER == "chuffed" ]; then
    SOLVER_CMD=$CHUFFED_CMD
elif [ $SOLVER == "ortools" ]; then
    SOLVER_CMD=$ORTOOLS_CMD
elif [ $SOLVER == "oscar" ]; then
    SOLVER_CMD=$OSCAR_CMD
else
    echo "Solver '$SOLVER' not found"
fi

#ULIMIT_CMD="ulimit -t $TIMELIMIT -S -v $VMEM_LIMIT"
CMD="/usr/bin/time -a -o log/$NAME-$SOLVER.log $SOLVER_CMD"

#echo $ULIMIT_CMD
#/bin/bash -c "$ULIMIT_CMD"
echo $CMD
/bin/bash -c "$CMD"
#GECODE_FZN = fzn-gecode -s -n 0 -a 1 fzn/$(1).fzn > output/$(1)-gecode.out

# Do postprocess
$PYTHON src/fzn_postprocess.py -n $NAME -i data/$NAME.xml -o output/$NAME-$SOLVER-$TIMELIMIT-$ID.out -r solutions/$NAME-$SOLVER-$TIMELIMIT-$ID.xml 



