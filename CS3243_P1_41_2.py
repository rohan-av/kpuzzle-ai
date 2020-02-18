# INFORMED SEARCH 1: Manhattan Distance

import os
import sys
import math
import heapq
from time import time # assumes Unix-based system; switch to clock if on Windows

class Node(object):
    def __init__(self, orientation):
        self.state = orientation # a list of lists corresponding to the orientation of the tiles
        self.current_cost = float('inf')
        self.heuristic_value = float('inf')
        self.previous_action = "START"
        self.previous_node = None
        
        # stats
        self.depth = float('inf')
    
    def __lt__(self, other):
        return (self.current_cost + self.heuristic_value) < (other.current_cost + other.heuristic_value)

    def __eq__(self, other):
        return (self.current_cost + self.heuristic_value) == (other.current_cost + other.heuristic_value)

    # set current path cost
    def set_current_cost(self, cost):
        self.current_cost = cost

    # get current path cost
    def get_current_cost(self):
        return self.current_cost

    # set heuristic value
    def set_heuristic_value(self, value):
        self.heuristic_value = value
    
    # get heuristic value
    def get_heuristic_value(self):
        return self.heuristic_value

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
        self.visited = dict()
        self.actions = list()
        self.max_depth = 0 # max depth reached by tree/graph search
        self.nodes_expanded = 0 # number of nodes expanded
        self.time_taken = 0 # time taken for the latest executed solve operation (in seconds)

    def solve(self):
        start = time()
        #TODO
        # implement your search algorithm here

        '''
        A* with h1: manhattan distance
        '''
        self.init_state.set_current_cost(0)
        self.init_state.set_current_depth(0)
        self.init_state.set_heuristic_value(self.get_heuristic_value(self.init_state))

        frontier = []
        heapq.heappush(frontier, self.init_state)

        while frontier[0].get_heuristic_value() > 0:
            curr = heapq.heappop(frontier)
            self.nodes_expanded += 1;
            # if self.nodes_expanded % 50000 == 0:
            #     print self.nodes_expanded, curr.get_current_cost()
            #     print curr.state
            self.visited[self.tupify(curr.state)] = curr.get_current_cost()

            for i in self.generate_possibilities(curr):
                i.set_current_cost(curr.get_current_cost() + 1)
                i.set_heuristic_value(self.get_heuristic_value(i))
                key = self.tupify(i.state)
                if key not in self.visited or i.get_current_cost() < self.visited[key]:
                    heapq.heappush(frontier, i)
                    self.visited[key] = i.get_current_cost()

            if len(frontier) == 0:
<<<<<<< Updated upstream
                return ["UNSOLVABLE"]
=======
                return ["IMPOSSIBLE"]
        
>>>>>>> Stashed changes

        backtrack = frontier[0]
        while backtrack != None:
            self.actions.append(backtrack.get_previous_action())
            backtrack = backtrack.get_previous_node()

        self.actions.reverse()
        self.time_taken = time() - start
        print self.nodes_expanded, self.time_taken
        return self.actions

    # returns Effective Branching Factor
    def get_EFB(self):
        return math.pow(self.nodes_expanded, 1/self.max_depth)

    # returns number of nodes expanded by latest exeuted solve operation
    def get_nodes_expanded(self):
        return self.nodes_expanded

    # calculates heuristic value for a given node (h1: manhattan distance)
    def get_heuristic_value(self, node):
        # count = 0

        # for i in range(self.size):
        #     for j in range(self.size):
        #         if node.state[i][j] != self.goal_state.state[i][j]:
        #             count += 1
        # return count
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                curr = node.state[i][j]
                if curr == 0:
                    continue
                coord_in_goal = self.search_in_goal(curr);
                count += (abs(coord_in_goal[0]-i) + abs(coord_in_goal[1]-j))
        return count

    def search_in_goal(self, query):
        goal = self.goal_state.state
        for i in range(self.size):
            for j in range(self.size):
                if goal[i][j] == query:
                    return (i, j);
        return (-1, -1)

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
        
        # move blank right
        if blank_x > 0:
            temp = self.twodimensional_copy(node.state)
            temp[blank_y][blank_x] = temp[blank_y][blank_x - 1]
            temp[blank_y][blank_x - 1] = 0
            if self.tupify(temp) not in self.visited:
                temp_node = Node(temp)
                temp_node.set_previous_node(node)
                temp_node.set_previous_action("RIGHT")
                nodes.append(temp_node)
        
        # move blank left
        if blank_x < self.size - 1:
            temp = self.twodimensional_copy(node.state)
            temp[blank_y][blank_x] = temp[blank_y][blank_x + 1]
            temp[blank_y][blank_x + 1] = 0
            if self.tupify(temp) not in self.visited:
                temp_node = Node(temp)
                temp_node.set_previous_node(node)
                temp_node.set_previous_action("LEFT")
                nodes.append(temp_node)
        
        # move blank down
        if blank_y > 0:
            temp = self.twodimensional_copy(node.state)
            temp[blank_y][blank_x] = temp[blank_y - 1][blank_x]
            temp[blank_y - 1][blank_x] = 0
            if self.tupify(temp) not in self.visited:
                temp_node = Node(temp)
                temp_node.set_previous_node(node)
                temp_node.set_previous_action("DOWN")
                nodes.append(temp_node)
        
        # move blank up
        if blank_y < self.size - 1:
            temp = self.twodimensional_copy(node.state)
            temp[blank_y][blank_x] = temp[blank_y + 1][blank_x]
            temp[blank_y + 1][blank_x] = 0
            if self.tupify(temp) not in self.visited:
                temp_node = Node(temp)
                temp_node.set_previous_node(node)
                temp_node.set_previous_action("UP")
                nodes.append(temp_node)

        return nodes
    
    def tupify(self, stateList):
        outer = []
        for i in stateList:
            outer.append(tuple(i))
        return tuple(outer)

    def twodimensional_copy(self, stateList):
        return [i[:] for i in stateList]
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
