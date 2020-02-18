# UNINFORMED SEARCH

import os
import sys
import math
from time import time # assumes Unix-based system; switch to clock if on Windows
import heapq

class Node(object):
    def __init__(self, orientation):
        self.state = orientation # a list of lists corresponding to the orientation of the tiles
        self.depth = 0
        self.previous_action = "START"
        self.previous_node = None
        self.current_cost = float('inf')

        self.depth = float('inf')
    
    # compare function to check whether two States have the same orientation of tiles
    def compare(self, other):
        return self.state == other.state

    # set current path cost
    def set_current_cost(self, cost):
        self.current_cost = cost

    # get current path cost
    def get_current_cost(self):
        return self.current_cost

    # set current depth
    def set_current_depth(self, depth):
        self.depth = depth

    def set_previous_action(self, action):
        self.previous_action = action

    def get_previous_action(self):
        return self.previous_action

    def set_previous_node(self, node):
        self.previous_node = node
    
    def get_previous_node(self):
        return self.previous_node

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.size = len(init_state)
        self.init_state = Node(init_state)
        self.goal_state = Node(goal_state)
        self.visited = set()
        self.actions = list()
        self.max_depth = 0 # max depth reached by tree/graph search
        self.nodes_expanded = 0 # number of nodes expanded
        self.time_taken = 0 # time taken for the latest executed solve operation (in seconds)

    def solve(self):
        start = time()
        #TODO
        # implement your search algorithm here

        frontier = []
        frontier.append(self.init_state);

        find = False

        while True :
            curr =  frontier.pop(0)
            self.visited.add(self.tupify(curr.state))

            for i in self.generate_possibilities(curr):
                i.set_current_cost(curr.get_current_cost() + 1)                
                frontier.append(i)
                if (curr.state == self.goal_state.state):
                    print("Found")
                    find = True
                    break
            if find:
                break

            if len(frontier) == 0:
                return ["IMPOSSIBLE"]

        backtrack = frontier[0]
        while backtrack != None:
            self.actions.append(backtrack.get_previous_action())
            backtrack = backtrack.get_previous_node()
        
        self.actions.reverse()
        self.time_taken = time() - start
        print(self.time_taken)
        return self.actions # sample output 

    def generate_possibilities(self, node):
        blank_x = -1
        blank_y = -1
        nodes = []

        for y in range(self.size):
            if blank_x != -1:
                break

            for x in range(self.size):
                if node.state[y][x] == 0:
                    blank_x = x
                    blank_y = y
                    break
        
        # move blank left
        if blank_x > 0:
            temp = self.twodimensional_copy(node.state)
            temp[blank_y][blank_x] = temp[blank_y][blank_x - 1]
            temp[blank_y][blank_x - 1] = 0
            if self.tupify(temp) not in self.visited:
                temp_node = Node(temp)
                temp_node.set_previous_node(node)
                temp_node.set_previous_action("LEFT")
                nodes.append(temp_node)
        
        # move blank right
        if blank_x < self.size - 1:
            temp = self.twodimensional_copy(node.state)
            temp[blank_y][blank_x] = temp[blank_y][blank_x + 1]
            temp[blank_y][blank_x + 1] = 0
            if self.tupify(temp) not in self.visited:
                temp_node = Node(temp)
                temp_node.set_previous_node(node)
                temp_node.set_previous_action("RIGHT")
                nodes.append(temp_node)
        
        # move blank up
        if blank_y > 0:
            temp = self.twodimensional_copy(node.state)
            temp[blank_y][blank_x] = temp[blank_y - 1][blank_x]
            temp[blank_y - 1][blank_x] = 0
            if self.tupify(temp) not in self.visited:
                temp_node = Node(temp)
                temp_node.set_previous_node(node)
                temp_node.set_previous_action("UP")
                nodes.append(temp_node)
        
        # move blank down
        if blank_y < self.size - 1:
            temp = self.twodimensional_copy(node.state)
            temp[blank_y][blank_x] = temp[blank_y + 1][blank_x]
            temp[blank_y + 1][blank_x] = 0
            if self.tupify(temp) not in self.visited:
                temp_node = Node(temp)
                temp_node.set_previous_node(node)
                temp_node.set_previous_action("DOWN")
                nodes.append(temp_node)

        return nodes

    # returns Effective Branching Factor
    def get_EFB(self):
        return math.pow(self.nodes_expanded, 1/self.max_depth)

    # returns number of nodes expanded by latest exeuted solve operation
    def get_nodes_expanded(self):
        return self.nodes_expanded

    # you may add more functions if you think is useful
    def tupify(self, stateList):
        outer = []
        for i in stateList:
            outer.append(tuple(i))
        return tuple(outer)

    def twodimensional_copy(self, stateList):
        return [i[:] for i in stateList]

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
