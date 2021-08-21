import xml.etree.ElementTree as ET
import re
import sys
import os
import tabulate

instance_names = [
    "wbg-fal10", "lums-sum17", "bet-sum18", "pu-cs-fal07", "pu-llr-spr07",
    "pu-c8-spr07", "agh-fis-spr17", "agh-ggis-spr17", "bet-fal17", "iku-fal17",
    "mary-spr17", "muni-fi-spr16", "muni-fsps-spr17", "muni-pdf-spr16c",
    "pu-llr-spr17", "tg-fal17"
]

dists = {
    "SameStart": "SS",
    "SameTime": "ST",
    "DifferentTime": "DT",
    "SameDays": "SD",
    "DifferentDays": "DD",
    "SameWeeks": "SW",
    "DifferentWeeks": "DW",
    "SameRoom": "SR",
    "DifferentRoom": "DR",
    "Overlap": "O",
    "NotOverlap": "NO",
    "SameAttendees": "SA",
    "Precedence": "P",
    "WorkDay": "WD",
    "MinGap": "MG",
    "MaxDays": "MD",
    "MaxDayLoad": "MDL",
    "MaxBreaks": "MBR",
    "MaxBlock": "MBL"
}

data_dir = sys.argv[1]
if len(sys.argv) > 2:
    output_format = sys.argv[2]
else:
    output_format = "plain"

table = []

for dn in dists.keys():
    print(dn)
    row = []
    row.append(dists[dn])
    for instance_name in instance_names:
        hard = 0
        soft = 0
        instance_file = os.path.join(data_dir, instance_name + ".xml")

        tree = ET.parse(instance_file)
        # Grap problem variables
        root = tree.getroot()
        if root.tag != "problem":
            sys.error("instance does not contain a problem\n")

        for child in root:
            if child.tag == "distributions":
                for d in child:
                    if re.match("^{}".format(dn), d.attrib['type']):
                        if 'required' in d.attrib.keys():
                            hard += 1
                        else:
                            soft += 1
        row.append("{} - {}".format(hard, soft))

    table.append(row)

header = [""] + instance_names
if output_format == "latex":
    print(tabulate.tabulate(table, headers=header, tablefmt='latex_booktabs'))
else:
    print(tabulate.tabulate(table, headers=header))
