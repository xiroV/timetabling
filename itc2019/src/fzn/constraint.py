"""
Constraint class definition and methods for adding constraints to a model
"""

import itertools


class Constraint:
    def __init__(self):
        self.soft_vars = []
        self.penalties = []

    def precedence_hard(self, classes, fzn, dat, succeeding):
        for c1, c2 in itertools.combinations(classes, 2):
            pos = []
            i = 1
            if len(dat.classes[c1].schedules) > 1 or len(
                    dat.classes[c2].schedules) > 1:
                for s1 in dat.classes[c1].schedules:
                    sched1 = dat.unique_schedules[s1]

                    c1schedule1 = fzn.bool_var("C{}Schedule{}".format(
                        c1, sched1.id))
                    fzn.int_eq_reif("C{0}_Schedule".format(c1),
                                    dat.unique_schedules[s1].id,
                                    c1schedule1,
                                    defines=c1schedule1,
                                    name="Precedence_H")
                    c2succeedsc1 = fzn.bool_var("C{}SucceedsC{}S{}".format(
                        c2, c1, sched1.id))
                    fzn.set_in_reif("C{}_Schedule".format(c2),
                                    succeeding[sched1.id],
                                    c2succeedsc1,
                                    defines=c2succeedsc1,
                                    name="Precedence_H")
                    c1c2precedence = fzn.bool_var("C{}C{}Precedence_{}".format(
                        c1, c2, i))
                    fzn.array_bool_and([c2succeedsc1, c1schedule1],
                                       c1c2precedence,
                                       defines=c1c2precedence,
                                       name="Precedence_H")
                    pos.append(c1c2precedence)
                    i += 1

                fzn.array_bool_or(pos, True, name="Precedence_H")

    def precedence_soft(self, classes, fzn, dat, succeeding, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            pos = []
            i = 1
            for s1 in dat.classes[c1].schedules:
                sched1 = dat.unique_schedules[s1]

                c1schedule1 = fzn.bool_var("C{}Schedule{}".format(
                    c1, sched1.id))
                fzn.int_eq_reif("C{0}_Schedule".format(c1),
                                dat.unique_schedules[s1].id,
                                c1schedule1,
                                defines=c1schedule1,
                                name="Precedence_S")
                c2succeedsc1 = fzn.bool_var("C{}SucceedsC{}S{}".format(
                    c2, c1, sched1.id))
                fzn.set_in_reif("C{}_Schedule".format(c2),
                                succeeding[sched1.id],
                                c2succeedsc1,
                                name="Precedence_S")
                c1c2precedencei = fzn.bool_var("C{}C{}Precedence_{}".format(
                    c1, c2, i))
                fzn.array_bool_and([c2succeedsc1, c1schedule1],
                                   c1c2precedencei,
                                   c1c2precedencei,
                                   name="Precedence_S")
                pos.append(c1c2precedencei)
                i += 1

            c1c2precedence = fzn.bool_var("C{}C{}Precedence".format(c1, c2))
            c1c2succeeds = fzn.bool_var("C{}C{}Succeeds".format(c1, c2))
            c1c2succeeds_int = fzn.int_var("C{}C{}Succeeds_int".format(c1, c2),
                                           domain="0..1")

            fzn.array_bool_or(pos,
                              c1c2precedence,
                              defines=c1c2precedence,
                              name="Precedence_S")
            fzn.bool_xor(c1c2precedence,
                         True,
                         c1c2succeeds,
                         defines=c1c2succeeds,
                         name="Precedence_S")

            fzn.bool2int(c1c2succeeds,
                         c1c2succeeds_int,
                         defines=c1c2succeeds_int,
                         name="Precedence_S")

            self.soft_vars.append(c1c2succeeds_int)
            self.penalties.append(penalty)

    def overlap_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1

            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if dat.schedule_overlaps[s1][s2]:
                    c1c2_overlap = fzn.bool_var(
                        "C{0}C{1}OverlapS{2}S{3}".format(
                            c1, c2, sched1.id, sched2.id))
                    fzn.array_bool_and([
                        "C{0}Schedule{1}".format(c1, sched1.id),
                        "C{0}Schedule{1}".format(c2, sched2.id)
                    ],
                                       c1c2_overlap,
                                       defines=c1c2_overlap,
                                       name="Overlap_H")
                    pos_var.append(c1c2_overlap)
                    i += 1

            if len(pos_var) > 0:
                fzn.array_bool_or(pos_var, True, name="Overlap_H")

    def overlap_soft(self, classes, fzn, dat, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1

            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if not dat.schedule_overlaps[s1][s2]:
                    c1c2_notoverlap = fzn.bool_var(
                        "C{0}C{1}NotOverlapS{2}S{3}".format(
                            c1, c2, sched1.id, sched2.id))
                    fzn.array_bool_and([
                        "C{0}Schedule{1}".format(c1, sched1.id),
                        "C{0}Schedule{1}".format(c2, sched2.id)
                    ],
                                       c1c2_notoverlap,
                                       defines=c1c2_notoverlap,
                                       name="Overlap_S")
                    pos_var.append(c1c2_notoverlap)
                    i += 1

            if len(pos_var) > 0:
                c1c2_notoverlap = fzn.bool_var("C{}C{}NotOverlap".format(
                    c1, c2))
                fzn.array_bool_or(pos_var, c1c2_notoverlap)

                c1c2_notoverlap_int = fzn.int_var(
                    "C{}C{}NotOverlap_int".format(c1, c2), domain="0..1")
                fzn.bool2int(c1c2_notoverlap,
                             c1c2_notoverlap_int,
                             defines=c1c2_notoverlap_int,
                             name="Overlap_S")

                self.soft_vars.append(c1c2_notoverlap_int)
                self.penalties.append(penalty)

    def not_overlap_hard(self, classes, fzn, dat, notoverlap_schedules):
        for c1, c2 in itertools.combinations(classes, 2):
            not_overlap_vars = []
            for s1 in dat.classes[c1].schedules:
                sched1 = dat.unique_schedules[s1]

                b_c1_sched = fzn.bool_var("C{}Schedule{}".format(
                    c1, sched1.id))
                fzn.int_eq_reif(c1,
                                sched1.id,
                                b_c1_sched,
                                defines=b_c1_sched,
                                name="NotOverlap_H")

                b_sched_not_overlap = fzn.bool_var(
                    "C{}InNotOverlapC{}S{}".format(c2, c1, sched1.id))
                fzn.set_in_reif("C{}_Schedule".format(c2),
                                notoverlap_schedules[sched1.id],
                                b_sched_not_overlap,
                                defines=b_sched_not_overlap,
                                name="NotOverlap_H")

                b_not_overlap = fzn.bool_var("C{}S{}NotOverlapC{}".format(
                    c1, sched1.id, c2))
                fzn.array_bool_and([b_sched_not_overlap, b_c1_sched],
                                   b_not_overlap,
                                   defines=b_not_overlap,
                                   name="NotOverlap_H")
                not_overlap_vars.append(b_not_overlap)
            fzn.array_bool_or(not_overlap_vars, True, name="NotOverlap_H")

    def not_overlap_soft(self, classes, fzn, dat, overlap_schedules, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            c1c2_viol_opts = []
            for s1 in dat.classes[c1].schedules:
                sched1 = dat.unique_schedules[s1]
                if len(overlap_schedules[sched1.id]) > 0:
                    c1s1c2_overlap = fzn.bool_var("C{}OverlapC{}S{}".format(
                        c2, c1, sched1.id))
                    c2sched_overlapc1s1 = fzn.bool_var(
                        "C{}ScheduleOverlapC{}S{}".format(c2, c1, sched1.id))
                    c1schedule1 = fzn.bool_var("C{}Schedule{}".format(
                        c1, sched1.id))
                    fzn.set_in_reif("C{}_Schedule".format(c2),
                                    overlap_schedules[sched1.id],
                                    c2sched_overlapc1s1,
                                    defines=c2sched_overlapc1s1,
                                    name="NotOverlap_S")
                    fzn.array_bool_and([c1schedule1, c2sched_overlapc1s1],
                                       c1s1c2_overlap,
                                       defines=c1s1c2_overlap,
                                       name="NotOverlap_S")
                    c1c2_viol_opts.append(c1s1c2_overlap)

                    self.soft_vars.append(c1s1c2_overlap)
                    self.penalties.append(penalty)

    def same_room_hard(self, classes, fzn):
        for c1, c2 in itertools.combinations(classes, 2):
            fzn.int_eq("C{}_Room".format(c1),
                       "C{}_Room".format(c2),
                       name="SameRoom_H")

    def same_room_soft(self, classes, fzn, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            diffroom = fzn.bool_var("DiffRoomC{0}C{1}".format(c1, c2))
            fzn.int_ne_reif("C{}_Room".format(c1),
                            "C{}_Room".format(c2),
                            diffroom,
                            defines=diffroom,
                            name="SameRoom_S")

            diffroom_int = fzn.int_var("DiffRoomC{0}C{1}_int".format(c1, c2),
                                       domain="0..1")
            fzn.bool2int(diffroom,
                         diffroom_int,
                         defines=diffroom_int,
                         name="SameRoom_S")

            self.soft_vars.append(diffroom_int)
            self.penalties.append(penalty)

    def different_room_hard(self, classes, fzn):
        for c1, c2 in itertools.combinations(classes, 2):
            fzn.int_ne("C{}_Room".format(c1),
                       "C{}_Room".format(c2),
                       name="DifferentRoom_H")

    def different_room_soft(self, classes, fzn, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            sameroom = fzn.bool_var("SameRoomC{0}C{1}".format(c1, c2))
            fzn.int_eq_reif("C{}_Room".format(c1),
                            "C{}_Room".format(c2),
                            sameroom,
                            defines=sameroom,
                            name="DifferentRoom_S")

            sameroom_int = fzn.int_var("SameRoomC{0}C{1}_int".format(c1, c2),
                                       domain="0..1")
            fzn.bool2int(sameroom,
                         sameroom_int,
                         defines=sameroom_int,
                         name="DifferentRoom_S")

            self.soft_vars.append(sameroom_int)
            self.penalties.append(penalty)

    def same_time_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if (sched1.start <= sched2.start and sched2.end <= sched1.end
                    ) or (sched2.start <= sched1.start
                          and sched1.end <= sched2.end):
                    c1c2_sametime = fzn.bool_var("C{0}C{1}SameTime{2}".format(
                        c1, c2, i))
                    fzn.array_bool_and([
                        "C{}Schedule{}".format(c1, sched1.id),
                        "C{}Schedule{}".format(c2, sched2.id)
                    ],
                                       c1c2_sametime,
                                       defines=c1c2_sametime,
                                       name="SameTime_H")
                    pos_var.append("C{0}C{1}SameTime{2}".format(c1, c2, i))
                    i += 1

            if len(pos_var) > 0:
                fzn.array_bool_or(pos_var, True, name="SameTime_H")

    def same_time_soft(self, classes, fzn, dat, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if (sched1.end <= sched2.start) or (sched2.end <=
                                                    sched1.start):
                    c1c2_sametime = fzn.bool_var("C{0}C{1}SameTime{2}".format(
                        c1, c2, i))
                    fzn.array_bool_and([
                        "C{}Schedule{}".format(c1, sched1.id),
                        "C{}Schedule{}".format(c2, sched2.id)
                    ],
                                       c1c2_sametime,
                                       defines=c1c2_sametime,
                                       name="SameTime_S")
                    pos_var.append("C{0}C{1}SameTime{2}".format(c1, c2, i))
                    i += 1

            if len(pos_var) > 0:
                c1c2_difftime = fzn.bool_var("C{}C{}DiffTime".format(c1, c2))
                fzn.array_bool_or(pos_var, c1c2_difftime, name="SameTime_S")

                c1c2_difftime_int = fzn.int_var("C{}C{}DiffTime_int".format(
                    c1, c2),
                                                domain="0..1")
                fzn.bool2int(c1c2_difftime,
                             c1c2_difftime_int,
                             defines=c1c2_difftime_int,
                             name="SameTime_S")
                self.soft_vars.append(c1c2_difftime_int)
                self.penalties.append(penalty)

    def same_start_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if sched1.start == sched2.start:
                    c1c2_samestart = fzn.bool_var(
                        "C{0}C{1}SameStart{2}".format(c1, c2, i))
                    fzn.array_bool_and([
                        "C{}Schedule{}".format(c1, sched1.id),
                        "C{}Schedule{}".format(c2, sched2.id)
                    ],
                                       c1c2_samestart,
                                       defines=c1c2_samestart,
                                       name="SameStart_H")
                    pos_var.append(c1c2_samestart)
                    i += 1

            if len(pos_var) > 0:
                fzn.array_bool_or(pos_var, True, name="SameStart_H")

    def same_start_soft(self, classes, fzn, dat, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if sched1.start != sched2.start:
                    c1c2_diffstarti = fzn.bool_var(
                        "C{0}C{1}DiffStart{2}".format(c1, c2, i))
                    fzn.array_bool_and([
                        "C{}Schedule{}".format(c1, sched1.id),
                        "C{}Schedule{}".format(c2, sched2.id)
                    ],
                                       c1c2_diffstarti,
                                       defines=c1c2_diffstarti,
                                       name="SameStart_S")
                    pos_var.append(c1c2_diffstarti)
                    i += 1

            if len(pos_var) > 0:
                c1c2_diffstart = fzn.bool_var("C{}C{}DiffStart".format(c1, c2))
                fzn.array_bool_or(pos_var, c1c2_diffstart, name="SameStart_S")

                c1c2_diffstart_int = fzn.int_var("C{}C{}DiffStart_int".format(
                    c1, c2),
                                                 domain="0..1")
                fzn.bool2int(c1c2_diffstart,
                             c1c2_diffstart_int,
                             defines=c1c2_diffstart_int,
                             name="SameStart_S")
                self.soft_vars.append(c1c2_diffstart_int)
                self.penalties.append(penalty)

    def same_weeks_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if ((sched1.weeks | sched2.weeks) != sched1.weeks) and (
                    (sched1.weeks | sched2.weeks) != sched2.weeks):
                    c1notsched1 = fzn.bool_var("C{}NotSchedule{}".format(
                        c1, sched1.id))
                    c2notsched2 = fzn.bool_var("C{}NotSchedule{}".format(
                        c2, sched2.id))
                    fzn.int_ne_reif("C{}_Schedule".format(c1),
                                    sched1.id,
                                    c1notsched1,
                                    defines=c1notsched1,
                                    name="SameWeeks_H")
                    fzn.int_ne_reif("C{}_Schedule".format(c2),
                                    sched2.id,
                                    c2notsched2,
                                    defines=c2notsched2,
                                    name="SameWeeks_H")

                    fzn.array_bool_or([c1notsched1, c2notsched2],
                                      True,
                                      name="SameWeeks_H")

    def same_weeks_soft(self, classes, fzn, dat, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            for s1 in dat.classes[c1].schedules:
                diffweeks_schedules = []
                sched1 = dat.unique_schedules[s1]
                for s2 in dat.classes[c2].schedules:
                    sched2 = dat.unique_schedules[s2]
                    if not (((sched1.weeks | sched2.weeks) == sched1.weeks) or
                            ((sched1.weeks | sched2.weeks) == sched2.weeks)):
                        diffweeks_schedules.append(sched2.id)

                c1s1c2_diffweeks = fzn.bool_var("C{}DiffWeeks{}S{}".format(
                    c2, c1, sched1.id))
                c2sched_diffweeksc1s1 = fzn.bool_var(
                    "C{}ScheduleDiffWeeksC{}S{}".format(c2, c1, sched1.id))
                c1schedule1 = fzn.bool_var("C{}Schedule{}".format(
                    c1, sched1.id))
                fzn.set_in_reif("C{}_Schedule".format(c2),
                                diffweeks_schedules,
                                c2sched_diffweeksc1s1,
                                defines=c2sched_diffweeksc1s1,
                                name="SameWeeks_S")
                fzn.array_bool_and([c1schedule1, c2sched_diffweeksc1s1],
                                   c1s1c2_diffweeks,
                                   defines=c1s1c2_diffweeks,
                                   name="SameWeeks_S")

                self.soft_vars.append(c1s1c2_diffweeks)
                self.penalties.append(penalty)

    def different_weeks_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]
                if ((sched1.weeks | sched2.weeks) == sched1.weeks) or (
                    (sched1.weeks | sched2.weeks) == sched2.weeks):
                    c1notsched1 = fzn.bool_var("C{}NotSchedule{}".format(
                        c1, sched1.id))
                    c2notsched2 = fzn.bool_var("C{}NotSchedule{}".format(
                        c2, sched2.id))
                    fzn.int_ne_reif("C{}_Schedule".format(c1),
                                    sched1.id,
                                    c1notsched1,
                                    defines=c1notsched1,
                                    name="DifferentWeeks_H")
                    fzn.int_ne_reif("C{}_Schedule".format(c2),
                                    sched2.id,
                                    c2notsched2,
                                    defines=c2notsched2,
                                    name="DifferentWeeks_H")

                    fzn.array_bool_or([c1notsched1, c2notsched2],
                                      True,
                                      name="DifferentWeeks_H")

    def different_weeks_soft(self, classes, fzn, dat, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            c1c2_viol_opts = []
            for s1 in dat.classes[c1].schedules:
                sameweeks_schedules = []
                sched1 = dat.unique_schedules[s1]
                for s2 in dat.classes[c2].schedules:
                    sched2 = dat.unique_schedules[s2]
                    if ((sched1.weeks | sched2.weeks) == sched1.weeks) or (
                        (sched1.weeks | sched2.weeks) == sched2.week):
                        sameweeks_schedules.append(sched2.id)

                c1s1c2_sameweeks = fzn.bool_var("C{}SameWeeks{}S{}".format(
                    c2, c1, sched1.id))
                c2sched_sameweeksc1s1 = fzn.bool_var(
                    "C{}ScheduleSameWeeksC{}S{}".format(c2, c1, sched1.id))
                c1schedule1 = fzn.bool_var("C{}Schedule{}".format(
                    c1, sched1.id))
                fzn.set_in_reif("C{}_Schedule".format(c2),
                                sameweeks_schedules,
                                c2sched_sameweeksc1s1,
                                defines=c2sched_sameweeksc1s1,
                                name="DifferentWeeks_S")
                fzn.array_bool_and([c1schedule1, c2sched_sameweeksc1s1],
                                   c1s1c2_sameweeks,
                                   defines=c1s1c2_sameweeks,
                                   name="DifferentWeeks_S")
                c1c2_viol_opts.append(c1s1c2_sameweeks)

                self.soft_vars.append(c1s1c2_sameweeks)
                self.penalties.append(penalty)

    def same_days_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if ((sched1.days | sched2.days) != sched1.days) and (
                    (sched1.days | sched2.days) != sched2.days):
                    c1notsched1 = fzn.bool_var("C{}NotSchedule{}".format(
                        c1, sched1.id))
                    c2notsched2 = fzn.bool_var("C{}NotSchedule{}".format(
                        c2, sched2.id))
                    fzn.int_ne_reif("C{}_Schedule".format(c1),
                                    sched1.id,
                                    c1notsched1,
                                    defines=c1notsched1,
                                    name="SameDays_H")
                    fzn.int_ne_reif("C{}_Schedule".format(c2),
                                    sched2.id,
                                    c2notsched2,
                                    defines=c2notsched2,
                                    name="SameDays_H")

                    fzn.array_bool_or([c1notsched1, c2notsched2],
                                      True,
                                      name="SameDays_H")

    def same_days_soft(self, classes, fzn, dat, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            for s1 in dat.classes[c1].schedules:
                diffdays_schedules = []
                sched1 = dat.unique_schedules[s1]
                for s2 in dat.classes[c2].schedules:
                    sched2 = dat.unique_schedules[s2]
                    if not (((sched1.days | sched2.days) == sched1.days) or
                            ((sched1.days | sched2.days) == sched2.days)):
                        diffdays_schedules.append(sched2.id)

                c1s1c2_diffdays = fzn.bool_var("C{}DiffDays{}S{}".format(
                    c2, c1, sched1.id))
                c2sched_diffdaysc1s1 = fzn.bool_var(
                    "C{}ScheduleDiffDaysC{}S{}".format(c2, c1, sched1.id))
                c1schedule1 = fzn.bool_var("C{}Schedule{}".format(
                    c1, sched1.id))
                fzn.set_in_reif("C{}_Schedule".format(c2),
                                diffdays_schedules,
                                c2sched_diffdaysc1s1,
                                defines=c2sched_diffdaysc1s1,
                                name="SameDays_S")
                fzn.array_bool_and([c1schedule1, c2sched_diffdaysc1s1],
                                   c1s1c2_diffdays,
                                   defines=c1s1c2_diffdays,
                                   name="SameDays_S")

                self.soft_vars.append(c1s1c2_diffdays)
                self.penalties.append(penalty)

    def different_days_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if ((sched1.days | sched2.days) == sched1.days) or (
                    (sched1.days | sched2.days) == sched2.days):
                    c1notsched1 = fzn.bool_var("C{}NotSchedule{}".format(
                        c1, sched1.id))
                    c2notsched2 = fzn.bool_var("C{}NotSchedule{}".format(
                        c2, sched2.id))
                    fzn.int_ne_reif("C{}_Schedule".format(c1),
                                    sched1.id,
                                    c1notsched1,
                                    defines=c1notsched1,
                                    name="DifferentDays_H")
                    fzn.int_ne_reif("C{}_Schedule".format(c2),
                                    sched2.id,
                                    c2notsched2,
                                    defines=c2notsched2,
                                    name="DifferentDays_H")

                    fzn.array_bool_or([c1notsched1, c2notsched2],
                                      True,
                                      name="DifferentDays_H")

    def different_days_soft(self, classes, fzn, dat, penalty):
        # Soft Constraints
        for c1, c2 in itertools.combinations(classes, 2):
            for s1 in dat.classes[c1].schedules:
                samedays_schedules = []
                sched1 = dat.unique_schedules[s1]
                for s2 in dat.classes[c2].schedules:
                    sched2 = dat.unique_schedules[s2]
                    if ((sched1.days | sched2.days) == sched1.days) or (
                        (sched1.days | sched2.days) == sched2.days):
                        samedays_schedules.append(sched2.id)

                c1s1c2_samedays = fzn.bool_var("C{}SameDays{}S{}".format(
                    c2, c1, sched1.id))
                c2sched_samedaysc1s1 = fzn.bool_var(
                    "C{}ScheduleSameDaysC{}S{}".format(c2, c1, sched1.id))
                c1schedule1 = fzn.bool_var("C{}Schedule{}".format(
                    c1, sched1.id))
                fzn.set_in_reif("C{}_Schedule".format(c2),
                                samedays_schedules,
                                c2sched_samedaysc1s1,
                                defines=c2sched_samedaysc1s1,
                                name="DifferentDays_S")
                fzn.array_bool_and([c1schedule1, c2sched_samedaysc1s1],
                                   c1s1c2_samedays,
                                   defines=c1s1c2_samedays,
                                   name="DifferentDays_S")

                self.soft_vars.append(c1s1c2_samedays)
                self.penalties.append(penalty)

    def different_time_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            if (not dat.classes[c1].is_fixed()) and (
                    not dat.classes[c2].is_fixed()):
                pos_var = []
                i = 1
                for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                                dat.classes[c2].schedules):
                    sched1 = dat.unique_schedules[s1]
                    sched2 = dat.unique_schedules[s2]

                    if (sched1.end <= sched2.start) or (sched2.end <=
                                                        sched1.start):
                        fzn.bool_var("C{0}C{1}DiffTime{2}".format(c1, c2, i))
                        fzn.array_bool_and(
                            [
                                "C{}Schedule{}".format(c1, sched1.id),
                                "C{}Schedule{}".format(c2, sched2.id)
                            ],
                            "C{}C{}DiffTime{}".format(c1, c2, i),
                            defines="C{}C{}DiffTime{}".format(c1, c2, i),
                            name="DifferentTime_H")
                        pos_var.append("C{}C{}DiffTime{}".format(c1, c2, i))
                        i += 1

                if len(pos_var) > 0:
                    fzn.array_bool_or(pos_var, True, name="DifferentTime_H")

    def different_time_soft(self, classes, fzn, dat, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1
            for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                            dat.classes[c2].schedules):
                sched1 = dat.unique_schedules[s1]
                sched2 = dat.unique_schedules[s2]

                if (sched1.start <= sched2.start and sched2.end <= sched1.end
                    ) or (sched2.start <= sched1.start
                          and sched1.end <= sched2.end):
                    c1c2_sametime = fzn.bool_var("C{0}C{1}SameTime{2}".format(
                        c1, c2, i))
                    fzn.array_bool_and([
                        "C{}Schedule{}".format(c1, sched1.id),
                        "C{}Schedule{}".format(c2, sched2.id)
                    ],
                                       c1c2_sametime,
                                       defines=c1c2_sametime,
                                       name="DifferentTime_S")
                    pos_var.append("C{0}C{1}SameTime{2}".format(c1, c2, i))
                    i += 1

            if len(pos_var) > 0:
                c1c2_sametime = fzn.bool_var("C{}C{}SameTime".format(c1, c2))
                fzn.array_bool_or(pos_var,
                                  c1c2_sametime,
                                  name="DifferentTime_S")

                c1c2_sametime_int = fzn.int_var("C{}C{}SameTime_int".format(
                    c1, c2),
                                                domain="0..1")
                fzn.bool2int(c1c2_sametime,
                             c1c2_sametime_int,
                             defines=c1c2_sametime_int,
                             name="DifferentTime_S")
                self.soft_vars.append(c1c2_sametime_int)
                self.penalties.append(penalty)

    def same_attendees_hard(self, classes, fzn, dat):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1

            for r1, r2 in itertools.product(dat.classes[c1].rooms,
                                            dat.classes[c2].rooms):
                c1room1 = fzn.bool_var("C{0}Room{1}".format(c1, r1))
                c2room2 = fzn.bool_var("C{0}Room{1}".format(c2, r2))
                fzn.int_eq_reif("C{}_Room".format(c1),
                                r1,
                                c1room1,
                                defines=c1room1,
                                name="SameAttendees_H")
                fzn.int_eq_reif("C{}_Room".format(c2),
                                r2,
                                c2room2,
                                defines=c2room2,
                                name="SameAttendees_H")

                for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                                dat.classes[c2].schedules):
                    sched1 = dat.unique_schedules[s1]
                    sched2 = dat.unique_schedules[s2]

                    if (sched1.end + dat.rooms[r1]['travel'][r2] <=
                            sched2.start
                        ) or (sched2.end + dat.rooms[r2]['travel'][r1] <=
                              sched1.start) or (
                                  not (sched1.weeks & sched2.weeks).any()) or (
                                      not (sched1.days & sched2.days).any()):
                        pass
                    else:
                        fzn.bool_var("C{0}C{1}SameAttendees{2}".format(
                            c1, c2, i))
                        fzn.array_bool_and(
                            [
                                "C{}Schedule{}".format(
                                    c1, sched1.id), "C{}Schedule{}".format(
                                        c2, sched2.id), c1room1, c2room2
                            ],
                            "C{}C{}SameAttendees{}".format(c1, c2, i),
                            defines="C{}C{}SameAttendees{}".format(c1, c2, i),
                            name="SameAttendees_H")
                        pos_var.append("C{0}C{1}SameAttendees{2}".format(
                            c1, c2, i))
                        i += 1

            if len(pos_var) > 0:
                fzn.array_bool_or(pos_var, False, name="SameAttendees_H")

    def same_attendees_soft(self, classes, fzn, dat, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            pos_var = []
            i = 1
            for r1, r2 in itertools.product(dat.classes[c1].rooms,
                                            dat.classes[c2].rooms):
                c1roomx = fzn.bool_var("C{0}Room{1}".format(c1, r1))
                c2roomy = fzn.bool_var("C{0}Room{1}".format(c2, r2))
                fzn.int_eq_reif("C{}_Room".format(c1),
                                r1,
                                c1roomx,
                                defines=c1roomx,
                                name="SameAttendees_S")
                fzn.int_eq_reif("C{}_Room".format(c2),
                                r2,
                                c2roomy,
                                defines=c2roomy,
                                name="SameAttendees_S")

                for s1, s2 in itertools.product(dat.classes[c1].schedules,
                                                dat.classes[c2].schedules):
                    sched1 = dat.unique_schedules[s1]
                    sched2 = dat.unique_schedules[s2]

                    if (sched1.end + dat.rooms[r1]['travel'][r2] <= sched2.start) or \
                       (sched2.end + dat.rooms[r2]['travel'][r1] <= sched1.start) or \
                       (not (sched1.weeks & sched2.weeks).any()) or (not (sched1.days & sched2.days).any()):
                        pass
                    else:
                        c1c2sameattendeesi = fzn.bool_var(
                            "C{0}C{1}SameAttendees{2}".format(c1, c2, i))
                        fzn.array_bool_and([
                            "C{}Schedule{}".format(
                                c1, sched1.id), "C{}Schedule{}".format(
                                    c2, sched2.id), c1roomx, c2roomy
                        ],
                                           c1c2sameattendeesi,
                                           defines=c1c2sameattendeesi,
                                           name="SameAttendees_S")
                        pos_var.append(c1c2sameattendeesi)
                        i += 1
            if len(pos_var) > 0:
                c1c2sameattendees = fzn.bool_var(
                    "C{0}C{1}SameAttendees".format(c1, c2))
                fzn.array_bool_or(pos_var,
                                  c1c2sameattendees,
                                  defines=c1c2sameattendees,
                                  name="SameAttendees_S")

                c1c2sameattendees_int = fzn.int_var(
                    "C{0}C{1}SameAttendees_int".format(c1, c2), domain="0..1")
                fzn.bool2int(c1c2sameattendees,
                             c1c2sameattendees_int,
                             defines=c1c2sameattendees_int,
                             name="SameAttendees_S")

                self.soft_vars.append(c1c2sameattendees_int)
                self.penalties.append(penalty)

    def max_block_hard(self, classes, fzn, dat, m, s):
        arrs = list(dat.classes[c].schedules for c in classes)
        for schedules in itertools.product(*arrs):
            pos_viol = False
            for week in range(0, dat.numWeeks):
                if pos_viol:
                    break
                for day in range(0, 7):
                    inblock = []
                    blockstart = 288
                    blockend = 0
                    for sched in schedules:
                        # Check if schedule occurs on day and week
                        if dat.unique_schedules[sched].days[
                                day] and dat.unique_schedules[sched].weeks[
                                    week]:
                            # Check if it belongs to the block
                            if len(inblock) == 0:
                                inblock.append(sched)
                                blockstart = int(
                                    dat.unique_schedules[sched].start)
                                blockend = int(dat.unique_schedules[sched].end)
                            elif dat.unique_schedules[
                                    sched].start - blockend <= s:
                                inblock.append(sched)
                                if dat.unique_schedules[
                                        sched].start < blockstart:
                                    blockstart = dat.unique_schedules[
                                        sched].start

                                if dat.unique_schedules[sched].end > blockend:
                                    blockend = dat.unique_schedules[sched].end

                    # A block consist of more than 1 class
                    if len(inblock) > 1:
                        # check length of block: B.end - B.start <= M
                        if blockend - blockstart > int(m):
                            pos_viol = True

            if pos_viol:
                for i in range(0, len(classes)):
                    c1notsched1 = fzn.bool_var("C{}NotSchedule{}".format(
                        classes[i], dat.unique_schedules[schedules[i]].id))
                    fzn.int_ne_reif("C{}_Schedule".format(classes[i]),
                                    dat.unique_schedules[schedules[i]].id,
                                    c1notsched1,
                                    defines=c1notsched1,
                                    name="MaxBlock_H")

                fzn.array_bool_or([
                    "C" + str(classes[i]) + "NotSchedule" +
                    str(dat.unique_schedules[schedules[i]].id)
                    for i in range(0, len(classes))
                ],
                                  True,
                                  name="MaxBlock_H")

    def max_block_soft(self, classes, fzn, dat, m, s, penalty):
        arrs = list(dat.classes[c].schedules for c in classes)
        for schedules in itertools.product(*arrs):
            pos_viol = False
            for week in range(0, dat.numWeeks):
                if pos_viol:
                    break
                for day in range(0, 7):
                    inblock = []
                    blockstart = 288
                    blockend = 0
                    for sched in schedules:
                        # Check if schedule occurs on day and week
                        if dat.unique_schedules[sched].days[
                                day] and dat.unique_schedules[sched].weeks[
                                    week]:
                            # Check if it belongs to the block
                            if len(inblock) == 0:
                                inblock.append(sched)
                                blockstart = dat.unique_schedules[sched].start
                                blockend = dat.unique_schedules[sched].end
                            elif dat.unique_schedules[
                                    sched].start - blockend <= int(s):
                                inblock.append(sched)
                                if dat.unique_schedules[
                                        sched].start < blockstart:
                                    blockstart = dat.unique_schedules[
                                        sched].start

                                if dat.unique_schedules[sched].end > blockend:
                                    blockend = dat.unique_schedules[sched].end

                    # A block consist of more than 1 class
                    if len(inblock) > 1:
                        # check length of block: B.end - B.start <= M
                        if blockend - blockstart > int(m):
                            pos_viol = True

            if pos_viol:
                maxblocksofti = fzn.bool_var("MaxBlockSoft{}".format(
                    len(self.soft_vars)))
                maxblocksofti_int = fzn.int_var("MaxBlockSoft{}_int".format(
                    len(self.soft_vars)),
                                                domain="0..1")
                fzn.array_bool_and([
                    "C" + str(classes[i]) + "Schedule" +
                    str(dat.unique_schedules[schedules[i]].id)
                    for i in range(0, len(classes))
                ],
                                   maxblocksofti,
                                   defines=maxblocksofti,
                                   name="MaxBlock_S")
                fzn.bool2int(maxblocksofti,
                             maxblocksofti_int,
                             defines=maxblocksofti_int,
                             name="MaxBlock_S")

                self.soft_vars.append(maxblocksofti_int)
                self.penalties.append(penalty)

    def max_breaks_hard(self, classes, fzn, dat, r, s):
        arrs = list(dat.classes[c].schedules for c in classes)
        for schedules in itertools.product(*arrs):
            pos_viol = False
            for week in range(0, dat.numWeeks):
                if pos_viol:
                    break
                for day in range(0, 7):
                    blocks = []
                    blockstart = []
                    blockend = []
                    num_blocks = 0
                    for s in schedules:
                        # Check if schedule occurs on day and week
                        if dat.unique_schedules[s].days[
                                day] and dat.unique_schedules[s].weeks[week]:
                            # Check if it belongs to the block
                            if len(blocks) == 0:
                                blocks.append([s])
                                blockstart.append(
                                    dat.unique_schedules[s].start)
                                blockend.append(dat.unique_schedules[s].end)
                                num_blocks += 1
                            else:
                                for b in range(0, len(blocks)):
                                    if dat.unique_schedules[
                                            s].start - blockend[b] <= int(s):
                                        blocks[b].append(s)
                                        if dat.unique_schedules[
                                                s].start < blockstart[b]:
                                            blockstart[
                                                b] = dat.unique_schedules[
                                                    s].start
                                            num_blocks += 1

                                        if dat.unique_schedules[
                                                s].end > blockend[b]:
                                            blockend[b] = dat.unique_schedules[
                                                s].end
                                            num_blocks += 1

                    # A block consist of more than 1 class
                    for b in blocks:
                        if len(b) > 1:
                            # check length of block: B.end - B.start <= M
                            if num_blocks > int(r):
                                pos_viol = True

            if pos_viol:
                fzn.array_bool_and([
                    "C" + str(classes[i]) + "Schedule" +
                    str(dat.unique_schedules[schedules[i]].id)
                    for i in range(0, len(classes))
                ],
                                   False,
                                   name="MaxBreaks_H")

    def max_breaks_soft(self, classes, fzn, dat, r, s, penalty):
        arrs = list(dat.classes[c].schedules for c in classes)
        for schedules in itertools.product(*arrs):
            pos_viol = False
            for week in range(0, dat.numWeeks):
                if pos_viol:
                    break
                for day in range(0, 7):
                    blocks = []
                    blockstart = []
                    blockend = []
                    num_blocks = 0
                    for s in schedules:
                        # Check if schedule occurs on day and week
                        if dat.unique_schedules[s].days[
                                day] and dat.unique_schedules[s].weeks[week]:
                            # Check if it belongs to the block
                            if len(blocks) == 0:
                                blocks.append([s])
                                blockstart.append(
                                    dat.unique_schedules[s].start)
                                blockend.append(dat.unique_schedules[s].end)
                                num_blocks += 1
                            else:
                                for b in range(0, len(blocks)):
                                    if dat.unique_schedules[
                                            s].start - blockend[b] <= int(s):
                                        blocks[b].append(s)
                                        if dat.unique_schedules[
                                                s].start < blockstart[b]:
                                            blockstart[
                                                b] = dat.unique_schedules[
                                                    s].start
                                            num_blocks += 1

                                        if dat.unique_schedules[
                                                s].end > blockend[b]:
                                            blockend[b] = dat.unique_schedules[
                                                s].end
                                            num_blocks += 1

                    # A block consist of more than 1 class
                    for b in blocks:
                        if len(b) > 1:
                            # check length of block: B.end - B.start <= M
                            if num_blocks > int(r):
                                pos_viol = True

            if pos_viol:
                maxbreakssofti = fzn.bool_var("MaxBreaksSoft{}".format(
                    len(self.soft_vars)))
                maxbreakssofti_int = fzn.int_var("MaxBreaksSoft{}_int".format(
                    len(self.soft_vars)),
                                                 domain="0..1")
                fzn.array_bool_and([
                    "C" + str(classes[i]) + "Schedule" +
                    str(dat.unique_schedules[schedules[i]].id)
                    for i in range(0, len(classes))
                ],
                                   maxbreakssofti,
                                   defines=maxbreakssofti,
                                   name="MaxBreaks_S")
                fzn.bool2int(maxbreakssofti,
                             maxbreakssofti_int,
                             defines=maxbreakssofti_int,
                             name="MaxBreaks_S")

                self.soft_vars.append(maxbreakssofti_int)
                self.penalties.append(penalty)

    def max_day_load_hard(self, classes, fzn, dat, ps):
        # Notes
        # For every class, schedule, day and week
        # cs_day_d_and_week_w <-> S_c == s /\ s in indayschedules /\ s in inweekschedules
        #
        # Meaning that cs_day_d_and_week_w is 1 if c has schedule s and s is in day d and s is in week w
        #
        # for d in days and w in weeks:
        #   int_lin_le([cs_day_d_and_week_w | c in classes, s in schedules], [cs.len | c in classes, s in schedules],S)

        # Write scheduleInDay and scheduleInWeek
        cs_lengths = []
        cs_in_week_and_day = []
        for c in classes:
            for w in range(0, dat.numWeeks):
                inweekschedules = set()
                for s in dat.classes[c].schedules:
                    if dat.unique_schedules[s].weeks[w]:
                        inweekschedules.add(dat.unique_schedules[s].id)
                cinweeki = fzn.bool_var("C{0}InWeek{1}".format(c, w))
                fzn.set_in_reif("C{}_Schedule".format(c),
                                inweekschedules,
                                cinweeki,
                                defines=cinweeki,
                                name="MaxDayLoad_H")
            for d in range(0, 7):
                indayschedules = set()
                for s in dat.classes[c].schedules:
                    if dat.unique_schedules[s].days[d]:
                        indayschedules.add(dat.unique_schedules[s].id)
                cindayi = fzn.bool_var("C{0}InDay{1}".format(c, d))
                fzn.set_in_reif("C{}_Schedule".format(c),
                                indayschedules,
                                cindayi,
                                defines=cindayi,
                                name="MaxDayLoad_H")

            for s in dat.classes[c].schedules:
                sched = dat.unique_schedules[s]
                for w in range(0, dat.numWeeks):
                    for d in range(0, 7):
                        cs_in_week_day_var = fzn.bool_var(
                            "C{}S{}InWeek{}Day{}".format(c, sched.id, w, d))
                        cs_in_week_day_int = fzn.int_var(
                            "C{}S{}InWeek{}Day{}_int".format(
                                c, sched.id, w, d),
                            domain="0..1")
                        fzn.array_bool_and([
                            "C{}Schedule{}".format(c, sched.id),
                            "C{}InWeek{}".format(c, w), "C{}InDay{}".format(
                                c, d)
                        ],
                                           cs_in_week_day_var,
                                           defines=cs_in_week_day_var,
                                           name="MaxDayLoad_H")
                        fzn.bool2int(cs_in_week_day_var,
                                     cs_in_week_day_int,
                                     defines=cs_in_week_day_int,
                                     name="MaxDayLoad_H")

        for w in range(0, dat.numWeeks):
            for d in range(0, 7):
                fzn.int_lin_le([
                    dat.unique_schedules[s].length for c in classes
                    for s in dat.classes[c].schedules
                ], [
                    "C{}S{}InWeek{}Day{}_int".format(
                        c, dat.unique_schedules[s].id, w, d) for c in classes
                    for s in dat.classes[c].schedules
                ],
                               ps,
                               name="MaxDayLoad_H")

    def max_day_load_soft(self, classes, fzn, dat, ps, distnum, penalty):
        # Notes
        # For every class, schedule, day and week
        # cs_day_d_and_week_w <-> S_c == s /\ s in indayschedules /\ s in inweekschedules
        #
        # Meaning that cs_day_d_and_week_w is 1 if c has schedule s and s is in day d and s is in week w
        #
        # for d in days and w in weeks:
        #   int_lin_le([cs_day_d_and_week_w | c in classes, s in schedules], [cs.len | c in classes, s in schedules],S)

        # Write scheduleInDay and scheduleInWeek
        cs_lengths = []
        cs_in_week_and_day = []
        for c in classes:
            for w in range(0, dat.numWeeks):
                inweekschedules = set()
                for s in dat.classes[c].schedules:
                    if dat.unique_schedules[s].weeks[w]:
                        inweekschedules.add(dat.unique_schedules[s].id)
                cinweeki = fzn.bool_var("C{0}InWeek{1}".format(c, w))
                fzn.set_in_reif("C{}_Schedule".format(c),
                                inweekschedules,
                                cinweeki,
                                defines=cinweeki,
                                name="MaxDayLoad_S")
            for d in range(0, 7):
                indayschedules = set()
                for s in dat.classes[c].schedules:
                    if dat.unique_schedules[s].days[d]:
                        indayschedules.add(dat.unique_schedules[s].id)
                cindayi = fzn.bool_var("C{0}InDay{1}".format(c, d))
                fzn.set_in_reif("C{}_Schedule".format(c),
                                indayschedules,
                                cindayi,
                                defines=cindayi,
                                name="MaxDayLoad_S")

            for s in dat.classes[c].schedules:
                sched = dat.unique_schedules[s]
                for w in range(0, dat.numWeeks):
                    for d in range(0, 7):
                        cs_in_week_day_var = fzn.bool_var(
                            "C{}S{}InWeek{}Day{}".format(c, sched.id, w, d))
                        cs_in_week_day_int = fzn.int_var(
                            "C{}S{}InWeek{}Day{}_int".format(
                                c, sched.id, w, d),
                            domain="0..1")
                        fzn.array_bool_and([
                            "C{}Schedule{}".format(c, sched.id),
                            "C{}InWeek{}".format(c, w), "C{}InDay{}".format(
                                c, d)
                        ],
                                           cs_in_week_day_var,
                                           defines=cs_in_week_day_var,
                                           name="MaxDayLoad_S")
                        fzn.bool2int(cs_in_week_day_var,
                                     cs_in_week_day_int,
                                     defines=cs_in_week_day_int,
                                     name="MaxDayLoad_S")

        dayload_viols = []
        coeff = []
        for w in range(0, dat.numWeeks):
            for d in range(0, 7):
                lengths = [
                    dat.unique_schedules[s].length for c in classes
                    for s in dat.classes[c].schedules
                    if dat.unique_schedules[s].days[d]
                    and dat.unique_schedules[s].weeks[w]
                ]
                dayload_wxdy = fzn.int_var("DayLoadWeek{}Day{}".format(w, d),
                                           domain="0..{}".format(sum(lengths)))
                inweekandday = [
                    "C{}S{}InWeek{}Day{}_int".format(
                        c, dat.unique_schedules[s].id, w, d) for c in classes
                    for s in dat.classes[c].schedules
                ]
                lengths.append(-1)
                inweekandday.append(dayload_wxdy)
                fzn.int_lin_eq(lengths,
                               inweekandday,
                               0,
                               defines=dayload_wxdy,
                               name="MaxDayLoad_S")

                dayload_wxdy_minus_s = fzn.int_var(
                    "DayLoadWeek{}Day{}MinusS{}".format(w, d, distnum),
                    domain="{}..{}".format(-1 * ps, sum(lengths)))
                fzn.int_minus(dayload_wxdy,
                              ps,
                              dayload_wxdy_minus_s,
                              defines=dayload_wxdy_minus_s,
                              name="MaxDayLoad_S")

                dayload_wxdy_viol = fzn.int_var(
                    "DayLoadWeek{}Day{}Viol".format(w, d, distnum),
                    domain="0..{}".format(sum(lengths)))
                fzn.int_max(dayload_wxdy_minus_s,
                            0,
                            dayload_wxdy_viol,
                            defines=dayload_wxdy_viol,
                            name="MaxDayLoad_S")

                dayload_viols.append(dayload_wxdy_viol)
                coeff.append(1)

        dayloadviol = fzn.int_var("DayLoadViol{}".format(distnum),
                                  domain="0..{}".format(sum(lengths)))
        coeff.append(-1)
        dayload_viols.append(dayloadviol)

        fzn.int_lin_eq(coeff,
                       dayload_viols,
                       dayloadviol,
                       defines=dayloadviol,
                       name="MaxDayLoad_S")

        dayloadpenviol = fzn.int_var("DayLoadPenViol{}".format(distnum),
                                     domain="0..{}".format(sum(lengths)))
        fzn.int_times(dayloadviol,
                      penalty,
                      dayloadpenviol,
                      defines=dayloadpenviol,
                      name="MaxDayLoad_S")

        dayloadsoftvar = fzn.int_var("DayLoadSoftVar{}".format(distnum),
                                     domain="0..{}".format(sum(lengths)))
        fzn.int_div(dayloadpenviol,
                    dat.numWeeks,
                    dayloadsoftvar,
                    defines=dayloadsoftvar,
                    name="MaxDayLoad_S")

        self.soft_vars.append(dayloadsoftvar)
        self.penalties.append(1)

    def max_days_hard(self, classes, fzn, dat, ps, distnum):
        # Define days for each of the classes
        for c in classes:
            fzn.bool_var("C{}Day1".format(c))
            fzn.bool_var("C{}Day2".format(c))
            fzn.bool_var("C{}Day3".format(c))
            fzn.bool_var("C{}Day4".format(c))
            fzn.bool_var("C{}Day5".format(c))
            fzn.bool_var("C{}Day6".format(c))
            fzn.bool_var("C{}Day7".format(c))

            for s in dat.classes[c].schedules:
                sched = dat.unique_schedules[s]
                for i in range(0, 7):
                    cdayi = fzn.bool_var("C{}Day{}".format(c, i + 1))
                    fzn.bool_and("C{}Schedule{}".format(c, sched.id),
                                 sched.days[i],
                                 cdayi,
                                 name="MaxDays")

        for i in range(0, 7):
            maxdaysdayi = fzn.bool_var("MaxDays{}Day{}".format(distnum, i + 1))
            maxdaysdayi_int = fzn.int_var("MaxDays{}Day{}_int".format(
                distnum, i + 1),
                                          domain="0..1")
            fzn.array_bool_or(["C{}Days{}".format(c, i + 1) for c in classes],
                              maxdaysdayi,
                              name="MaxDays_H")
            fzn.bool2int(maxdaysdayi,
                         maxdaysdayi_int,
                         defines=maxdaysdayi_int,
                         name="MaxDays_H")

        fzn.int_lin_le(
            [1, 1, 1, 1, 1, 1, 1],
            ["MaxDays{0}Day{1}".format(distnum, i + 1) for i in range(0, 7)],
            ps,
            name="MaxDays_H")

    def max_days_soft(self, classes, fzn, dat, ps, distnum, penalty):
        # Define days for each of the classes
        for c in classes:
            fzn.bool_var("C{}Day1".format(c))
            fzn.bool_var("C{}Day2".format(c))
            fzn.bool_var("C{}Day3".format(c))
            fzn.bool_var("C{}Day4".format(c))
            fzn.bool_var("C{}Day5".format(c))
            fzn.bool_var("C{}Day6".format(c))
            fzn.bool_var("C{}Day7".format(c))

            for s in dat.classes[c].schedules:
                sched = dat.unique_schedules[s]
                for i in range(0, 7):
                    cdayi = fzn.bool_var("C{}Day{}".format(c, i + 1))
                    fzn.bool_and("C{}Schedule{}".format(c, sched.id),
                                 sched.days[i],
                                 cdayi,
                                 name="MaxDays_S")

        for i in range(0, 7):
            maxdaysdayi = fzn.bool_var("MaxDays{}Day{}".format(distnum, i + 1))
            maxdaysdayi_int = fzn.int_var("MaxDays{}Day{}_int".format(
                distnum, i + 1),
                                          domain="0..1")
            fzn.array_bool_or(["C{}Days{}".format(c, i + 1) for c in classes],
                              maxdaysdayi,
                              name="MaxDays_S")
            fzn.bool2int(maxdaysdayi,
                         maxdaysdayi_int,
                         defines=maxdaysdayi_int,
                         name="MaxDays_S")

        v = ["MaxDays{0}Day{1}".format(distnum, i + 1) for i in range(0, 7)]
        maxdaysi = fzn.int_var("MaxDays{0}".format(distnum), domain="0..7")
        v.append(maxdaysi)
        fzn.int_lin_eq([1, 1, 1, 1, 1, 1, 1, -1],
                       v,
                       0,
                       defines=maxdaysi,
                       name="MaxDays_S")
        penalty = fzn.int_var("MaxDays{}Penalty".format(distnum),
                              domain="0..7")
        fzn.int_minus(maxdaysi, ps, penalty, defines=penalty, name="MaxDays_S")
        self.soft_vars.append(maxdaysi)
        self.penalties.append(penalty)

    def min_gap_hard(self, classes, fzn, dat, mingap_schedules):
        for c1, c2 in itertools.combinations(classes, 2):
            pos = []
            i = 0
            for s1 in dat.classes[c1].schedules:
                sched1 = dat.unique_schedules[s1]
                c1sched1 = fzn.bool_var("C{}Schedule{}".format(c1, sched1.id))
                c2sched_in_c1mingap = fzn.bool_var(
                    "C{}ScheduleInC{}MinGap".format(c2, c1))
                fzn.set_in_reif("C{0}_Schedule".format(c2),
                                mingap_schedules[sched1.id],
                                c2sched_in_c1mingap,
                                name="MinGap_H")
                c1c2mingap = fzn.bool_var("C{}C{}MinGap{}".format(c1, c2, i))
                fzn.array_bool_and([c1sched1, c2sched_in_c1mingap],
                                   c1c2mingap,
                                   defines=c1c2mingap,
                                   name="MinGap_H")
                pos.append(c1c2mingap)
                i += 1
            fzn.array_bool_or(pos, True, name="MinGap_H")

    def min_gap_soft(self, classes, fzn, dat, notmingap_schedules, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            pos = []
            i = 0
            for s1 in dat.classes[c1].schedules:
                sched1 = dat.unique_schedules[s1]
                c1sched1 = fzn.bool_var("C{}Schedule{}".format(c1, sched1.id))
                c2sched_notin_c1mingap = fzn.bool_var(
                    "C{}ScheduleNotInC{}MinGap".format(c2, c1))
                fzn.set_in_reif("C{0}_Schedule".format(c2),
                                notmingap_schedules[sched1.id],
                                c2sched_notin_c1mingap,
                                defines=c2sched_notin_c1mingap,
                                name="MinGap_S")
                c1c2notmingapi = fzn.bool_var("C{}C{}NotMinGap{}".format(
                    c1, c2, i))
                fzn.array_bool_and([c1sched1, c2sched_notin_c1mingap],
                                   c1c2notmingapi,
                                   defines=c1c2notmingapi,
                                   name="MinGap_S")
                pos.append(c1c2notmingapi)
                i += 1
            c1c2notmingap = fzn.bool_var("C{}C{}NotMinGap".format(c1, c2))
            c1c2notmingap_int = fzn.int_var("C{}C{}NotMinGap_int".format(
                c1, c2),
                                            domain="0..1")
            fzn.array_bool_or(pos,
                              c1c2notmingap,
                              defines=c1c2notmingap,
                              name="MinGap_S")
            fzn.bool2int(c1c2notmingap,
                         c1c2notmingap_int,
                         defines=c1c2notmingap_int,
                         name="MinGap_S")
            self.soft_vars.append(c1c2notmingap_int)
            self.penalties.append(penalty)

    def work_day_hard(self, classes, fzn, dat, workday_schedules):
        for c1, c2 in itertools.combinations(classes, 2):
            pos = []
            i = 1
            for s1 in dat.classes[c1].schedules:
                sched1 = dat.unique_schedules[s1]
                c1sched1 = fzn.bool_var("C{}Schedule{}".format(c1, sched1.id))
                c2sched_in_c1workday = fzn.bool_var(
                    "C{}ScheduleInC{}S{}WorkDay".format(c2, c1, sched1.id))
                pos_schedules = [
                    dat.unique_schedules[s].id for s in workday_schedules[s1]
                ]
                if len(pos_schedules) > 0:
                    fzn.set_in_reif("C{0}_Schedule".format(c2),
                                    pos_schedules,
                                    c2sched_in_c1workday,
                                    defines=c2sched_in_c1workday,
                                    name="WorkDay_H")
                    c1c2workday = fzn.bool_var("C{}C{}Workday{}".format(
                        c1, c2, i))
                    fzn.array_bool_and([c1sched1, c2sched_in_c1workday],
                                       c1c2workday,
                                       defines=c1c2workday,
                                       name="WorkDay_H")
                    pos.append(c1c2workday)
                    i += 1
            fzn.array_bool_or(pos, True, name="WorkDay_H")

    def work_day_soft(self, classes, fzn, dat, notworkday_schedules, penalty):
        for c1, c2 in itertools.combinations(classes, 2):
            pos = []
            i = 1
            for s1 in dat.classes[c1].schedules:
                sched1 = dat.unique_schedules[s1]
                c1sched1 = fzn.bool_var("C{}Schedule{}".format(c1, sched1.id))
                c2sched_in_c1workday = fzn.bool_var(
                    "C{}ScheduleNotInC{}S{}WorkDay".format(c2, c1, sched1.id))
                pos_schedules = [
                    dat.unique_schedules[s].id
                    for s in notworkday_schedules[s1]
                ]
                if pos_schedules:
                    fzn.set_in_reif("C{0}_Schedule".format(c2),
                                    pos_schedules,
                                    c2sched_in_c1workday,
                                    defines=c2sched_in_c1workday,
                                    name="WorkDay_S")
                    c1c2notworkdayi = fzn.bool_var("C{}C{}NotWorkday{}".format(
                        c1, c2, i))
                    fzn.array_bool_and([c1sched1, c2sched_in_c1workday],
                                       c1c2notworkdayi,
                                       defines=c1c2notworkdayi,
                                       name="WorkDay_S")
                    pos.append(c1c2notworkdayi)
                    i += 1

            c1c2notworkday = fzn.bool_var("C{}C{}NotWorkDay".format(c1, c2))
            c1c2notworkday_int = fzn.int_var("C{}C{}NotWorkDay_int".format(
                c1, c2),
                                             domain="0..1")
            fzn.array_bool_or(pos,
                              c1c2notworkday,
                              defines=c1c2notworkday,
                              name="WorkDay_S")
            fzn.bool2int(c1c2notworkday,
                         c1c2notworkday_int,
                         defines=c1c2notworkday_int,
                         name="WorkDay_S")

            self.soft_vars.append(c1c2notworkday_int)
            self.penalties.append(penalty)
