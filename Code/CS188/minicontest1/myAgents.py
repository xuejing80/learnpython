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
    # 为了能够在多个吃豆人之间共享信息，必须创建类变量
    # pacmanAmount表示一共有多少个吃豆人
    pacmanAmount = 0
    # chasingGoal表示哪些豆豆已经被设定为目标，其他的吃豆人可以不用管了
    chasingGoal = []
    
    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        # 如果通过之前的计算，确认该豆豆的任务都已经完成了，为了节约计算资源，直接停止该豆豆
        if self.isFinished:
            return Directions.STOP
        else:
            # 如果行动序列中已经没有接下来的步骤，那么就要生成新的行动序列
            if len(self.actions) == 0:
                actions = search.bfs(CoopFoodSearchProblem(state, self.index))
                self.actions = actions
                # print(actions)
            # 只要行动序列不为空，就把第一个行动返回出去，并更新行动序列
            if len(self.actions) > 0:
                nextAction = self.actions[0]
                del self.actions[0]
                return nextAction
            # 如果行动序列中已经没有后续步骤了，那么就认为该豆豆的任务都完成了
            else:
                self.isFinished = True
                return Directions.STOP

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE"
        # 初始化一些吃豆人的信息
        # isFinished表示吃豆人是不是已经完成了自己的任务，初始为False
        self.isFinished = False
        # actions表示目前正在执行的行动序列，初始为一个空列表
        self.actions = []
        # 吃豆人总数+1
        MyAgent.pacmanAmount += 1

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

        "*** YOUR CODE HERE ***"
        # 直接调用我们现成的BFS算法进行问题求解，找最近的豆豆
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
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"
        # self.food是一个用0和1表示的关于豆豆的矩阵，0和1可以直接被当做逻辑值返回
        return self.food[x][y]

# 为了描述这个合作吃豆豆的问题，我重新定义了一个新的问题类
class CoopFoodSearchProblem(PositionSearchProblem):
    '''
    版权声明：这个类是Shaohua Yuan原创的，Jing Xue进行了注释和改进
    '''
    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

        # 为了提升每个吃豆人的工作效率，我们把所有的豆豆平均分给每个吃豆人
        self.agentIndex = agentIndex
        self.foodAll = self.food.asList()
        # 这个变量用于存放分给每个吃豆人的豆豆的总数
        avgFood = len(self.foodAll) // MyAgent.pacmanAmount + 1
        # 接下来用分片操作完成平均分配
        self.foodByAgent = self.foodAll[agentIndex*avgFood : (agentIndex+1)*avgFood]
        
    def isGoalState(self, state):
        # 这个分支用于解决吃到最后，吃豆人比豆豆多的情况
        if len(self.foodAll) <= MyAgent.pacmanAmount:
            return state in self.foodAll
        # 接着我们判断当前位置如果有豆豆的情况
        if state in self.foodAll:
            # 如果豆豆在自己的目标任务中，且还没有被别的吃豆人设置为目标
            if (state in self.foodByAgent) and (state not in MyAgent.chasingGoal):
                MyAgent.chasingGoal.append(state)
                return True
            # 如果豆豆离自己非常近，并且没有被别的吃豆人设定为目标的话，执行此分支
            elif (util.manhattanDistance(state, self.startState) <= (1+self.agentIndex)*(1+self.agentIndex)) \
              and (state not in MyAgent.chasingGoal):
                MyAgent.chasingGoal.append(state)
                return True
            # 最后的分支用来处理一些不知道的情况，以找到自己任务中的豆豆作为目标
            else:
                return state in self.foodByAgent
        else:
            return False
