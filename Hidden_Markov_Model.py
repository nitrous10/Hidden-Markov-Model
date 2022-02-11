import numpy

class Hidden_Markov_Model:
    def __init__(self, test_maze, all_colors, color_dict, evidence):
        self.test_maze = test_maze
        self.all_colors = all_colors
        self.color_dict = color_dict
        self.evidence = evidence

        self.initial_distribution = self.get_initial_distribution() # Starting distribution across all coordinates

        # Create sensor model for each color
        self.sensor_tables = {}
        for color in self.all_colors:
            self.sensor_tables[color] = self.get_cur_sensor_table(color)

        # Create transition model for each coordinate
        self.transition_tables = {}
        for coordinate in self.color_dict:
            self.transition_tables[coordinate] = self.get_cur_transition_table(coordinate)

    # Performs the filtering algorithm. Start with the initial distribution, and update the distribution with every sensor reading
    def filtering(self):
        distribution_list = [] # Keeps track of the distributions at every step
        cur_distribution = self.initial_distribution # Start with the initial distribution
        distribution_list.append(numpy.flipud(cur_distribution))

        # Loop over every color in the list of sensor readings
        for color in self.evidence:
            correct_sensor_model = self.sensor_tables[color] # Get the corresponding sensor model
            running_sum = numpy.zeros((self.test_maze.height, self.test_maze.width)) # To store values for the transition portion of the algorithm

            # Loop over each coordinate in the distribution
            for i in range(self.test_maze.width):
                for j in range(self.test_maze.height):
                    if not self.test_maze.is_floor(i, j): # Skip non-floor states
                        continue
                    cur_coordinate = (i, j)
                    transition_model = self.transition_tables[cur_coordinate] # Transition model for current coordinate
                    cur_cell = cur_distribution[j][i]
                    running_sum += cur_cell*transition_model # Add to transition portion of the algorithm

            # Incorporate sensor model into new distribution and normalize
            new_distribution = correct_sensor_model*running_sum
            new_distribution = self.normalize_distribution(new_distribution)

            distribution_list.append(numpy.flipud(new_distribution))
            cur_distribution = new_distribution

        return distribution_list

    # Sets the initial distribution by setting the probability of each floor ot the same value
    def get_initial_distribution(self):
        num_floors = len(self.color_dict.keys())
        probability = 1 / num_floors # Probability to be inserted for each floor
        initial_distribution = numpy.empty((self.test_maze.height, self.test_maze.width)) # To store the distirbution

        # Loop over all coordinates in the maze
        for i in range(self.test_maze.width):
            for j in range(self.test_maze.height):
                if self.test_maze.is_floor(i, j):
                    initial_distribution[j][i] = probability # Floor, set probability
                else:
                    initial_distribution[j][i] = 0 # Not a floor, no possibility the robot is here

        return initial_distribution

    # Creates the sensor model for a specified color
    def get_cur_sensor_table(self, color):
        cur_sensor_table = numpy.empty((self.test_maze.height, self.test_maze.width)) # To store the sensor model

        # Loop over every coordinate in the maze
        for i in range(self.test_maze.width):
            for j in range(self.test_maze.height):
                if not self.test_maze.is_floor(i, j): # Skip coordinates that are walls
                    continue
                if not self.color_dict[(i, j)] == color: # If colors don't match, still small chance sensor would read it
                    cur_sensor_table[j][i] = 0.04
                else: # Large chance sensor correctly sensed the real color
                    cur_sensor_table[j][i] = 0.88

        return cur_sensor_table

    # Generate the transition model given a coordinate
    def get_cur_transition_table(self, coordinate):
        transition_table = numpy.zeros((self.test_maze.height, self.test_maze.width)) # To store the transition model
        next_states = self.generate_next_states(coordinate) # List of all possible next states from current state (could include duplicates)

        for coordinate in next_states: # Loop over every potential next state
            coord_x = coordinate[0]
            coord_y = coordinate[1]
            transition_table[coord_y][coord_x] += 1/len(next_states) # Increment the probability by a fraction (increment because there could be duplicate next states)

        return transition_table


    # Given a coordinate, generate all possible successor states in the maze (and record duplicates for probability purposes)
    def generate_next_states(self, coordinate):
        potential_nexts = []
        x, y = coordinate[0], coordinate[1]

        # Test each adjacent state. Add if it is a floor, or add the current state otherwise
        if self.test_maze.is_floor(x + 1, y):
            potential_nexts.append((x + 1, y))
        else:
            potential_nexts.append((x, y))
        if self.test_maze.is_floor(x, y + 1):
            potential_nexts.append((x, y + 1))
        else:
            potential_nexts.append((x, y))
        if self.test_maze.is_floor(x, y - 1):
            potential_nexts.append((x, y - 1))
        else:
            potential_nexts.append((x, y))
        if self.test_maze.is_floor(x - 1, y):
            potential_nexts.append((x - 1, y))
        else:
            potential_nexts.append((x, y))

        return potential_nexts

    # Given a distribution, make the sum of the probabilities equal to 1
    def normalize_distribution(self, distribution):
        distribution /= numpy.sum(distribution)
        return distribution