# MiniZinc Stuff

This directory contains models and utilities for solving different timetabling problems.

## Models

`models/imada-int.mzn` contains the MiniZinc model for the IMADA Timetabling problem modelled as a MILP problem using mostly integer variables and constraints.

`models/imada-bin.mzn` contains the MiniZinc model for the IMADA Timetabling problem, using mostly binary variables and contraints. (Not finished).


## Data
**NOTE:** No data from IMADA have been included in this repository. I might generate some dummy data at some point.

`data/imada-output.dzn` contains the MiniZinc data file for the IMADA Timetabling problem, (output from CTT). This works using `imada-int.mzn`

## Running Tests
(Current state, this may change in the future)

The models can be automatically tested by changing the variables `numtests` (number of tests per solver) and `timelimit` (time limit per test) in the `Makefile`.

If *sunny-cp* is installed locally, the tests can be run using

```
make all
```

otherwise pull *sunny-cp* from Docker Hub using:

```
sudo docker pull jacopomauro/sunny-cp
```

Then start the docker container:

```
docker run --entrypoint="/bin/bash" -i --rm -t -v `pwd`:/mydir jacopomauro/sunny-cp
```

and run

```
make tests
```

which will run the targets which are dependent on *sunny-cp*.

Afterwards, exit the container and run

```
make results
```

The output from all runs will be output to the `output` directory, and the processed results will be stored in the `results` directory.

