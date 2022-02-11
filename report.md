# PA6 - Hidden Markov Models
Assignment: PA6 - Hidden Markov Models  
Date: Fall 2021, CS76  
Author: Noah Yusen

## Description

### Modeling the Problem
In modeling the problem, I leveraged the Maze code from PA2 and extended the information that is relevant to each maze.
Specifically, I mapped each floor coordinate in the given maze to a color from the set `['r', 'b', 'g', 'y']`. I also specified
the true path a robot might take through the maze and a simulation of the sensor readings that the robot might generate
as it traverses this path. There is an 88% chance that the robot correctly identifies the color of each traversed floor square,
and a 12 % chance that one of the other incorrect colors is chosen. Thus, given the real path traversed (and thus the ground truth floor colors)
and the list of sensor readings, I can pass this information to the Hidden Markov Model, perform filtering, and provide
the observed color, real color, and probability distribution at each step of the robot's journey.

### Representing the Hidden Markov Model
The Hidden Markov Model is designed to work with the mazes, floor colorings, and sensor readings that are defined in the
`HMM_Driver.py` file. First, an initial distribution matrix is created before any floor color values are sensed. This initial distribution
matrix has an equal probability for every potential floor location in the maze (the matrix coordinates correspond to the floor coordinates,
as is the case with each computed model in the HMM). In addition, before filtering is performed, models that
are needed for the filtering algorithm are generated. In a Hidden Markov Model, the sensor models and transition models are
needed to perform filtering. Thus, to create the sensor models, I create a dictionary that maps each color in the maze to a matrix that corresponds to the sensor
model for that color. For example, for the sensor model that corresponds to red, floor locations that are truly red have a probability of 0.88,
while floor locations that are not red have a probability of 0.04. In this way, I can account for the probabilities given the
imperfect sensor readings. The transition models are also stored in a dictionary. There is a transition model (represented
as a matrix with the same dimensions as the maze) for each floor location in the maze, and this transition model specifies the
possible locations (with corresponding probabilities) that a robot could end up after taking a step from a given location.
A robot has an equally likely chance of moving in any of the four cardinal directions, but if a floor does not exist in one of these
directions, then the robot stays put. Since a robot may have walls on more than one side of it, it could be the case that
there is a higher probability that the robot stays put as opposed to moving to an adjacent square. After initializing the
sensor models and transition models, filtering can be performed.

The filtering process starts with the initial state and continually makes updates to the state as the algorithm iterates
over all of the sensor readings. Within each iteration, the correct sensor model is retrieved based on the color of the
current sensor reading. Then, a matrix is created that will store the eventual summation of the transition models. For every
floor location in the probability distribution, the current probability of the floor location is multiplied by the corresponding
transition model for that coordinate. These resulting matrices are added together and multiplied by the retrieved sensor model,
and the result is normalized and saved to the probability distribution history list. The resulting distribution is equivalent to the
calculation specified in the lecture (`update*transition*previous_state_estimate`). This process is repeated for every 
sensor reading, and in each iteration the resulting probability from the last iteration is used as the starting point (this
way, there is a running probability distribution whose value gets continually updated until the final probability distribution
is calculated). The probability distribution history is returned such that the user can see how the robot's belief state changes
over time (as time progresses, the robot should get an increasingly good sense as to where it is within the maze).

## Evaluation
In evaluating my implementation of the Hidden Markov Model, I utilized the test maze, path, and sensor readings that Professor
Li gave over Slack. After running the filtering algorithm and printing the history of probability distributions, I was able
to witness the probability distributions change as the sensor readings were considered. The probability distribution after
the first sensor reading was considered showed higher probabilities for floor locations that were of the sensor color,
consistent with my expectations and consistent with the coefficients that were defined in the corresponding sensor model.
Similarly, after the second sensor reading was considered (yellow), the floor spaces with the highest probabilities were
the yellow floor locations that were next to green floor locations (green was the first sensor color), suggesting that the
transition model also successfully contributes to the updated probability distribution (the highest probability squares would
be the yellow squares adjacent to green squares, as the likelihood that the sensor senses the correct color is high and
robots can only move to adjacent squares after each iteration). The first three probability distributions are shown below
(note: the matrix entries correspond to floor locations in the maze, in the same orientation as the original maze file):

```
Location: -
Observed Color: -
Real Color: -
Distribution:
[[0.06666667 0.06666667 0.06666667 0.06666667]
 [0.06666667 0.06666667 0.06666667 0.06666667]
 [0.06666667 0.06666667 0.         0.06666667]
 [0.06666667 0.06666667 0.06666667 0.06666667]]
-----
Location: (2, 2)
Observed Color: g
Real Color: g
Distribution:
[[0.01282051 0.01282051 0.01282051 0.01282051]
 [0.01282051 0.01282051 0.28205128 0.01282051]
 [0.01282051 0.01282051 0.         0.01282051]
 [0.01282051 0.28205128 0.01282051 0.28205128]]
-----
Location: (3, 2)
Observed Color: y
Real Color: y
Distribution:
[[0.00293686 0.00293686 0.01835536 0.00293686]
 [0.00293686 0.01835536 0.01835536 0.40381791]
 [0.00293686 0.40381791 0.         0.01835536]
 [0.01835536 0.01835536 0.03377386 0.03377386]]
``` 

The final probability distribution is consistent with the expected distribution from the test case as well (when taking
rounding into account) suggesting that the iterative portion of the algorithm was employed successfully:


PREDICTED:
```
Location: (3, 2)
Observed Color: y
Real Color: y
Distribution:
[[3.69069183e-03 4.79197107e-03 2.03024429e-02 3.37349005e-02]
 [9.83976587e-03 4.50909397e-03 4.14976728e-03 6.57121628e-01]
 [1.24825076e-02 1.91376687e-01 0.00000000e+00 2.73483192e-02]
 [1.34633863e-02 3.36330646e-03 3.97087470e-04 1.34284443e-02]]
```

EXPECTED:
```
0.00369	0.00479	0.02030	0.03373	
0.00984	0.00451	0.00415	0.65712	
0.01248	0.19138	0.00000	0.02735	
0.01346	0.00336	0.00040	0.01343	
```

In the test case, each sensor reading was correct. However, we can see what happens to the probability distribution when
we change one of the sensor readings to be an incorrect value. If we change the second to last sensor reading to be `'b'`
instead of `'r'`, our final distribution probability is radically different, and the robot predicts that it is in a different
location (1,1):

```
Location: (3, 3)
Observed Color: b
Real Color: r
Distribution:
[[0.11259444 0.0065048  0.00904594 0.05381444]
 [0.00604179 0.53778985 0.04868215 0.04973009]
 [0.02730538 0.02503134 0.         0.04701858]
 [0.00952319 0.02452023 0.03973062 0.00266715]]
-----
Location: (3, 2)
Observed Color: y
Real Color: y
Distribution:
[[0.0112715  0.03157327 0.00559685 0.00788958]
 [0.03241704 0.00408976 0.03059246 0.2078253 ]
 [0.00321935 0.64111514 0.         0.00694274]
 [0.00336018 0.00468455 0.00505642 0.00436586]]
```

This is likely a result of the encoded high probability that the sensor detects the correct color, and sensing blue adds
doubt that the robot is in the same location as in the original path.