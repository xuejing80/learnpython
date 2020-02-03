
from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
def createAgents(num_pacmen, agent='MyAgent'):	
	return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
	currentGoals = [set()]
	def getAction(self, state):
		if self.index not in self.action.keys():
			#print(self.index)
			self.action[self.index] = self.findPathToClosestDot(state)
			if  self.action[self.index][0] == ['Stop']:
				return 'Stop'
			self.currentGoals[0].add(self.action[self.index][1])
			
		if self.action[self.index][0] == ['Stop']:
			return 'Stop'
		
		if  len(self.action[self.index][0]) == 0:
			self.currentGoals[0].discard(self.action[self.index][1])
			#print(self.index)
			self.action[self.index] = self.findPathToClosestDot(state)
			if  self.action[self.index][0] == ['Stop']:
				return 'Stop'
			self.currentGoals[0].add(self.action[self.index][1])
			
		if  self.action[self.index][0] == ['Stop']:
			return 'Stop'

		return self.action[self.index][0].pop()

	def initialize(self):
		self.action = {}
		self.currentGoals[0] = set()
		
	
	def findPathToClosestDot(self, gameState):
		if gameState.getNumFood() < len(self.currentGoals[0]):
			return newbreadthFirstSearch(AnyFoodSearchProblem(gameState, self.index))
		return breadthFirstSearch(AnyFoodSearchProblem(gameState, self.index), self.currentGoals[0])
	
	def getGoal(self, agentIndex):
		return self.currentGoals[0]

class AnyFoodSearchProblem(PositionSearchProblem):
	def __init__(self, gameState, agentIndex):
		"Stores information from the gameState.  You don't need to change this."
		self.food = gameState.getFood()
		self.walls = gameState.getWalls()
		self.startState = gameState.getPacmanPosition(agentIndex)
		self.costFn = lambda x: 1
		self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

	def isGoalState(self, state):
		return self.food[state[0]][state[1]]

def breadthFirstSearch(problem, goals):
	visited = {}
	solution = []
	queue = util.Queue()
	route = {}
	flag = False
	counter = 0

	start = problem.getStartState()

	queue.push((start, 'None', 0))
	visited[start] = 'None'
	child = 0
	while not (queue.isEmpty() or flag):
		counter += 1
		vertex = queue.pop()
		visited[vertex[0]] = vertex[1]
		if problem.isGoalState(vertex[0]):
			if vertex[0] not in goals:
				child = vertex[0]
				flag = True
				break
		for i in problem.getSuccessors(vertex[0]):
			if i[0] not in visited.keys() and i[0] not in route.keys():
				route[i[0]] = vertex[0]
				queue.push(i)
		if counter > 600:
			return [['Stop']]
	goal = child
	if child == 0:
		return [['Stop']]

	while (child in route.keys()):
		parent = route[child]
		solution.append(visited[child])
		child = parent
		
	return [solution, goal]

def newbreadthFirstSearch(problem):
	visited = {}
	solution = []
	queue = util.Queue()
	route = {}
	flag = False
	counter = 0

	start = problem.getStartState()

	queue.push((start, 'None', 0))
	visited[start] = 'None'
	child = 0
	while not (queue.isEmpty() or flag):
		counter += 1
		vertex = queue.pop()
		visited[vertex[0]] = vertex[1]
		if problem.isGoalState(vertex[0]):
			child = vertex[0]
			flag = True
			break
		for i in problem.getSuccessors(vertex[0]):
			if i[0] not in visited.keys() and i[0] not in route.keys():
				route[i[0]] = vertex[0]
				queue.push(i)
		if counter > 20:
			return [['Stop']]
	goal = child
	if child == 0:
		return [['Stop']]

	while (child in route.keys()):
		parent = route[child]
		solution.append(visited[child])
		child = parent
		
	return [solution, goal]
