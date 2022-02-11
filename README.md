# PA6 - Hidden Markov Models
Assignment: PA6 - Hidden Markov Models
Date: Fall 2021, CS76
Author: Noah Yusen

## Running the Program
Running the program requires the user to specify the maze that the robot is navigating. The definition of this maze is
consistent with the maze definitions from PA2, in which floors are represented with "." and walls are represented with "#".
In addition to specifying the name of the maze file in the `HMM_Driver.py` file, the user must also specify: 1) the mapping
of floor locations in the maze to colors, in which each floor square corresponds to a color from the set `['r', 'g', 'b', 'y']`, 2)
the path that the robot takes through the maze (to generate the ground truth colors for comparison purposes), and 3) the list
of sensor readings that is consistent with the length of the path. Once these values are specified, the program can be run
by running the code within the `HMM_Driver.py` file (in Pycharm, click the green play button).

If the user wishes to perform calculations on a different maze with a different floor coloring and path, the user should define
another maze file consistent with the maze standards from PA2, provide a new floor color dictionary, and specify a new path and a
new list of sensor readings that the robot senses. 