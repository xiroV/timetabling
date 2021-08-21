#!/bin/bash
for((i=1;i<=$1;i++)) do
    echo "  test $i of $1"
    if [ ! -f "output/imada-int/gecode_$2/$i.out" ]; then
        let "timelimit = $2 * 1000"
        minizinc \
            -d data/imada-output.dzn \
            -a \
            -o output/imada-int/gecode_$2/$i.out \
            --solver gecode \
            --output-objective \
            --output-time \
            --time-limit $timelimit \
            models/imada-int.mzn
    else
        echo "    Already exist"
    fi
done
