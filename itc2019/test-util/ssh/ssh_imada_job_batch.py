#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
import datetime
import logging
import datetime
import subprocess
import sys
#------------------------------------------------------------------------------#
#                             Import local libraries                           #
#------------------------------------------------------------------------------#
from runcommands import RunCommands


def subprocess_start(commandline_args, wait=True):
    """
    """
    s = subprocess.Popen(commandline_args, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    if wait:
        return s.communicate()
    else:
        return s

def run(commandline_args, remote_virtenv_path, remote_est_path):
    """
    """
    remote_machines = ["13", "15", "16", "17", "18", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
    # remote_machines = ["13", "14", "15", "16", "17", "18", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
    # remote_machines = ["13", "14", "15", "16", "17", "18", "19", "23", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
    # remote_machines = ["10", "11", "13", "14", "15", "16", "17", "18", "19", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
    print("Remote machines: ", len(remote_machines))
    if len(commandline_args) > len(remote_machines):
        print("ERROR: More commands specified, than remote machines!")
        print("--> Terminating...")
        raise SystemExit
    remote_machines = remote_machines[:len(commandline_args)]
    hostname = ["imada-1063" + m + ".imada.sdu.dk" for m in remote_machines]
    username = [""] * len(remote_machines)
    password = [""] * len(remote_machines)
    via_username = [""]
    via_password = [""]
    via_hostname = ["logon.sdu.dk"]
    commands = []
    for command in commandline_args:
        commands.append("tmux kill-session -t session0;" + \
            "tmux new-session -d -s session0;" + \
            "tmux send-keys -t 0 '" + remote_virtenv_path + "' C-m;" + \
            "tmux send-keys -t 0 'cd " + remote_est_path + "' C-m;" + \
            "tmux send-keys -t 0 '" + command + "' C-m;" + \
            "tmux attach-session;")
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
        subprocess_start(commandline_args)
    else:
        print("--> Terminating...")
        raise SystemExit


def attach_to_session():
    """
    """
    remote_machines = ["13", "15", "16", "17", "18", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
    # remote_machines = ["13", "14", "15", "16", "17", "18", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
    # remote_machines = ["13", "14", "15", "16", "17", "18", "19", "23", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
    # remote_machines = ["10", "11", "13", "14", "15", "16", "17", "18", "19", "21", "22", "23", "24", "26", "27", "28", "29", "30", "31"]
    # remote_machines = ["10", "11", "13", "14", "15", "16", "17", "18", "19", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
    print("Remote machines: ", len(remote_machines))
    hostname = ["imada-1063" + m + ".imada.sdu.dk" for m in remote_machines]
    username = ["brped13"] * len(remote_machines)
    password = [""] * len(remote_machines)
    via_username = ["brped13"]
    via_password = [""]
    via_hostname = ["logon.sdu.dk"]
    commands = []
    for remote_machine in remote_machines:
        commands.append("tmux attach -d;")
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
        subprocess_start(commandline_args)
    else:
        print("--> Terminating...")
        raise SystemExit


#------------------------------------------------------------------------------#
class RunExperiments:

    def __init__(self, simulators, traffic_flow_models,  simulator_executables,
        interval_start, interval_end, aggregation_intervals, constant_demand,
        total_demand, test_data_prefix, networks, dua_iterations,
        random_seed, sensor_coverages, max_idle_iterations, max_of_evals,
        weight_configs, gencons, seedmats):
        """
        """
        # Default variables and parameters
        self.simulators = simulators
        self.traffic_flow_models = traffic_flow_models
        self.interval_start = interval_start
        self.interval_end = interval_end
        self.aggregation_intervals = aggregation_intervals # List
        self.constant_demand = constant_demand
        self.total_demand = total_demand
        self.test_data_prefix = test_data_prefix
        self.networks = networks
        self.dua_iterations = dua_iterations
        self.random_seed = random_seed
        self.simulator_executables = simulator_executables
        self.sensor_coverages = sensor_coverages # List
        self.network_file = "../data/networks/"
        self.taz_file = "../data/networks/"
        self.gencon = False
        self.output_path = "../data/output"
        self.log_path = "../data/log"
        # "constraints"
        self.gencons = gencons
        self.seedmats = seedmats
        # Algorithm parameters
        self.max_idle_iterations = max_idle_iterations
        self.max_of_evals = max_of_evals
        self.weight_configs = weight_configs
        # SPSA algorithm specific parameters
        self.step_length = None
        self.gradient_approximations = None
        # SM algorithm specific parameters
        self.data_dir = None
        self.model_types = None # List
        self.samples = None
        self.sample_index = None

    def create_experiment_run_id(self, name, simulator, traffic_flow_model, intervals, network, weight_config, sensor_coverage, gencon, seedmat):
        """ Create experiment run id/name.
        Args:
            intervals (int):  The number of time intervals (m vary across experiments).
        Returns:
            experiment_run_id (str): The id of experiment files.
        """

        experiment_run_id = name + "_" + \
            simulator + "-" + traffic_flow_model + "_" + \
            self.interval_start + "-" + self.interval_end + "-" +  intervals + "_" + \
            simulator + "-" + network + "_" + sensor_coverage + "_"
        if not (self.total_demand is None) and self.constant_demand is None:
            experiment_run_id += "t" + self.total_demand + "_"
        elif not (self.constant_demand is None) and self.total_demand is None:
            experiment_run_id += "c" + self.constant_demand + "_"
        experiment_run_id += weight_config[0] + "-" + weight_config[1] + "-" + weight_config[2] + "_"
        experiment_run_id += "gencon" + "-" + str(gencon) + "_" + str(seedmat)
        return experiment_run_id

    def get_test_data_run_id(self, simulator, traffic_flow_model, intervals, network, weight_config):
        """ Get the test data run id/name.
        Args:
            intervals (int):  The number of time intervals (m may vary across test
                instances).
        Returns:
            test_data_run_id (str): The id of a test data files.
        """
        test_data_run_id = self.test_data_prefix + "_" + \
            simulator + "-" + traffic_flow_model + "_" + \
            self.interval_start + "-" + self.interval_end + "-" + intervals + "_" + \
            simulator + "-" + network + "_" + "none" + "_"
        if not (self.total_demand is None) and self.constant_demand is None:
            test_data_run_id += "t" + self.total_demand + "_"
        elif not (self.constant_demand is None) and self.total_demand is None:
            test_data_run_id += "c" + self.constant_demand #+ "_"
        # test_data_run_id += weight_config[0] + "-" + weight_config[1] + "-" + weight_config[2]
        return test_data_run_id

    def generate_default_commandline_args(self, name, simulator, simulator_executable, traffic_flow_model,
        intervals, network, experiment_run_id):
        """
        """
        default_args = "default " + \
            "--run_id " + experiment_run_id + " " + \
            "--taz_file " + self.taz_file + simulator + "-" + network + ".taz.xml" + " " + \
            "--net_file " + self.network_file + simulator + "-" + network + ".net.xml" + " " + \
            "--random_seed " + self.random_seed + " " + \
            "--simulation_timespan " + self.interval_start + " " + self.interval_end + " " + \
            "--aggregation_intervals " + intervals + " " + \
            "--output_path " + self.output_path + " " + \
            "--log_path " + self.log_path + " " + \
            "--simulator " + simulator + " " + \
            "--traffic_flow_model " + traffic_flow_model + " " + \
            "--simulator_executable " + simulator_executable + " " + \
            "--dua_iterations " + self.dua_iterations + " "
        return default_args

    def run_spsa(self, step_length, gradient_approximations):
        """
        Run Discrete Simultaneous Pertubation Stochastic Approximation (DSPSA) experiments...
        """
        self.step_length = step_length
        self.gradient_approximations = gradient_approximations
        name = "SPSA2" + "-" + str(self.step_length) + "-" + self.gradient_approximations; spsa_experiments = []
        for s in range(len(self.simulators)):
            for traffic_flow_model in traffic_flow_models[s]:
                for network in self.networks:
                    for intervals in self.aggregation_intervals:
                        for sensor_coverage in self.sensor_coverages:
                            for weight_config in self.weight_configs:
                                for seed_odmat in self.seedmats:
                                    for gencon in self.gencons:
                                        # print(self.simulators[s], " ", traffic_flow_model, " ", network, " ", intervals, " ", sensor_coverage, " ", weight_config)
                                        test_data_run_id = self.get_test_data_run_id(self.simulators[s], traffic_flow_model, intervals, network, weight_config)
                                        # print("TestData ID      : ", test_data_run_id)
                                        experiment_run_id = self.create_experiment_run_id(name, self.simulators[s], traffic_flow_model, intervals, network, weight_config, sensor_coverage, gencon, seed_odmat)
                                        # print("ExperimentData ID: ", experiment_run_id)
                                        spsa_args = "spsa " + \
                                            "--true_odmat " + "../data/log_" + test_data_run_id + "/" + \
                                                test_data_run_id + "_1_odmat_true.csv " + \
                                            "--true_simdata " + "../data/log_" + test_data_run_id + "/" + \
                                                test_data_run_id + "_1_simdata_true.csv " + \
                                            "--det_subset_file " + "../data/networks/" + self.simulators[s] + "-" + \
                                                network + "_" + sensor_coverage + ".det_subset.xml " + \
                                            "--step_length " + self.step_length + " " + \
                                            "--gradient_approximations " + self.gradient_approximations + " "
                                        if not (seed_odmat is None):
                                            spsa_args += "--weights " + "1" + " " + weight_config[1] + " " + weight_config[2] + " "
                                        else:
                                            spsa_args += "--weights " + weight_config[0] + " " + weight_config[1] + " " + weight_config[2] + " "
                                        if not (self.max_of_evals is None) and self.max_idle_iterations is None:
                                            spsa_args += "--max_of_evals " + self.max_of_evals + " "
                                        elif not (self.max_idle_iterations is None) and self.max_of_evals is None:
                                            spsa_args += "--max_idle_iterations " + self.max_idle_iterations + " "
                                        if gencon == True:
                                            spsa_args += "--gencon " + "../data/log_" + test_data_run_id + "/" + \
                                                test_data_run_id + "_1_gencon.csv "
                                        if not (seed_odmat is None):
                                            spsa_args += "--seed_odmat " + "../data/log_" + test_data_run_id + "/" + \
                                                test_data_run_id + "_1_"  + seed_odmat + ".csv "
                                        commandline_args = "python run_main_alg.py " + \
                                            self.generate_default_commandline_args(name, self.simulators[s], self.simulator_executables[s][traffic_flow_model], traffic_flow_model, intervals, network, experiment_run_id) + \
                                            spsa_args
                                        spsa_experiments.append(commandline_args)
        return spsa_experiments

    def create_test_data(self):
        """
        """
        test_data = []
        for s in range(len(self.simulators)):
            for traffic_flow_model in traffic_flow_models[s]:
                for network in self.networks:
                    for intervals in self.aggregation_intervals:
                        for sensor_coverage in self.sensor_coverages:
                            for weight_config in self.weight_configs:
                                test_data_run_id = self.get_test_data_run_id(self.simulators[s], traffic_flow_model, intervals, network, weight_config)
                                test_args = "test "
                                if not (self.total_demand is None) and self.constant_demand is None:
                                    test_args += "--total_demand " + self.total_demand + " "
                                elif not (self.constant_demand is None) and self.total_demand is None:
                                    test_args += "--constant_demand " + self.constant_demand + " "
                                commandline_args = "python run_main_test.py " + \
                                    self.generate_default_commandline_args("", self.simulators[s], self.simulator_executables[s][traffic_flow_model], traffic_flow_model, intervals, network, test_data_run_id) + \
                                    test_args
                                test_data.append(commandline_args)
        return test_data

    # def run_sm(self):
    #     """
    #     Run Surrogae Model (SM) experiments...
    #     """
    #     name = "SM"; sm_experiments = []
    #     for model_type in self.model_types:
    #         for intervals in self.aggregation_intervals:
    #             for coverage in self.sensor_coverages:
    #                 test_data_run_id = self.get_test_data_run_id(intervals)
    #                 experiment_run_id = self.create_experiment_run_id(intervals, coverage)
    #                 sm_args = "sm " + \
    #                     "--true_odmat " + "../data/log_" + \
    #                         self.test_data_prefix + "_" + test_data_run_id + "/" + \
    #                         self.test_data_prefix + "_" + test_data_run_id + "_1_odmat_true.csv " + \
    #                     "--true_simdata " + "../data/log_" + \
    #                         self.test_data_prefix + "_" + test_data_run_id + "/" + \
    #                         self.test_data_prefix + "_" + test_data_run_id + "_1_simdata_true.csv " + \
    #                     "--gencon " + "../data/log_" + \
    #                         self.test_data_prefix + "_" + test_data_run_id + "/" + \
    #                         self.test_data_prefix + "_" + test_data_run_id + "_1_gencon.csv " + \
    #                     "--det_subset_file " + "../data/networks/" + \
    #                         self.network_name + "_" + coverage + ".det_subset.xml " + \
    #                     "--weights " + self.weights + " " + \
    #                     "--max_of_evals " + self.max_of_evals + " " + \
    #                     "--data_dir " + self.data_dir + " " + \
    #                     "--model_type " + model_type + " " + \
    #                     "--samples " + self.samples  + " " + \
    #                     "--counts " + self.sample_index
    #                 commandline_args = "python run_main.py " + \
    #                     self.generate_default_commandline_args(name, experiment_run_id, intervals) + \
    #                     sm_args
    #                 sm_experiments.append(commandline_args)
    #     return sm_experiments




#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """
    """
    # simulators = ["sumo", "matsim"]
    simulators = ["sumo"]
    # traffic_flow_models = [["macro", "meso", "micro"], ["meso"]]
    # traffic_flow_models = [["macro", "meso"], ["meso"]]

    traffic_flow_models = [["macro"]]
    # traffic_flow_models = [["meso"]]
    # traffic_flow_models = [["meso", "macro"]]

    # simulator_executables = [{
    #     "macro": "../../sumo_libraries/sumo/bin/marouter",
    #     "meso": "../../sumo_libraries/sumo/tools/assign/duaIterate_new.py",
    #     "micro": "../../sumo_libraries/sumo/tools/assign/duaIterate_new.py"
    #     }, {"meso": "../../matsim_local/matsim-0.10.1.jar"}] # Path relative to estimation program
    # simulator_executables = [{
    #     "macro": "../../sumo_libraries/sumo/bin/marouter"}] # Path relative to estimation program

    simulator_executables = [{
        "macro": "../../sumo_local/sumo/bin/marouter"}] # Path relative to estimation program
    # simulator_executables = [{
    #     "meso": "../../sumo_local/sumo/tools/assign/duaIterate_new.py"}] # Path relative to estimation program

    # simulator_executables = [{
    #     "meso": "../../sumo_local/sumo/tools/assign/duaIterate_new.py",
    #     "macro": "../../sumo_local/sumo/bin/marouter", # Path relative to estimation program
    #     }] # Path relative to estimation program

    # simulator_executables = [{
    #     "macro": "../../sumo_libraries/sumo/bin/marouter",
    #     "meso": "../../sumo_libraries/sumo/tools/assign/duaIterate_new.py",
    #     }, {"meso": "../../matsim_local/matsim-0.10.1.jar"}] # Path relative to estimation program
    interval_start = "0"
    interval_end = "3600"
    aggregation_intervals = ["1"]

    # constant_demand = "25"
    # total_demand = None

    constant_demand = None
    total_demand = "600"

    test_data_prefix = "TestData"
    lst = ["2", "6", "12", "20", "30"]
    # lst = ["56", "72", "90", "110", "132"];
    network_prefix1 = "grid-network-od"
    # network_prefix2 = "matchstick-network-od"
    # networks = [network_prefix1 + i for i in lst] + [network_prefix2 + i for i in lst]
    networks = [network_prefix1 + i for i in lst] # run 1
    # networks = [network_prefix2 + i for i in lst] # run 2
    gencons = [True]
    # gencons = [False]
    # gencons = [True, False]
    seedmats = [None, "seedmat07", "seedmat08", "seedmat09"]
    # networks = ["grid-network-scale-1-od32",
    #     "grid-network-scale-1-od16",
    #     "grid-network-scale-1-od8",
    #     "grid-network-scale-1-od4",
    # ]
    # networks = ["grid-network-scale-1-od32",
    #     "grid-network-scale-1-od16",
    #     "grid-network-scale-1-od8",
    #     "grid-network-scale-1-od4",
    # ]
        # "grid-network-scale-1-od2",
        # "grid-network-scale-1-od1",
    dua_iterations = "1000"
    random_seed = "3333"
    sensor_coverages = ["100"]
    max_idle_iterations = "25"
    max_of_evals = None
    weight_configs = [["0", "1", "1"]]

    run_experiments = RunExperiments(simulators, traffic_flow_models, simulator_executables, interval_start, interval_end,
         aggregation_intervals, constant_demand, total_demand, test_data_prefix, networks, dua_iterations, random_seed,
        sensor_coverages, max_idle_iterations, max_of_evals, weight_configs, gencons, seedmats)

    commandline_args = []
    # Add commandline args to the list
    # commandline_args += run_experiments.create_test_data()
    # Print out commandline args
    # for item in run_experiments.create_test_data():
    #     print(item, " \n ")
    # print("Number of experiments: ", len(commandline_args))

    #commandline_args = []
    # # Generate SPSA commandline args
    commandline_args += run_experiments.run_spsa(step_length="100", gradient_approximations="1")
    # for item in run_experiments.run_spsa(step_length="25", gradient_approximations="1"):
    #     print(item, " \n ")
    print("Number of experiments: ", len(commandline_args))

    # # Generate SM commandline args
    # # for item in run_experiments.run_sm():
    # #     print(item, " \n ")

    # ###############
    # #     SSH     #
    # ###############
    remote_virtenv_path = "source .local/bin/sumoenv/bin/activate"
    remote_est_path = "~/files/run8/estimation_procedure"
    run(commandline_args, remote_virtenv_path, remote_est_path)

    # Attach to an existing tmux session
    # attach_to_session()
