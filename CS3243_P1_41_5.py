import os
import sys
import math
from fractions import Fraction  

import CS3243_P1_41_1 as uninformed
import CS3243_P1_41_2 as informedHOne # Manhattan Distance
import CS3243_P1_41_3 as informedHTwo # Manhattan Distance + Linear Conflict
import CS3243_P1_41_4 as informedHThree # Euclidean Distance

class PuzzleTester(object):
    def __init__(self):
        self.uninformed = uninformed
        self.informedHOne = informedHOne
        self.informedHTwo = informedHTwo
        self.informedHThree = informedHThree

    def testUninformed(self, initial, goal_state):
        currentAlgo = self.uninformed.Puzzle(initial, goal_state)
        printIntro(currentAlgo, initial)
        currentAlgo.solve()
        generateStatistics(currentAlgo)
    
    def testInformed(self, initial, goal_state):
        for i in [self.informedHOne, self.informedHTwo, self.informedHThree]:
            currentAlgo = i.Puzzle(initial, goal_state)
            printIntro(currentAlgo, initial)
            currentAlgo.solve()
            generateStatistics(currentAlgo)

    def test_three(self):
        cases = [
            [[4, 1, 0], [7, 5, 3], [8, 2, 6]],
            [[3, 0, 2], [1, 4, 5], [8, 7, 6]], 
            [[8, 6, 7], [2, 5, 4], [3, 0, 1]]
        ]
    #self.uninformed, self.informedHOne, self.informedHTwo, 
        for j in cases:
            for i in [self.uninformed, self.informedHOne, self.informedHTwo, self.informedHThree]:
                currentAlgo = i.Puzzle(j, goal_state)
                printIntro(currentAlgo, j)
                currentAlgo.solve()
                generateStatistics(currentAlgo)

def printIntro(puzzle, initial):
    print "---------------------"
    print "Heuristic:", puzzle.name
    print ""

    puzzle_size = len(initial)
    for i in initial:
        line = " "
        for j in i:
            line += (str(j) + (" " if j > 9 else "  "))
        print "|", line, "|" 
    print ""

def generateStatistics(puzzle):
    print "No. of Inversions:", puzzle.inversions
    print "Nodes Expanded:", puzzle.nodes_expanded
    print "Max Frontier Size:", puzzle.max_size
    print "Time Taken:", puzzle.time_taken
    print "Length of Solution:", (len(puzzle.actions) - 1)
    print "Effective Branching Factor:", math.pow(puzzle.nodes_expanded, Fraction(1, (len(puzzle.actions) - 1))) if (len(puzzle.actions) - 1) > 0 else "undef"
    print "Input difficulty:", float(len(puzzle.actions) - 1) / float(205 if puzzle.size == 5 else (80 if puzzle.size == 4 else 31))
    print ""

if __name__ == "__main__":
    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    # argv[3] represents if uninformed search should be included

    if len(sys.argv) != 3 and len(sys.argv) != 4:
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

    puzzleTester = PuzzleTester()

    if len(sys.argv) == 4:
        if sys.argv[3] == '2':
            puzzleTester.test_three()
            quit()
        else:
            puzzleTester.testUninformed(init_state, goal_state)

    puzzleTester.testInformed(init_state, goal_state)
    