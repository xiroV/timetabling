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

        self.parse_assignments()
        self.get_schedules()

    def parse_assignments(self):
        with open(self.output_file) as f:
            for line in f.readlines():
                if re.match("^A,", line):
                    ass = (line.strip()).split(',')
                    self.assignments[ass[1]] = {}
                    self.assignments[ass[1]]['id'] = ass[1][1:]
                    self.assignments[ass[1]]['schedule'] = ass[2]
                    if ass[3] == "None":
                        self.assignments[ass[1]]['room'] = None
                    else:
                        self.assignments[ass[1]]['room'] = ass[3][1:]
                if re.match("^% time elapsed", line):
                    self.runtime = (line.split(' '))[3]

    def get_schedules(self):
        for ass in self.assignments:
            for sch in self.inst.schedules:
                if sch['id'] == self.assignments[ass]['schedule']:
                    self.assignments[ass]['start'] = sch['start']
                    self.assignments[ass]['length'] = sch['length']
                    self.assignments[ass]['weeks'] = sch['weeks'].to01()
                    self.assignments[ass]['days'] = sch['days'].to01()

    def get_students(self, clas):
        res = []
        for stu in self.inst.students:
            if clas in self.inst.students[stu]['classes']:
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
                if self.assignments[ass]['room'] is None:
                    f.write('    <class id="{}" days="{}" start="{}" weeks="{}">'.format(
                        self.assignments[ass]['id'],
                        self.assignments[ass]['days'],
                        self.assignments[ass]['start'],
                        self.assignments[ass]['weeks'])
                    )
                else:
                    f.write('    <class id="{}" days="{}" start="{}" weeks="{}" room="{}">'.format(
                        self.assignments[ass]['id'],
                        self.assignments[ass]['days'],
                        self.assignments[ass]['start'],
                        self.assignments[ass]['weeks'],
                        self.assignments[ass]['room'])
                    )
                    
                    for stu in self.get_students(self.assignments[ass]['id']):
                        f.write('\n        <student id="{}" />'.format(stu))

                f.write("\n    </class>\n")
            f.write("</solution>")






