#------------------------------------------------------------------------------#
#                          Import thid-party libraries                         #
#------------------------------------------------------------------------------#
import paramiko
#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
import subprocess
import logging
import argparse
import sys
#------------------------------------------------------------------------------#
#                               Import local scripts                           #
#------------------------------------------------------------------------------#
import interactive


# Set up a logger, that is going to record different program events
ROOT_LOGGER = logging.getLogger("ROOT_LOGGER")
LOG_FILE = "tmuxsession.log"


#------------------------------------------------------------------------------#
def configure_logger():
    """ Log different program events and the byobu-tmux commands that are
    being executed.
    Args:
        None
    Returns:
        None
    """
    global ROOT_LOGGER, LOG_FILE
    if not len(ROOT_LOGGER.handlers):
        # Set the level for which we record events (debug level logs every event)
        ROOT_LOGGER.setLevel(logging.DEBUG)
        # Define the output format: (timestamp, logger name, output message)
        formatter = logging.Formatter("%(asctime)-2s %(message)-2s")
        # Set up a "FileHandler" for writing the recorded events to a .log file
        fh = logging.FileHandler(LOG_FILE, "+a")  
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        ROOT_LOGGER.addHandler(fh)
        # Set up a "StreamHandler" for writing the recorded events to the terminal
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        ROOT_LOGGER.addHandler(ch)


def read_commandline_args(args=None):
    """ Setup a parser and parse given commandline options.
    Args:
        args (list(str)):
    Returns:
        args_namespaces: (dict(Namespace)):
    """
    # Setup a logger
    configure_logger()
    # Create main parser
    parser = argparse.ArgumentParser(description="")
    # Add subparser
    subparser = parser.add_subparsers(dest="options")
    add_subparser_args(subparser)
    # Parse commandline arguments
    args_namespaces = parse_args(parser, args)
    return args_namespaces


def add_subparser_args(subparser):
    """ This function adds a number of different subparsers. 
    Args:
        subparser (argparse.ArgumentParser): Add additional 
            commandline options.
    Returns:
        None
    """
    # Add send-keys commandline options
    subparser_args_send(subparser)
    # Add the ssh connection commandline options 
    subparser_args_ssh(subparser)


def subparser_args_send(subparser):
    """ Add commandline options related to: Sending commands to certain windows
    and panes.
    Args:
        subparser (argparse.ArgumentParser):
    Returns:
        None
    """
    subparser_args = subparser.add_parser(name="send")
    subparser_args.add_argument("-command", "--command",
        required=False,
        default=None,
        type=str,
        help = "Specify a command to execute in the target panes.")


def subparser_args_ssh(subparser):
    """ Add commandline options related to: Establishing an ssh connection to
    several a remote machine.
    Args:
        subparser (argparse.ArgumentParser):
    Returns:
        None
    """
    subparser_args = subparser.add_parser(name="ssh")
    subparser_args.add_argument("-username", "--username",
        required=True,
        default=None,
        type=str,
        help = "Specify a username.")
    subparser_args.add_argument("-via_username", "--via_username",
        required=False,
        default=None,
        type=str,
        help = "Specify a via username.")
    subparser_args.add_argument("-hostname", "--hostname",
        required=True,
        default=None,
        type=str,
        help = "Specify a via hostname.")
    subparser_args.add_argument("-via_hostname", "--via_hostname",
        required=False,
        default=None,
        type=str,
        help = "Specify a via hostname.")
    subparser_args.add_argument("-password", "--password",
        required=True,
        default=None,
        type=str,
        help = "Specify a password.")
    subparser_args.add_argument("-via_password", "--via_password",
        required=False,
        default=None,
        type=str,
        help = "Specify a via password.")


def parse_args(parser, args_list=None):
    """
    """
    if args_list is None:
        args_list = sys.argv[1:]
    tmp_lst = []
    # Add the default commandline arguments to the list, if these were not given
    if not ("ssh" in args_list):
        args_list = ["ssh"] + args_list
    if not ("send" in args_list):
        args_list = ["send"] + args_list
    # Parse the list of given commandline arguments 
    while args_list:
        options, args_list = parser.parse_known_args(args_list)
        tmp_lst.append(vars(options))
        if not options.options:
            break
    # Convert the given commandline arguments to a dictionary for easy access
    args_dict = {}
    for i in range(len(tmp_lst)):
        args_dict = merge_dicts(args_dict, tmp_lst[i])
    return args_dict


def flatten(lst):
    """
    """
    new_lst = []
    for y in lst:
        if type(y) is str:
            new_lst.append(y)
        elif type(y) is list:
            for x in y:
                new_lst.append(x)
    return new_lst


def merge_dicts(x, y):
    """
    """
    for key in x:
        if key in y:
            y[key] = flatten([x[key], y[key]])
    z = x.copy(); z.update(y)
    return z


#------------------------------------------------------------------------------#
class SSHConnection:
    """
    """

    def __init__(self, args=None):
        """
        """
        self.transport = None        
        # Read in the commandline arguments
        self.args = read_commandline_args(args)
        # Try to establish a connection
        try:
            self.setup_shh_connection()
        except paramiko.SSHException:
            ROOT_LOGGER.info("ERROR: A connection to the remote machine could" + \
            " not be established")
            raise paramiko.SSHException
    
    def open_interactive_shell(self):
        """
        """
        channel = self.transport.open_session()
        channel.get_pty()
        channel.invoke_shell()
        if not (self.args["command"] is None):
            self.execute_commands(channel)
        interactive.interactive_shell(channel)

    def execute_commands(self, channel):
        """
        """
        if "send" in self.args["options"]:
            if not (self.args["command"] is None):
                # Execute each of the given commands seperately     
                for command in self.args["command"].split(";"):
                    channel.send(command + "\n")

    def setup_shh_connection(self):     
        """
        """
        if not (self.args["via_hostname"] is None):
            t0 = paramiko.Transport((self.args["via_hostname"], 22))
            t0.start_client()
            t0.auth_password(self.args["via_username"], 
                self.args["via_password"])
            channel = t0.open_channel("direct-tcpip", 
                (self.args["hostname"], 22), ("127.0.0.1", 0))
            self.transport = paramiko.Transport(channel)
        else:
            self.transport = paramiko.Transport((self.args["hostname"], 22))
        self.transport.start_client()
        self.transport.auth_password(self.args["username"],
            self.args["password"])
        # Open an interactive shell
        self.open_interactive_shell()


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """
    Script entry point.
    """
    ssh = SSHConnection()