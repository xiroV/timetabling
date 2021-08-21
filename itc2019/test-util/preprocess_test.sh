#!/bin/bash

# Run like this:
# ./preprocess_test.sh solver test_name 

#NAMES="wbgfal lumssum betsum pucsfal pullrspr07 puc8spr aghfisspr aghggisspr betfal ikufal maryspr munifispr munifspsspr munipdfspr pullrspr17 tgfal"
NAMES="wbgfal lumssum betsum pucsfal pullrspr07 puc8spr maryspr munifispr munifspsspr pullrspr17 tgfal"

for NAME in $NAMES; do
    echo $NAME
    CMD="/usr/bin/time -a -o log/$NAME-preprocess.log make fzn-$NAME-preprocess >> log/$NAME-preprocess.log"
    /bin/bash -c "$CMD"
done



# Do postprocess
#$PYTHON src/fzn_postprocess.py -n $NAME -i data/$NAME.xml -o output/$NAME-$SOLVER-$TIMELIMIT-$ID.out -r solutions/$NAME-$SOLVER-$TIMELIMIT-$ID.xml 



