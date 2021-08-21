#!/bin/bash
for((i=1;i<=$1;i++)) do
    echo "  test $i of $1"
    if [ ! -f "output/imada-int/choco_$2/$i.out" ]; then
        timeout $2s sunny-cp \
            -a \
            -P choco \
            models/imada-int.mzn \
            data/imada-output.dzn \
            | solns2out models/imada-int.ozn \
            > output/imada-int/choco_$2/$i.out
    else
        echo "    Already exist"
    fi
done
