#Import sys module
import sys
#Import random module
import random
#Import array module
from array import array

#Class Board to construct a board to display the sketch
class Board:
    # initialize the board class by geting user inputs for number of rods 
    # number of disks and the target rod 
    def __init__(self,num_of_Rods,num_of_Disks,target_Rod):
        self.rods = []
        self.num_of_Disks = num_of_Disks
        
        if num_of_Rods < 9:
            self.num_of_Rods = num_of_Rods
        else:
            raise ValueError("Number of rods must be 8 or less")
        
        if target_Rod < num_of_Rods:
            self.target_Rod = target_Rod
        else:
            raise ValueError("Target rod must be < number of rods!")

        for i in range(num_of_Rods):
            self.rods.append(array('b'))

        for disk in range(num_of_Disks,0,-1):
            self.rods[0].append(disk)

    # function to check if the problem solved or not
    def isproblemSolved(self):
        return len(self.rods[self.target_Rod]) == self.num_of_Disks

    # function to move a disk from one rod to another rod
    def moveDisk(self,fromRodIndex,toRodIndex):
        fRod = self.rods[fromRodIndex]

        if len(fRod):
            disk = fRod.pop()
        else:
            return -2

        tRod = self.rods[toRodIndex]

        if not len(tRod) or tRod[len(tRod)-1] > disk:
            tRod.append(disk)
        else:
            fRod.append(disk)
            return -1

        return (disk,fromRodIndex,toRodIndex)

    # function to calculate hash value
    def hash(self):
        output = 0
        
        for i,rod in enumerate(self.rods):
            for disk in rod:
                output += i << (3 * (disk - 1))
        
        return output

    # function to make copy of the board to check the result
    def makeboardCopy(self):
        new = Board(self.num_of_Rods,self.num_of_Disks,self.target_Rod)
        new.rods = []

        for rod in self.rods:
            new.rods.append(array('b',rod))

        return new

    # function to print the board after the move
    def printBoard(self):
        output = ""
        for rod in self.rods:
            output += "|"
            for disk in rod:
                output += str(disk) + " "
            output += "\n"
        output += "\n"
        sys.stdout.write(output)
        sys.stdout.flush()

    # function to create successor of a node (node with the least value)
    def successor(self):
        succ = []
        child = self.makeboardCopy()

        for fromRod in range(self.num_of_Rods):
            for toRod in range(self.num_of_Rods):
                if fromRod == toRod:
                    continue
                
                moveResults = child.moveDisk(fromRod,toRod)

                if moveResults == -1:
                    continue
                elif moveResults == -2:
                    break
                else:
                    succ.append((child,moveResults))
                    child = self.makeboardCopy()

        return succ

    # heuristic value of a node
    def heuristic(self):
        val = 0
        largetNotON = -1

        for i in range(self.num_of_Disks,0,-1):
            if i not in self.rods[self.target_Rod]:
                largetNotON = i
                break
            
        if largetNotON == -1:
            return 0
        
        for rod in self.rods:
            if largetNotON in rod:
                largetNotONLocation = rod

        val += len(largetNotONLocation) * 2 - 1
        val += largetNotON - len(largetNotONLocation)

        return val

# tower of hanoy function to intialize object
def towerOfHanoi(num_of_Rods,num_of_Disks,target_Rod):
    new  = Board(num_of_Rods,num_of_Disks,target_Rod)
    
    for i in range(len(new.rods)):
        new.rods[i] = array('b')
    
    for disk in range(num_of_Disks,0,-1):
        new.rods[0].append(disk)
    
    return new

# function to construct target board
def constructTargetBoard(num_of_Rods,num_of_Disks,target_Rod):
    new = Board(num_of_Rods,num_of_Disks,target_Rod)

    for i in range(len(new.rods)):
        new.rods[i] = array('b')

    for i in range(num_of_Disks,0,-1):
        new.rods[target_Rod].append(i)

    return new

# function to return the board object
def constructBoard(hash,num_of_Rods,num_of_Disks,target_Rod):
    new = Board(num_of_Rods,num_of_Disks,target_Rod)

    for i in range(len(new.rods)):
        new.rods[i] = array('b')

    for i in range(num_of_Disks,0,-1):
        bit1 = (hash >> (3 * (i - 1))) & 1
        bit2 = (hash >> (3 * (i - 1) + 1)) & 1
        bit3 = (hash >> (3 * (i - 1) + 2)) & 1

        rodNum = bit1 + (bit2 * 2) + (bit3 * 4)
        new.rods[rodNum].append(i)

    return new
