import data
import json

class logger:
    def __init__(self, data, dirname):
        #with open(dirname+"/rooms.json","w") as filehandle:
        #    json.dump(data.rooms,filehandle,indent=2,separators=(', ',': '))
        #with open(dirname+"/courses.json","w") as filehandle:
        #    json.dump(data.courses,filehandle,indent=2,separators=(', ',': '))
        with open(dirname+"/students.json","w") as filehandle:
            json.dump(data.students,filehandle,indent=2,separators=(', ',': '))
        with open(dirname+"/distributions.json","w") as filehandle:
            json.dump(data.distributions,filehandle,indent=2,separators=(', ',': '))
        with open(dirname+"/course_tree.json", "w") as filehandle:
            json.dump(data.course_tree,filehandle,indent=2,separators=(', ',': '))

    
