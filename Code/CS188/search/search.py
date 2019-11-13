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
    
    # 因为后继节点中的方向是字符串，用这个字典可以把字符串转换成表示方向的常量
    from game import Directions
    D = {
    "South" : Directions.SOUTH,
    "West" : Directions.WEST,
    "North" : Directions.NORTH,
    "East" : Directions.EAST,
    }
    
    def Recursive_DFS(node,problem,solution,closedSet):
        # 测试当前送进来的节点是否满足目标要求，如果是一个可行解，就返回行动方案
        if problem.isGoalState(node):
            return solution
        # 否则，就构造循环遍历这个节点的所有子节点
        else:
            for child,direction,cost in problem.getSuccessors(node):
                # 如果子节点是还没有计算过的节点，就开始继续往下走
                if child not in closedSet:
                    # 在行动方案中增加当前子节点的执行动作
                    solution.append(D[direction])
                    # 然后把这个子节点增加到计算过的节点集合中
                    closedSet.add(child)
                    # 调用递归函数继续从当前子节点往下计算
                    result = Recursive_DFS(child,problem,solution,closedSet)
                    # 判定一下计算结果
                    if result!=False:
                        # 如果找到了可行路线，则把行动方案返回出去吧
                        # 附带一句：return有停止当前函数继续运行的效果哟！
                        return solution
                    else:
                        # 如果从这个节点往下没有可行路线，就要撤销刚才的执行动作
                        solution.pop()
            # 这个else和for对应，表示所有的子节点都遍历过了，没找到合适的行动方案，查找失败
            else:
                return False
    
    solution = []
    # 因为我们的数据结构是图，不是树，所以要构造一个集合用于判定某个节点是否已经算过了，否则会死循环
    closedSet = set()
    # 一开始把初始位置加入上述集合中，意味着Pacman不能经过这个节点了
    closedSet.add(problem.getStartState())
    # 调用递归函数进行问题求解，多一个参数就是上面的集合
    solution = Recursive_DFS(problem.getStartState(),problem,solution,closedSet)
    return solution

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # 因为后继节点中的方向是字符串，用这个字典可以把字符串转换成表示方向的常量
    from game import Directions
    D = {
    "South" : Directions.SOUTH,
    "West" : Directions.WEST,
    "North" : Directions.NORTH,
    "East" : Directions.EAST,
    }
    
    # 初始化相关参数，算法描述中的Path-Cost感觉没啥用呀-_-!
    node, pathCost = problem.getStartState(), 0
    # 特别注意，与深度优先不同，广度优先需要为每一个节点记录行动方案，所以空间成本好大呀！
    solution = {node:[]}
    # 测试当前送进来的节点是否满足目标要求，如果已经是一个可行解，就返回行动方案
    if problem.isGoalState(node):
        return solution[node]
    # 如果上面的测试不成立，则建立一个队列frontier，并将节点塞进队列中
    frontier = util.Queue()
    frontier.push(node)
    explored = set()
    # while True表示反复执行循环体，但是，循环体中的return语句可以打破循环并返回结果
    while True:
        # 如果frontier队列中已经没有节点了，表示此题无解
        if frontier.isEmpty():
            return None
        # 从frontier队列中弹出一个节点node，并将该节点加入explored集合中
        node = frontier.pop()
        explored.add(node)
        # 遍历节点node的子节点child，尝试找到可行解
        for child,direction,cost in problem.getSuccessors(node):
            # 如果该child已经访问过了，就跳过吧
            if child not in explored:
                # 先把父节点node的行动方案复制一份，再把当前子节点的动作加到方案里面
                solution[child] = solution[node].copy()
                solution[child].append(D[direction])
                # 如果该子节点满足目标要求，就返回这个子节点对应的行动方案
                if problem.isGoalState(child):
                    return solution[child]
                # 如果该子节点不满足目标要求，就把它塞到frontier里面，过会儿继续展开
                frontier.push(child)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    # 后继节点中的方向是以字符串形式表示的，用这个字典可以把字符串转换成表示方向的常量
    from game import Directions
    D = {
    "South" : Directions.SOUTH,
    "West" : Directions.WEST,
    "North" : Directions.NORTH,
    "East" : Directions.EAST,
    }
    
    # 初始化相关参数
    node = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push(node, 0)
    explored = set()
    solution = {node:[]}
    # 为了记录每个节点的行动代价，只能再定义一个字典来存放
    pathcost = {node:0}
    # while True表示反复执行循环体，但是，循环体中的return语句可以打破循环并返回结果
    while True:
        # 如果frontier队列中已经没有节点了，表示此题无解
        if frontier.isEmpty():
            return None
        # 从frontier队列中弹出一个节点node
        node = frontier.pop()
        # 测试当前节点是否满足目标要求，如果是一个可行解，就返回行动方案
        if problem.isGoalState(node):
            return solution[node]
        # 将该节点加入explored集合中
        explored.add(node)
        # 遍历节点node的子节点child，尝试找到可行解
        for child,direction,cost in problem.getSuccessors(node):
            # 根据该子节点是否访问过，更新frontier队列
            if child not in explored:
                frontier.push(child,cost)
                # 把当前子节点的动作加到行动方案里面，并记录其行动代价
                solution[child] = solution[node].copy()
                solution[child].append(D[direction])
                pathcost[child] = pathcost[node] + cost
            elif pathcost[child] > pathcost[node] + cost:
                # 如果已经记录的行动代价比当前路径的行动代价要高，则替换原来的方案
                frontier.update(child,cost)
                solution[child] = solution[node].copy()
                solution[child].append(D[direction])
                pathcost[child] = pathcost[node] + cost

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # 后继节点中的方向是以字符串形式表示的，用这个字典可以把字符串转换成表示方向的常量
    from game import Directions
    D = {
    "South" : Directions.SOUTH,
    "West" : Directions.WEST,
    "North" : Directions.NORTH,
    "East" : Directions.EAST,
    }
    
    # 初始化相关参数
    node = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push(node, 0)
    explored = set()
    solution = {node:[]}
    # 为了记录每个节点的行动代价，只能再定义一个字典来存放
    pathcost = {node:0}
    # while True表示反复执行循环体，但是，循环体中的return语句可以打破循环并返回结果
    while True:
        # 如果frontier队列中已经没有节点了，表示此题无解
        if frontier.isEmpty():
            return None
        # 从frontier队列中弹出一个节点node
        node = frontier.pop()
        # 测试当前节点是否满足目标要求，如果是一个可行解，就返回行动方案
        if problem.isGoalState(node):
            return solution[node]
        # 将该节点加入explored集合中
        explored.add(node)
        # 遍历节点node的子节点child，尝试找到可行解
        for child,direction,cost in problem.getSuccessors(node):
            # 根据该子节点是否访问过，更新frontier队列
            if child not in explored:
                # 和之前的一致代价搜索不一样的是，此处需要把启发值算进去
                frontier.push(child,cost + heuristic(node, problem))
                # 把当前子节点的动作加到行动方案里面，并记录其行动代价
                solution[child] = solution[node].copy()
                solution[child].append(D[direction])
                pathcost[child] = pathcost[node] + cost
            elif pathcost[child] > pathcost[node] + cost:
                # 如果已经记录的行动代价比当前路径的行动代价要高，则替换原来的方案
                # 同样的道理，在更新froniter队列的时候，也要将启发值算进去
                frontier.update(child,cost + heuristic(node, problem))
                solution[child] = solution[node].copy()
                solution[child].append(D[direction])
                pathcost[child] = pathcost[node] + cost

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
