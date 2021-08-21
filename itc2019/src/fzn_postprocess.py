import getopt
import sys
from fznresult import Result
import data

def main(argv):
    try:                                
        opts, args = getopt.getopt(argv, "ho:r:n:i:", ["help", "outputfile=", "resultfile=", "instancename=", "instancefile="]) 
    except getopt.GetoptError:           
        usage()                     
        sys.exit("Parsing error in command line options")                     
        
    if (len(opts)<1):
        usage()
        sys.exit("Command line options missing")                     

    output_file = ""
    result_file = ""
    instance_file = ""
    instance_name = ""
    for opt, arg in opts:                
        if opt in ("-h", "--help"):      
            usage()                     
            sys.exit(0)
        if opt in ("-o", "--outputfile"):      
            output_file = arg
        elif opt in ("-r", "--resultfile"): 
            result_file = arg        
        elif opt in ("-i", "--instancefile"): 
            instance_file = arg        
        elif opt in ("-n", "--instancename"): 
            instance_name = arg
        

    instance = data.Data(instance_file)
    out = Result(instance_name, instance, output_file)
    out.write_result(result_file)

if __name__ == "__main__":
    main(sys.argv[1:])

