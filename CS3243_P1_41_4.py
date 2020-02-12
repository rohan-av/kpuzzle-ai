#INFORMED SEARCH 3

import os
import sys
import math
from time import time # assumes Unix-based system; switch to clock if on Windows

class Node(object):
    def __init__(self, orientation):
        self.state = orientation # a list of lists corresponding to the orientation of the tiles
        self.depth = 0
    
    # compare function to check whether two States have the same orientation of tiles
    def compare(self, other):
        return self.state == other.state

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = Node(init_state)
        self.goal_state = Node(goal_state)
        self.actions = list()
        self.max_depth = 0 # max depth reached by tree/graph search
        self.nodes_expanded = 0 # number of nodes expanded
        self.time_taken = 0 # time taken for the latest executed solve operation (in seconds)

    def solve(self):
        start = time()
        #TODO
        # implement your search algorithm here
        self.time_taken = time() - start
        return ["LEFT", "RIGHT"] # sample output 

    # returns Effective Branching Factor
    def get_EFB(self):
        return math.pow(self.nodes_expanded, 1/self.max_depth)

    # returns number of nodes expanded by latest exeuted solve operation
    def get_nodes_expanded(self):
        return self.nodes_expanded

    # you may add more functions if you think is useful

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
