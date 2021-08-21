import schedule

class Clas:
    def __init__(self, cid):
        self.cid = cid
        self.schedule_var = "C" + str(cid) + "_Schedule"
        self.room_var = "C" + str(cid) + "_Room"
        self.schedules = set()
        self.rooms = set()
        self.schedule_penalty = {}
        self.room_penalty = {}
        self.attending = 0
        self.limit = 0

    def add_schedule(self, schedule):
        self.schedules.add(schedule)

    def add_room(self, room):
        self.rooms.add(room)

    def add_room_penalty(self, room, penalty):
        self.room_penalty[room] = penalty

    def is_fixed(self):
        if len(self.rooms) <= 1 and len(self.schedules) <= 1:
            return True
        return False

    def has_fixed_room(self):
        if len(self.rooms) <= 1:
            return True
        return False

    def has_fixed_schedule(self):
        if len(self.rooms) <= 1:
            return True
        return False
