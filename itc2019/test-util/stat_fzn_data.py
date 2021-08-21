import sys
import math
import tabulate
import glob
import os
import re
from operator import itemgetter
from collections import defaultdict

instance_names = [
    "wbg-fal10",
    "lums-sum17",
    "bet-sum18",
    "pu-cs-fal07",
    "pu-llr-spr07",
    "pu-c8-spr07",
    #    "agh-fis-spr17",
    #    "agh-ggis-spr17",
    #    "bet-fal17",
    #    "iku-fal17",
    "mary-spr17",
    "muni-fi-spr16",
    "muni-fsps-spr17",
    #    "muni-pdf-spr16c",
    "pu-llr-spr17",
    "tg-fal17"
]

dists = []

table = []

data_dir = sys.argv[1]
if len(sys.argv) > 2:
    output_format = sys.argv[2]
else:
    output_format = "plain"

re_constraint = re.compile('^constraint')
re_contain_constraint_name = re.compile("mzn_constraint_name")
re_get_constraint_name = re.compile('mzn_constraint_name\(".*"\)')

result = {}

for instance_name in instance_names:
    res = defaultdict(int)
    with open(os.path.join(data_dir, instance_name + ".fzn")) as f:
        for line in f.readlines():
            if re.search(re_constraint, line):
                if re.search(re_contain_constraint_name, line):
                    try:
                        s = re.search(re_get_constraint_name, line)
                        start = s.start()
                        end = s.end()
                        name = line[start + 21:end - 2]

                        if name not in res.keys():
                            res[name] = 0

                            if name not in dists:
                                dists.append(name)

                        res[name] += 1
                    except AttributeError:
                        print("Error when parsing line:")
                        print(line)
                else:
                    print("{} does not contain a name".format(line[0:-1]))

    result[instance_name] = res

print(dists)

unique_dists = []

for d in dists:
    if d not in ["ScheduleOverlaps", "SchedulePenalty", "RoomPenalty", "RoomUnavailabilities"]:
        n = (d.split("_"))[0]
        if n not in unique_dists:
            unique_dists.append(n)
    else:
        unique_dists.append(d)

print("\nDone Parsing Instances\n")

for d in unique_dists:
    row = []
    row.append(d)

    for i in instance_names:
        try:
            if d not in ["ScheduleOverlaps", "SchedulePenalty", "RoomPenalty", "RoomUnavailabilities"]:
                row.append("{}".format(str(result[i][d + "_H"]) + " - " + str(result[i][d + "_S"])))
            else:
                row.append("{}".format(result[i][d]))
        except KeyError:
            print("Key {} not found for instance {}".format(d, i))
            row.append('---')

    table.append(row)

header = [""] + instance_names
if output_format == "latex":
    print(tabulate.tabulate(table, headers=header, tablefmt='latex_booktabs'))
else:
    print(tabulate.tabulate(table, headers=header))
