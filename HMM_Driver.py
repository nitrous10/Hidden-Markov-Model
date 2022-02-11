from Maze import Maze
from Hidden_Markov_Model import Hidden_Markov_Model

# Constants for length of path and possible colors
COLORS = {"r", "g", "y", "b"}

# TESTING
test_maze = Maze("test_maze3.maz")
color_dict = { # Maps floor coordinates to colors
    (0, 0): "r",
    (1, 0): "g",
    (2, 0): "b",
    (3, 0): "g",
    (0, 1): "r",
    (1, 1): "y",
    (3, 1): "r",
    (0, 2): "r",
    (1, 2): "b",
    (2, 2): "g",
    (3, 2): "y",
    (0, 3): "b",
    (1, 3): "r",
    (2, 3): "r",
    (3, 3): "r"
}
path = [(2, 2), (3, 2), (3, 3), (3, 3), (2, 3), (2,3), (3, 3), (3, 2), (3, 3), (3, 2)] # Test path taken by the robot
sensor_test = ['g', 'y', 'r', 'r', 'r', 'r', 'r', 'y', 'r', 'y'] # Values sensed by the robot


# Used by random path generator, generates all of the potential moves (successor locations) for the robot
# For each action (NSEW), add the result location to a list (location might not change)
# def generate_next_states(test_maze):
#     potential_nexts = []
#     x, y = test_maze.robotloc
#     if test_maze.is_floor(x+1, y):
#         potential_nexts.append((x+1, y))
#     else:
#         potential_nexts.append((x, y))
#     if test_maze.is_floor(x, y+1):
#         potential_nexts.append((x, y+1))
#     else:
#         potential_nexts.append((x, y))
#     if test_maze.is_floor(x, y-1):
#         potential_nexts.append((x, y-1))
#     else:
#         potential_nexts.append((x, y))
#     if test_maze.is_floor(x-1, y):
#         potential_nexts.append((x-1, y))
#     else:
#         potential_nexts.append((x, y))
#     return potential_nexts

# def color_floor(test_maze):
#     color_dict = {}
#     for i in range(test_maze.width):
#         for j in range(test_maze.height):
#             if test_maze.is_floor(i, j):
#                 coordinate = (i, j)
#                 color_dict[coordinate] = rand.choice(list(COLORS))
#     return color_dict


# Create a random path for the robot to travel
# def create_path(test_maze):
#     original_loc = tuple(test_maze.robotloc)
#     path = [original_loc]
#
#     for i in range(PATH_LENGTH-1):
#         next = rand.choice(generate_next_states(test_maze)) # Randomly choose a state, which corresponds to randomly choosing an action
#         test_maze.robotloc = next
#         path.append(next)
#
#     test_maze.robotloc = original_loc
#
#     return path

def run_test(test_maze, path, color_dict, sensor_test):
    # Start with "-" because no reading at the first distribution
    real_colors = ["-"]
    robot_locs = ["-"]

    for i in range(len(path)): # Populate the locations and colors that should be seen by the robot
        robot_locs.append(path[i])
        real_colors.append(color_dict[path[i]])

    # Perform the filtering
    model = Hidden_Markov_Model(test_maze, COLORS, color_dict, sensor_test)
    distribution_list = model.filtering()

    sensor_test.insert(0, "-") # Prepend "-" because no sensor value at first distribution

    # Print location, sensor reading, real color, and distribution at every step
    for i in range(len(distribution_list)):
        print("Location: " + str(robot_locs[i]))
        print("Observed Color: " + str(sensor_test[i]))
        print("Real Color: " + str(real_colors[i]))
        print("Distribution:")
        print(distribution_list[i])
        print("-----")

run_test(test_maze, path, color_dict, sensor_test)


