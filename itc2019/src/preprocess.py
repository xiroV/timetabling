import sys
import getopt
import data
import logger
import dznwriter
import time

def usage():
    print("\n")
    print("Usage: [--help, --instance=, --dznoutfile=, --mznoutfile]\n")

def main(argv):
    try:                                
        opts, args = getopt.getopt(argv, "hf:o:m:", ["help", "instance=", "dznoutfile=", "mznoutfile="]) 
    except getopt.GetoptError:           
        usage()                     
        sys.exit("Parsing error in command line options")                     
        
    if (len(opts)<1):
        usage()
        sys.exit("Command line options missing")                     


    instance_file = ""
    dzn_out_file=""
    mzn_out_file=""
    for opt, arg in opts:                
        if opt in ("-h", "--help"):      
            usage()                     
            sys.exit(0)
        if opt in ("-f", "--instance"):      
            instance_file = arg
        elif opt in ("-o", "--dznoutfile"): 
            dzn_out_file = arg        
        elif opt in ("-m", "--mznoutfile"): 
            mzn_out_file = arg        

    start_time = time.time()
    instance = data.Data(instance_file)
    logger.logger(instance,'log')
    print("Finished reading and parsing data from {} in {} seconds".format(instance_file, round(time.time()-start_time,2)))
  
    start_time = time.time()
    wri = dznwriter.DznWriter(instance)
    wri.write_dzn(dzn_out_file)
    print("Finished writing data to {} in {} seconds".format(dzn_out_file, round(time.time()-start_time,2)))

if __name__ == "__main__":
    main(sys.argv[1:])

