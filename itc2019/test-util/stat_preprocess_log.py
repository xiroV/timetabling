import xml.etree.ElementTree as ET
import sys
import math
import tabulate
import glob
import os
import re
from operator import itemgetter

instance_names = [
    "wbgfal",
    "lumssum",
    "betsum",
    "pucsfal",
    "pullrspr07",
    "puc8spr",
    #    "aghfisspr",
    #    "aghggisspr",
    #    "betfal",
    #    "ikufal",
    "maryspr",
    "munifispr",
    "munifspsspr",
    #    "munipdfspr",
    "pullrspr17",
    "tgfal"
]

dists = [
    "ScheduleOverlaps", "RoomUnavailable", "SameStart", "SameTime",
    "DifferentTime", "SameDays", "DifferentDays", "SameWeeks",
    "DifferentWeeks", "SameRoom", "DifferentRoom", "Overlap", "NotOverlap",
    "SameAttendees", "Precedences", "WorkDay", "MinGap", "MaxDays",
    "MaxDayLoad", "MaxBreaks", "MaxBlock"
]

hard_data_dir = sys.argv[1]
all_data_dir = sys.argv[2]
if len(sys.argv) > 3:
    output_format = sys.argv[3]
else:
    output_format = "plain"

con_table = []
var_table = []

for dist in dists:
    print(dist)
    con_row = []
    var_row = []
    con_row.append(dist)
    var_row.append(dist)
    for instance_name in instance_names:
        hard_log_file = os.path.join(hard_data_dir,
                                     instance_name + "-preprocess.log")
        all_log_file = os.path.join(all_data_dir,
                                    instance_name + "-preprocess.log")

        unique_sched = set()

        with open(hard_log_file) as f:
            for line in f.readlines():
                if re.search(" {} \(".format(dist), line):
                    if re.search("c: ", line):
                        con_row.append(int(((line.split(' '))[6])[0:-1]))

                    if re.search("v: ", line):
                        var_row.append(int(((line.split(' '))[4])[0:-1]))

        with open(all_log_file) as f:
            for line in f.readlines():
                if re.search(" {} \(".format(dist), line):
                    if re.search("c: ", line):
                        #soft_cons = (int(((line.split(' '))[6])[0:-1]))-con_row[-1]
                        soft_cons = int(((line.split(' '))[6])[0:-1])
                        con_row.append(soft_cons)

                    if re.search("v: ", line):
                        #soft_vars = (int(((line.split(' '))[4])[0:-1]))-var_row[-1]
                        soft_vars = int(((line.split(' '))[4])[0:-1])
                        var_row.append(soft_vars)

    con_table.append(con_row)
    var_table.append(var_row)

# Find total constraints
row = [0] * len(con_table[0])
for c in range(1, len(con_table[0])):
    for r in range(0, len(con_table)):
        row[c] += con_table[r][c]

con_table.append(["Total"] + row)

# Find total variables
row = [0] * len(var_table[0])
for c in range(1, len(var_table[0])):
    for r in range(0, len(var_table)):
        row[c] += var_table[r][c]

var_table.append(["Total"] + row)

header = [""] + instance_names
print("Constraints Table")
if output_format == "latex":
    print(
        tabulate.tabulate(con_table, headers=header,
                          tablefmt='latex_booktabs'))
else:
    print(tabulate.tabulate(con_table, headers=header))

print()
print("Variables Table")
if output_format == "latex":
    print(
        tabulate.tabulate(var_table, headers=header,
                          tablefmt='latex_booktabs'))
else:
    print(tabulate.tabulate(var_table, headers=header))
