import os
import re

output_dir = "output"

assignments = []

for model in os.listdir(output_dir):
    for solver_dir in os.listdir(os.path.join(output_dir, model)): 

        solver, timelimit = solver_dir.split("_") 
        file_ass = []

        for test_file_name in os.listdir(os.path.join(output_dir, model, solver_dir)):
            full_path = os.path.join(output_dir, model, solver_dir, test_file_name)

            assign = []
            ass = {}

            with open(full_path) as testf:
                for line in testf.readlines():
                    # If is assignment
                    if re.match("^A ", line):
                        spl_line = line.split(" ")
                        ass['course'] = (spl_line[1].split("_"))[0]
                        ass['type'] = (spl_line[1].split("_"))[1]
                        ass['day'] = spl_line[2]
                        ass['start'] = spl_line[3]
                        ass['end'] = spl_line[4]
                        ass['week'] = spl_line[5]
                        ass['room'] = spl_line[6].strip()
                        ass['timelimit'] = timelimit
                        ass['solver'] = solver
                        assign.append(ass)
                        ass = {}

                    if re.match("^\-\-\-\-\-\-\-\-\-\-$", line):
                        if len(assign) > 0:
                            file_ass.append(assign)
                            assign = []

                if len(file_ass) > 0:
                    assignments.append(file_ass)
                    file_ass = []

all_timelimits = []
all_solvers = []

for ass in assignments:
    for fass in ass:
        all_timelimits.append(fass[0]['timelimit'])
        all_solvers.append(fass[0]['solver'])

for timelimit in set(all_timelimits):
    for solver in set(all_solvers):
        for ass in assignments:
            best = ass[-1]
            if best[0]['timelimit'] == timelimit and best[0]['solver'] == solver:
                with open(os.path.join("results", "assignments", solver + "_" + timelimit + ".csv"), 'w') as assf:
                    assf.write("{} {} {}".format(timelimit, solver, len(ass)))
                    for a in best:
                        assf.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                            a['course'],
                            a['type'],
                            a['day'],
                            a['start'],
                            a['end'],
                            a['week'],
                            a['room']
                        ))

