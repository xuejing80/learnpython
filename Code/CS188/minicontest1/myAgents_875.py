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
from searchProblems import PositionSearchProblem

import util
import time
import search
import random

"""
IMPORTANT
`agent` defines which agent yopython pacman.py --pacman myAgents.pyu will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
#ClosestDotAgent MyAgent
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

food_chasing = util.Queue()
index_chasing = util.Queue()
retarget_list = []
time = 0
agent_position = []

class MyAgent(Agent):
    """
    Implementation of your agent.
    """
    def manhattan_dist(self, position1, position2):
        """
        This gives the manhatten distance between position1 and position2.
        """
        return abs(position1[0]-position2[0])+abs(position1[1]-position2[1])
    def take1(self, elem):
                return elem[1]
    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        global agent_position
        global retarget_list
        agent_position[self.index] = state.getPacmanPosition(self.index)

        if retarget_list[self.index] == 0:
            while self.action_pool.isEmpty() == False:
                trashcan = self.action_pool.pop()
        
        if self.action_pool.isEmpty():
            #print("1")
            food = state.getFood().asList()
            self.food = food
            global food_chasing
            global index_chasing
            startPosition = state.getPacmanPosition(self.index)

            for i in range(len(food_chasing.list)):
                j = food_chasing.pop()
                s = index_chasing.pop()
                if j != self.goal:
                    food_chasing.push(j)
                    index_chasing.push(s)

            #print("startPosition",startPosition)
            ''' get a list of nearby food in food_2(index-in-food, manhanttan-dist-between-current-and-food)
            '''

            food_2 = food[:]
            for i in range(len(food)):
                food_2[i] = (i, self.manhattan_dist(food[i], startPosition))

            food_2.sort(key = self.take1)
            #print(food_2)
            #print([food[x[0]] for x in food_2])
            ''' select best goal for this step
            '''

            choice_len = len(food)
            if choice_len >5:
                choice_len = 5

            global time
            time += 1
            flag = True
            for l in range(choice_len):
                i=food_2[l]
                g = food[i[0]]
                dist = i[1]
                t = False
                for j in range(len(food_chasing.list)):
                    if (self.manhattan_dist(food_chasing.list[j], g) <= 3):
                        flag_2 = True
                        if (dist+2>=self.manhattan_dist(g, agent_position[index_chasing.list[j]])):
                        #print('inside the loop',self.index, g, food_chasing.list[j], dist, index_chasing.list[j][1])
                        #index_chasing.list[j][1] <= dist+2
                            t = True
                            flag_2 = False
                            break
                        retarget_list[index_chasing.list[j]] = 0
                if t == True:
                    continue
                flag = False
                break
            if flag == False:
                self.goal = g
            else:
                self.goal = food[food_2[0][0]]   
                dist = food_2[0][1]


            #print(self.index, self.goal,dist)
            food_chasing.push(self.goal)
            index_chasing.push(self.index)
            retarget_list[self.index] = 1
            #print(food_chasing.list, index_chasing.list)

            problem = TheFoodSearchProblem(state, self.index, self.goal)
            action_list = search.aStarSearch(problem, heuristic=self.manhattanHeuristic)
            #if (len(action_list) < 100):
            action_len = len(action_list)
            #else:
            #    action_len = 100
            for j in range(action_len):
                i = action_list[j]
                self.action_pool.push(i)
            #print(action_list, self.index)

        action = self.action_pool.pop()
        return action


        #raise NotImplementedError()

    def manhattanHeuristic(self, position, problem, info={}):
        "The Manhattan distance heuristic for a PositionSearchProblem"
        xy1 = position
        xy2 = self.goal
        dist =  abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
        food = self.food
        if xy2 in food:
            dist += 10
        return dist
    def euclideanHeuristic(self, position, problem, info={}):
        "The Euclidean distance heuristic for a PositionSearchProblem"
        xy1 = position
        xy2 = self.goal
        dist = ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5 * (-0.4)
        food = self.food
        if xy2 in food:
            dist += 10
        return dist
    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        #startPosition = state.getPacmanPosition(self.index)
        self.action_pool = util.Queue()
        self.goal = (0,0)
        global agent_position
        agent_position.append((0,0))
        global retarget_list
        retarget_list.append(0)
        #for i in range(10):
        #    x = util.Queue()
        #    self.action_pool.append(x[:])
        "*** YOUR CODE HERE"

        #raise NotImplementedError()

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
        return search.uniformCostSearch(problem)

        "*** YOUR CODE HERE ***"
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
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        foods = self.food.asList()
        if state in foods:
            return True
        else:
            return False
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class TheFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to a specific food.
    """
    def __init__(self, gameState, agentIndex, goal):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()
        self.goal = goal
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        #foods = self.food.asList()
        if x == self.goal[0] and y == self.goal[1]:
            return True
        else:
            return False
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
