import time

class WriterStatus:
    def __init__(self, name):
        self.start_time = time.time()
        self.name = name
        self.num = 0
        self.constraints = 0
        self.variables = 0

    def update(self, num = None):
        if num is not None:
            self.num = num
        else:
            self.num += 1
        print("Writing {} {}".format(self.name, self.num), end="\r")

    def addvar(self):
        self.variables += 1

    def addcon(self):
        self.constraints += 1

    def done(self, num = None):
        if num is not None:
            self.num = num
        else:
            self.num += 1
        spacer = 50 - (len(str(self.num)) + len(self.name))
        print("Wrote {} {} (v: {}, c: {}) {}{:0.3f} seconds".format(self.num, self.name, self.variables, self.constraints,"." * spacer, time.time()-self.start_time))
       
