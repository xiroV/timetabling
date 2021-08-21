import bitarray
import itertools
import math
import time
from status import WriterStatus

class DznWriter:
    def __init__(self, inst):
        self.courses = inst.courses
        self.rooms = inst.rooms
        self.students = inst.students
        self.numWeeks = inst.numWeeks
        self.numDays = inst.daysPerWeek
        self.schedules = inst.schedules
        self.distributions = inst.distributions

    def get_schedules(self, cid):
        res = []
        for s in self.schedules:
            if s['class'] == cid:
                res.append(s)

        return res

    def write_classes(self, f):
        stat = WriterStatus("Classes")
        i = 0
        f.write("Classes = {")
        for course in self.courses:
            for config in self.courses[course]:
                for subpart in self.courses[course][config]:
                    for classes in self.courses[course][config][subpart]:
                        f.write("C{}, ".format(classes))
                        i += 1
        f.write("};\n\n")
        stat.done(i)

    def write_max_violations(self, f):
        # Find largest set of classes for SameRoom dist
        for d_type in self.distributions.keys():
            n = 0
            for dist in self.distributions[d_type]:
                if n < len(dist['classes']):
                    n = len(dist['classes'])

            if n == 0:
                max_viol = 0
            else:
                max_viol = math.factorial(n)/(math.factorial(2)*math.factorial(n-2))
            print("max{}Violations = {};".format(d_type, math.ceil(max_viol)))
            f.write("max{}Violations = {};\n".format(d_type, math.ceil(max_viol)))

    def write_same_starts(self, f):
        stat = WriterStatus("SameStarts")
        i = 0
        found = {}

        for dist_type in ["SameStart"]:
            for dist in self.distributions[dist_type]:
                for c1_id,c2_id in itertools.combinations(dist['classes'], 2):
                    c1_s = self.get_schedules(c1_id)
                    c2_s = self.get_schedules(c2_id)

                    for s1,s2 in itertools.product(c1_s, c2_s):
                        if not s1['id'] in found.keys():
                            found[s1['id']] = []
                            #print(" - SameTime {}".format(i), end="\r")
                            i += 1
                        if s1['class'] != s2['class']:
                            if s1['start'] == s2['start']:
                                if not s2['id'] in found[s1['id']]:
                                    found[s1['id']].append(s2['id'])

        f.write("SameStarts = [\n")
        for s1 in self.schedules:
            f.write("{")
            if s1['id'] in found.keys():
                for s2 in found[s1['id']]:
                    f.write("{}, ".format(s2))
                    #f.write("  {}, {} |\n".format(s1,s2))
            f.write("},\n")
        f.write("];\n")




        """f.write("SameStarts = [|\n")
        for dist in self.distributions['SameStart']:
            for clas in dist['classes']:
                for s1,s2 in itertools.combinations(self.schedules, 2):
                    if s1['class'] == clas:
                        if s1['id'] != s2['id'] and s2['class'] in dist['classes']:
                            if s1['start'] == s2['start']:
                                f.write("  {}, {} |\n".format(s1['id'],s2['id']))
                                i += 1
        f.write("|];\n")"""

        stat.done(i)

    def write_same_time(self, f):
        stat = WriterStatus("SameTime")
        i = 1
        found = {}

        for dist_type in ["SameTime", "DifferentTime"]:
            for dist in self.distributions[dist_type]:
                for c1_id,c2_id in itertools.combinations(dist['classes'], 2):
                    c1_s = self.get_schedules(c1_id)
                    c2_s = self.get_schedules(c2_id)

                    for s1,s2 in itertools.product(c1_s, c2_s):
                        if not s1['id'] in found.keys():
                            found[s1['id']] = []
                            #print(" - SameTime {}".format(i), end="\r")
                            i += 1
                        if s1['class'] != s2['class']:
                            s1_end = s1['start'] + s1['length']
                            s2_end = s2['start'] + s2['length']
                            if (s1['start'] <= s2['start'] and s2_end <= s1_end) or (s2['start'] <= s1['start'] and s1_end <= s2_end):
                                if not s2['id'] in found[s1['id']]:
                                    found[s1['id']].append(s2['id'])
                                    #print("SameTime: found {}:{} , {}:{}".format(s1['class'],s1['id'],s2['class'],s2['id']))

        #print(found)

        f.write("SameTime = [\n")
        for s1 in self.schedules:
            f.write("{")
            if s1['id'] in found.keys():
                for s2 in found[s1['id']]:
                    f.write("{}, ".format(s2))
                    #f.write("  {}, {} |\n".format(s1,s2))
            f.write("},\n")
        f.write("];\n")

        """for dist_type in ["SameTime", "DifferentTime"]:
            for dist in self.distributions[dist_type]:
                for s1_id,s2_id in itertools.combinations(dist['classes'], 2):
                    s1 = self.get_schedule(s1_id)
                    s2 = self.get_schedule(s2_id)
                    if not s1['id'] in found.keys():
                        found[s1['id']] = []
                        print(" - SameTime {}".format(i), end="\r")
                        i += 1
                    if s1['class'] != s2['class']:
                        s1_end = s1['start'] + s1['length']
                        s2_end = s2['start'] + s2['length']
                        if (s1['start'] <= s2['start'] and s2_end <= s1_end) or (s2['start'] <= s1['start'] and s1_end <= s2_end):
                            if not s2['id'] in found[s1['id']]:
                                found[s1['id']].append(s2['id'])

        f.write("SameTime = [|\n")
        for s1 in found.keys():
            for s2 in found[s1]:
                f.write("  {}, {} |\n".format(s1,s2))
        f.write("|];\n")"""



        """for dist_type in ["SameTime", "DifferentTime"]:
            for s1,s2 in itertools.combinations(self.schedules, 2):
                for dist in self.distributions[dist_type]:
                    for clas in dist['classes']:
                        if s1['class'] == clas and s2['class'] in dist['classes']:
                            if not s1['id'] in found.keys():
                                found[s1['id']] = []
                                print(" - SameTime {}".format(i), end="\r")
                                i += 1
                            if s1['id'] != s2['id']:
                                if s1['class'] != s2['class']:
                                    s1_end = s1['start'] + s1['length']
                                    s2_end = s2['start'] + s2['length']
                                    if (s1['start'] <= s2['start'] and s2_end <= s1_end) or (s2['start'] <= s1['start'] and s1_end <= s2_end):
                                        if not s2['id'] in found[s1['id']]:
                                            found[s1['id']].append(s2['id'])

        f.write("SameTime = [|\n")
        for s1 in found.keys():
            for s2 in found[s1]:
                f.write("  {}, {} |\n".format(s1,s2))
        f.write("|];\n")"""


        """i = 1
        f.write("SameTime = [\n")
        for s1 in self.schedules:
            print(" - SameTime {}/{}".format(i, len(self.schedules)), end="\r")
            f.write("  {")
            for dist_type in self.distributions.keys():
                if dist_type in ['SameTime', 'DifferentTime']:
                    for dist in self.distributions[dist_type]:
                        for clas in dist['classes']:
                            if s1['class'] == clas:
                                s1_end = s1['start'] + s1['length']
                                for s2 in self.schedules:
                                    if s2['class'] in dist['classes']:
                                        if s1['id'] != s2['id']:
                                            s2_end = s2['start'] + s2['length']
                                            if (s1['start'] <= s2['start'] and s2_end <= s1_end) or (s2['start'] <= s1['start'] and s1_end <= s2_end):
                                                f.write("{}, ".format(s2['id']))
            f.write("},\n")
            i+=1
        f.write("];\n")"""
        stat.done(i)


    def write_schedule_starts(self, f):
        stat = WriterStatus("ScheduleStarts")
        start_time = time.time()
        i = 0
        f.write("ScheduleStarts = [")
        for schedule in self.schedules:
            f.write("{}, ".format(schedule['start']))
            i += 1
        f.write("];\n");
        stat.done(i)

    def write_schedule_lengths(self, f):
        stat = WriterStatus("ScheduleLengths")
        start_time = time.time()
        i = 0
        f.write("ScheduleLengths = [")
        for schedule in self.schedules:
            f.write("{}, ".format(schedule['length']))
            i+= 1
        f.write("];\n");
        stat.done(i)

    def write_rooms(self, f):
        stat = WriterStatus("Rooms")
        i = 0
        f.write("Rooms = {") 
        for r in self.rooms:
            if r != "None":
                f.write("R{}, ".format(r))
            else: 
                f.write("{}, ".format(r))
            i+=1
        f.write("None };\n\n")
        stat.done(i)

    def write_room_distances(self, f):
        stat = WriterStatus("RoomDistances")
        i = 0
        f.write("RoomDistances = [|\n");
        for room1 in self.rooms:
            for room2 in self.rooms:
                distance = self.rooms[room1]['travel'][room2]
                f.write("{}, ".format(distance))
                i += 1
            f.write("{}, ".format(0))
            f.write("|\n")
        for room2 in self.rooms:
            f.write("{}, ".format(0))
        f.write("{}, ".format(0))
        f.write("|\n")
        f.write("|];\n")
        stat.done(i)

    def write_distributions(self, f):
        print(" - Distributions")
        for dtype in self.distributions:
            print("   {} {}".format(len(self.distributions[dtype]), dtype))
            #print("    {}".format(dtype))
            f.write("{}Hard = [\n".format(dtype)) 
            for d in self.distributions[dtype]:
                if d['required']:
                    cids = ", ".join(["C" + str(cid) for cid in d['classes']])
                    f.write("{" + cids + "},\n")
            f.write("];\n")

            f.write("{}Soft = [\n".format(dtype)) 
            penalties = []
            for d in self.distributions[dtype]:
                if not d['required']:
                    cids = ", ".join(["C" + str(cid) for cid in d['classes']])
                    penalties.append(d['penalty'])
                    f.write("{" + cids + "},\n")
            f.write("];\n")

            f.write("{}Penalties = [".format(dtype)) 
            for penalty in penalties:
                f.write("{} ,".format(penalty))
            f.write("];\n\n")

    def write_schedules(self, f):
        stat = WriterStatus("Schedules")
        start_time = time.time()
        f.write("Schedules = {") 
        sid = 1
        for schedule in self.schedules:
            f.write(" T{},".format(sid))
            sid += 1
        f.write("};\n\n")
        stat.done(sid-1)

    def write_class_schedules(self, f):
        stat = WriterStatus("Schedules")
        start_time = time.time()
        f.write("ClassSchedules = [") 
        sid = 1
        for course in self.courses:
            for config in self.courses[course]:
                for subpart in self.courses[course][config]:
                    for classes in self.courses[course][config][subpart]:
                        f.write("{")
                        for schedule in self.courses[course][config][subpart][classes]['schedules']:
                            f.write(" T{},".format(sid))
                            sid += 1
                        f.write("},\n")
        f.write("];\n\n")
        stat.done(sid-1)

    def write_schedule_overlaps(self, f):
        stat = WriterStatus("ScheduleOverlaps")
        num_schedules = len(self.schedules)
        start_time = time.time()
        found = {}
        snum = 1
        """for s1 in self.schedules:
            print(" - ScheduleOverlaps {}/{}".format(snum,num_schedules), end="\r")
            overlaps = []

            if s1['id'] not in found.keys():
                found[s1['id']] = []

            s1_start = s1['start']
            s1_end = s1_start + s1['length']

            for s2 in self.schedules:
                if s1['class'] != s2['class']:

                    s2_start = s2['start']
                    s2_end = s2_start + s2['length']

                    # Time overlap
                    if (s1_end > s2_start and s1_start <= s2_start) \
                       or (s2_end > s1_start and s2_start <= s1_start) \
                       or (s2_start <= s1_start and s2_end > s1_end) \
                       or (s1_start <= s2_start and s1_end > s2_end):
                        # Week overlap
                        if (s1['weeks'] & s2['weeks']).any():
                            # Day overlap
                            if (s1['days'] & s2['days']).any():
                                if s2['id'] not in found[s1['id']]:
                                    found[s1['id']].append(s2['id'])
                                    overlaps.append("{}".format(s2['id']))

            #f.write("{" + ", ".join(overlaps) + "},\n")
            for o in overlaps:
                f.write("  {}, {} |\n".format(s1['id'], o))
            snum += 1"""


        found = {}
        for s1,s2 in itertools.combinations(self.schedules, 2):
            if s1['id'] not in found.keys():
                snum += 1
                stat.update("{}/{}".format(snum,num_schedules))
                found[s1['id']] = []
                s1_start = s1['start']
                s1_end = s1_start + s1['length']

            if s1['class'] != s2['class']:

                # The two classes must have one or more feasible rooms in common.
                if len(set(s1['avail_rooms']) & set(s2['avail_rooms'])) > 0:

                    s2_start = s2['start']
                    s2_end = s2_start + s2['length']

                    # Time overlap
                    if (s1_end > s2_start and s1_start <= s2_start) \
                       or (s2_end > s1_start and s2_start <= s1_start) \
                       or (s2_start <= s1_start and s2_end > s1_end) \
                       or (s1_start <= s2_start and s1_end > s2_end):
                        # Week overlap
                        if (s1['weeks'] & s2['weeks']).any():
                            # Day overlap
                            if (s1['days'] & s2['days']).any():
                                if s2['id'] not in found[s1['id']]:
                                    found[s1['id']].append(s2['id'])

        f.write("ScheduleOverlaps = [\n")
        for s1 in found:
            f.write("  {{ {} }},\n".format(" ,".join(found[s1])))
        f.write("{}\n];\n\n")

        stat.done(snum)

    def write_schedule_precedences(self, f):
        stat = WriterStatus("Precedences")
        num_schedules = len(self.schedules)
        f.write("Precedences = [\n")
        snum = 1
        for s1 in self.schedules:
            stat.update("{}/{}".format(snum,num_schedules))
            precede = []

            for dist in self.distributions['Precedence']:
                for clas in dist['classes']:
                    if s1['class'] == clas:

                        s1_end = s1['start'] + s1['length']

                        for s2 in self.schedules:
                            if s1['class'] != s2['class']:
                                s2['start']

                                # Precede by week
                                if s1['weeks'] < s2['weeks']:
                                    precede.append("{}".format(s2['id'])) 
                                elif s1['weeks'] == s2['weeks']:
                                    # Precede by day
                                    if s1['days'] < s2['days']:
                                        precede.append("{}".format(s2['id'])) 
                                    elif s1['days'] == s2['days']:
                                        # Precede by time
                                        if s1_end <= s2['start']:
                                            precede.append("{}".format(s2['id'])) 

            f.write("{" + ", ".join(precede) + "},\n")
            snum += 1
        f.write("];\n\n")

        stat.done(snum)
 


    def write_class_rooms(self, f):
        stat = WriterStatus("ClassRooms")
        f.write("ClassRooms = [\n") 
        i = 0
        for course in self.courses:
            for config in self.courses[course]:
                for subpart in self.courses[course][config]:
                    for classes in self.courses[course][config][subpart]:
                        f.write("{")
                        if len(self.courses[course][config][subpart][classes]['rooms']) > 0:
                            for room in self.courses[course][config][subpart][classes]['rooms']:
                                if room != "None":
                                    f.write(" R{},".format(room))
                                else:
                                    f.write(" {},".format(room))
                        else:
                            f.write(" {},".format("None"))
                        f.write("},\n")
                        i += 1
        f.write("];\n\n")
        stat.done(i)

    def write_class_room_penalties(self, f):
        stat = WriterStatus("ClassRoomPenalties")
        i = 0
        f.write("ClassRoomPenalties = [|\n") 
        for course in self.courses:
            for config in self.courses[course]:
                for subpart in self.courses[course][config]:
                    for classes in self.courses[course][config][subpart]:
                        #If no rooms are specified, all rooms should be added with a penalty of 0
                        if len(self.courses[course][config][subpart][classes]['rooms']) == 0:
                            for room in self.rooms:
                                f.write(" {},".format(0))
                            f.write(" {},".format(0))
                        else:
                            for room in self.rooms:
                                if str(room) in self.courses[course][config][subpart][classes]['rooms']:
                                    f.write(" {},".format(self.courses[course][config][subpart][classes]['rooms'][str(room)]['penalty']))
                                else:
                                    f.write(" {},".format(0))
                            f.write(" {},".format(0))
                        f.write("|\n")
                        i += 1
        f.write("|];\n\n")
        stat.done(i)

    def write_class_schedule_penalties(self, f):
        stat = WriterStatus("ClassSchedulePenalties")
        start_time = time.time()
        f.write("ClassSchedulePenalties = [|\n") 
        i = 1
        for course in self.courses:
            stat.update("{}/{}".format(i, len(self.courses)))
            for config in self.courses[course]:
                for subpart in self.courses[course][config]:
                    for classes in self.courses[course][config][subpart]:
                        for schedule in self.schedules:
                            if schedule['class'] == int(classes):
                                f.write(" {},".format(schedule['penalty']))
                            else:
                                f.write(" {},".format(0))
                        f.write("|\n")
            i += 1
        f.write("|];\n")
        stat.done(i)

    def write_weeks(self, f):
        f.write("Weeks = {")
        for i in range(1, self.numWeeks+1):
            f.write("W{},".format(i))
        f.write("};\n")

    def write_days(self, f):
        f.write("Days = {")
        for i in range(1, self.numDays+1):
            f.write("D{},".format(i))
        f.write("};\n")

    def write_schedule_weeks(self, f):
        stat = WriterStatus("ScheduleDays")
        i = 0
        f.write("ScheduleWeeks = [\n")
        for s in self.schedules:
            f.write("  {")
            weekNum = 1;
            for inWeek in s['weeks'].to01():
                if inWeek == "1":
                    f.write("W{}, ".format(weekNum))
                weekNum += 1
            f.write("},\n")
            i+=1
        f.write("];\n")
        stat.done(i)

    def write_schedule_days(self, f):
        stat = WriterStatus("ScheduleDays")
        i = 0
        start_time = time.time()
        f.write("ScheduleDays = [\n")
        for s in self.schedules:
            f.write("  {")
            dayNum = 1;
            for inWeek in s['days'].to01():
                if inWeek == "1":
                    f.write("D{}, ".format(dayNum))
                    i+=1
                dayNum += 1
            f.write("},\n")
        f.write("];\n")
        stat.done(i)

    def write_same_days(self, f):
        stat = WriterStatus("SameDays")
        start_time = time.time()
        i = 1
        found = {}

        for dist_type in ["SameDays", "DifferentDays", "SameAttendees"]:
            for dist in self.distributions[dist_type]:
                for c1_id,c2_id in itertools.combinations(dist['classes'], 2):
                    c1_s = self.get_schedules(c1_id)
                    c2_s = self.get_schedules(c2_id)

                    for s1,s2 in itertools.product(c1_s, c2_s):
                        if not s1['id'] in found.keys():
                            found[s1['id']] = []
                            stat.update(i)
                            i += 1
                        if ((s1['days'] | s2['days']) == s1['days']) or ((s1['days'] | s2['days']) == s2['days']):
                            if not s2['id'] in found[s1['id']]:
                                found[s1['id']].append(s2['id'])

        f.write("SameDays = [\n")
        for s1 in self.schedules:
            f.write("  {")
            if s1['id'] in found.keys():
                for s2 in found[s1['id']]:
                    f.write("{},\n".format(s2))
            f.write("},\n")

        f.write("];\n")




        """for dist_type in ["SameDays", "DifferentDays", "SameAttendees"]:
            for dist in self.distributions[dist_type]:
                for s1_id,s2_id in itertools.combinations(dist['classes'], 2):
                    s1 = self.get_schedule(s1_id)
                    s2 = self.get_schedule(s2_id)
                    if not s1['id'] in found.keys():
                        found[s1['id']] = []
                        print(" - SameDays {}".format(i), end="\r")
                        i += 1
                    if s1['class'] != s2['class']:
                        if ((s1['days'] | s2['days']) == s1['days']) or ((s1['days'] | s2['days']) == s2['days']):
                            if not s2['id'] in found[s1['id']]:
                                found[s1['id']].append(s2['id'])


        f.write("SameDays = [|\n")
        for s1 in found.keys():
            for s2 in found[s1]:
                f.write("  {}, {} |\n".format(s1,s2))

        f.write("|];\n")"""



        # SameDays
        """for dist_type in ["SameDays", "DifferentDays", "SameAttendees"]:
            for s1,s2 in itertools.combinations(self.schedules, 2):
                for dist in self.distributions[dist_type]:
                    for clas in dist['classes']:
                        if s1['class'] == clas and s2['class'] in dist['classes']:
                            if not s1['id'] in found.keys():
                                found[s1['id']] = []
                                print(" - SameDays {}".format(i), end="\r")
                                i += 1
                            if s1['id'] != s2['id']:
                                if s1['class'] != s2['class']:
                                    if ((s1['days'] | s2['days']) == s1['days']) or ((s1['days'] | s2['days']) == s2['days']):
                                        if not s2['id'] in found[s1['id']]:
                                            found[s1['id']].append(s2['id'])

        f.write("SameDays = [|\n")
        for s1 in found.keys():
            for s2 in found[s1]:
                f.write("  {}, {} |\n".format(s1,s2))

        f.write("|];\n")"""
        stat.done(i-1)


    def write_same_weeks(self, f):
        stat = WriterStatus("SameWeeks")
        i = 1
        found = {}

        for dist_type in ["SameWeeks", "DifferentWeeks", "SameAttendees"]:
            for dist in self.distributions[dist_type]:
                for c1_id,c2_id in itertools.combinations(dist['classes'], 2):
                    c1_s = self.get_schedules(c1_id)
                    c2_s = self.get_schedules(c2_id)

                    for s1,s2 in itertools.product(c1_s, c2_s):
                        if not s1['id'] in found.keys():
                            found[s1['id']] = []
                            stat.update(i)
                            i += 1
                        if s1['class'] != s2['class']:
                            if ((s1['weeks'] | s2['weeks']) == s1['weeks']) or ((s1['weeks'] | s2['weeks']) == s2['weeks']):
                                if not s2['id'] in found[s1['id']]:
                                    found[s1['id']].append(s2['id'])


        """for dist_type in ['SameWeeks', 'DifferentWeeks', 'SameAttendees']:
            for s1,s2 in itertools.combinations(self.schedules, 2):
                for dist in self.distributions[dist_type]:
                    for clas in dist['classes']:
                        if s1['class'] == clas and s2['class'] in dist['classes']:
                            if not s1['id'] in found.keys():
                                found[s1['id']] = []
                                print(" - SameWeeks {}".format(i), end="\r")
                                i += 1
                            if s1['id'] != s2['id']:
                                if s1['class'] != s2['class']:
                                    if ((s1['weeks'] | s2['weeks']) == s1['weeks']) or ((s1['weeks'] | s2['weeks']) == s2['weeks']):
                                        if not s2['id'] in found[s1['id']]:
                                            found[s1['id']].append(s2['id'])"""

        f.write("SameWeeks = [\n")
        for s1 in self.schedules:
            f.write("{")
            if s1['id'] in found.keys():
                for s2 in found[s1['id']]:
                    f.write("{},".format(s2))
                    #f.write("  {}, {} |\n".format(s1,s2))
            f.write("},\n")

        f.write("];\n")


        """for s1 in self.schedules:
            this_set = []
            print(" - SameWeeks {}/{}".format(i, len(self.schedules)), end="\r")
            f.write("  {")
            for dist_type in self.distributions.keys():
                if dist_type in ['SameWeeks', 'DifferentWeeks', 'SameAttendees']:
                    for dist in self.distributions[dist_type]:
                        for clas in dist['classes']:
                            if s1['class'] == clas:
                                for s2 in self.schedules:
                                    if s2['class'] in dist['classes']:
                                        if s1['id'] != s2['id']:
                                            if ((s1['weeks'] | s2['weeks']) == s1['weeks']) or ((s1['weeks'] | s2['weeks']) == s2['weeks']):
                                                if not s2['id'] in this_set:
                                                    this_set.append(s2['id'])
            for sch in this_set:
                f.write("{}, ".format(sch))
            f.write("},\n")
            i += 1
        f.write("];\n")
        print()"""

        stat.done(i)


    def write_room_available(self, f):
        stat = WriterStatus("RoomUnavailable")
        i = 0
        f.write("RoomUnavailable = [\n") 
        for schedule in self.schedules:
            f.write("  {")

            s_end = schedule['start'] + schedule['length']

            for room in self.rooms:
                available = True
                for room_unavail in self.rooms[room]['unavailable']:
                    ru_end = room_unavail['start'] + room_unavail['length']

                    # Week overlap
                    if (schedule['weeks'] & room_unavail['weeks']).any():
                        # Day overlap
                        if (schedule['days'] & room_unavail['days']).any():
                            # Time overlap
                            if (s_end > room_unavail['start'] and schedule['start'] <= room_unavail['start']) \
                                or (ru_end > schedule['start'] and room_unavail['start'] <= schedule['start']) \
                                or (room_unavail['start'] <= schedule['start'] and ru_end > s_end) \
                                or (schedule['start'] <= room_unavail['start'] and s_end > ru_end):
                                    available = False
                                    break

                if not available:
                    f.write("R{}, ".format(room))
                    i += 1

            f.write("},\n")
        f.write("];\n\n")
        stat.done(i)

    def write_dzn(self, outfile):
        print("Writing data file")
        with open(outfile, 'w') as f:
            self.write_max_violations(f)
            self.write_classes(f)
            self.write_weeks(f)
            self.write_days(f)
            self.write_schedules(f)
            self.write_schedule_starts(f)
            self.write_same_starts(f)
            self.write_same_time(f)
            self.write_schedule_lengths(f)
            self.write_schedule_days(f)
            self.write_same_days(f)
            self.write_schedule_weeks(f)
            self.write_same_weeks(f)
            self.write_class_schedules(f)
            self.write_class_schedule_penalties(f)
            self.write_schedule_overlaps(f)
            self.write_schedule_precedences(f)
            self.write_rooms(f)
            self.write_class_rooms(f)
            self.write_room_distances(f)
            self.write_room_available(f)
            self.write_class_room_penalties(f)
            self.write_distributions(f)
            #self.write_workday_pars(f)
            #self.write_mingap_pars(f)
            self.write_dist_parameters_1d(f)
            self.write_dist_parameters_2d(f)

    # Writing the parameters for the distribution constraints that take one parameter
    def write_dist_parameters_1d(self, f):
        par_dists = ["WorkDay", "MinGap", "MaxDays", "MaxDayLoad"]

        for dist_name in par_dists:
            # Parameters for hard constraints
            f.write(dist_name + "HardParameters = [")
            for dist in self.distributions[dist_name]:
                if dist['required']:
                    f.write("{}, ".format(dist['params'][0])) 
            f.write("];\n")

            # Parameters for soft constraints
            f.write(dist_name + "SoftParameters = [")
            for dist in self.distributions[dist_name]:
                if not dist['required']:
                    f.write("{}, ".format(dist['params'][0])) 
            f.write("];\n")

    # Writing the parameters for the distribution constraints that takes two parameters
    def write_dist_parameters_2d(self, f):
        par_dists = ["MaxBreaks", "MaxBlock"]

        for dist_name in par_dists:
            # Parameters for hard constraints
            f.write(dist_name + "HardParameters = [|")
            for dist in self.distributions[dist_name]:
                if dist['required']:
                    f.write("{},{} | ".format(dist['params'][0], dist['params'][1])) 
            f.write("|];\n")

            # Parameters for soft constraints
            f.write(dist_name + "SoftParameters = [|")
            for dist in self.distributions[dist_name]:
                if not dist['required']:
                    f.write("{},{} |".format(dist['params'][0], dist['params'][1])) 
            f.write("|];\n")

# Below is not used anymore, but kept for now
        '''did = 0
        # Hard constraints
        for dist in self.distributions["MinGap"]:
            f.write("MinGap{}Schedules = [\n".format(did))
            for s1 in self.schedules:
                f.write("{")
                for clas in dist['classes']:
                    if clas == s1['class']:
                        for s2 in self.schedules:
                            if (not (s1['days'] & s2['days']).any()) \
                              or (not (s1['days'] & s2['days']).any()) \
                              or (s1['start'] + s1['length'] + dist['params'][0] <= s2['start']) \
                              or (s2['start'] + s2['length'] + dist['params'][0] <= s1['start']):
                                f.write("{}, ".format(s2['id']))
                f.write("},")
            f.write("];\n")
            did += 1'''
'''
    def write_var_workday(self, f):
        print("WOOHOOO")
        exit(0)
        did = 0
        # Hard constraints
        for dist in self.distributions["WorkDay"]:
            f.write("array[Schedules] of set of Schedules: WorkDay{}Schedules;\n".format(did))
            if dist['required']:
                f.write("array[1..{}] of Classes: WorkDayHard{} = [".format(len(dist['classes']), did))
                f.write(", ".join(["C" + str(d) for d in dist['classes']]))
                f.write("];")
                
                f.write("""
constraint forall(c1,c2 in WorkDayHard{0})(
    ScheduledTime[c2] in WorkDay{0}Schedules[ScheduledTime[c1]]
);
                """.format(did,dist['params'][0])) 

            did += 1


    def write_var_mingap(self, f):
        did = 0
        # Hard constraints
        for dist in self.distributions["MinGap"]:
            f.write("array[Schedules] of set of Schedules: MinGap{}Schedules;\n".format(did))
            if dist['required']:
                f.write("array[1..{}] of Classes: MinGapHard{} = [".format(len(dist['classes']), did))
                f.write(", ".join(["C" + str(d) for d in dist['classes']]))
                f.write("];")
                
                f.write("""
constraint forall(c1,c2 in MinGapHard{0})(
    ScheduledTime[c2] in MinGap{0}Schedules[ScheduledTime[c1]]
);
                """.format(did,dist['params'][0])) 

            did += 1

    def write_var_maxdays(self, f):
        did = 0
        # Hard constraints
        for dist in self.distributions["MaxDays"]:
            if dist['required']:
                f.write("array[int] of Classes: MaxDaysHard{} = [".format(did))
                f.write(", ".join(["C" + str(d) for d in dist['classes']]))
                f.write("];")
                
                f.write("""
constraint sum(c in MaxDaysHard{0})(length(ScheduleDays[ScheduledTime[c]])) <= {1};
                """.format(did,dist['params'][0])) 

                did += 1


    # Method for writing the special/variable distributions
    def write_var_distributions(self, outfile):
        print("Writing variable distributions file")
        with open(outfile, 'w') as f:
            for dist in self.distributions:
                if dist == "WorkDay" and len(self.distributions[dist])>0:
                    self.write_var_workday(f)
                elif dist == "MinGap" and len(self.distributions[dist])>0:
                    self.write_var_mingap(f)
                elif dist == "MaxDays" and len(self.distributions[dist])>0:
                    self.write_var_maxdays(f)
                elif dist == "MaxDayLoad" and len(self.distributions[dist])>0:
                    print("TODO: {} constraints not implemented yet".format(dist))
                elif dist == "MaxBreaks" and len(self.distributions[dist])>0:
                    print("TODO: {} constraints not implemented yet".format(dist))
                elif dist == "MaxBlock" and len(self.distributions[dist])>0:
                    print("TODO: {} constraints not implemented yet".format(dist))

'''

