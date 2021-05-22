#import modules
import copy
import queue

# import the user defined modules
from board import *
from priority import PQ

# search class to search the best move
class Search:
    def __init__(self,start):
        self.parentTrace = {}
        self.start = start
        self.finalPath = []
        self.movePath = []
        self.numMoves = 0
        self.end = None

    # function to create the path to be printed
    def createPath(self):
        if self.end:
            target = self.end
        else:
            target = constructTargetBoard(self.start.num_of_Rods,self.start.num_of_Disks,self.start.target_Rod)

        startHash = self.start.hash()
        nextHash = target.hash()

        self.finalPath = []
        self.movePath = []

        if not startHash == nextHash:
            while(True):
                self.finalPath.insert(0,constructBoard(nextHash,self.start.num_of_Rods,self.start.num_of_Disks,self.start.target_Rod))
                if startHash == nextHash:
                    break
                else:
                    moves = self.parentTrace[nextHash][1]
                    self.movePath.insert(0,moves)
                    nextHash = self.parentTrace[nextHash][0]
        
        self.numMoves = len(self.movePath)

    # fucntion to print the path
    def printPath(self,verbose = False):
        if verbose:
            counter = 0
            for i in range(len(self.finalPath)):
                if counter == 0:
                    print("original")
                    print("Heuristic = " + str(self.finalPath[i].heuristic()) + " : Actual Dist = " + str(len(self.finalPath) - counter - 1))
                    self.finalPath[i].printBoard()
                else:
                    print("Move = " + str(counter) + " : " + str(self.movePath[counter - 1]))
                    print("Heuristic = " + str(self.finalPath[i].heuristic()) + " : Actual Dist = " + str(len(self.finalPath) - counter - 1))
                    self.finalPath[i].printBoard()
                print("----------------------------------------")
                counter += 1
        else:
            for i in range(len(self.movePath)):
                print("Move = " + str(i + 1) + " : " + str(self.movePath[i]))
    
# Breadth First Search Class
class bfsSearch(Search):
    def __init__(self,start,end=None):
        super().__init__(start)
        if end is None:
            self.end = constructTargetBoard(start.num_of_Rods,start.num_of_Disks,start.target_Rod)
        else:
            self.end = end
        self.endHash = self.end.hash()
        self.parentTrace = {}
        self.search()

    # function to create a tree and apply Breadth First Search using queue
    def search(self):
        self.parentTrace = {}
        q = queue.Queue()
        q.put((self.start,(0,0,0)))
        while (not q.empty()):
            problem = q.get()[0]
            hash = problem.hash()
            if problem.isproblemSolved():
                self.createPath()
                return
            successors = problem.successor()
            successors[:] = filter(lambda x: x[0].hash() not in self.parentTrace,successors)
            for successor in successors:
                self.parentTrace[successor[0].hash()] = (hash,successor[1])
                q.put(successor)          

# main function
if __name__ == "__main__":
    rods = int(input("Please enter the number of rods: "))
    disks = int(input("Please enter the number of disks: "))
    target_Rod = int(input("Please enter the target rod number: "))
    board = towerOfHanoi(rods,disks,target_Rod-1)
    
    # loop until exit
    while(True):

        print("\n")
        print("Menu...")
        print("\n")

        print("1. Press '1' to Breadth First Search algorithm")
        print("0. Press '0' to exit")

        print("\n")

        # take choice from user
        ch = int(input("Enter your choice based on the menu above..."))
        print("Smallest Disk is Number 1 ....")

        print("\n")

        # choice conditions
        if ch == 0:
            exit(0)
        elif ch == 1:
            bfsSearch(board).printPath(True)
        else:
            print("Please enter a correct choice value")
