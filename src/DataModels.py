import enum
import numpy as np

class State(enum.Enum):
    """Enum class to for easier identification of the state of a Person"""
    susceptible = 0
    infected = 1
    immune = 2
    dead = 3


class Person(object):
    """Common class for a generic person"""

    def __init__(self, id, x, y):
        self.id = id
        self.state = State.susceptible
        self.sick_days = 0
        self.neighbours = None
        self.day_of_infection = None
        self.day_of_death = None
        self.day_of_immunity = None
        self.coordinates = {'x': x, 'y': y}

    def __repr__(self):
        representation = {
            'id': self.id,
            'state': self.state.name,
            'number of sick days': self.sick_days,
            'day of infection': self.day_of_infection,
            'day of death': self.day_of_death,
            'day of immunity': self.day_of_immunity,
            'coordinates': self.coordinates
        }
        return repr(representation)

    def infect(self, infection_probability, current_day, interval):
        """Infect the person based on infection probability"""
        if self.state == State.susceptible:
            min_days = interval['minDays']
            max_days = interval['maxDays'] + 1
            weights = [infection_probability, 1.0 - infection_probability]
            outcomes = [1, 0]
            infected = np.random.choice(outcomes, p=weights)
            if infected:
                self.day_of_infection = current_day
                self.state = State.infected
                self.sick_days = np.random.randint(min_days, max_days)

    def update(self, current_day, mortality_probability):
        """Update the status of the person after each passing day"""
        if self.state == State.infected:

            if self.sick_days > 0 and current_day - self.day_of_infection >= self.sick_days:
                # Person has recovered and is henceforth immune
                self.state = State.immune
                self.day_of_immunity = current_day

            else:
                # Person might die due to the mortality probability
                weights = [mortality_probability, 1.0 - mortality_probability]
                outcomes = [1, 0]
                died = np.random.choice(outcomes, p=weights)
                if died:
                    self.state = State.dead
                    self.day_of_death = current_day

    def get_neighbours(self):
        """Get the list of neighbours to the person"""
        return self.neighbours


class Population:
    'Common base class for the population'

    def __init__(self, data_handler):
        # Initialize the population with regards to the input parameters 'population size' and 'number of sick individuals initially'.
        self.population_size = data_handler.population_size
        self.population = np.empty(
            [self.population_size, self.population_size], dtype=Person)
        id = 1
        for x in range(0, self.population_size):
            for y in range(0, self.population_size):
                person = Person(id, x, y)
                for initial in data_handler.init_people_coordinates:
                    if initial == (x, y):
                        person.infect(1.0, 0, data_handler.interval)
                self.population[x, y] = person
                id += 1

    def generate_neighbours(self):
        """Generate 8 closest neighbours in 8 directions"""
        max_range = self.population_size
        for i in range(0, max_range):
            for j in range(0, max_range):
                x = self.population[i, j].coordinates['x']
                y = self.population[i, j].coordinates['y']
                neighbours = np.empty([8, 1], dtype=Person)
                above = (y + max_range + 1) % max_range
                below = (y + max_range - 1) % max_range
                left = (x + max_range - 1) % max_range
                right = (x + max_range + 1) % max_range
                neighbours[0] = self.population[right, y]
                neighbours[1] = self.population[left, y]
                neighbours[2] = self.population[x, above]
                neighbours[3] = self.population[x, below]
                neighbours[4] = self.population[right, above]
                neighbours[5] = self.population[right, below]
                neighbours[6] = self.population[left, below]
                neighbours[7] = self.population[left, above]
                self.population[x, y].neighbours = neighbours.flatten()

    def infected_present(self):
        """Return True if any infected people are present, False otherwise"""
        for x in self.population.flatten():
            if x.state == State.infected:
                return True
        return False
