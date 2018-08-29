from DataHandler import DataHandler
from Simulation import Simulation
import numpy as np
import csv
data_handler = DataHandler()


def read_random_seeds():
    """Reads in the random seeds from a csv file and sorts them in ascending order."""
    random_seeds = []
    with open('./final.csv') as data_file:
        csvReader = csv.reader(data_file)
        for row in csvReader:
            random_seeds.append(int(row[0]))

    random_seeds.sort()
    random_seeds = random_seeds[:]
    return random_seeds


def user_input():
    while True:
        try:
            # cast to int
            # if no value is entered catch the exception and use defualt values
            population_size = int(input("Population size: "))
            data_handler.population_size = population_size
            print("The population size is: ",
                  data_handler.population_size, "\n")
            break
        except ValueError:
            # got something that could not be cast to a int. Interpret as user wanting default value.
            print("Default value used.")
            print("The population size is: ",
                  data_handler.population_size, "\n")
            break
    while True:
        try:
            # cast to float
            # check it is in the correct range and is so save
            infection_probability = float(input("Infection probability: "))
            if 0 <= infection_probability <= 1:
                data_handler.infection_probability = infection_probability
                print("The infection probability is: ",
                      data_handler.infection_probability, "\n")
                break
            # else tell user they are not in the correct range
            print("Please try again, it must be a decimal number between 0 and 1")
        except ValueError:
            # got something that could not be cast to a float. Interpret as user wanting default value.
            print("Default value used.")
            print("The infection probability is: ",
                  data_handler.infection_probability, "\n")
            break
    while True:
        try:
            # cast to int
            min_days = int(
                input("Minimum days of infection interval as an integer: "))
            # check that min days is at least 1 day.
            if 0 < min_days:
                data_handler.interval["minDays"] = min_days
                print("The minimum number of days for infection is: ",
                      data_handler.interval["minDays"], "\n")
                break
            # else tell user they have choosen a number to small.
            print('Please try again. The minimum number of days must be larger than 0')
        except ValueError:
            # got something that could not be cast to a int. Interpret as user wanting default value.
            print("Default value used.")
            print("The minimum number of days for infection is: ",
                  data_handler.interval["minDays"], "\n")
            break
    while True:
        try:
            # cast to int
            max_days = int(
                input("Maximum days of infection interval as an integer: "))
            # check that max days is larger than min days
            if max_days > data_handler.interval["minDays"]:
                data_handler.interval["maxDays"] = max_days
                print("The maximum number of days for infection is: ",
                      data_handler.interval["maxDays"], "\n")
                break
            # else tell user they have choosen a number too small.
            print(
                "Please try again, the maximum number of days must be larger than the minimum number of days.")
        except ValueError:
            # got something that could not be cast to a int. Interpret as user wanting default value.
            print("Default value used.")
            print("The maximum number of days for infection is: ",
                  data_handler.interval["maxDays"], "\n")
            break
    while True:
        try:
            # cast to float
            # check it is in the correct range and if so save it.
            mortality_probability = float(input("Mortality probability: "))
            if 0 <= mortality_probability <= 1:
                data_handler.mortality_probability = mortality_probability
                print("The mortality probability is: ",
                      data_handler.mortality_probability, "\n")
                break
            # else tell user they are not in the correct range
            print("Please try again, it must be a decimal number between 0 and 1")
        except ValueError:
            # got something that could not be cast to a float. Interpret as user wanting default value.
            print("Default value used.")
            print("The mortality probability is: ",
                  data_handler.mortality_probability, "\n")
            break
    while True:
        # The user can decide the number and positions of the initially infected people.
        try:
            init_people_coordinates = []
            x = int(np.floor(data_handler.population_size / 2))
            y = int(np.floor(data_handler.population_size / 2))

            init_number_sick = int(
                input("Enter number of initially sick people: "))
            if 0 < init_number_sick:
                for i in range(0, init_number_sick):
                    while True:
                        try:
                            print("Possible x values are: 0 to ",
                                  data_handler.population_size - 1)
                            x = int(
                                input("Enter the x value of person " + str((i + 1)) + ": "))
                            if 0 <= x < data_handler.population_size:
                                break
                            print("The coordinate choosen is out of range.")
                        except ValueError:
                            pass
                    while True:
                        try:
                            print("Possible y values are: 0 to ",
                                  data_handler.population_size - 1)
                            y = int(
                                input("Enter the y value of person " + str((i + 1)) + ": "))
                            if 0 <= x < data_handler.population_size:
                                break
                            print("The coordinate choosen is out of range.")
                        except ValueError:
                            pass
                    init_people_coordinates.append((x, y))
            data_handler.init_people_coordinates = init_people_coordinates
            break

        except ValueError:
            # got something that could not be cast to int. Interpret as user wanting default value.
            print("Default value used.")
            print("1 sick indivual is placed at the center at position: ", (x, y))
            init_people_coordinates.append((x, y))
            data_handler.init_people_coordinates = init_people_coordinates
            print("\n")
            break
    while True:
        try:
            # Visualization is the day by day status of the population.
            visualize = input(
                "Do you want to visualize the simulation, y/n?: ")
            if visualize == "y":
                data_handler.visualize = 1
                print("Visualization enabled.\n")
                break
            elif visualize == "n":
                print("Visualization disabled.\n")
                break
            print("Please try again. Choose between y or n")
        except ValueError:
            print("Default value used. Visualization disabled. \n")
            break

    while True:
        try:
            # The user can choose a random seed from the list of 100 seeds, or use the default which is the first seed in the list.
            data_handler.random_seeds = read_random_seeds()
            seed = int(
                input("Choose a number between 1-100 to choose the random seed: "))
            if 0 < seed <= 100:
                data_handler.seed = data_handler.random_seeds[seed - 1]
                print("Seed value used is: ", data_handler.seed)
                break
            print("The number choosen is out of range, please try again.")
        except ValueError:
            data_handler.seed = data_handler.random_seeds[0]
            print("Default value used.")
            print("Seed value used is: ", data_handler.seed)
            break

    while True:
        try:
            action = input("Start simulation, y/n?: ")
            if action == "y":
                print("Simluation started!")
                simulation = Simulation(data_handler)
                data = simulation.run_simluation()
                #simulation.run_full_simulation() #autmation for finding the threshold for the infection probability leading to an epidemic
                break
            elif action == "n":
                print("Program exited.")
                break
            # else tell user they are not in the correct range
            print("Please try again. Choose between y or n")
        except ValueError:
            # Something went wrong
            print("Something went wrong. Program exited.")
            break
    while True:
        try:
            # The user can choose which data to show directly in the program for quick access,
            # although all the data is saved to csv at the end of the simulation.
            choices = []
            keys = []
            print(0, 'All data')
            choices.append(data['df'])
            keys.append('All data')
            for i, key in enumerate(data['df']):
                print(i + 1, key)
                choices.append(data['df'][key])
                keys.append(key)
            print(9, 'Exit')
            choice = int(
                input('Choose which data you would like to view or 9 for exit:\n'))
            if choice == 0:
                print(keys[choice])
                print(choices[0])
            elif 1 <= choice <= 8:
                print(keys[choice])
                print(choices[choice])
            elif choice == 9:
                print('Program exited.')
                break
            else:
                print('The choice is out of range. Please try again.')
        except ValueError:
            print('Invalid value. Program exited.')


print("Welcome to epidemic simulation 1.0.")
print("Please enter parameter values followed by enter, or just press enter to use default values.\n")

user_input()
