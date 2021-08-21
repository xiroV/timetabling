# Analyses a ITC 2019 XML instance file, and outputs statistics.
#
#   python analyse_instance.py data_directory output_format

import xml.etree.ElementTree as ET
import sys
import math
import tabulate
import glob
import os
from operator import itemgetter

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

data_dir = sys.argv[1]
if len(sys.argv) > 2:
    output_format = sys.argv[2]
else:
    output_format = "plain"

table = []

for instance_name in instance_names:
    instance_file = os.path.join(data_dir, instance_name + ".xml")
    instance_size = round(os.path.getsize(instance_file)/math.pow(1024, 2), 2)

    tree = ET.parse(instance_file)
    # Grap problem variables
    root = tree.getroot()
    if root.tag != "problem":
        sys.error("instance does not contain a problem\n")

    num = {}
    num['students'] = 0
    num['rooms'] = 0
    num['dists'] = {}
    num['dists']['hard'] = 0
    num['dists']['soft'] = 0
    num['courses'] = 0
    num['course_classes'] = {}
    num['course_rooms'] = {}
    num['clas_sched'] = {}
    num['clas_rooms'] = {}

    unique_sched = set()

    for child in root:
        if child.tag == "rooms":
            for _ in child:
                num['rooms'] += 1
        elif child.tag == "courses":
            for course in child:
                num['courses'] += 1
                for config in course.findall('config'):
                    for subpart in config.findall('subpart'):
                        for clas in subpart.findall('class'):
                            if course.attrib['id'] not in num['course_classes'].keys():
                                num['course_classes'][course.attrib['id']] = 0
                            num['course_classes'][course.attrib['id']] += 1
                            for item in clas:
                                if item.tag == "time":
                                    if clas.attrib['id'] not in num['clas_sched'].keys():
                                        num['clas_sched'][clas.attrib['id']] = 0
                                    num['clas_sched'][clas.attrib['id']] += 1
                                    sched_key = item.attrib['weeks'] + "_" + item.attrib['days'] + "_" + item.attrib['start'] + "_" + item.attrib['length']
                                    if sched_key not in unique_sched:
                                        unique_sched.add(sched_key)
                                if item.tag == "room":
                                    if clas.attrib['id'] not in num['clas_rooms'].keys():
                                        num['clas_rooms'][clas.attrib['id']] = 0
                                    num['clas_rooms'][clas.attrib['id']] += 1

        elif child.tag == "distributions":
            for d in child:
                if 'required' in d.attrib.keys():
                    num['dists']['hard'] += 1
                else:
                    num['dists']['soft'] += 1
        elif child.tag == "students":
            for _ in child:
                num['students'] += 1
        elif child.tag == "optimization":
            pass
        else:
            print("ERROR: Unhandled tag {}".format(child.tag))

    avg_clas_per_course = round(float(sum(num['course_classes'].values())/len(num['course_classes'])), 2)

    table.append([
        instance_name,
        str(instance_size),
        num['courses'],
        sum(num['course_classes'].values()),
        num['rooms'],
        num['students'],
        num['dists']['hard'],
        num['dists']['soft'],
        sum(num['clas_sched'].values()),
        len(unique_sched),
    ])

header = ["Instance", "Size (MiB)", "Courses", "Classes", "Rooms", "Students", "Hard", "Soft", "All", "Unique"]
if output_format == "latex":
    print(tabulate.tabulate(table, headers = header, tablefmt='latex_booktabs'))
else:
    print(tabulate.tabulate(table, headers = header))
