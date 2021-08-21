import clas
import itertools
import bitarray
import schedule
import fzn
from collections import defaultdict
from status import WriterStatus
import time


class FznWriter:
    def __init__(self, instance, include_names=False):
        self.dat = instance
        self.fzn = fzn.Fzn(include_names)
        self.include_soft_vars = True
        self.minimize = True

    def write(self, file_path):
        self.class_schedules()
        self.class_rooms()
        self.schedule_overlaps()
        self.room_available()

        self.same_start()

        self.same_time()
        self.different_time()

        self.same_days()
        self.different_days()

        self.same_weeks()
        self.different_weeks()

        self.same_room()
        self.different_room()

        self.overlap()
        self.not_overlap()

        self.same_attendees()

        # if self.include_soft_vars:
        #    self.student_conflicts()

        self.precedence()

        self.work_day()
        self.min_gap()
        self.max_days()
        self.max_block()
        self.max_breaks()
        self.max_day_load()

        print("Introduced {} vars".format(len(self.fzn.introduced_vars)))
        print("Defined {} vars".format(len(self.fzn.defined_vars)))

        self.objective()

        with open(file_path, 'w') as f:
            self.fzn.write(f)
            self.write_solve(f)

    def precedence(self):
        stat = WriterStatus("Precedences")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        succeeding = defaultdict(set)
        for dist in self.dat.distributions['Precedence']:
            for c1, c2 in itertools.combinations(dist['classes'], 2):
                for s1 in self.dat.classes[c1].schedules:
                    sched1 = self.dat.unique_schedules[s1]
                    for s2 in self.dat.classes[c2].schedules:
                        sched2 = self.dat.unique_schedules[s2]

                        # succeed by week
                        if sched1.first_week() < sched2.first_week():
                            succeeding[sched1.id].add(sched2.id)
                        elif sched1.first_week() == sched2.first_week():
                            # succeed by day
                            if sched1.first_day() < sched2.first_day():
                                succeeding[sched1.id].add(sched2.id)
                            elif sched1.first_day() == sched2.first_day():
                                # succeed by time
                                if sched1.end <= sched2.start:
                                    succeeding[sched1.id].add(sched2.id)

        pruned = 0
        for dist in self.dat.distributions['Precedence']:
            if dist['required']:
                constraint.precedence_hard(dist['classes'], self.fzn, self.dat,
                                           succeeding)
            else:
                if self.include_soft_vars:
                    constraint.precedence_soft(dist['classes'], self.fzn,
                                               self.dat, succeeding,
                                               dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            precedence_penalty = self.fzn.int_var(
                "PrecedencePenalty",
                output=True,
                domain="0..{}".format(sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(precedence_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=precedence_penalty,
                                name="Precedence_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()
        print(" - Pruned {}".format(pruned))

    def overlap(self):
        stat = WriterStatus("Overlap")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["Overlap"]:
            if dist['required']:
                constraint.overlap_hard(dist['classes'], self.fzn, self.dat)
            else:
                if self.include_soft_vars:
                    constraint.overlap_soft(dist['classes'], self.fzn,
                                            self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            overlap_penalty = self.fzn.int_var("OverlapPenalty",
                                               output=True,
                                               domain="0..{}".format(
                                                   sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(overlap_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=overlap_penalty,
                                name="Precedence_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def same_time(self):
        stat = WriterStatus("SameTime")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["SameTime"]:
            if dist['required']:
                constraint.same_time_hard(dist['classes'], self.fzn, self.dat)
            else:
                if self.include_soft_vars:
                    constraint.same_time_soft(dist['classes'], self.fzn,
                                              self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            sametime_penalty = self.fzn.int_var("SameTimePenalty",
                                                output=True,
                                                domain="0..{}".format(
                                                    sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(sametime_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=sametime_penalty,
                                name="SameTime_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def different_time(self):
        stat = WriterStatus("DifferentTime")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["DifferentTime"]:
            if dist['required']:
                constraint.different_time_hard(dist['classes'], self.fzn,
                                               self.dat)
            else:
                if self.include_soft_vars:
                    constraint.different_time_soft(dist['classes'], self.fzn,
                                                   self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            differenttime_penalty = self.fzn.int_var(
                "DifferentTimePenalty",
                output=True,
                domain="0..{}".format(sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(differenttime_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=differenttime_penalty,
                                name="DifferentTime_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def same_start(self):
        stat = WriterStatus("SameStart")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        soft_vars = []
        penalties = []
        for dist in self.dat.distributions["SameStart"]:
            if dist['required']:
                constraint.same_start_hard(dist['classes'], self.fzn, self.dat)
            else:
                if self.include_soft_vars:
                    constraint.same_start_soft(dist['classes'], self.fzn,
                                               self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            samestart_penalty = self.fzn.int_var("SameStartPenalty",
                                                 output=True,
                                                 domain="0..{}".format(
                                                     sum(penalties)))
            penalties.append(-1)
            soft_vars.append(samestart_penalty)
            self.fzn.int_lin_eq(penalties,
                                soft_vars,
                                0,
                                defines=samestart_penalty,
                                name="SameStart_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def same_weeks(self):
        stat = WriterStatus("SameWeeks")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        n = 1
        for dist in self.dat.distributions["SameWeeks"]:
            if dist['required']:
                constraint.same_weeks_hard(dist['classes'], self.fzn, self.dat)
            else:
                if self.include_soft_vars:
                    constraint.same_weeks_soft(dist['classes'], self.fzn,
                                               self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            soft_vars_int = []

            for v in constraint.soft_vars:
                ivar = self.fzn.int_var("{}_int".format(v), domain='0..1')
                self.fzn.bool2int(v,
                                  ivar,
                                  defines="{}_int".format(v),
                                  name="SameWeeks_S")
                soft_vars_int.append(ivar)

            ub = sum(constraint.penalties)
            soft_vars_int.append("SameWeeksPenalty")
            constraint.penalties.append(-1)

            self.fzn.int_var("SameWeeksPenalty",
                             output=True,
                             domain="0..{}".format(ub))
            self.fzn.int_lin_eq(constraint.penalties,
                                soft_vars_int,
                                0,
                                defines="SameWeeksPenalty",
                                name="SameWeeks_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def different_weeks(self):
        stat = WriterStatus("DifferentWeeks")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["DifferentWeeks"]:
            if dist['required']:
                constraint.different_weeks_hard(dist['classes'], self.fzn,
                                                self.dat)
            else:
                if self.include_soft_vars:
                    constraint.different_weeks_soft(dist['classes'], self.fzn,
                                                    self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            diffweeks_penalty = self.fzn.int_var(
                "DifferentWeeksPenalty",
                output=True,
                domain="0..{}".format(sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(diffweeks_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=diffweeks_penalty,
                                name="DifferentWeeks_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def same_days(self):
        stat = WriterStatus("SameDays")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["SameDays"]:
            if dist['required']:
                constraint.same_days_hard(dist['classes'], self.fzn, self.dat)
            else:
                if self.include_soft_vars:
                    constraint.same_days_soft(dist['classes'], self.fzn,
                                              self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            soft_vars_int = []

            for v in constraint.soft_vars:
                ivar = self.fzn.int_var("{}_int".format(v), domain='0..1')
                self.fzn.bool2int(v,
                                  ivar,
                                  defines="{}_int".format(v),
                                  name="SameDays_S")
                soft_vars_int.append(ivar)

            ub = sum(constraint.penalties)
            soft_vars_int.append("SameDaysPenalty")
            constraint.penalties.append(-1)

            self.fzn.int_var("SameDaysPenalty",
                             output=True,
                             domain="0..{}".format(ub))
            self.fzn.int_lin_eq(constraint.penalties,
                                soft_vars_int,
                                0,
                                defines="SameDaysPenalty",
                                name="SameDays_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def different_days(self):
        stat = WriterStatus("DifferentDays")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["DifferentDays"]:
            if dist['required']:
                constraint.different_days_hard(dist['classes'], self.fzn,
                                               self.dat)
            else:
                if self.include_soft_vars:
                    constraint.different_days_soft(dist['classes'], self.fzn,
                                                   self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            soft_vars_int = []

            for v in constraint.soft_vars:
                ivar = self.fzn.int_var("{}_int".format(v), domain="0..1")
                self.fzn.bool2int(v,
                                  ivar,
                                  defines=ivar,
                                  name="DifferentDays_S")
                soft_vars_int.append(ivar)

            soft_vars_int.append("DifferentDaysPenalty")
            ub = sum(constraint.penalties)
            constraint.penalties.append(-1)
            self.fzn.int_var("DifferentDaysPenalty",
                             output=True,
                             domain="0..{}".format(ub))
            self.fzn.int_lin_eq(constraint.penalties,
                                soft_vars_int,
                                0,
                                defines="DifferentDaysPenalty",
                                name="DifferentDays_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def same_room(self):
        stat = WriterStatus("SameRoom")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["SameRoom"]:
            if dist['required']:
                constraint.same_room_hard(dist['classes'], self.fzn)
            else:
                if self.include_soft_vars:
                    constraint.same_room_soft(dist['classes'], self.fzn,
                                              dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            sameroom_penalty = self.fzn.int_var("SameRoomPenalty",
                                                output=True,
                                                domain="0..{}".format(
                                                    sum(constraint.penalties)))
            constraint.soft_vars.append(sameroom_penalty)
            constraint.penalties.append(-1)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines="SameRoomPenalty",
                                name="SameRoom_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def different_room(self):
        stat = WriterStatus("DifferentRoom")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["DifferentRoom"]:
            if dist['required']:
                constraint.different_room_hard(dist['classes'], self.fzn)
            else:
                if self.include_soft_vars:
                    constraint.different_room_soft(dist['classes'], self.fzn,
                                                   dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            diffroom_penalty = self.fzn.int_var("DifferentRoomPenalty",
                                                output=True,
                                                domain="0..{}".format(
                                                    sum(constraint.penalties)))
            constraint.soft_vars.append(diffroom_penalty)
            constraint.penalties.append(-1)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines="DifferentRoomPenalty",
                                name="DifferentRoom_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def not_overlap(self):
        stat = WriterStatus("NotOverlap")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        notoverlap_schedules = defaultdict(set)
        overlap_schedules = defaultdict(set)
        for dist in self.dat.distributions["NotOverlap"]:
            if dist['required']:
                for c1, c2 in itertools.combinations(dist['classes'], 2):
                    for s1, s2 in itertools.product(
                            self.dat.classes[c1].schedules,
                            self.dat.classes[c2].schedules):
                        sched1 = self.dat.unique_schedules[s1]
                        sched2 = self.dat.unique_schedules[s2]

                        if not self.dat.schedule_overlaps[s1][s2]:
                            notoverlap_schedules[sched1.id].add(sched2.id)
            else:
                for c1, c2 in itertools.combinations(dist['classes'], 2):
                    for s1, s2 in itertools.product(
                            self.dat.classes[c1].schedules,
                            self.dat.classes[c2].schedules):
                        sched1 = self.dat.unique_schedules[s1]
                        sched2 = self.dat.unique_schedules[s2]

                        if self.dat.schedule_overlaps[s1][s2]:
                            overlap_schedules[sched1.id].add(sched2.id)
                            overlap_schedules[sched1.id].add(sched1.id)

            stat.update()

        # Write constraints
        i = 1
        for dist in self.dat.distributions["NotOverlap"]:
            if dist['required']:
                constraint.not_overlap_hard(dist['classes'], self.fzn,
                                            self.dat, notoverlap_schedules)
            else:
                if self.include_soft_vars:
                    constraint.not_overlap_soft(dist['classes'], self.fzn,
                                                self.dat, overlap_schedules,
                                                dist['penalty'])

        if self.include_soft_vars:
            soft_vars_int = []

            for v in constraint.soft_vars:
                ivar = self.fzn.int_var("{}_int".format(v), domain='0..1')
                self.fzn.bool2int(v, ivar, defines=ivar, name="NotOverlap_S")
                soft_vars_int.append(ivar)

            self.fzn.int_var("NotOverlapPenalty",
                             output=True,
                             domain="0..{}".format(sum(constraint.penalties)))
            soft_vars_int.append("NotOverlapPenalty")
            constraint.penalties.append(-1)
            self.fzn.int_lin_eq(constraint.penalties,
                                soft_vars_int,
                                0,
                                defines="NotOverlapPenalty",
                                name="NotOverlap_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def same_attendees(self):
        stat = WriterStatus("SameAttendees")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["SameAttendees"]:
            if dist['required']:
                constraint.same_attendees_hard(dist['classes'], self.fzn,
                                               self.dat)
            else:
                if self.include_soft_vars:
                    constraint.same_attendees_soft(dist['classes'], self.fzn,
                                                   self.dat, dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            sameattendees_penalty = self.fzn.int_var(
                "SameAttendeesPenalty",
                output=True,
                domain="0..{}".format(sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(sameattendees_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=sameattendees_penalty,
                                name="SameAttendees_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def room_available(self):
        stat = WriterStatus("RoomUnavailable")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)

        i = 0

        for s in self.dat.unique_schedules:
            sched = self.dat.unique_schedules[s]
            for room in self.dat.rooms:
                # Find out if room is available for schedule
                available = True
                for room_unavail in self.dat.rooms[room]['unavailable']:
                    ru_end = room_unavail['start'] + room_unavail['length']

                    # Week overlap
                    if (sched.weeks & room_unavail['weeks']).any():
                        # Day overlap
                        if (sched.days & room_unavail['days']).any():
                            # Time overlap
                            if (sched.end > room_unavail['start'] and sched.start <= room_unavail['start']) \
                                    or (ru_end > sched.start and room_unavail['start'] <= sched.start) \
                                    or (room_unavail['start'] <= sched.start and ru_end > sched.end) \
                                    or (sched.start <= room_unavail['start'] and sched.end > ru_end):
                                available = False
                                break

                # Prevent every class (with that room and schedule) from using that combination
                if not available:
                    for c in self.dat.classes:
                        if s in self.dat.classes[
                                c].schedules and room in self.dat.classes[
                                    c].rooms:
                            cnotroomr = self.fzn.bool_var(
                                "C{}NotRoom{}".format(c, room))
                            cnotscheds = self.fzn.bool_var(
                                "C{}NotSchedule{}".format(c, sched.id))
                            self.fzn.int_ne_reif("C{}_Room".format(c),
                                                 room,
                                                 cnotroomr,
                                                 defines=cnotroomr,
                                                 name="RoomUnavailabilities")
                            self.fzn.int_ne_reif("C{}_Schedule".format(c),
                                                 sched.id,
                                                 cnotscheds,
                                                 defines=cnotscheds,
                                                 name="RoomUnavailabilities")

                            self.fzn.array_bool_or([cnotscheds, cnotroomr],
                                                   True,
                                                   name="RoomUnavailabilities")
                            stat.update()
                    i += 1

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def schedule_overlaps(self):
        stat = WriterStatus("ScheduleOverlaps")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)

        pruned = 0

        for c in self.dat.classes:
            for s in self.dat.classes[c].schedules:
                cschedules = self.fzn.bool_var("C{}Schedule{}".format(
                    c, self.dat.unique_schedules[s].id))
                self.fzn.int_eq_reif("C{}_Schedule".format(c),
                                     self.dat.unique_schedules[s].id,
                                     cschedules,
                                     defines=cschedules,
                                     name="ScheduleOverlaps")

        for c1, c2 in itertools.combinations(self.dat.classes, 2):
            if len(self.dat.classes[c1].rooms
                   & self.dat.classes[c2].rooms) > 0:
                if self.dat.classes[c1].is_fixed(
                ) and self.dat.classes[c2].is_fixed():
                    pruned += 1
                else:
                    for s1, s2 in itertools.product(
                            self.dat.classes[c1].schedules,
                            self.dat.classes[c2].schedules):
                        if self.dat.schedule_overlaps[s1][s2]:
                            sched1 = self.dat.unique_schedules[s1]
                            sched2 = self.dat.unique_schedules[s2]
                            c1c2diffroom = self.fzn.bool_var(
                                "C{}C{}DiffRoom".format(c1, c2))
                            self.fzn.int_ne_reif("C{}_Room".format(c1),
                                                 "C{}_Room".format(c2),
                                                 c1c2diffroom,
                                                 defines=c1c2diffroom,
                                                 name="ScheduleOverlaps")
                            c1notsched1 = self.fzn.bool_var(
                                "C{}NotSchedule{}".format(c1, sched1.id))
                            c2notsched2 = self.fzn.bool_var(
                                "C{}NotSchedule{}".format(c2, sched2.id))
                            self.fzn.int_ne_reif("C{}_Schedule".format(c1),
                                                 sched1.id,
                                                 c1notsched1,
                                                 defines=c1notsched1,
                                                 name="ScheduleOverlaps")
                            self.fzn.int_ne_reif("C{}_Schedule".format(c2),
                                                 sched2.id,
                                                 c2notsched2,
                                                 defines=c2notsched2,
                                                 name="ScheduleOverlaps")
                            self.fzn.array_bool_or(
                                [c1notsched1, c2notsched2, c1c2diffroom],
                                True,
                                name="ScheduleOverlaps")
            stat.update()

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def work_day(self):
        stat = WriterStatus("WorkDay")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        workday_schedules = defaultdict(set)
        notworkday_schedules = defaultdict(set)
        for dist in self.dat.distributions["WorkDay"]:
            for c1, c2 in itertools.combinations(dist['classes'], 2):
                for s1, s2 in itertools.product(
                        self.dat.classes[c1].schedules,
                        self.dat.classes[c2].schedules):
                    sched1 = self.dat.unique_schedules[s1]
                    sched2 = self.dat.unique_schedules[s2]
                    if (not (sched1.days & sched2.days).any()) or (
                            not (sched1.weeks & sched2.weeks).any()
                    ) or (max([sched1.end, sched2.end]) - min(
                        [sched1.start, sched2.start])) <= dist['params'][0]:
                        workday_schedules[s1].add(s2)
                    else:
                        notworkday_schedules[s1].add(s2)

        # Write constraints
        for dist in self.dat.distributions["WorkDay"]:
            if dist['required']:
                constraint.work_day_hard(dist['classes'], self.fzn, self.dat,
                                         workday_schedules)
            else:
                if self.include_soft_vars:
                    constraint.work_day_soft(dist['classes'], self.fzn,
                                             self.dat, workday_schedules,
                                             dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            workday_penalty = self.fzn.int_var("WorkDayPenalty",
                                               output=True,
                                               domain="0..{}".format(
                                                   sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(workday_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=workday_penalty,
                                name="WorkDay_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def min_gap(self):
        stat = WriterStatus("MinGap")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        mingap_schedules = defaultdict(set)
        notmingap_schedules = defaultdict(set)
        for dist in self.dat.distributions["MinGap"]:
            for c1, c2 in itertools.combinations(dist['classes'], 2):
                for s1, s2 in itertools.product(
                        self.dat.classes[c1].schedules,
                        self.dat.classes[c2].schedules):
                    sched1 = self.dat.unique_schedules[s1]
                    sched2 = self.dat.unique_schedules[s2]
                    if (not (sched1.days & sched2.days).any()) or (
                            not (sched1.weeks & sched2.weeks).any()
                    ) or (sched1.end + dist['params'][0] <= sched2.start) or (
                            sched2.end + dist['params'][0] <= sched1.start):
                        mingap_schedules[sched1.id].add(sched2.id)
                    else:
                        notmingap_schedules[sched1.id].add(sched2.id)

        # Write constraints
        for dist in self.dat.distributions["MinGap"]:
            if dist['required']:
                constraint.min_gap_hard(dist['classes'], self.fzn, self.dat,
                                        mingap_schedules)
            else:
                if self.include_soft_vars:
                    constraint.min_gap_soft(dist['classes'], self.fzn,
                                            self.dat, notmingap_schedules,
                                            dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            mingap_penalty = self.fzn.int_var("MinGapPenalty",
                                              output=True,
                                              domain="0..{}".format(
                                                  sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(mingap_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=mingap_penalty,
                                name="MinGap_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def max_days(self):
        stat = WriterStatus("MaxDays")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()
        distnum = 1

        for dist in self.dat.distributions["MaxDays"]:
            if dist['required']:
                constraint.max_days_hard(dist['classes'], self.fzn, self.dat,
                                         dist['params'][0], distnum)
            else:
                if self.include_soft_vars:
                    constraint.max_days_soft(dist['classes'], self.fzn,
                                             self.dat, dist['params'][0],
                                             distnum, dist['penalty'])
            distnum += 1
            stat.update()

        if self.include_soft_vars:
            maxdays_penalty = self.fzn.int_var(
                "MaxDaysPenalty",
                output=True,
                domain="0..{}".format(len(constraint.penalties) * 7))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(maxdays_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=maxdays_penalty,
                                name="MaxDays_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def max_day_load(self):
        stat = WriterStatus("MaxDayLoad")
        stat.update()
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()
        distnum = 1

        for dist in self.dat.distributions["MaxDayLoad"]:
            if dist['required']:
                constraint.max_day_load_hard(dist['classes'], self.fzn,
                                             self.dat, dist['params'][0])
            else:
                if self.include_soft_vars:
                    constraint.max_day_load_soft(dist['classes'], self.fzn,
                                                 self.dat, dist['params'][0],
                                                 distnum, dist['penalty'])
                    distnum += 1
            stat.update()

        if self.include_soft_vars:
            maxdayload_penalty = self.fzn.int_var("MaxDayLoadPenalty",
                                                  output=True)
            constraint.penalties.append(-1)
            constraint.soft_vars.append(maxdayload_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=maxdayload_penalty,
                                name="MaxDayLoad_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def max_breaks(self):
        stat = WriterStatus("MaxBreaks")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["MaxBreaks"]:
            if dist['required']:
                constraint.max_breaks_hard(dist['classes'], self.fzn, self.dat,
                                           dist['params'][0],
                                           dist['params'][1])
            else:
                if self.include_soft_vars:
                    constraint.max_breaks_soft(dist['classes'], self.fzn,
                                               self.dat, dist['params'][0],
                                               dist['params'][1],
                                               dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            maxbreaks_penalty = self.fzn.int_var(
                "MaxBreaksPenalty",
                output=True,
                domain="0..{}".format(sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(maxbreaks_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=maxbreaks_penalty,
                                name="MaxBreaks_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def max_block(self):
        stat = WriterStatus("MaxBlock")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)
        constraint = fzn.Constraint()

        for dist in self.dat.distributions["MaxBlock"]:
            if dist['required']:
                constraint.max_block_hard(dist['classes'], self.fzn, self.dat,
                                          dist['params'][0], dist['params'][1])
            else:
                if self.include_soft_vars:
                    constraint.max_block_soft(dist['classes'], self.fzn,
                                              self.dat, dist['params'][0],
                                              dist['params'][1],
                                              dist['penalty'])
            stat.update()

        if self.include_soft_vars:
            maxblock_penalty = self.fzn.int_var("MaxBlockPenalty",
                                                output=True,
                                                domain="0..{}".format(
                                                    sum(constraint.penalties)))
            constraint.penalties.append(-1)
            constraint.soft_vars.append(maxblock_penalty)
            self.fzn.int_lin_eq(constraint.penalties,
                                constraint.soft_vars,
                                0,
                                defines=maxblock_penalty,
                                name="MaxBlock_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def class_schedules(self):
        stat = WriterStatus("ClassSchedules")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)

        for c in self.dat.classes:
            self.fzn.int_var(self.dat.classes[c].schedule_var,
                             output=True,
                             domain="{{{}}}".format(','.join([
                                 str(self.dat.unique_schedules[s].id)
                                 for s in self.dat.classes[c].schedules
                             ])))
            stat.update()

        if self.include_soft_vars:
            penalties = []
            penalties.append(-1)
            svars = []
            svars.append("SchedulePenalty")
            ub = 0
            for c in self.dat.classes:
                for s in self.dat.classes[c].schedules:
                    sched1 = self.dat.unique_schedules[s]
                    c1schedule1 = self.fzn.bool_var("C{}Schedule{}".format(
                        c, sched1.id))
                    self.fzn.int_eq_reif("C{0}_Schedule".format(c),
                                         sched1.id,
                                         c1schedule1,
                                         defines=c1schedule1,
                                         name="SchedulePenalty")
                    c1schedule1int = self.fzn.int_var(
                        "C{}Schedule{}int".format(c, sched1.id), domain='0..1')
                    self.fzn.bool2int(c1schedule1,
                                      c1schedule1int,
                                      defines=c1schedule1int,
                                      name="SchedulePenalty")
                    penalties.append(self.dat.classes[c].schedule_penalty[s])
                    svars.append(c1schedule1int)
                    ub += self.dat.classes[c].schedule_penalty[s]

            self.fzn.int_var("SchedulePenalty",
                             domain="0..{}".format(ub),
                             output=True)
            self.fzn.int_lin_eq(penalties,
                                svars,
                                0,
                                defines="SchedulePenalty",
                                name="SchedulePenalty")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    # Minimize student overlaps
    def student_conflicts(self):
        stat = WriterStatus("StudentConflicts")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)

        soft_vars = []
        penalties = []
        for student in self.dat.students:
            if len(self.dat.students[student]['classes']) > 1:
                for c1, c2 in itertools.combinations(
                        self.dat.students[student]['classes'], 2):
                    c1 = int(c1)
                    c2 = int(c2)
                    if not self.dat.classes[c1].is_fixed(
                    ) and not self.dat.classes[c2].is_fixed():
                        pos_var = []
                        i = 1

                        for r1, r2, s1, s2 in itertools.product(
                                self.dat.classes[c1].rooms,
                                self.dat.classes[c2].rooms,
                                self.dat.classes[c1].schedules,
                                self.dat.classes[c2].schedules):
                            sched1 = self.dat.unique_schedules[s1]
                            sched2 = self.dat.unique_schedules[s2]

                            if (
                                    sched1.end +
                                    self.dat.rooms[r1]['travel'][r2] <=
                                    sched2.start
                            ) or (sched2.end + self.dat.rooms[r2]['travel'][r1]
                                  <= sched1.start) or (
                                      not (sched1.weeks & sched2.weeks).any()
                                  ) or (not (sched1.days & sched2.days).any()):
                                c1schedule1 = self.fzn.bool_var(
                                    "C{}Schedule{}".format(c1, sched1.id))
                                self.fzn.int_eq_reif(
                                    "C{0}_Schedule".format(c1),
                                    sched1.id,
                                    c1schedule1,
                                    defines=c1schedule1)
                                c2schedule2 = self.fzn.bool_var(
                                    "C{}Schedule{}".format(c2, sched2.id))
                                self.fzn.int_eq_reif(
                                    "C{0}_Schedule".format(c2),
                                    sched2.id,
                                    c2schedule2,
                                    defines=c2schedule2)

                                c1c2sameattendeesi = self.fzn.bool_var(
                                    "C{0}C{1}SameAttendees{2}".format(
                                        c1, c2, i))

                                c1room1 = self.fzn.bool_var("C{}Room{}".format(
                                    c1, r1))
                                self.fzn.int_eq_reif("C{}_Room".format(c1),
                                                     r1,
                                                     c1room1,
                                                     defines=c1room1)
                                c2room2 = self.fzn.bool_var("C{}Room{}".format(
                                    c2, r2))
                                self.fzn.int_eq_reif("C{}_Room".format(c2),
                                                     r2,
                                                     c2room2,
                                                     defines=c2room2)

                                self.fzn.array_bool_and(
                                    [
                                        c1schedule1, c2schedule2, c1room1,
                                        c2room2
                                    ],
                                    c1c2sameattendeesi,
                                    defines=c1c2sameattendeesi,
                                    name="StudentConflicts")
                                pos_var.append(c1c2sameattendeesi)

                                i += 1

                        if len(pos_var) > 0:
                            c1c2sameattendees = self.fzn.bool_var(
                                "C{0}C{1}SameAttendees".format(c1, c2))
                            self.fzn.array_bool_or(pos_var,
                                                   c1c2sameattendees,
                                                   defines=c1c2sameattendees,
                                                   name="StudentConflicts")

                            c1c2sameattendees_int = self.fzn.int_var(
                                "C{0}C{1}SameAttendees_int".format(c1, c2),
                                domain="0..1")
                            self.fzn.bool2int(c1c2sameattendees,
                                              c1c2sameattendees_int,
                                              defines=c1c2sameattendees_int)

                            soft_vars.append(c1c2sameattendees_int)
                            penalties.append(self.dat.weights['student'])
            stat.update()

        sameattendees_penalty = self.fzn.int_var("StudentConflictsPenalty",
                                                 output=True,
                                                 domain="0..{}".format(
                                                     sum(penalties)))
        penalties.append(-1)
        soft_vars.append(sameattendees_penalty)
        self.fzn.int_lin_eq(penalties,
                            soft_vars,
                            0,
                            defines=sameattendees_penalty,
                            name="StudentConflicts_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons

        stat.done()

    def class_rooms(self):
        stat = WriterStatus("ClassRooms")
        num_vars = len(self.fzn.variables)
        num_cons = len(self.fzn.constraints)

        for c in self.dat.classes:
            if len(self.dat.classes[c].rooms) > 0:
                self.fzn.int_var(self.dat.classes[c].room_var,
                                 output=True,
                                 domain="{{{}}}".format(','.join([
                                     str(r) for r in self.dat.classes[c].rooms
                                 ])))
            else:
                # In case the class does not need a room
                self.fzn.int_var(self.dat.classes[c].room_var,
                                 domain="{{{}}}".format(len(self.dat.rooms)))
            stat.update()

        if self.include_soft_vars:
            penalties = []
            penalties.append(-1)
            rvars = []
            rvars.append("RoomPenalty")
            ub = 0
            for c in self.dat.classes:
                for r in self.dat.classes[c].rooms:
                    c1room1 = self.fzn.bool_var("C{}Room{}".format(c, r))
                    self.fzn.int_eq_reif("C{0}_Room".format(c),
                                         r,
                                         c1room1,
                                         defines=c1room1,
                                         name="RoomPenalty")
                    c1room1int = self.fzn.int_var("C{}Room{}int".format(c, r),
                                                  domain='0..1')
                    self.fzn.bool2int(c1room1,
                                      c1room1int,
                                      defines=c1room1int,
                                      name="RoomPenalty")
                    penalties.append(self.dat.classes[c].room_penalty[str(r)])
                    rvars.append(c1room1int)
                    ub += self.dat.classes[c].room_penalty[str(r)]

            self.fzn.int_var("RoomPenalty",
                             domain="0..{}".format(ub),
                             output=True)
            self.fzn.int_lin_eq(penalties,
                                rvars,
                                0,
                                defines="RoomPenalty",
                                name="RoomPenalty_S")

        stat.variables = len(self.fzn.variables) - num_vars
        stat.constraints = len(self.fzn.constraints) - num_cons
        stat.done()

    def objective(self):
        if self.include_soft_vars:
            self.fzn.int_var("obj", output=True)
            self.fzn.int_lin_eq(
                [
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    -1
                ],
                [
                    "SchedulePenalty",
                    "RoomPenalty",
                    "SameStartPenalty",
                    "SameTimePenalty",
                    "DifferentTimePenalty",
                    "SameDaysPenalty",
                    "DifferentDaysPenalty",
                    "SameWeeksPenalty",
                    "DifferentWeeksPenalty",
                    "SameAttendeesPenalty",
                    # "StudentConflictsPenalty",
                    "SameRoomPenalty",
                    "DifferentRoomPenalty",
                    "WorkDayPenalty",
                    "MinGapPenalty",
                    "MaxDaysPenalty",
                    "OverlapPenalty",
                    "NotOverlapPenalty",
                    "PrecedencePenalty",
                    "MaxBreaksPenalty",
                    "MaxBlockPenalty",
                    "obj"
                ],
                0,
                defines="obj")

    def write_solve(self, f):
        if self.include_soft_vars and self.minimize:
            f.write("solve minimize obj;\n")
        else:
            f.write("solve satisfy;")
