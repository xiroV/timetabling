import re
import json
import data

# Functionality for reading and parsing output
# and writing results
class Result:
    def __init__(self, instance_name, inst, output_file):
        self.output_file = output_file  
        self.assignments = {}
        self.cores = 1
        self.author = "Brian Alberg"
        self.technique = ""
        self.institution = "The University of Southern Denmark"
        self.country = "Denmark"
        self.instance_name = instance_name
        self.runtime = 0
        self.inst = inst
        self.penalties = {}

        self.parse_assignments()
        self.print_stats()

    def parse_assignments(self):
        with open(self.output_file) as f:
            for line in f.readlines():
                if re.match("^C(\d)*_Schedule", line):
                    ass = (line.strip()).split(' = ')
                    sched = ass[1][:-1]
                    clas = ((ass[0].split('_'))[0])[1:]
                    if clas not in self.assignments.keys():
                        self.assignments[clas] = {}
                    self.assignments[clas]['schedule'] = sched
                if re.match("^C(\d)*_Room", line):
                    ass = (line.strip()).split(' = ')
                    clas = ((ass[0].split('_'))[0])[1:]
                    room = ass[1][:-1]
                    if clas not in self.assignments.keys():
                        self.assignments[clas] = {}
                    self.assignments[clas]['room'] = room
                if re.match("^% time elapsed", line):
                    self.runtime = (line.split(' '))[3]
                if re.match(".*Penalty = .*", line):
                    penalty_id = (line.split(' '))[0]
                    penalty = ((line.split(' '))[2])[0:-2]
                    if penalty_id not in self.penalties.keys():
                        self.penalties[penalty_id] = []
                    self.penalties[penalty_id].append(int(penalty))

    def print_stats(self):
        # Find obj value
        obj = 0
        for p in self.penalties.keys():
            obj += self.penalties[p][-1]

        print("Best found: {}".format(obj))
        for p in self.penalties.keys():
            print(" - {}: {}".format(p, self.penalties[p][-1]))


    def get_students(self, clas):
        res = []
        for stu in self.inst.students:
            if int(clas) in self.inst.students[stu]['classes']:
                res.append(stu[1:])
        return res 



    def write_result(self, resfile):
        with open(resfile,'w') as f:
            f.write("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE solution PUBLIC "-//ITC 2019//DTD Problem Format/EN" "http://www.itc2019.org/competition-format.dtd">
            """)
            f.write("""
<solution name="{}"
    runtime="{}"
    cores="{}"
    technique="{}"
    author="{}"
    institution="{}"
    country="{}">\n""".format(self.instance_name,
                              self.runtime,
                              self.cores,
                              self.technique,
                              self.author,
                              self.institution,
                              self.country)
            )
            for ass in self.assignments:
                for s in self.inst.unique_schedules:
                    if self.inst.unique_schedules[s].id == int(self.assignments[ass]['schedule']):
                        sched = self.inst.unique_schedules[s]
                        break
                    
                if 'room' not in self.assignments[ass].keys():
                    f.write('    <class id="{}" days="{}" start="{}" weeks="{}">'.format(
                        ass,
                        sched.days.to01(),
                        sched.start,
                        sched.weeks.to01())
                    )
                else:
                    f.write('    <class id="{}" days="{}" start="{}" weeks="{}" room="{}">'.format(
                        ass,
                        sched.days.to01(),
                        sched.start,
                        sched.weeks.to01(),
                        self.assignments[ass]['room'])
                    )
                for stu in self.get_students(ass):
                    f.write('\n        <student id="{}" />'.format(stu))
                

                f.write("\n    </class>\n")
            f.write("</solution>")






