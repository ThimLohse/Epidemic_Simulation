from DataModels import Person
from DataModels import Population
from DataModels import State
import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.graphics.gofplots import qqplot


class Simulation:
    """Simluation class"""

    def __init__(self, data_handler):
        """Init the population for the simluation"""
        self.data_handler = data_handler
        self.population_holder = Population(data_handler)
        self.population_holder.generate_neighbours()

    def reset(self):
        """Resets the simulation class with the current data handler values"""
        self.population_holder = Population(self.data_handler)
        self.population_holder.generate_neighbours()

    def set_random_seed(self, random_seed):
        """Set the random seed for the random generator. This is needed for reproducability"""
        np.random.seed(random_seed)

    def compile_results(self):
        """Compile simple statistical information from the simulation"""
        infected = []
        dead = []
        data = {
            'avg_infected': 0,
            'med_infected': 0,
            'std_infected': 0,
            'average_median_difference_infected': 0,
            'avg_dead': 0,
            'med_dead': 0,
            'std_dead': 0,
            'average_median_difference_dead': 0
        }
        for obj in self.data_handler.data_frames:
            if obj['prob'] == self.data_handler.infection_probability:
                infected.append(np.max(obj['df']['infected_accumulated']))
                dead.append(np.max(obj['df']['dead_accumulated']))
        data['avg_infected'] = np.mean(infected)
        data['med_infected'] = np.median(infected)
        data['avg_dead'] = np.mean(dead)
        data['med_dead'] = np.median(dead)
        data['std_infected'] = np.std(infected)
        data['std_dead'] = np.std(dead)
        data['average_median_difference_infected'] = np.abs(
            np.mean(infected) - np.median(infected))
        data['average_median_difference_dead'] = np.abs(
            np.mean(dead) - np.median(dead))
        return data

    def append_results(self, seed, data_frame):
        """Append the result frame for a simulation with a specific seed and infection probability"""
        self.data_handler.data_frames.append(
            {'prob': self.data_handler.infection_probability, 'seed': seed, 'df': data_frame})

    def visualize_results(self, seed):
        """Visualize the status of the population"""
        g1_x = []
        g1_y = []
        g2_x = []
        g2_y = []
        g3_x = []
        g3_y = []
        g4_x = []
        g4_y = []
        infected = 0
        healthy = 0
        immune = 0
        dead = 0
        for person in self.population_holder.population.flatten():

            if person.state == State.infected:
                g1_x.append(person.coordinates['x'])
                g1_y.append(person.coordinates['y'])
                infected += 1
            if person.state == State.susceptible:
                g2_x.append(person.coordinates['x'])
                g2_y.append(person.coordinates['y'])
                healthy += 1
            if person.state == State.immune:
                g3_x.append(person.coordinates['x'])
                g3_y.append(person.coordinates['y'])
                immune += 1
            if person.state == State.dead:
                g4_x.append(person.coordinates['x'])
                g4_y.append(person.coordinates['y'])
                dead += 1
        g1 = (g1_x, g1_y)
        g2 = (g2_x, g2_y)
        g3 = (g3_x, g3_y)
        g4 = (g4_x, g4_y)

        dot_scale_value = 100

        if 30 <= self.population_holder.population_size:
            dot_scale_value = 10
        elif 10 < self.population_holder.population_size < 30:
            dot_scale_value = 30
        else:
            dot_scale_value = 80

        data = (g1, g2, g3, g4)
        colors = ("red", "green", "blue", "black")
        groups = ("infected: " + str(infected), "healthy: " +
                  str(healthy), "immune: " + str(immune), "dead: " + str(dead))
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, facecolor="1.0")

        for data, color, group in zip(data, colors, groups):
            x, y = data
            ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none',
                       s=dot_scale_value, label=group)

        plt.title('Population Infected status for day: ' +
                  str(self.data_handler.current_day))
        # Shrink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ticks = []
        labels = []
        for i in range(0, self.data_handler.population_size):
            ticks.append(i)
            labels.append(str(i))
        plt.xticks(ticks, labels)
        plt.yticks(ticks, labels)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xlim(-1, self.data_handler.population_size)
        plt.ylim(-1, self.data_handler.population_size)

        if dot_scale_value == 10:
            plt.tick_params(axis='both', labelsize=5.0)
            plt.tick_params(axis='x', labelrotation=90.0)
        elif dot_scale_value == 30:
            plt.tick_params(axis='both', labelsize=5.0)
            plt.tick_params(axis='x', labelrotation=90.0)



        # Save the image of the current day in a folder specific to the infection probability.
        path = "../res/" + str(self.data_handler.infection_probability)
        if os.path.isdir(path):
            inner = path + "/img"
            if os.path.isdir(inner):
                plt.savefig(inner + '/' + str(seed) + '.' +
                            str(self.data_handler.current_day) + '.png')
            else:
                try:
                    os.mkdir(inner)
                    plt.savefig(inner + '/' + str(seed) + '.' +
                                str(self.data_handler.current_day) + '.png')
                except OSError:
                    print("Creation of the directory %s failed" % path)

        else:
            try:
                os.mkdir(path)
                inner = path + "/img"
                if os.path.isdir(inner):
                    plt.savefig(inner + '/' + str(seed) + '.' +
                                str(self.data_handler.current_day) + '.png')
                else:
                    try:
                        os.mkdir(inner)
                        plt.savefig(inner + '/' + str(seed) + '.' +
                                    str(self.data_handler.current_day) + '.png')
                    except OSError:
                        print("Creation of the directory %s failed" % path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)
        plt.close()

    def analyze(self):
        """Analyze and save the current status of the population numerically"""
        susceptible_count = 0
        infected_count = 0
        sick_count = 0
        recovered_count = 0
        dead_count = 0
        for person in self.population_holder.population.flatten():
            if person.state == State.susceptible:
                susceptible_count += 1
            if person.state == State.infected and person.day_of_infection < self.data_handler.current_day:
                sick_count += 1
            if person.state == State.infected and person.day_of_infection == self.data_handler.current_day:
                infected_count += 1
            if person.state == State.immune and person.day_of_immunity == self.data_handler.current_day:
                recovered_count += 1
            if person.state == State.dead and person.day_of_death == self.data_handler.current_day:
                dead_count += 1
        self.data_handler.susceptible_per_day.append(susceptible_count)
        self.data_handler.infected_per_day.append(infected_count)
        self.data_handler.sick_per_day.append(sick_count)
        self.data_handler.recovered_per_day.append(recovered_count)
        self.data_handler.dead_per_day.append(dead_count)

        if len(self.data_handler.acc_dead_per_day) < 1:
            self.data_handler.acc_dead_per_day.append(dead_count)
        else:
            self.data_handler.acc_dead_per_day.append(
                dead_count + self.data_handler.acc_dead_per_day[self.data_handler.current_day - 1])

        if len(self.data_handler.acc_infected_per_day) < 1:
            self.data_handler.acc_infected_per_day.append(infected_count)
        else:
            self.data_handler.acc_infected_per_day.append(
                infected_count + self.data_handler.acc_infected_per_day[self.data_handler.current_day - 1])

        if len(self.data_handler.acc_recovered_per_day) < 1:
            self.data_handler.acc_recovered_per_day.append(recovered_count)
        else:
            self.data_handler.acc_recovered_per_day.append(
                recovered_count + self.data_handler.acc_recovered_per_day[self.data_handler.current_day - 1])

    def run_full_simulation(self):
        """An automation function to run simulations with a collection of infection probabilities to find the threshold for the infection probability turning into an epidemic."""
        for prob in self.data_handler.infection_probabilities:
            self.data_handler.infection_probability = prob
            for seed in self.data_handler.random_seeds:
                self.data_handler.seed = seed
                self.run_simluation()
            print(self.compile_results())

        self.plot_results()

    def plot_results(self):
        """Function to plot the Mean and Median of each infection probability when using multiple seeds."""
        columns = ['Population Infected', 'Infection Probability']
        df_total_data = pd.DataFrame(columns=columns)
        list_of_frames = []
        for frame in self.data_handler.data_frames:
            df = {'Population Infected': np.max(
                frame['df']['infected_accumulated']), 'Infection Probability': frame['prob']}
            list_of_frames.append(df)

        df_total_data = df_total_data.append(list_of_frames)

        # Plot the mean
        ax = sns.pointplot(scale=0.5, data=df_total_data, x="Infection Probability",
                           y="Population Infected", capsize=.2, errwidth=0.6, estimator=np.mean)
        plt.axhline(np.square(self.data_handler.population_size) / 2,
                    color="k", linestyle="--", label='Epidemic Outbreak Threshold')
        plt.legend()
        title = "Mean Total number of people infected per infection probability"
        plt.title(title)
        plt.show(ax)

        # Plot the median
        ax = sns.pointplot(scale=0.5, data=df_total_data, x="Infection Probability",
                           y="Population Infected", capsize=.2, errwidth=0.6, estimator=np.median)
        plt.axhline(np.square(self.data_handler.population_size) / 2,
                    color="k", linestyle="--", label='Epidemic Outbreak Threshold')
        plt.legend()
        title = "Median Total number of people infected per infection probability"
        plt.title(title)
        plt.show(ax)

        self.plot_distribution()

    def plot_distribution(self):
        """Function to plot and visualize central tendencies and normality of the simulation results."""
        x = []
        for frame in self.data_handler.data_frames:
            x.append(np.max(frame['df']['infected_accumulated']))
        serie = pd.Series(x, name="Number of infected for different seeds")
        ax = sns.distplot(serie, rug=True, hist=False)
        plt.title("Central tendencies of distribution")
        plt.ylabel('Kernel Density Estimation')
        plt.show(ax)

        data = np.array(x)
        ax = qqplot(data, line='s')
        plt.show(ax)

    def run_simluation(self):
        """The central simulation function."""
        seed = self.data_handler.seed
        print("Simulating with seed: ", seed)
        self.set_random_seed(seed)
        self.data_handler.reset()
        self.reset()

        # Run until entire population is either dead or immune
        while self.population_holder.infected_present():

            # Examine and infect
            for person in self.population_holder.population.flatten():

                # The incubation time for an infected individual to start being contagious is 1 day.
                # An infected individual cannot infect neighbours until after 1 day of getting infected.
                if person.state == State.infected and person.day_of_infection < self.data_handler.current_day:

                    for neighbour in person.get_neighbours().flatten():
                        neighbour.infect(self.data_handler.infection_probability,
                                         self.data_handler.current_day, self.data_handler.interval)

            # Update the status of each person after the entire population has been examined
            for person in self.population_holder.population.flatten():
                person.update(self.data_handler.current_day,
                              self.data_handler.mortality_probability)

            # Analyze the status of the population and save data for current day
            self.analyze()

            # Visualize the status of the population as a grid
            if(self.data_handler.visualize == 1):
                self.visualize_results(seed)
            self.data_handler.current_day += 1

        # Summarize the data for the simulation with the current seed and save it.
        self.append_results(seed, self.data_handler.data_summary(seed))

        # return the simulation data.
        return(self.data_handler.data_frames[0])
