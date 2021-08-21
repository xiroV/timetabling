import getopt
import sys
from fznwriter import FznWriter
import data

def main(argv):
    try:                                
        opts, args = getopt.getopt(argv, "ho:r:n:i:", ["help", "outputfile=", "include_names=", "instancename=", "instancefile="]) 
    except getopt.GetoptError:           
        usage()                     
        sys.exit("Parsing error in command line options")                     
        
    if (len(opts)<1):
        usage()
        sys.exit("Command line options missing")                     

    output_file = ""
    include_names = ""
    instance_file = ""
    instance_name = ""
    for opt, arg in opts:                
        if opt in ("-h", "--help"):      
            usage()                     
            sys.exit(0)
        if opt in ("-o", "--outputfile"):      
            output_file = arg
        elif opt in ("-i", "--instancefile"): 
            instance_file = arg        
        elif opt in ("-n", "--instancename"): 
            instance_name = arg
        elif opt in ("--include_names"): 
            if arg in ["true", "True", "1"]:
                include_names = True
            else:
                include_names = False

        

    instance = data.Data(instance_file)
    instance.find_schedule_overlaps()
    fznwriter = FznWriter(instance, include_names)
    fznwriter.write(output_file)


if __name__ == "__main__":
    main(sys.argv[1:])

