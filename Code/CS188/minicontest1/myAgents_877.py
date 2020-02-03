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

from game import Agent
from game import Directions
from searchProblems import PositionSearchProblem

import util
import time
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""


def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]


class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def findPathToClosestNoTargetedDot(self, gameState):
        problem = AnyNotTargetdFoodSearchProblem(gameState, self.index)
        actions = search.bfs(problem)
        return problem.lastTargetFood, actions

    def findPathToClosestDot(self, gameState):
        problem = AnyFoodSearchProblem(gameState, self.index)
        actions = search.bfs(problem)
        return problem.lastTargetFood, actions

    def isFood(self, gameState, targetFood):
        x, y = targetFood
        return gameState.getFood()[x][y]

    def getAction(self, gameState):
        """
        Returns the next action the agent will take
        """

        if self.curTargetDot == None or not self.isFood(gameState, self.curTargetDot):
            self.curTargetDot, self.plannedActionsToCurTargetDot = self.findPathToClosestNoTargetedDot(gameState)
            self.curActionIndex = 0

        if self.curTargetDot == None:
            self.curTargetDot, self.plannedActionsToCurTargetDot = self.findPathToClosestDot(gameState)
            self.curActionIndex = 0

        i = self.curActionIndex
        self.curActionIndex += 1
        if i < len(self.plannedActionsToCurTargetDot):
            return self.plannedActionsToCurTargetDot[i]
        else:
            return Directions.STOP

    agents = {}
    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        MyAgent.agents[self.index] = self

        self.curTargetDot = None
        self.plannedActionsToCurTargetDot = []
        self.curActionIndex = 0


class AnyNotTargetdFoodSearchProblem(PositionSearchProblem):

    def __init__(self, gameState, agentIndex):
        self.gameState = gameState
        self.food = gameState.getFood()
        self.walls = gameState.getWalls()
        self.agentIndex = agentIndex
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self.lastTargetFood = None

        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        x, y = state

        for i in range(self.agentIndex):
            agent = MyAgent.agents[i]
            if agent.curTargetDot == state:
                return False

        isFood = self.food[x][y]
        if isFood:
            self.lastTargetFood = state

        return isFood


"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
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

        return search.bfs(problem)

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
        self.lastTargetFood = None
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x, y = state
        isFood = self.food[x][y]
        if isFood:
            self.lastTargetFood = state

        return isFood
