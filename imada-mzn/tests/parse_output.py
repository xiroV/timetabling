import os
import re

output_dir = "output"

results = []

for model in os.listdir(output_dir):
    for solver_dir in os.listdir(os.path.join(output_dir, model)): 

        solver, timelimit = solver_dir.split("_") 
        for test_file_name in os.listdir(os.path.join(output_dir, model, solver_dir)):
            full_path = os.path.join(output_dir, model, solver_dir, test_file_name)

            test_res = []

            with open(full_path) as testf:
                if re.match("=====UNKNOWN=====", testf.readline()):
                    res_found = dict()
                    res_found['timelimit'] = timelimit
                    res_found['obj'] = ""
                    res_found['id'] = "test" + (test_file_name.split("."))[0]
                    res_found['model'] = model
                    res_found['solver'] = solver
                    res_found['time'] = ""
                    res_found['state'] = "unknown"
                    test_res.append(res_found)
                elif re.match("=====UNSATISFIABLE=====", testf.readline()):
                    res_found = dict()
                    res_found['timelimit'] = timelimit
                    res_found['obj'] = ""
                    res_found['id'] = "test" + (test_file_name.split("."))[0]
                    res_found['model'] = model
                    res_found['solver'] = solver
                    res_found['time'] = ""
                    res_found['state'] = "unsatisfiable"
                    test_res.append(res_found)
                elif re.match("=====UNSATorUNBOUNDED=====", testf.readline()):
                    res_found = dict()
                    res_found['timelimit'] = timelimit
                    res_found['obj'] = ""
                    res_found['id'] = "test" + (test_file_name.split("."))[0]
                    res_found['model'] = model
                    res_found['solver'] = solver
                    res_found['time'] = ""
                    res_found['state'] = "unsat_or_unbounded"
                    test_res.append(res_found)
                elif re.match("=====UNBOUNDED=====", testf.readline()):
                    res_found = dict()
                    res_found['timelimit'] = timelimit
                    res_found['obj'] = ""
                    res_found['id'] = "test" + (test_file_name.split("."))[0]
                    res_found['model'] = model
                    res_found['solver'] = solver
                    res_found['time'] = ""
                    res_found['state'] = "unbounded"
                    test_res.append(res_found)
                elif re.match("=====ERROR=====", testf.readline()):
                    res_found = dict()
                    res_found['timelimit'] = timelimit
                    res_found['obj'] = ""
                    res_found['id'] = "test" + (test_file_name.split("."))[0]
                    res_found['model'] = model
                    res_found['solver'] = solver
                    res_found['time'] = ""
                    res_found['state'] = "error"
                    test_res.append(res_found)
                else:
                    res_found = dict()
                    for line in testf.readlines():
                        if re.match("^timeStability: \d", line):
                            res_found['timeStability'] = int((line.split(" "))[1].strip())
                        if re.match("^roomStability: \d", line):
                            res_found['roomStability'] = int((line.split(" "))[1].strip())
                        if re.match("^maxEventsxDayxTeacher: \d", line):
                            res_found['maxEventsxDayxTeacher'] = int((line.split(" "))[1].strip())
                        if re.match("^maxEventsxDayxStudent: \d", line):
                            res_found['maxEventsxDayxStudent'] = int((line.split(" "))[1].strip())
                        if re.match("^maxStudentOverlaps: \d", line):
                            res_found['maxStudentOverlaps'] = int((line.split(" "))[1].strip())
                        if re.match("^badSlots: \d", line):
                            res_found['badSlots'] = int((line.split(" "))[1].strip())
                        # Minizinc solution time
                        if re.match("^% time elapsed", line):
                            res_found['time'] = float((line.split(" "))[3])
                        # Sunny-cp solution time
                        if re.match("^% Current Solution Time:", line):
                            res_found['time'] = float((line.split(" "))[4])
                        if re.match("^\-\-\-\-\-\-\-\-\-\-$", line):
                            res_found['state'] = "feas"
                            res_found['model'] = model
                            res_found['timelimit'] = timelimit
                            res_found['solver'] = solver
                            res_found['id'] = "test" + (test_file_name.split("."))[0]
                            objectives = [res_found['timeStability'], res_found['roomStability'], res_found['maxEventsxDayxTeacher'], res_found['maxEventsxDayxStudent'], res_found['maxStudentOverlaps'], res_found['badSlots']]
                            res_found['obj'] = sum(objectives)
                            test_res.append(res_found)
                            res_found = dict()
 

            results.append(test_res)

#timelimits = set( val for dic in results for val in dic.values())

all_timelimits = []
for res in results:
    for f in res:
        all_timelimits.append(f['timelimit'])

for timelimit in set(all_timelimits):
    with open('results/all_results_' + timelimit + '.csv', 'w') as outf:
        outf.write("{},{},{},{},{},{}\n".format('Model', 'Solver', 'Test_id', 'State', 'Time', 'Obj'))
        for res in results:
            for test in res:
                if test['timelimit'] == timelimit:
                    outf.write("{},{},{},{},{},{}\n".format(test['model'], test['solver'], test['id'], test['state'], test['time'], test['obj']))


                


            
