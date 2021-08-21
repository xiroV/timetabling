tmux new-session -d -A -s tests -n test_1
tmux send-keys -t testses "make dirs" C-m

for i in 16 17 18 19 26 27 28 29 30 31 32 33 34 35 36 37; do 
    tmux new-window -t tests -n test_$i
    tmux send-keys -t tests:test_$i "ssh imada-1063$i" C-m
    tmux send-keys -t tests:test_$i "cd test1/GLS/itc2019/" C-m
    tmux send-keys -t tests:test_$i "tmux new-session -A -s test" C-m
done

tmux attach -t tests

