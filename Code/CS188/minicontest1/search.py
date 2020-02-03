# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

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
    fringe = util.Stack()
    node = {"state":problem.getStartState(), "path":[], "cost":0}
    fringe.push(node)
    explored = set()
    
    while (not fringe.isEmpty()):
        node = fringe.pop()
        if problem.isGoalState(node["state"]):
            return node["path"]
        else:
            if node["state"] not in explored:
                for nextnode in problem.getSuccessors(node["state"]):
                    if nextnode[0] not in explored:
                        nextnode = {"state":nextnode[0],
                                    "path":node["path"]+[nextnode[1]],
                                    "cost":node["cost"]+nextnode[2]}
                        fringe.push(nextnode)
                explored.add(node["state"])

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    node = {"state":problem.getStartState(), "path":[], "cost":0}
    fringe.push(node)
    explored = set()
    
    while (not fringe.isEmpty()):
        node = fringe.pop()
        if problem.isGoalState(node["state"]):
            return node["path"]
        else:
            if node["state"] not in explored:
                for nextnode in problem.getSuccessors(node["state"]):
                    if nextnode[0] not in explored:
                        nextnode = {"state":nextnode[0],
                                    "path":node["path"]+[nextnode[1]],
                                    "cost":node["cost"]+nextnode[2]}
                        fringe.push(nextnode)
                explored.add(node["state"])
    else:
        return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    node = {"state":problem.getStartState(), "path":[], "cost":0}
    fringe.update(node, node["cost"])
    explored = set()
    
    while (not fringe.isEmpty()):
        node = fringe.pop()
        if problem.isGoalState(node["state"]): 
            return node["path"]
        else:
            if node["state"] not in explored:
                for nextnode in problem.getSuccessors(node["state"]):
                    if nextnode[0] not in explored:
                        nextnode = {"state":nextnode[0],
                                    "path":node["path"]+[nextnode[1]],
                                    "cost":node["cost"]+nextnode[2]}
                        fringe.update(nextnode, nextnode["cost"])
                explored.add(node["state"])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # 初始化搜索状态
    fringe = util.PriorityQueue()
    node = {"state":problem.getStartState(), "path":[], "cost":0}
    fringe.update(node, node["cost"]+heuristic(node["state"], problem))
    explored = set()
    # 构造循环展开搜索树
    while (not fringe.isEmpty()):
        # 获得待判定的叶子节点
        node = fringe.pop()
        # 判断节点是否满足目标要求，如果是一个可行解，就返回行动方案
        if problem.isGoalState(node["state"]):
            return node["path"]
        # 否则，就继续从这个叶子节点往下展开
        else:
            # 先判断一下这个节点是不是已经展开过了，避免重复展开
            if node["state"] not in explored:
                for nextnode in problem.getSuccessors(node["state"]):
                    # 为了适应可能的数据结构为图，必须判定叶子节点是否已经访问过
                    if nextnode[0] not in explored:
                        nextnode = {"state":nextnode[0],
                                    "path":node["path"]+[nextnode[1]],
                                    "cost":node["cost"]+nextnode[2]}
                        # 如果没有访问过，就将叶子节点的信息更新到添加到待搜索的节点集合中
                        fringe.update(nextnode, nextnode["cost"]+heuristic(nextnode["state"], problem))
                # 最后不要忘记把搜索过的节点添加到访问过的节点集合中
                explored.add(node["state"])

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
