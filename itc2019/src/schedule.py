import bitarray

class Schedule:
    def __init__(self, sid, weeks, days, start, length):
        self.id = sid
        self.name = "T" + str(sid)
        self.weeks = weeks
        self.days = days
        self.start = start
        self.length = length
        self.end = self.start + self.length

    def key(self):
        return self.weeks.to01() + "_" + self.days.to01() + "_" + str(self.start) + "_" + str(self.length)

    def overlap_with(self, s):
        # Time overlap
        if (self.end > s.start and self.start <= s.start) \
           or (s.end > self.start and s.start <= self.start) \
           or (s.start <= self.start and s.end > self.end) \
           or (self.start <= s.start and self.end > s.end):

                # Day overlap
                if (self.days & s.days).any():

                    # Week overlap
                    if (self.weeks & s.weeks).any():
                        return True

        return False

    def first_week(self):
        i = 1
        for w in self.weeks:
            if w:
                return i
            i += 1

    def first_day(self):
        i = 1
        for d in self.days:
            if d:
                return i
            i += 1


