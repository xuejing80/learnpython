# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        # print("Selected action:",legalMoves[chosenIndex],"\n")
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # 求出最近的鬼怪，计算危险值
        nearestGhost = min([manhattanDistance(newPos,ghostState.configuration.pos) for ghostState in newGhostStates])
        # 为了让吃豆人不要总是躲着鬼怪，我们只考虑距离2步以内的鬼怪造成的影响
        # 为什么取-20？因为接下来我会把豆豆的启发值设置在10以内，两者相加一定为负数，这样就可以抵消豆豆对吃豆人的诱惑，^_^
        # 为什么不是-10？因为如果下一步直接吃到豆豆，那个successorGameState.getScore()会算上吃到豆豆的10分
        dangerScore = -20 if nearestGhost <2 else 0

        # 如果豆豆还没有吃光，用最近的豆豆的坐标计算出一个启发值，优先考虑吃掉最近的豆豆
        # 这个程序从字面上看，是用曼哈顿距离计算启发值，所以如果吃豆人和豆豆之间有墙的话……吃豆人就卡在墙后面了
        # 但是，又因为有鬼怪的存在，它会驱动吃豆人离开卡死在墙后面的状态，勉强算是通过测试了
        if len(newFood.asList())>0:
            nearestFood = (min([manhattanDistance(newPos, food) for food in newFood.asList()]))
            # 为什么启发值是“9/距离”呢？因为按照我的设计，这个值不能为负数，负数用来表示下一步可能遇到鬼怪
            # 同时，因为吃到隔壁的豆豆得9分(移动需要扣1分)，且距离越远启发值越小，按照这些规则，我就设计了这样一个启发函数
            # 如果下一个豆豆就在隔壁，距离为1，那么启发值为9，且距离放在分母，其值越大，启发值就越小，OK！
            foodHeuristic = 9/nearestFood
        else:
            foodHeuristic = 0
        
        # 把计算好的各种值加起来，并返回
        # print("Action:",action,"Score:",successorGameState.getScore(),"Danger:",dangerScore,"Food:",foodHeuristic,"Total:",successorGameState.getScore()+foodHeuristic+dangerScore)
        return successorGameState.getScore()+foodHeuristic+dangerScore

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maxVal = -float('inf')
        bestAction = None
        # 从吃豆人最初的位置，遍历所有可行的下一步
        for action in gameState.getLegalActions(0):
            # 求出接下来的所有MIN值，并和maxVal比较，求出MAX值
            value = self._getMin(gameState.generateSuccessor(0, action))
            # 如果当前的value比maxVal还要大，更新maxVal值，并记下bestAction
            if value is not None and value > maxVal:
                maxVal = value
                bestAction = action
        # 最后返回最佳选择
        return bestAction
        
    def _getMax(self, gameState, depth = 0, agentIndex = 0):
        # 获得吃豆人下一步所有合法的操作
        legalActions = gameState.getLegalActions(agentIndex)
        # 如果展开深度达到限制或者没有可行的下一步，则终止展开，并返回评价值
        if depth == self.depth or len(legalActions)==0:
            return self.evaluationFunction(gameState)
        # 否则就进行继续向下展开
        maxVal = -float('inf')
        # 对吃豆人下一步可行的操作进行遍历
        for action in legalActions:
            # 注意观察agentIndex参数位置的值为1，表示从第一个鬼怪开始MIN遍历
            value = self._getMin(gameState.generateSuccessor(agentIndex, action), depth, 1)
            if value is not None and value > maxVal:
                maxVal = value
        return maxVal
    
    def _getMin(self, gameState, depth = 0, agentIndex = 1):
        # 获得鬼怪们的下一步合法操作，注意：是一群鬼怪，可能不止一只，所以MIN函数会反复调用
        legalActions = gameState.getLegalActions(agentIndex)
        # 同样，如果展开深度达到限制或者没有可行的下一步，则终止展开，并返回评价值
        if depth == self.depth or len(legalActions)==0:
            return self.evaluationFunction(gameState)
        # 否则，继续往下展开可行的行动
        minVal = float('inf')
        # 对当前鬼怪的可行下一步进行遍历，其中要递归调用以计算其他鬼怪的行动
        for action in legalActions:
            # 如果当前已经是最后一只鬼怪，那么下一轮就该是计算吃豆人的行为了，即调用MAX函数
            if agentIndex == gameState.getNumAgents() - 1:
                # 注意观察agentIndex参数位置的值为0，表示吃豆人
                value = self._getMax(gameState.generateSuccessor(agentIndex, action), depth+1, 0)
            else:
                # 注意观察agentIndex参数位置的值为agentIndex+1，表示下一个鬼怪
                value = self._getMin(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1)
            if value is not None and value < minVal:
                minVal = value
        return minVal

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # 从根节点开始展开，求MAX值，注意：返回值中下标为1的项才是行动内容
        return self._getMax(gameState)[1]
        
    def _getMax(self, gameState, depth = 0, agentIndex = 0, alpha = -float('inf'),
               beta = float('inf')):
        # 如果深度超限，或者无法继续展开，则返回当前状态的评价值
        legalActions = gameState.getLegalActions(agentIndex)
        if depth == self.depth or len(legalActions)==0:
            return self.evaluationFunction(gameState), None
        # 否则，就继续往下遍历吃豆人可能的下一步
        maxVal = None
        bestAction = None
        for action in legalActions:
            # 考虑只有一个吃豆人的情况，直接求其MIN分支的评价值，agentIndex从1开始遍历所有鬼怪
            value = self._getMin(gameState.generateSuccessor(agentIndex, action), depth, 1, alpha, beta)[0]
            if value is not None and (maxVal == None or value > maxVal):
                maxVal = value
                bestAction = action
            # 按照α-β剪枝算法，如果v>β，则直接返回v
            if value is not None and value > beta:
                return value, action
            # 按照α-β剪枝算法，这里还需要更新α的值
            if value is not None and value > alpha:
                alpha = value
        return maxVal, bestAction
    
    def _getMin(self, gameState, depth = 0, agentIndex = 0, alpha = -float('inf'),
               beta = float('inf')):
        # 如果深度超限，或者无法继续展开，则返回当前状态的评价值
        legalActions = gameState.getLegalActions(agentIndex)
        if depth == self.depth or len(legalActions)==0:
            return self.evaluationFunction(gameState), None
        # 否则，就继续往下遍历当前鬼怪可能的下一步
        minVal = None
        bestAction = None
        for action in legalActions:
            # 如果当前是最后一个鬼怪，那么下一轮就该是计算吃豆人的行为了，即调用MAX函数
            if agentIndex >= gameState.getNumAgents() - 1:
                # 注意观察参数，除了agentIndex参数位置的值为0表示吃豆人之外，还多了α和β的值
                value = self._getMax(gameState.generateSuccessor(agentIndex, action), depth+1, 0, alpha, beta)[0]
            else:
                # 如果不是最后一个鬼怪，则继续遍历下一个鬼怪，即agentIndex+1
                value = self._getMin(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1, alpha, beta)[0]
            if value is not None and (minVal == None or value < minVal):
                minVal = value
                bestAction = action
            # 按照α-β剪枝算法，如果v<α，则直接返回v
            if value is not None and value < alpha:
                return value, action
            # 按照α-β剪枝算法，这里还需要更新β的值
            if value is not None and value < beta:
                beta = value
        return minVal, bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self._getMax(gameState)
        
    def _getMax(self, gameState, depth = 0, agentIndex = 0):
        # 获得吃豆人所有合法的下一步行动
        legalActions = gameState.getLegalActions(agentIndex)
        # 如果深度超限或者没有可行的行动，则返回评价函数值
        if depth == self.depth or len(legalActions)==0:
            return self.evaluationFunction(gameState)
        # 否则初始化，并对合法的下一步进行轮询
        maxVal = None
        bestAction = None
        for action in legalActions:
            # 从第一个鬼怪开始，进行Expectimax操作
            value = self._getExpectation(gameState.generateSuccessor(agentIndex, action), depth, 1)
            if value is not None and (maxVal == None or value > maxVal):
                maxVal = value
                bestAction = action
        # 下面的程序，是对根节点展开的另外一种表达方式
        if depth is 0 and agentIndex is 0:
            return bestAction
        else:
            return maxVal
    
    def _getExpectation(self, gameState, depth = 0, agentIndex = 0):
        legalActions = gameState.getLegalActions(agentIndex)
        # 如果搜索深度超限，或者没有下一步了，则返回评价函数值
        if depth == self.depth or len(legalActions)==0:
            return self.evaluationFunction(gameState) 
        # 初始化效用值总计
        totalUtil = 0
        numActions = len(legalActions)
        # 轮询当前鬼怪所有可行的下一步
        for action in legalActions:
            # 同样，如果是最后一个鬼怪，那么接下来要去算吃豆人的MAX值，并计入效用总计
            if agentIndex >= gameState.getNumAgents() - 1:
                totalUtil += self._getMax(gameState.generateSuccessor(agentIndex, action), depth+1, 0)
            # 否则，挨个遍历各个鬼怪，计算Expectation值，并计入效用总计
            else:
                totalUtil += self._getExpectation(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1)
        # 最后需要把所有可能的下一步的效用值求平均，并返回
        return totalUtil / float(numActions)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # 初始化可能需要的信息
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    # 根据鬼怪的状态计算危险值
    if len(GhostStates)>0:
        nearestGhost = min([manhattanDistance(Pos,ghostState.configuration.pos) for ghostState in GhostStates])
        if len(Food.asList()) > 0:
            if nearestGhost <2:
                dangerScore = -10/float(nearestGhost+1)
            else:
                dangerScore=0
        else:
            dangerScore = 100000 / float(nearestGhost**2)
    else:
        dangerScore = 0
    # 根据最近的食物计算启发值
    if len(Food.asList()) > 0:
        nearestFood = (min([manhattanDistance(Pos, food) for food in Food.asList()]))
        nearFoodHeuristic = 1/float(nearestFood**2)
    else:
        nearFoodHeuristic = 0
    # 这个值是告诉吃豆人尽量让鬼怪保持可以被吃掉的状态
    totalScaredTimes = sum(ScaredTimes)
    # 最后将上述三个值加到下一个状态的得分，构成总计值，进行返回
    return currentGameState.getScore()*10+nearFoodHeuristic*2+dangerScore+totalScaredTimes/10

# Abbreviation
better = betterEvaluationFunction
