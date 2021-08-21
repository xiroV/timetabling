#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
from functools import wraps
import subprocess
import logging
import time
import os
#------------------------------------------------------------------------------#
#                          Import local libraries                              #
#------------------------------------------------------------------------------#
from ssh import *


def subprocess_start(commandline_args):
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
        stderr=subprocess.STDOUT, shell=True)
    return s


#------------------------------------------------------------------------------#
class RunCommands:
    """
    Class RunCommands.
    """

    def __init__(self,commands, username, password, hostname, via_username=None,
        via_password=None, via_hostname=None, max_panes=8):
        """
        """
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        self.commands = commands
        self.username = username
        self.password = password
        self.hostname = hostname
        self.via_username = via_username
        self.via_password = via_password
        self.via_hostname = via_hostname
        self.ssh_options
        self.panes = max_panes
        self.windows = int(len(commands)/float(self.panes))
        self.set_ssh_options()

    def set_ssh_options(self):
        """
        """
        if not ((self.via_hostname is None and self.via_password is None) and \
        self.via_username is None):
            self.ssh_options = "--via_username " + self.via_username + " " + \
                "--via_password " + self.via_password + " " + \
                "--via_hostname " + self.via_hostname + " "
        else:
            self.ssh_options = ""

    def run(self):
        """
        """
        if len(self.hostname) < len(self.commands):
            ROOT_LOGGER.info("ERROR: More commands have been specified" + \
            ", than remote machines.")
        else:
            self.send_commands()

    def send_commands(self):
        """
        """
        commands = []
        processes = []
        counter = 0
        if not (self.via_hostname is None):
            for hostname in self.hostname:
                run_script = "python ssh.py ssh" + " " + \
                    "--username " + self.username + " " + \
                    "--password " + self.password + " " + \
                    "--hostname " + hostname + " " + \
                    self.set_ssh_options + \
                    "send --command \"" + self.commands[counter] + "\""
            for command in commands:
                processes.append(subprocess_start(run_script))
                counter += 1
                if counter >= len(self.commands):
                    break
            for subprocess in processes:
                subprocess.communicate()

    # def send_commands(self):
    #     """
    #     """
    #     commands = []
    #     processes = []
    #     counter = 0
    #     if not (self.via_hostname is None):
    #         for hostname in self.hostname:
    #             run_script = "python ssh.py ssh" + " " + \
    #                 "--username " + self.username + " " + \
    #                 "--password " + self.password + " " + \
    #                 "--hostname " + hostname + " " + \
    #                 self.set_ssh_options + \
    #                 "send --command \"" + self.commands[counter] + "\""
    #         for command in commands:
    #             processes.append(subprocess_start(run_script))
    #             counter += 1
    #             if counter >= len(self.commands):
    #                 break
    #         for subprocess in processes:
    #             subprocess.communicate()
