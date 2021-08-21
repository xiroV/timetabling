#!/bin/bash
for problem_path in data/*.xml;
do
    problem_file=${problem_path##*/}
    problem_name=${problem_file%.xml}
    if [ "$problem_name" != "agh-fis-spr17" ] && [ "$problem_name" != "agh-ggis-spr17" ] && [ "$problem_name" != "bet-fal17" ] && [ "$problem_name" != "iku-fal17" ]; then
        echo "Running itc2fzn on "$problem_name""
        time timeout 1800s python3 src/itc2fzn.py -i "$problem_path" -o fzn/"$problem_name".fzn
    fi
done
