import xml.etree.ElementTree as ET
import itertools
from collections import defaultdict 
from bitarray import bitarray
import re
import json
import functools
import schedule
import clas
import time

class Data:
    def __init__(self, file):
        tree = ET.parse(file)
        # Grap problem variables
        root = tree.getroot()
        if root.tag != "problem":
            sys.error("instance does not contain a problem\n")
        
        self.__dict__.update(
            slotsPerDay = int(root.attrib['slotsPerDay']),
            numWeeks = int(root.attrib['nrWeeks']),
            daysPerWeek = int(root.attrib['nrDays']),
            time_id = 1,
            rooms = {},
            weights = {},
            schedules = [],
            courses = {},
            classes = {},
            unique_schedules = {},
            schedule_overlaps = {},
            students = {},
            distributions = {},
            course_tree = {},
        )        

        
        for child in root:
            if child.tag == "rooms":
                self.get_rooms(child)
            elif child.tag == "optimization":
                self.get_weights(child)
            elif child.tag == "courses":
                self.get_courses(child)
                self.build_course_tree()
                self.find_schedules()
                self.find_classes()
            elif child.tag == "distributions":
                self.get_distributions(child)
            elif child.tag == "students":
                self.get_students(child)
            else:
                print("ERROR: Unhandled tag {}".format(child.tag))

        #self.find_schedule_overlaps()

    def find_schedule_overlaps(self):
        print("Finding Schedule Overlaps", end="\r")
        t1 = time.time()
        sid = 0
        for s1,s2 in itertools.product(self.unique_schedules, repeat=2):
            if s1 not in self.schedule_overlaps.keys():
                self.schedule_overlaps[s1] = {} 
            if s2 not in self.schedule_overlaps.keys():
                self.schedule_overlaps[s2] = {} 

            if self.unique_schedules[s1].overlap_with(self.unique_schedules[s2]):
                self.schedule_overlaps[s1][s2] = True
                self.schedule_overlaps[s2][s1] = True
            else:
                self.schedule_overlaps[s1][s2] = False
                self.schedule_overlaps[s2][s1] = False
        print("Found Schedule Overlaps in {} seconds".format(round(time.time()-t1,3)))


    def find_schedules(self):
        schedule_id = 1
        for course in self.courses:
            for config in self.courses[course]:
                for subpart in self.courses[course][config]:
                    for clas in self.courses[course][config][subpart]:
                        for sch in self.courses[course][config][subpart][clas]['schedules']:
                            s = self.courses[course][config][subpart][clas]['schedules'][sch]

                            s['id'] = "T"+str(schedule_id)
                            s['course'] = course
                            s['config'] = config
                            s['subpart'] = subpart
                            s['class'] = int(clas)
                            s['avail_rooms'] = [r for r in self.courses[course][config][subpart][clas]['rooms']]
                            self.schedules.append(s)

                            schedule_id += 1


    def find_classes(self):
        # First we find all the unique schedules
        sid = 1
        for s in self.schedules:
            sched = schedule.Schedule(sid, s['weeks'], s['days'], s['start'], s['length'])
            if sched.key() not in self.unique_schedules.keys():
                self.unique_schedules[sched.key()] = sched
                sid += 1


        # Then we get the classes, which contain the keys for the schedules
        for course in self.courses:
            for config in self.courses[course]:
                for subpart in self.courses[course][config]:
                    for cid in self.courses[course][config][subpart]:
                        self.classes[int(cid)] = clas.Clas(int(cid))
                        # Write schedules
                        for s in self.schedules:
                            if s['class'] == int(cid):
                                sched = schedule.Schedule(0, s['weeks'], s['days'], s['start'], s['length'])
                                self.classes[int(cid)].add_schedule(sched.key())
                                self.classes[int(cid)].schedule_penalty[sched.key()] = s['penalty']

                        for r in self.courses[course][config][subpart][cid]['rooms']:
                            self.classes[int(cid)].add_room_penalty(r, self.courses[course][config][subpart][cid]['rooms'][r]['penalty'])
                            self.classes[int(cid)].add_room(int(r))
                            self.classes[int(cid)].limit = self.courses[course][config][subpart][cid]['limit'] 

    def build_course_tree(self):
        # Initialize/build tree from only top-level/parent classes
        for course in self.courses:
            self.course_tree[course] = {}
            for conf in self.courses[course]:
                self.course_tree[course][conf] = {}
                for subp in self.courses[course][conf]:
                    self.course_tree[course][conf][subp] = {}
                    for clas in self.courses[course][conf][subp]:
                        if self.courses[course][conf][subp][clas]['parent'] is None:
                            self.course_tree[course][conf][subp][clas] = {}
                            #self.course_tree[course][conf][clas] = {}

        # Add children
        for course in self.courses:
            for conf in self.courses[course]:
                subparts = []
                for subp in self.courses[course][conf]:
                    subparts.append(subp)
                    for clas in self.courses[course][conf][subp]:
                        parent = self.courses[course][conf][subp][clas]['parent']
                        if parent is not None:
                            for sp in subparts:
                                res = self.add_child_class(clas, parent, self.course_tree[course][conf][sp])
                                #res = self.add_child_class(clas, parent, self.course_tree[course][conf])
                                if res is not None:
                                    self.course_tree[course][conf][sp] = res
                                    #self.course_tree[course][conf] = res
                                    break

    def add_child_class(self, clas, parent, classes):
        new_classes = classes
        for c in classes:
            if c == parent:
                new_classes[c][clas] = {}
                break
            else:
                if len(classes[c]) > 0:
                    res = self.add_child_class(clas, parent, classes[c])
                    if res is not None:
                        new_classes[c] = res
                        break
                else:
                    return None

        return new_classes

    def get_weights(self, root):
        self.weights = {
            'time': int(root.attrib['time']),
            'room': int(root.attrib['room']),
            'distribution': int(root.attrib['distribution']),
            'student': int(root.attrib['student'])
        }

    def match_any(self, patterns, string):
        for p in patterns:
            if re.match(p, string):
                return True
        return False


    def get_distributions(self, root):
        distribution_types = ["SameStart", "SameTime", "DifferentTime", "SameDays", "DifferentDays", "SameWeeks", "DifferentWeeks", "SameRoom", "DifferentRoom", "Overlap", "NotOverlap",
                "SameAttendees", "Precedence", "WorkDay", "MinGap", "MaxDays", "MaxDayLoad", "MaxBreaks", "MaxBlock"]

        for dtype in distribution_types:
            self.distributions[dtype] = []

        special_type_patterns = ["^WorkDay\(\d+\)$", "^MaxDays\(\d+\)$", "^MinGap\(\d+\)$", "^MaxDayLoad\(\d+\)$",
               "^MaxBreaks\(\d+,\d+\)$", "^MaxBlock\(\d+,\d+\)$"]
        for dist in root:
            d = {}
            d['classes'] = []

            # Handle required and penalty
            if 'required' in dist.attrib:
                d['required'] = bool(dist.attrib['required'])
            else:
                d['required'] = False
                if 'penalty' in dist.attrib:
                    d['penalty'] = int(dist.attrib['penalty']) * self.weights['distribution']
                else:
                    print("ERROR: distribution is neither required or has a penalty")
                    exit()

            # Handle distribution type and classes
            for clas in dist:
                d['classes'].append(int(clas.attrib['id']))

            # Sorting the list of classes
            d['classes'].sort()

            if self.match_any(special_type_patterns, dist.attrib['type']):
                d['params'] = []
                params_str = (dist.attrib['type'].split("("))[1]
                params = params_str[0:-1].split(',')
                for p in params:
                    d['params'].append(int(p))
                dtype = (dist.attrib['type'].split("("))[0]
            else:
                dtype = dist.attrib['type']

            self.distributions[dtype].append(d)
        
    def get_rooms(self, root):
        for room in root:
            room_unavail = []
            room_id = int(room.attrib['id'])
            if room_id not in self.rooms.keys():
                self.rooms[room_id] = {}
                self.rooms[room_id]['travel'] = defaultdict(int)
            self.rooms[room_id]['unavailable'] = []
            for attr in room:
                if attr.tag == "travel":
                    self.rooms[room_id]['travel'][int(attr.attrib['room'])] = int(attr.attrib['value'])
                    if int(attr.attrib['room']) not in self.rooms.keys():
                        self.rooms[int(attr.attrib['room'])] = {}
                        self.rooms[int(attr.attrib['room'])]['travel'] = defaultdict(int)
                    self.rooms[int(attr.attrib['room'])]['travel'][room_id] = int(attr.attrib['value'])
                elif attr.tag == "unavailable":
                    self.rooms[room_id]['unavailable'].append( self.get_room_schedule(attr) )
            self.rooms[room_id]['capacity'] = int(room.attrib['capacity'])
        self.rooms[len(self.rooms)+1] = {"unavailable": [], "capacity": 2000, "travel":defaultdict(int)}

    def get_courses(self, root):
        for course in root:
            course_id = "C" + course.attrib['id']
            crs = {}
            for config in course:
                crs[config.attrib['id']] = defaultdict(dict)
                for subpart in config:              
                    crs[config.attrib['id']][subpart.attrib['id']].update( self.get_subpart(subpart) )
            self.courses[course_id] = crs


    def get_subpart(self, subpart):
        subp = {}
        for clas in subpart:
            subp[ clas.attrib['id'] ] = {
                'limit': int(clas.attrib['limit']),
                'attending': 0,
                #'schedules': defaultdict(list),
                'schedules': {},
                #'slots2': defaultdict(list),
                'rooms': {},
                'parent': None if 'parent' not in clas.attrib else clas.attrib['parent']
            }

            cla = subp[ clas.attrib['id'] ]
            time_schedule_id = 0
            for attr in clas:
                if attr.tag == "room":
                    cla['rooms'][attr.attrib['id']] ={"penalty":int(attr.attrib['penalty']) * self.weights['room']}
                elif attr.tag == "time":
                    #cla['schedules'][time_schedule_id].append( self.getTimeSchedule(attr) )
                    cla['schedules'][time_schedule_id] = self.get_time_schedule(attr)
                    time_schedule_id += 1
        return subp


    def get_time_schedule(self,schedule):
        return {
            'weeks': bitarray(schedule.attrib['weeks']), #str(bitarray(schedule.attrib['weeks'])),
            'days':  bitarray(schedule.attrib['days']), #str(bitarray(schedule.attrib['days'])),
            'start': int(schedule.attrib['start']),
            'length': int(schedule.attrib['length']),
            'penalty': int(schedule.attrib['penalty']) * self.weights['time']
        }
    
    def get_room_schedule(self,schedule):
        return {
            'weeks': bitarray(schedule.attrib['weeks']), #str(bitarray(schedule.attrib['weeks'])),
            'days':  bitarray(schedule.attrib['days']), #str(bitarray(schedule.attrib['days'])),
            'start': int(schedule.attrib['start']),
            'length': int(schedule.attrib['length']) * self.weights['room']
        }
 
    def get_students(self, child):
        print("Sectioning students...")
        n = 0
        for student in child:
            print("Sectioning student {}".format(student.attrib['id']), end="\r")
            student_id = "S" + student.attrib['id']
            stud = {}
            stud['classes'] = []
            chosen_classes = []

            # Needed courses
            for course in student:
                course_id = "C" + course.attrib['id']
                crs = self.courses[course_id] if course_id in self.courses else None

                for conf in self.course_tree[course_id]:
                    for subp in self.course_tree[course_id][conf]:
                        if len(self.course_tree[course_id][conf][subp]) > 0:
                            chosen_classes = self.choose_student_classes(self.course_tree[course_id][conf][subp], chosen_classes)

                    if len(chosen_classes) > 0:
                        stud['classes'] = chosen_classes
                        break

            self.students[student_id] = stud
            n += 1


        print("Done sectioning {} students".format(n))


    def choose_student_classes(self, subpart, chosen = []):
        for clas in subpart: 
            if self.classes[int(clas)].attending < self.classes[int(clas)].limit:
                chosen.append(int(clas))
                self.classes[int(clas)].attending += 1
                if len(subpart[clas]) > 0:
                    chosen = self.choose_student_classes(subpart[clas], chosen)
                break
        return chosen


if __name__ == "__main__":
    import sys
    data = Data(sys.argv[1])
