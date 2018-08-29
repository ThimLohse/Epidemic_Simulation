import pandas as pd
import os


class DataHandler:
    """A class that handles input and output data for the simulation."""

    def __init__(self):
        "Indata"
        self.population_size = 50
        self.infection_probability = 0.045
        self.interval = {'minDays': 4, 'maxDays': 8}
        self.mortality_probability = 0.0
        self.random_seeds = None
        self.init_people_coordinates = []
        self.visualize = 0

        "Outdata for each run"
        self.susceptible_per_day = []
        self.infected_per_day = []
        self.dead_per_day = []
        self.recovered_per_day = []
        self.acc_recovered_per_day = []
        self.sick_per_day = []
        self.acc_infected_per_day = []
        self.acc_dead_per_day = []

        "Infection probability. Used for determining the threshold for an epidemic."
        self.infection_probabilities = [0.04, 0.042, 0.044, 0.046, 0.048, 0.05]


        "Active simulation data"
        self.seed = None
        self.current_day = 0
        self.data_frames = []

    def data_summary(self, random_seed):
        """Summarize the data for a simulation"""
        data = {
            'susceptible_per_day': self.susceptible_per_day,
            'infected_per_day': self.infected_per_day,
            'dead_per_day': self.dead_per_day,
            'recovered_per_day': self.recovered_per_day,
            'recovered_accumulated': self.acc_recovered_per_day,
            'sick_per_day': self.sick_per_day,
            'infected_accumulated': self.acc_infected_per_day,
            'dead_accumulated': self.acc_dead_per_day
        }

        df = pd.DataFrame(data)
        path = "../res/" + str(self.infection_probability)

        if os.path.isdir(path):
            df.to_csv(path +
                      "/" + str(random_seed) + ".csv")
        else:
            try:
                os.mkdir(path)
                df.to_csv(path +
                          "/" + str(random_seed) + ".csv")
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)

        return df

    def input_data_summary(self):
        """Summarize input data. Used for debugging"""
        data = {
            'population size': self.population_size,
            'infection probability': self.infection_probability,
            'interval': self.interval,
            'mortality probability': self.mortality_probability,
            'random seeds': self.random_seeds,
            'initial coordinates': self.init_people_coordinates,
            'visualization': self.visualize
        }
        return data

    def reset(self):
        """Reset datahandler fields"""
        self.current_day = 0
        self.susceptible_per_day = []
        self.infected_per_day = []
        self.dead_per_day = []
        self.recovered_per_day = []
        self.acc_recovered_per_day = []
        self.sick_per_day = []
        self.acc_infected_per_day = []
        self.acc_dead_per_day = []
