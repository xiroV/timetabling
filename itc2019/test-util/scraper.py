from bs4 import BeautifulSoup
import os

problems = []

instance_info_dir = "instance_info"

dirs = os.listdir(instance_info_dir)

for d in dirs:
    instance_files = os.listdir(os.path.join(instance_info_dir,d))

    for ifile in instance_files:
        ifile_path = os.path.join(instance_info_dir,d,ifile)
        
        with open(ifile_path) as f:
            soup = BeautifulSoup(f, 'html.parser')

            p = {}
            p['set'] = d

            for tr in soup.find_all('tr'):
                try:
                    rname = tr.contents[0].contents[0]
                    rval = tr.contents[1].contents[0]

                    if rname == "Instance Name:":
                        p['name'] = rval
                    elif rname == "Instance Size:":
                        p['size'] = rval
                    elif rname == "Number of Courses:":
                        p['courses'] = rval
                    elif rname == "Number of Classes:":
                        sval = rval.split(" ")
                        p['classes'] = sval[0]
                        if len(sval) > 1:
                            p['classes_fixed'] = sval[1]
                        else:
                            p['classes_fixed'] = '0'

                    elif rname == "Hard Distributions:":
                        p['hard_dist'] = rval
                    elif rname == "Soft Distributions:":
                        p['soft_dist'] = rval
                    elif rname == "Number of Rooms:":
                        p['rooms'] = rval
                    elif rname == "Number of Students:":
                        p['students'] = rval
                    elif rname == "Number of Weeks:":
                        p['weeks'] = rval
                    elif rname == "Classes without Room:":
                        p['classes_noroom'] = rval
                    elif rname == "Average Times of a Class:":
                        p['class_avg_schedules'] = rval
                    elif rname == "Average Rooms of a Class:":
                        p['class_avg_rooms'] = rval
                    elif rname == "Average Availability:":
                        p['avg_avail'] = rval[:-1] + "\%"
                except AttributeError:
                    pass

            problems.append(p)
                    

attr_name = {}
attr_name['name'] = "Name"
attr_name['classes'] = "Classes"
attr_name['size'] = "Size (MB)"
attr_name['courses'] = "Courses"
attr_name['classes_fixed'] = "Fixed Classes"
attr_name['hard_dist'] = "Hard Dist."
attr_name['soft_dist'] = "Soft Dist."
attr_name['rooms'] = "Rooms"
attr_name['students'] = "Students"
attr_name['weeks'] = "Weeks"
attr_name['classes_noroom'] = "Classes W/o Room"
attr_name['class_avg_schedules'] = "Avg. Schedules/Class"
attr_name['class_avg_rooms'] = "Avg. Rooms/Class"
attr_name['avg_avail'] = "Avg. Availability"

attrs = problems[0].keys()

for d in dirs:
    for attr in attrs:
        if attr != 'set':
            print(attr_name[attr]," & "," & ".join([x[attr] for x in problems if x['set'] == d]),"\\\\")
    print("")
