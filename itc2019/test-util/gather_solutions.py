import os 
import sys
import re
import math
import tabulate

instance_names = [
    "wbg-fal10",
    "lums-sum17",
    "bet-sum18",
    "pu-cs-fal07",
    "pu-llr-spr07",
    "pu-c8-spr07",
    "agh-fis-spr17",
    "agh-ggis-spr17",
    "bet-fal17",
    "iku-fal17",
    "mary-spr17",
    "muni-fi-spr16",
    "muni-fsps-spr17",
    "muni-pdf-spr16c",
    "pu-llr-spr17",
    "tg-fal17"
]

solvers = ["gecode", "chuffed", "yuck", "ortools","oscar"]

test_dir = sys.argv[1]
num_tests = sys.argv[2]
seconds = sys.argv[3]
if len(sys.argv) > 4:
    output_format = sys.argv[4]
else:
    output_format = "plain"

table = []

for inst_name in instance_names:
    row = []
    row.append(inst_name)
    for solver in solvers:
        opt = []
        res = []
        for test_num in range(0,int(num_tests)):
            test_name = inst_name + "-" + solver + "-" + str(seconds) + "-" + str(test_num)
            file_name = test_name + ".out"
            file_path = os.path.join(test_dir, file_name)
            nf = False


        
            try:
                with open(file_path) as f:
                    opt.append(False)
                    penalties = {}
                    for line in f.readlines():
                        if re.match(".*Penalty = .*", line):
                            penalty_id = (line.split(' '))[0]
                            penalty = ((line.split(' '))[2])[0:-2]
                            if penalty_id not in penalties.keys():
                                penalties[penalty_id] = []
                            penalties[penalty_id].append(int(penalty))
                        if re.match("==========", line):
                            opt[-1] = True

                    if len(penalties) != 0:
                        penalty = 0
                        for pen in penalties.keys():
                            penalty += penalties[pen][-1] 
                        res.append(penalty)
                    else:
                        res.append(None)

            except FileNotFoundError:
                print("Test not found: {}".format(file_name))
                nf = True

        if len(res) > 0 and res[0] is not None:
            #result[test_name] = {'optimal': opt[0], 'average': math.floor(sum(res)/len(res))}
            if opt[0]:
                row.append(str(math.floor(sum(res)/len(res)))+ "*")
            else:
                row.append(math.floor(sum(res)/len(res)))
        else:
            if nf:
                row.append("fgf")
            else:
                row.append('--')

    table.append(row)

header = ["Instances"] + solvers

if output_format == "latex":
    print(tabulate.tabulate(table, headers = header, tablefmt='latex_booktabs'))
else:
    print(tabulate.tabulate(table, headers = header))

    

