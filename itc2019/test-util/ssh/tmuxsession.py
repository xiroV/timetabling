#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
from functools import wraps
from abc import abstractmethod
import subprocess
import datetime
import logging
import argparse
import sys
import time
import os
import math

# Set up a logger, such that we can record different program events
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
        # Get the current time and date
        dt = datetime.datetime.now()
        # Set up a "FileHandler" for writing the recorded events to a .log file
        fh = logging.FileHandler(LOG_FILE, "+a")
        # fh = logging.FileHandler("{:02.0f}:{:02.0f}:{:02.0f}_{:02.0f}_{:02.0f}".\
        #     format(dt.hour, dt.minute, dt.second, dt.day, dt.month) + "_" + LOG_FILE)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        ROOT_LOGGER.addHandler(fh)
        # Set up a "StreamHandler" for writing the recorded events to the terminal
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        ROOT_LOGGER.addHandler(ch)


def timing(f):
    """ A decorator function that can be used to time a function call.
    Note:
        The function f is called in an ordinary manner and the result is returned.
        The time of the function call is simply written to a log.
    Args:
        f (function): The function to be timed.
    Returns:
        wrapper (function): The result of the function f.
    """
    global ROOT_LOGGER
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        ROOT_LOGGER.info("INFO: Call to {}. Elapsed time: {}".format(f, end - start))
        return result
    return wrapper


@timing
def subprocess_start(commandline_args, wait=True):
    """ Default behavior: Start a process and wait for it to finish.
    Optional behavior: Start a process and continue.
    Args:
        commandline_args (list(str)): A list of commands, that should be executed
            on the commandline.
    Returns:
        tuple(str, str): stdout and stderr output resulting from executing the
            list of commands in "commanline_args".
    """
    s = subprocess.Popen(commandline_args, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    if wait:
        return s.communicate()
    else:
        return s


def str2bool(string):
    """ Convert a given string to a boolean value. This function is used to
    interpret the commandline argument for the subparser optione "--read_config".
    Args:
        string (str): A given string to be interpreted as a boolean value.
    Returns:
        (bool): Return True or Flase depending on how "string" is interpreted.
    """
    global ROOT_LOGGER
    if string.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif string.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        ROOT_LOGGER.info("INFO: A string was expected, but got " + \
            str(type(string)))
        raise SystemExit


def is_number(string):
    """ Check whether or not a given input argument "s" is a string or a
        number
    Args:
        string (str): A string.
    Returns:
        (bool): True if the string can be cast to a float (it is actually a number).
            False if the string can not be cast to a float (it is actually not a
            number).
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


@timing
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
    args_dict = parse_args(parser, args)
    # Check and validate the commandline args
    args_dict = validate_args(args_dict)
    return args_dict


def add_subparser_args(subparser):
    """ This function adds a number of different subparsers.
    Args:
        subparser (argparse.ArgumentParser): Add additional
            commandline options.
    Returns:
        None
    """
    # Add general tmux commandline options
    subparser_args_tmux(subparser)
    # Add send-keys commandline options
    subparser_args_send(subparser)
    # Try to import the python library "paramiko". This library is used for
    # establishing ssh-connections with remote machines.
    try:
        import paramiko
    except ImportError:
        # Provide an error message if the library is not installed
        ROOT_LOGGER.info("ERROR: The python package \"paramiko\" is not installed.")
        raise ImportError
    # If the "paramiko" python library was imported, then add the ssh connection
    # commandline options
    subparser_args_ssh(subparser)


def subparser_args_tmux(subparser):
    """ Add commandline options related to: The setup of a tmux session i.e.,
        the number of windows to spawn, the number of panes to spawn in each window,
        the pane layout and so on.
    Args:
        subparser (argparse.ArgumentParser):
    Returns:
        None
    """
    subparser_args = subparser.add_parser(name="tmux")
    subparser_args.add_argument("-multiplexer", "--multiplexer",
        required=False,
        default="byobu-tmux",
        type=str,
        help = "Specify the terminal multiplexer (either byobu-tmux or tmux).")
    subparser_args.add_argument("-attach", "--attach",
        required=False,
        default=True,
        type=str2bool,
        help = "Indicate whether or not we should attach to the tmux session.")
    subparser_args.add_argument("-session_name", "--session_name",
        required=False,
        default="session0",
        type=str,
        help = "Specify the session name.")
    subparser_args.add_argument("-windows", "--windows",
        required=False,
        default=1,
        type=int,
        help = "Specify the number of windows to create.")
    subparser_args.add_argument("-panes", "--panes",
        required=False,
        default=1,
        type=int,
        help = "Specify the number of panes to create inside each window.")
    subparser_args.add_argument("-layout", "--layout",
        required=False,
        default="tiled",
        type=str,
        help="Specify how the panes in the different windows should be " + \
            "layed out. Choose between: \"tiled\", \"even-horizontal\", " + \
            "\"even-vertical\", \"main-horizontal\", \"main-vertical\".")


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
        type=str,
        default=None,
        nargs="+",
        help="Specify a command to execute in the target panes.")
    # subparser_args.add_argument("-to_window", "--to_window",
    #     required=False,
    #     default=None,
    #     type=str,
    #     help="Specify the the target window.")
    # subparser_args.add_argument("-to_pane", "--to_pane",
    #     required=False,
    #     default=None,
    #     type=str,
    #     help = "Specify the target panes in the specified target window.")


def subparser_args_ssh(subparser):
    """ Add commandline options related to: Establishing an ssh connection to
    several remote machines.
    Args:
        subparser (argparse.ArgumentParser):
    Returns:
        None
    """
    subparser_args = subparser.add_parser(name="ssh")
    subparser_args.add_argument("-username", "--username",
        required=True,
        type=str,
        nargs="+",
        help="Specify a username.")
    subparser_args.add_argument("-via_username", "--via_username",
        required=False,
        type=str,
        help="Specify a via username.")
    subparser_args.add_argument("-hostname", "--hostname",
        required=True,
        default=None,
        type=str,
        nargs="+",
        help="Specify a via hostname.")
    subparser_args.add_argument("-via_hostname", "--via_hostname",
        required=False,
        default=None,
        type=str,
        help="Specify a via hostname.")
    subparser_args.add_argument("-password", "--password",
        required=True,
        default=None,
        type=str,
        nargs="+",
        help="Specify a password.")
    subparser_args.add_argument("-via_password", "--via_password",
        required=False,
        default=None,
        type=str,
        help="Specify a via password.")


def parse_args(parser, args_list=None):
    """
    """
    if args_list is None:
        args_list = sys.argv[1:]
    tmp_lst = []
    # Add the default commandline arguments to the list, if these were not given
    if not ("tmux" in args_list):
        args_list = ["tmux"] + args_list
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


def validate_args(args_dict):
    """ This method checks the given commandline arguments, to make sure that these have the
    right type and format.
    Args:
        args_dict (dict()):

    Returns:
        args_dict (dict()):
    """
    global ROOT_LOGGER
    # If only a single option has been chosen, then convert it to a list before proceeding
    if not (type(args_dict["options"]) is list):
        args_dict["options"] = [args_dict["options"]]
    # Validate "send" commandline options
    # if "send" in args_dict["options"]:
    #     if not (args_dict["to_pane"] is None):
    #         # Split the space-seperated string of pane-indices into a list
    #         args_dict["to_pane"] = args_dict["to_pane"].split(" ")
    #     if not (args_dict["to_window"] is None):
    #         if not is_number(args_dict["to_window"]):
    #             ROOT_LOGGER.info("INFO: A single integer value was expected, but got " + \
    #                 str(type(args_dict["to_window"])))
    #             raise SystemExit
    # Validate "ssh" commandline options
    if "ssh" in args_dict["options"]:
        if not (len(args_dict["username"]) == len(args_dict["hostname"]) and \
        len(args_dict["username"]) == len(args_dict["password"])):
            ROOT_LOGGER.info("INFO: Three lists of equal size were expected, but got " + \
                "lists of length " + str(len(args_dict["username"])) + " (username), " + \
                str(len(args_dict["hostname"])) + " (hostname), " + \
                str(len(args_dict["password"])) + " (password).")
            raise SystemExit
        # Set the number of panes that should be used based on the number of given hostnames
        args_dict["panes"] = len(args_dict["hostname"])
    if args_dict["panes"] > 4:
        args_dict["windows"] = int(math.ceil(args_dict["panes"] / 4.0))
        args_dict["panes"] = 4
    return args_dict


#------------------------------------------------------------------------------#
class TmuxPane:
    """
    Class TmuxPane.
    """

    def __init__(self, window, pane, commands=[]):
        """ Instantiate and set input variables and parameters.
        Args:
            window (str): Window name/index.
            pane (str): Pane name/index.
            commands (list(str)): A list of commands to be executed.
        Returns:
            None
        """
        self.window = window
        self.pane = pane
        self.commands = commands
        self.timestamp = time.time()

    def set_commands(self, commands):
        """
        """
        self.commands = commands


#------------------------------------------------------------------------------#
class TmuxSession:
    """
    Class TmuxSession.
    """

    def __init__(self, args=None):
        """ Instantiate and set input variables and parameters.

        Args:
            args (list): A list of commandline arguments to be parsed.
            commands (list): A list of commands to execute. Each string of commands
                in the list is executed in its own seperate pane.
        Returns:
            None
        """
        # Read in the commandline arguments, if they were not given directly
        self.args = read_commandline_args(args)
        # Instantiate a variable, that is going to hold the total
        # number of panes that will be spawned
        self._panes_total = None
        # Create a new session by default, but set to Flase. All the given commands
        # should be executed in one particular session.
        self._new_session = True
        self._multiplexer_config = None
        # Variable that will be used to define some ssh connection specific options
        self.ssh_options = None
        # Finally, setup the tmux session
        self.setup_tmux_session()

    @timing
    def setup_multiplexer_config(self):
        """
        Args:
            None
        Returns:
            window_dict (dict(dict(TmuxPane))): Contains the tmux window and
                pane configuration i.e., the number of windows to spawn along
                with the number of panes to spawn in each of the windows.
        """
        global ROOT_LOGGER
        # Create a list that contains the file extensions of the files in the
        # current working directory
        files = [s.split(".")[-1] for s in os.listdir()]
        # If we should not read in an existing configuration file, but create
        # a new one, then continue here...
        if not ("tmpconf" in files):
                self.create_tmpconf()
        elif "tmpconf" in files:
            self.read_tmpconf()
        else:
            ROOT_LOGGER.info("INFO: A tmux configuration file could not be read in" + \
                ", as no tmux configuration file could be found.")
            raise SystemExit
        # Set the total number of panes
        self._panes_total = self.args["windows"] *  self.args["panes"]
        # Ceate a dictionary of windows and pane objects, such that we can keep
        # track of what commands should be executed in what panes
        window_dict = {}
        for i in range(self.args["windows"]):
            pane_dict = {}
            for j in range(self.args["panes"]):
                pane_dict[str(j)] = TmuxPane(i, j)
            window_dict[str(i)] = pane_dict
        return window_dict

    def create_tmpconf(self):
        """ Create a temporary tmux configuration file.
        Args:
            None
        Returns:
            None
        """
        with open(self.args["session_name"] + ".tmpconf", "w") as file:
            file.write("windows " + str(self.args["windows"]) + "\n")
            file.write("panes " + str(self.args["panes"]) + "\n")

    def read_tmpconf(self):
        """ Read the temporary tmux configuration file.
        Args:
            None
        Returns:
            None
        """
        global ROOT_LOGGER
        filename = self.args["session_name"] + ".tmpconf"
        try:
            ROOT_LOGGER.info("INFO: Reading temporary tmux configuration file...")
            with open(filename, "r") as file:
                for line in file.readlines():
                    name, val = line.split(" ")
                    if name == "windows":
                        self.args["windows"] = int(val)
                    if name == "panes":
                        self.args["panes"] = int(val)
        except IOError:
            ROOT_LOGGER.info("ERROR: Could not find or read temporary tmux \
                configuration file...")
            raise IOError

    def set_ssh_options(self):
        """
        """
        if not ((self.args["via_hostname"] is None and self.args["via_password"] is None) and \
        self.args["via_username"] is None):
            self.ssh_options = "--via_username " + self.args["via_username"] + " " + \
                "--via_password " + self.args["via_password"] + " " + \
                "--via_hostname " + self.args["via_hostname"] + " "
        else:
            self.ssh_options = ""

    @timing
    def open_ssh_connection(self):
        """
        Args:
            commands (list(str)):
        Returns:
            None
        """
        self.set_ssh_options()
        # Based on the given hostnames, usernames and passwords start a ssh session in each of
        # the panes:
        counter = 0
        for window in self._multiplexer_config:
            for pane in self._multiplexer_config[window]:
                l = ["python ssh.py ssh" + " " + \
                    "--username " + self.args["username"][counter] + " " + \
                    "--password " + self.args["password"][counter] + " " + \
                    "--hostname " + self.args["hostname"][counter] + " " + \
                    self.ssh_options + \
                    "--command " + "\"" + self.args["command"][counter] + "\""]
                self._multiplexer_config[window][pane].set_commands(l)
                counter += 1
                if counter == len(self.args["command"]):
                    break
        # Open ssh connections by executing the set commands
        self.execute_commands()

    # @timing
    # def set_commands(self):
    #     """ This method sets the commands that should be executed in each of the
    #     different panes. Depending on the given commandline arguments, the commands
    #     are set differently.
    #     Args:
    #         commands (list(str)):
    #     Returns:
    #         None
    #     """
    #     # If the commands are given as a commandline argument, then continue here:
    #     if not (self.args["command"] is None):
    #         # Split the given string of commands into a list, such that we can execute each
    #         # of them seperately
    #         l = self.args["command"].split(";;")
    #         # If no window was specified, then the given commands should be executed in all
    #         # windows and panes:
    #         if self.args["to_window"] is None:
    #             for window in self._multiplexer_config:
    #                 for pane in self._multiplexer_config[window]:
    #                     self._multiplexer_config[window][pane].set_commands(l)
    #         # If a window but no pane was specified, then the given commands should be executed
    #         # in all panes in the specified target window:
    #         elif not (self.args["to_window"] is None) and self.args["to_pane"] is None:
    #             window = self.args["to_window"]
    #             for pane in self._multiplexer_config[window]:
    #                 self._multiplexer_config[window][pane].set_commands(l)
    #         # If both a window and panes were specified, then the given commands should be executed
    #         # in all of the specified target panes residing in specified target window:
    #         elif not (self.args["to_window"] is None and self.args["to_pane"] is None):
    #             for window in self.args["to_window"]:
    #                 for pane in self.args["to_pane"]:
    #                     self._multiplexer_config[window][pane].set_commands(l)

    @timing
    @abstractmethod
    def setup_tmux_session(self):
        """ Setup a tmux session.
        Note: This method is declared abstract and can be re-implemented
            in a derived class, if needed.
        Args:
            None
        Returns:
            None
        """
        files = [s.split(".")[-1] for s in os.listdir()]
        if not ("tmpconf" in files):
            self.start_multiplexer()
        self._multiplexer_config = self.setup_multiplexer_config()
        if "ssh" in self.args["options"]:
            self.open_ssh_connection()
        # if "send" in self.args["options"]:
        #     # Set the given commands, that is to be executed in the different panes and windows
        #     self.set_commands()
        #     # Execute the commands
        #     self.execute_commands()
        if self.args["attach"]:
            self.attach_session()
            if os.path.exists(self.args["session_name"] + ".tmpconf"):
                os.remove(self.args["session_name"] + ".tmpconf")

    def tmux(self, *args):
        """ A wrapper function. This method simply starts a new process with
        additional arguments.
        Args:
            *args: One or more byobu-tmux/tmux commandline arguments.
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        return subprocess_start([self.args["multiplexer"]] + list(args))

    def new_session(self):
        """ Create a new tmux session.
        Args:
            None
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        return self.tmux("new-session", "-d", "-s", self.args["session_name"])

    def select_layout(self):
        """ This method sets the a pane layout i.e., how the panes are organized in
        the different windows.
        Args:
            None
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        return self.tmux("select-layout", "-t", self.args["session_name"],
            self.args["layout"])

    def attach_session(self):
        """ Attach to the tmux session.
        Args:
            None
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        return self.tmux("attach-session", "-t", self.args["session_name"])

    def add_panes(self):
        """ Add panes and windows to the tmux session and organize the panes according
        to  a user-specified pane layout.
        Args:
            None
        Returns:
            None
        """
        global ROOT_LOGGER
        for i in range(self.args["windows"]):
            window_name = str(i)
            if i > 0:
                self.new_window(window_name)
            for j in range(self.args["panes"] - 1):
                ROOT_LOGGER.info("INFO: Adding pane: " + str(j) + " to window " + str(i))
                self.split_window(window_name)
                self.select_layout()

    def start_multiplexer(self):
        """ Start the terminal multiplexer and add a user-specified number of windows
        and panes. Terminate with an error message if tmux or byobu-tmux is not
        installed.
        Args:
            None
        Returns:
            None
        """
        global ROOT_LOGGER
        try:
            self.new_session()
            self.add_panes()
        except EnvironmentError:
            ROOT_LOGGER.info("ERROR: The package \"byobu-tmux\" is not installed.")
            raise EnvironmentError

    def execute_commands(self):
        """ Go through all of the windows and panes. Execute commands in the panes that
        have a list of commands specified.
        Args:
            None
        Returns:
            None
        """
        # Go through the different panes and execute the commands that were specified
        # for each pane
        for window in self._multiplexer_config:
            for pane in self._multiplexer_config[window]:
                pane_object = self._multiplexer_config[window][pane]
                if len(pane_object.commands) > 0:
                    for command in pane_object.commands:
                        self.select_window(window)
                        self.send_keys(pane, command)

    def capture_pane(self, pane_name):
        """ This method caputures the standard output of a pane given the pane
        name/index. The selected pane resides in the window that is currently
        in focus.
        Args:
            pane_name (str): The name/index of the pane.
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        global ROOT_LOGGER
        ROOT_LOGGER.info("COMMAND: byobu-tmux capture-pane -pt " + pane_name + \
            " -S 0")
        return self.tmux("capture-pane", "-pt", pane_name, "-S 0")

    def new_window(self, window_name):
        """ This method spawns an additional window.
        Args:
            window_name (str): The name/index of the window.
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        global ROOT_LOGGER
        ROOT_LOGGER.info("COMMAND: byobu-tmux new-window -t " + \
            self.args["session_name"])
        return self.tmux("new-window", "-t", self.args["session_name"])

    def split_window(self, window_name):
        """ This method splits the window, that is currently in focus, into panes.
        Args:
            window_name (str): The name/index of the window.
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        global ROOT_LOGGER
        ROOT_LOGGER.info("COMMAND: byobu-tmux split-window -t " + \
            self.args["session_name"] + ":" + window_name)
        return self.tmux("split-window", "-t", self.args["session_name"] + \
            ":" + window_name)

    def select_window(self, window_name):
        """ This method selects a window given the window name/index.
        Args:
            window_name (str): The name/index of the window.
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        global ROOT_LOGGER
        ROOT_LOGGER.info("COMMAND: byobu-tmux select-window -t " + window_name)
        return self.tmux("select-window", "-t", window_name)

    def select_pane(self, pane_name):
        """ This method selects a pane given the pane name/index.
        Args:
            pane_name (str): The name/index of the pane.
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        global ROOT_LOGGER
        ROOT_LOGGER.info("COMMAND: byobu-tmux select-pane -t " + pane_name)
        return self.tmux("select-pane", "-t", pane_name)

    def send_keys(self, pane_name, command):
        """ This method sends commands to a pane given the name/index of the pane.
        The selected pane resides in the window that is currently in focus.
        Args:
            pane_name (str): The name/index of the pane.
            command  (str): The command to execute in the pane.
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        global ROOT_LOGGER
        ROOT_LOGGER.info("COMMAND: byobu-tmux send-keys -t " + pane_name + \
            " \"" + command + "\"" + " C-m")
        return self.tmux("send-keys", "-t", pane_name, command, "C-m")

    def display_panes(self, window_name):
        """ This method displays the pane indices in the window that is currently
        in focus.
        Args:
            window_name (str): The name/index of the window.
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command below.
        """
        global ROOT_LOGGER
        ROOT_LOGGER.info("COMMAND: byobu-tmux display-panes")
        return self.tmux("display-panes")

    def kill_session(self):
        """ This method kills the tmux session.
        Args:
            None
        Returns:
            tuple(str, str): stdout and stderr output resulting from running the
                tmux command.
        """
        global ROOT_LOGGER
        ROOT_LOGGER.info("COMMAND: byobu-tmux kill-session -t " + \
            self.args["session_name"])
        return self.tmux("kill-session", "-t", self.args["session_name"])


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """
    Script entry point.
    """
    session = TmuxSession()
