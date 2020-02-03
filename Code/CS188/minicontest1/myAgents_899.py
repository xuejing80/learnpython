# myAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
import searchProblems
from game import Directions
from game import Agent
from searchProblems import PositionSearchProblem

import util
import time

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
chasingGoal = []

def createAgents(num_pacmen, agent='MyAgent'):
    MyAgent.num_pacmen=0
    chasingGoal.clear()
    return [eval(agent)(index=i) for i in range(num_pacmen)]



class MyAgent(Agent):
    """
    Implementation of your agent.
    """
    num_pacmen = 0

    def findPathToAllDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        "*** YOUR CODE HERE ***"
        # Here are some useful elements of the startState
        # return aStarSearch(problem,cloestDotHeuristic)
        return breadthFirstSearch(UniformFoodSearchProblem(gameState, self.index))
        # return aStarSearch(problem)

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        "*** YOUR CODE HERE ***"
        if self.dead:
            return Directions.STOP
        elif self.curActionIndex + 1 >= len(self.nextActions):
            self.nextActions = list((self.findPathToAllDot(state)))
            if len(self.nextActions) is 0:
                self.dead=True
                return Directions.STOP
            else:
                self.curActionIndex = 0
                return self.nextActions[self.curActionIndex]
        else:
            self.curActionIndex += 1
            return self.nextActions[self.curActionIndex]

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE"
        MyAgent.num_pacmen = MyAgent.num_pacmen + 1
        self.curActionIndex = 0
        self.nextActions = []
        self.foodNum = 0
        self.dead = False
        # raise NotImplementedError()


"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""
"""
heuristic functions start
"""
def cloestDotHeuristic(state, problem):
    if len(problem.foodPositionsByAgent) == 0:
        return 0
    return util.manhattanDistance(problem.foodPositionsByAgent[0], state)

"""
Search methods start
"""


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    preSuccessor = {}  # Store backpointer to PreSuccessor, Key is CurrentState, Value is its PreSuccessor
    duplicate = []  # Store information regarding duplicate state
    ans = util.Stack()
    ans.push([problem.getStartState(), 'ORIGIN', 0])
    while not ans.isEmpty():
        state = ans.pop()
        duplicate.append(state[0])
        if problem.isGoalState(state[0]):
            finalAns = list()
            while state is not None:
                if state[1] is not "ORIGIN":
                    finalAns.append(state[1])
                state = preSuccessor.get(tuple(state))
            finalAns.reverse()
            # print("DFS: finalAns.reverse() :", finalAns)
            return finalAns
        else:
            for nextState in problem.getSuccessors(state[0]):
                if nextState[0] not in duplicate:
                    ans.push(nextState)
                    preSuccessor[tuple(nextState)] = state
    return []
    "*** YOUR CODE COMPLETE ***"
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    preSuccessor = {}
    duplicate = []
    ans = util.Queue()
    ans.push([problem.getStartState(), 'ORIGIN', 0])
    duplicate.append(problem.getStartState())
    while not ans.isEmpty():
        state = ans.pop()
        if problem.isGoalState(state[0]):
            finalAns = list()
            while state is not None:
                if state[1] is not "ORIGIN":
                    finalAns.append(state[1])
                state = preSuccessor.get(tuple(state))
            finalAns.reverse()
            return finalAns
        else:
            for nextState in problem.getSuccessors(state[0]):
                if nextState[0] not in duplicate:
                    ans.push(nextState)
                    duplicate.append(nextState[0])
                    preSuccessor[tuple(nextState)] = state
    return []
    "*** YOUR CODE FINISH ***"
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    preSuccessor = {}  # Store backpointer to PreSuccessor, Key is CurrentState, Value is its PreSuccessor
    duplicate = []  # Store information regarding duplicate state
    minCost = {}  # Store Cumulative Cost of each node
    ans = util.PriorityQueue()
    ans.push([problem.getStartState(), 'ORIGIN', 0], 0)
    duplicate.append(problem.getStartState())
    minCost[problem.getStartState()] = 0;
    while not ans.isEmpty():
        state = ans.pop()
        if problem.isGoalState(state[0]):
            finalAns = list()
            while state is not None:
                if state[1] is not "ORIGIN":
                    finalAns.append(state[1])
                state = preSuccessor.get(tuple(state))
            finalAns.reverse()
            return finalAns
        else:
            for nextState in problem.getSuccessors(state[0]):
                if nextState[0] not in duplicate or problem.isGoalState(nextState[0]):
                    minCost[nextState[0]] = nextState[2] + minCost[state[0]]
                    ans.update(nextState, minCost[nextState[0]])
                    duplicate.append(nextState[0])
                    preSuccessor[tuple(nextState)] = state
    return []
    "*** YOUR CODE COMPLETE ***"
    util.raiseNotDefined()


def aStarSearch(problem, heuristic=cloestDotHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    preSuccessor = {}  # Store backpointer to PreSuccessor, Key is CurrentState, Value is its PreSuccessor
    duplicate = []  # Store information regarding duplicate state
    minCost = {}  # Store Cumulative Cost of each node
    ans = util.PriorityQueue()
    ans.push([problem.getStartState(), 'ORIGIN', 0], 0)
    minCost[problem.getStartState()] = 0;
    while not ans.isEmpty():
        state = ans.pop()
        if problem.isGoalState(state[0]):
            finalAns = list()
            while state is not None:
                if state[1] is not "ORIGIN":
                    finalAns.append(state[1])
                state = preSuccessor.get(tuple(state))
            finalAns.reverse()
            return finalAns
        else:
            if state[0] not in duplicate:
                duplicate.append(state[0])
                for nextState in problem.getSuccessors(state[0]):
                    if nextState[0] not in duplicate:
                        minCost[nextState[0]] = nextState[2] + minCost[state[0]]
                        ans.update(nextState, minCost[nextState[0]] + heuristic(nextState[0], problem))
                        preSuccessor[tuple(nextState)] = state
    return []
    "*** YOUR CODE COMPLETE ***"
    util.raiseNotDefined()


"""
Search problems Start
"""


class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)

        "*** YOUR CODE HERE ***"
        return breadthFirstSearch(problem)
        "*** YOUR CODE COMPLETE ***"
        util.raiseNotDefined()

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.
    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.
    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.
    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x, y = state
        return self.food[x][y]
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class UniformFoodSearchProblem(PositionSearchProblem):

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

        # ADDED BY Shaohua Yuan#
        self.agentIdex = agentIndex
        self.foodPositions = self.food.asList()
        self.foodPositionsByAgent = []

        self.foodPositionsByAgent.extend(
            self.foodPositions[agentIndex * int(len(self.foodPositions) / MyAgent.num_pacmen):
                               agentIndex * int(len(self.foodPositions) / MyAgent.num_pacmen)
                               + int(len(self.foodPositions) / MyAgent.num_pacmen)])

        self.foodPositionsByAgent.extend(
                self.foodPositions[MyAgent.num_pacmen * int(len(self.foodPositions) / MyAgent.num_pacmen):
                                   MyAgent.num_pacmen * int(len(self.foodPositions) / MyAgent.num_pacmen) +
                                   len(self.foodPositions) % MyAgent.num_pacmen])


    def isGoalState(self, state):
        if len(self.foodPositions) <= MyAgent.num_pacmen:
            return state in self.foodPositions
        elif state in self.foodPositionsByAgent and state not in chasingGoal:
            chasingGoal.append(state)
            return True
        elif state in self.foodPositions \
                and util.manhattanDistance(state, self.startState) <= (1+self.agentIdex)*(1+self.agentIdex)\
                and state not in chasingGoal:
            chasingGoal.append(state)
            return True
        else:
            return False
