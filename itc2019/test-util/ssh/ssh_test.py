#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
import datetime
import logging
import datetime
import subprocess
import sys

def subprocess_start(commandline_args, wait=True):
    """
    """
    s = subprocess.Popen(commandline_args, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    if wait:
        return s.communicate()
    else:
        return s

def run(commandline_args, remote_virtenv_path, remote_est_path, remote_sumo_path):
    """
    """
    remote_machines = ["13", "14", "15", "16", "17", "18", "19", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
    if len(commandline_args) > len(remote_machines):
        print("ERROR: More commands specified, than remote machines!")
        print("--> Terminating...")
        raise SystemExit
    remote_machines = remote_machines[:len(commandline_args)]
    hostname = ["imada-1063" + m + ".imada.sdu.dk" for m in remote_machines]
    username = ["sdu\\brped13"] * len(remote_machines)
    password = ["a75xG4us8P78VuobGopC9qrat"] * len(remote_machines)
    via_username = ["brped13"]
    via_password = ["a75xG4us8P78VuobGopC9qrat"]
    via_hostname = ["logon.sdu.dk"]
    commands = []
    for command in commandline_args:
        commands.append("tmux attach-session;")# + \
         #"tmux kill-session -t session0;" + \
         #    "tmux new-session -d -s session0;" + \
         #    "tmux send-keys -t 0 '" + remote_virtenv_path + "' C-m;" + \
         #    "tmux send-keys -t 0 '" + command + "' C-m;" + \
         #"tmux send-keys -t 0 'cd " + remote_est_path + "' C-m;" + \

        # commands.append("tmux kill-session -t session0;" + \
        #     "tmux new-session -d -s session0;" + \
        #     "tmux send-keys -t 0 '" + remote_virtenv_path + "' C-m;")# + \
        #     # "tmux send-keys -t 0 'cd " + remote_est_path + "' C-m;" + \
        #     # "tmux send-keys -t 0 " + "\'" + string + "\' C-m;")
    print(commands)
    if ((len(hostname) == len(username) and len(hostname) == len(password)) and \
        (len(hostname) == len(commands))):
        # Re-define variable with complete commandline arguments
            commandline_args = ["python", "tmuxsession.py", "tmux", "--attach", "True"] + \
                ["ssh", "--via_password"] + via_password + \
                ["--password"] + password + \
                ["--via_hostname"] + via_hostname + \
                ["--hostname"] + hostname + \
                ["--via_username"] + via_hostname + \
                ["--username"] + username + \
                ["--via_username"] + via_username + \
                ["send", "--command"] + commands
                # ["send", "--command"] + ["ls;\n;cd ~/files;ls", "ls;\n;cd ~/files;ls", "ls;\n;cd ~/files;ls"]
            subprocess_start(commandline_args)


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """
    """
    remote_virtenv_path = "source .local/bin/sumoenv/bin/activate"
    remote_est_path = ""
    remote_sumo_path = ""
    commandline_args = ["ls"] * 8
    run(commandline_args, remote_virtenv_path, remote_est_path, remote_sumo_path)
