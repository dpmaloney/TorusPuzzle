import copy
import numpy as np

from PriorityQueue import PriorityQueue
class State:
    def __init__(self, values, nummoves=0, parent=None):
        self.board = np.array(values).reshape((3,3))
        self.nummoves = nummoves

    def successor_states(self):
        #find the open space
        openspot = np.where(self.board == 0)
        rowopen = list(zip(openspot[0]))[0][0]
        colopen = list(zip(openspot[1]))[0][0]
        liststates = []
        #swap 0 with one below
        newstate1 = copy.deepcopy(self.board)
        newstate1[rowopen][colopen] = newstate1[(rowopen + 1)%3][colopen]
        newstate1[(rowopen + 1)%3][colopen] = 0
        liststates.append(State(newstate1, self.nummoves+1, parent=self))

        # swap 0 with one above
        newstate2 = copy.deepcopy(self.board)
        newstate2[rowopen][colopen] = newstate2[(rowopen -1) % 3][colopen]
        newstate2[(rowopen - 1) % 3][colopen] = 0
        liststates.append(State(newstate2, self.nummoves + 1, parent=self))

        # swap 0 with one left
        newstate3 = copy.deepcopy(self.board)
        newstate3[rowopen][colopen] = newstate3[rowopen][(colopen - 1) % 3]
        newstate3[rowopen][(colopen - 1) % 3] = 0
        liststates.append(State(newstate3, self.nummoves + 1, self))

        # swap 0 with one right
        newstate4 = copy.deepcopy(self.board)
        newstate4[rowopen][colopen] = newstate4[rowopen][(colopen + 1) % 3]
        newstate4[rowopen][(colopen + 1) % 3] = 0
        liststates.append(State(newstate4, self.nummoves + 1, self))

        return liststates

    def get_h(self):
        currentstatecopy = copy.deepcopy(self.board)
        currentstatecopy = np.reshape(currentstatecopy, (1, 9))[0]
        cost = 0

        for i in range(9):
            if currentstatecopy[i] != i + 1 and i + 1 != 9:
                cost += 1

        return cost




def print_succ(state):
    stateGuy = State(state)
    listedstates = []

    succ_states = stateGuy.successor_states()
    for succ_state in succ_states:
        listedstates.append((list(np.reshape(succ_state.board, (1, 9))[0]), succ_state.get_h()))

    listedstates.sort()
    for succ_state in listedstates:
        print(str(succ_state[0]) + " h=" + str(succ_state[1]))


def solve(initialState):
    iState = State(initialState)
    open = PriorityQueue()
    closed = []
    iStateDict = {}
    iStateDict["state"] = initialState
    iStateDict["h"] = iState.get_h()
    iStateDict["parent"] = None
    iStateDict["g"] = 0
    iStateDict["f"] = iState.get_h()

    open.enqueue(iStateDict)

    while not open.is_empty():
        n = open.pop()
        closed.append(n)
        nState = State(n["state"])
        if n["h"] == 0:
            completedGuy = []
            completedGuy.append(n)
            itemToSearch = n
            while not itemToSearch["state"] == initialState:
                parent = search(itemToSearch, closed)
                completedGuy.append(parent)
                itemToSearch = parent

            completedGuy.reverse()
            for guy in completedGuy:
                print(str(guy["state"]) + " h=" + str(guy["h"]) + " moves: " + str(guy["g"]) )
            break
        else:
            successors = nState.successor_states()
            for successor in successors:
                successorDict = {}
                successorDict["state"] = np.reshape(successor.board, (1, 9))[0].tolist()
                successorDict["h"] = successor.get_h()
                successorDict["parent"] =  n["state"]
                successorDict["g"] = n["g"] + 1
                successorDict["f"] = successor.get_h() + n["g"] + 1
                open.enqueue(successorDict)

def search(state, listOfDicts):
    for parent in listOfDicts:
        if parent["state"] == state["parent"]:
            return parent


solve([0,1,2,3,4,5,6,7,8])


