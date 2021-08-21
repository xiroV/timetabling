numtests=3
timelimit=900

all: results

tests: test_gecode test_ortools test_chuffed test_choco

test_gecode: pre_test
	mkdir -p output/imada-int/gecode_$(timelimit)
	./tests/gecode.sh $(numtests) $(timelimit)

test_ortools: pre_test
	mkdir -p output/imada-int/ortools_$(timelimit)
	./tests/ortools.sh $(numtests) $(timelimit)

test_chuffed: pre_test
	mkdir -p output/imada-int/chuffed_$(timelimit)
	./tests/chuffed.sh $(numtests) $(timelimit)

test_choco: pre_test
	mkdir -p output/imada-int/choco_$(timelimit)
	./tests/choco.sh $(numtests) $(timelimit)

parse_output: tests
	python tests/parse_output.py	

results: parse_output
	Rscript tests/gen_results.R
	python tests/gen_assignments.py
	
pre_test:
	@echo "Running tests:"
	@echo "  tests per solver: $(numtests)"
	@echo "  timelimit: $(timelimit) seconds"
	minizinc -c models/imada-int.mzn data/imada-output.dzn
	mkdir -p output/imada-int
	mkdir -p results/assignments

clean:
	rm -r output
	rm -r results
