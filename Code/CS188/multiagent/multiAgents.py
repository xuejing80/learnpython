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
        # 通过鬼怪和当前pacman的位置计算危险值
        # 将所有鬼怪离当前的位置全部计算出来
        Ghosts = [manhattanDistance(ghost.configuration.pos, newPos) for ghost in newGhostStates]
        # 求最近的鬼怪的曼哈顿距离，其他的鬼怪可以不计
        nearestGhost = min(Ghosts)
        # 以为吃到豆豆可以+10，设置为-20可以抵消吃掉豆豆的得分和下方的豆豆启发值
        # 为什么小于2，因为大于等于2的鬼怪，不要考虑呀，否则，豆豆就老是躲着鬼怪
        dangousScore = -1000 if nearestGhost<2 else 0

        # 计算最近的豆豆，对自己的影响
        if len(newFood.asList())>0:
            Foods = [manhattanDistance(food, newPos) for food in newFood.asList()]
            # 求最近的豆豆的距离
            nearestFood = min(Foods)
            # 豆豆离我越近，其启发值就必须越大！吃一个豆豆+10，但是还要消耗1点精力移动，所以吃掉隔壁的豆豆的9分
            foodHeuristic = 9/nearestFood
        else:
            foodHeuristic = 0

        # 最后把下一个状态的得分也计入评价值结果
        return successorGameState.getScore() + dangousScore + foodHeuristic

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
        # 一开始肯定是先从吃豆人的行动开始遍历，这样的返回结果表示吃豆人的行动方案
        maxVal = -float('inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            # 求出所有可行的action中，哪一个是最优的
            # 参数中的0表示搜索深度从0开始，1表示下一个agent的Index是1，即第一个鬼怪
            value = self.getMin(gameState.generateSuccessor(0, action),0,1)
            # 通过比较最优值,将对应的action记录下来
            if value>maxVal:
                maxVal = value
                bestAction = action
        # 最后，只需将最优行动返回给吃豆人即可
        return bestAction   

    # getMax主要是计算吃豆人选择最佳的动作
    def getMax(self,gameState,depth=0,agentIndex=0):
        # 如果达到搜索深度，则将当前状态的评价值返回
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        # 如果接下来没有可行的行动，也要终止迭代
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        # 获得吃豆人的所有可行操作，并进行遍历
        maxVal = -float('inf')
        for action in gameState.getLegalActions(agentIndex):
            # 参数中最后的“1”，表示接下来的动作是计算鬼怪的行动影响
            value = self.getMin(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1)
            if value>maxVal:
                maxVal = value
        return maxVal            

    # getMin主要是计算鬼怪选择造成最坏影响的动作
    def getMin(self,gameState,depth=0,agentIndex=1):
        # 如果达到搜索深度，则将当前状态的评价值返回
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        # 如果接下来没有可行的行动，也要终止迭代
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        # 获得当前鬼怪的所有可行操作，并进行遍历
        minVal = float('inf')
        for action in gameState.getLegalActions(agentIndex):
            # 如果你是最后一个鬼怪的agent，那么接下来就要去计算吃豆人的行动，否则就去计算下一个鬼怪的行动
            if agentIndex == gameState.getNumAgents()-1:
                # 参数中最后的“0”，表示接下来的动作是计算吃豆人的行动影响
                value = self.getMax(gameState.generateSuccessor(agentIndex, action),depth+1,0)
            else:
                # 参数中最后的agentIndex(大于1)，表示接下来的动作是计算鬼怪的行动影响
                value = self.getMin(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1)
            if value<minVal:
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
        # 一开始肯定是先从吃豆人的行动开始，所以直接调用getMax函数
        maxVal, bestAction = self.getMax(gameState)
        return bestAction
        # 上述语句的另外一种写法
        return self.getMax(gameState)[1]

    # getMax主要是计算吃豆人选择最佳的动作
    def getMax(self,gameState,depth=0,agentIndex=0,alpha=-float('inf'),beta=float('inf')):
        # 如果达到搜索深度，则将当前状态的评价值返回
        if depth == self.depth:
            return self.evaluationFunction(gameState),None
        # 如果接下来没有可行的行动，也要终止迭代
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState),None
        # 获得吃豆人的所有可行操作，并进行遍历
        maxVal = -float('inf')
        bestAction = None
        for action in gameState.getLegalActions(agentIndex):
            # 参数中最后的“1”，表示接下来的动作是计算鬼怪的行动影响
            value = self.getMin(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1,alpha,beta)[0]
            if value>maxVal:
                maxVal = value
                bestAction = action
            # 如果v>beta,
            if value>beta:
                return value,action
            alpha = value if value>alpha else alpha
        return maxVal,bestAction

    # getMin主要是计算鬼怪选择造成最坏影响的动作
    def getMin(self,gameState,depth=0,agentIndex=1,alpha=-float('inf'),beta=float('inf')):
        # 如果达到搜索深度，则将当前状态的评价值返回
        if depth == self.depth:
            return self.evaluationFunction(gameState),None
        # 如果接下来没有可行的行动，也要终止迭代
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState),None
        # 获得当前鬼怪的所有可行操作，并进行遍历
        minVal = float('inf')
        bestAction = None
        for action in gameState.getLegalActions(agentIndex):
            # 如果你是最后一个鬼怪的agent，那么接下来就要去计算吃豆人的行动，否则就去计算下一个鬼怪的行动
            if agentIndex == gameState.getNumAgents()-1:
                # 参数中最后的“0”，表示接下来的动作是计算吃豆人的行动影响
                value = self.getMax(gameState.generateSuccessor(agentIndex, action),depth+1,0,alpha,beta)[0]
            else:
                # 参数中最后的agentIndex(大于1)，表示接下来的动作是计算鬼怪的行动影响
                value = self.getMin(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1,alpha,beta)[0]
            if value<minVal:
                minVal = value
                bestAction = action
            if value<alpha:
                return value,action
            beta = value if value<beta else beta # 这个条件选择语句和C语言中"exp1?exp2:exp3"一样
        return minVal,bestAction
        

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
        return self.getMax(gameState)[1]
        
    # 与Minimax算法一样，getMax主要是计算吃豆人的最佳行动
    def getMax(self,gameState,depth=0,agentIndex=0):
        # 如果达到搜索深度，则将当前状态的评价值返回
        if depth == self.depth:
            return self.evaluationFunction(gameState),None
        # 如果接下来吃豆人已经没有可行的行动，也要终止迭代
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState),None
        # 获得吃豆人的所有可行操作，并进行遍历
        maxVal = -float('inf')
        bestAction = None
        for action in gameState.getLegalActions(agentIndex):
            # 参数中最后的“1”，表示接下来的动作是计算鬼怪的行动影响
            value = self.getExpect(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1)
            if value>maxVal:
                maxVal = value
                bestAction = action
        return maxVal,bestAction

    # getExpect主要是计算鬼怪选择造成影响的状态的效用值，即各种可能的状态的效用值平均
    def getExpect(self,gameState,depth,agentIndex=1):
        # 如果达到搜索深度，则将当前状态的评价值返回
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        # 如果接下来没有可行的行动，也要终止迭代
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        # 获得当前鬼怪的所有可行操作，并进行遍历,求ExpectValue
        totalUtil = 0
        for action in gameState.getLegalActions(agentIndex):
            # 如果当前是最后一个鬼怪的agent，那么下一次轮到吃豆人
            if agentIndex == gameState.getNumAgents()-1:
                # 参数中最后的“0”，表示接下来的动作是计算吃豆人的行动影响
                value = self.getMax(gameState.generateSuccessor(agentIndex, action),depth+1,0)[0]
                # 因为当前的步骤依然是鬼怪的行动，所以即便下一步是吃豆人的行动，本次计算中依然要求ExpectValue
                totalUtil += value
            else:
                # 参数中最后的agentIndex(大于1)，表示接下来的动作是计算鬼怪的行动影响
                value = self.getExpect(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1)
                totalUtil += value
        # 将totalUtil除以所有可行的动作数，求得平均值，并返回
        return totalUtil/len(gameState.getLegalActions(agentIndex))

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # 获得计算需要的初始信息，包括吃豆人位置、食物、鬼怪以及鬼怪为惊吓状态的剩余时间
    pacmanPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    scaredTime = [ghost.scaredTimer for ghost in ghostStates]
    
    # 先计算最近的食物对吃豆人的影响
    if len(foods)>0:
        Foods = [manhattanDistance(food, pacmanPos) for food in foods]
        # 求最近的豆豆的距离
        nearestFood = min(Foods)
        # 豆豆离我越近，其启发值就必须越大！吃一个豆豆+10，但是还要消耗1点精力移动，所以吃掉隔壁的豆豆得9分
        foodHeuristic = 0
    else:
        foodHeuristic = 0
        
    # 通过鬼怪和当前pacman的位置计算危险值
    if len(ghostStates)>0:
        # 将所有鬼怪离当前的位置全部计算出来
        Ghosts = [manhattanDistance(ghost.configuration.pos, pacmanPos) for ghost in ghostStates]
        # 求最近的鬼怪的曼哈顿距离，其他的鬼怪可以不计
        nearestGhost = min(Ghosts)
        dangousScore = -1000 if nearestGhost<2 else 0

    # 尽量让鬼怪保持惊吓状态，因为这种状态下的鬼怪可以被吃豆人吃掉
    totalScaredTimes = sum(scaredTime)
    
    # 最后把下一个状态的得分也计入评价值结果
    return  currentGameState.getScore() + foodHeuristic + dangousScore + totalScaredTimes

# Abbreviation
better = betterEvaluationFunction
