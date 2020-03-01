# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # 第三步，参考第二步的程序，进行多轮迭代
        for i in range(self.iterations):
            states = self.mdp.getStates()
            # 关于util.Counter，建议去代码里面看一下说明，其实就是一个加强版的字典
            temp_counter = util.Counter()
            # 在每一次的迭代中，需要把MDP中每一个状态都要考虑到
            for state in states:
                max_val = float("-inf")
                for action in self.mdp.getPossibleActions(state):
                    q_value = self.computeQValueFromValues(state, action)
                    if q_value > max_val:
                        max_val = q_value
                    temp_counter[state] = max_val
            # 最后需要把计算好的数据更新到MDP里面去
            self.values = temp_counter

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # 第一步计算Q值，因为Q值中包含概率的概念，所以需要遍历每一个action
        action_prob_pairs = self.mdp.getTransitionStatesAndProbs(state, action)
        total = 0
        for next_state, prob in action_prob_pairs:
            # 用预先定义好的函数求Reward
            reward = self.mdp.getReward(state, action, next_state)
            # 使用Q值的公式，算出总值
            total += prob * (reward + self.discount * self.values[next_state])
        return total

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # 第二步，计算V值，其实就是求出所有Q值中最大的
        best_action = None
        max_val = float("-inf")
        # 遍历从当前状态可以衍生出的所有action的Q值，并求出最大的作为V值
        for action in self.mdp.getPossibleActions(state):
          q_value = self.computeQValueFromValues(state, action)
          if q_value > max_val:
            max_val = q_value
            best_action = action
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        # 为了在一次迭代中只更新一个state，我们需要计算本次更新的state的序号
        num_states = len(states)
        for i in range(self.iterations):
            # 求这个序号的方法，就是求迭代次数除以state的总数的余数
            state = states[i % num_states]
            # 题目中要求不更新Terminal状态
            if not self.mdp.isTerminal(state):
                # 剩下的内容和前面的更新过程一样
                max_val = float("-inf")
                for action in self.mdp.getPossibleActions(state):
                    q_value = self.computeQValueFromValues(state, action)
                    if q_value > max_val:
                        max_val = q_value
                # 最后需要把计算好的数据更新到state里面去
                self.values[state] = max_val

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # Compute predecessors of all states.
        predecessors = {}
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        if nextState in predecessors:
                            predecessors[nextState].add(state)
                        else:
                            predecessors[nextState] = {state}
        # Initialize an empty priority queue.
        pq = util.PriorityQueue()
        # For each non-terminal state s, do:
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                # Find the absolute value of the difference between the current value of s in self.values
                # and the highest Q-value across all possible actions from s; call this number diff. 
                values = []
                for action in self.mdp.getPossibleActions(state):
                    q_value = self.computeQValueFromValues(state, action)
                    values.append(q_value)
                diff = abs(max(values) - self.values[state])
                # Push s into the priority queue with priority -diff. 
                pq.update(state, - diff)

        # For iteration in 0, 1, 2, ..., self.iterations - 1, do:
        for i in range(self.iterations):
            # If the priority queue is empty, then terminate.
            if pq.isEmpty():
                break
            # Pop a state s off the priority queue.
            temp_state = pq.pop()
            # Update the value of s (if it is not a terminal state) in self.values.
            if not self.mdp.isTerminal(temp_state):
                values = []
                for action in self.mdp.getPossibleActions(temp_state):
                    q_value = self.computeQValueFromValues(temp_state, action)
                    values.append(q_value)
                self.values[temp_state] = max(values)
            # For each predecessor p of s, do:
            for p in predecessors[temp_state]:
                # Find the absolute value of the difference between the current value of p in self.values
                # and the highest Q-value across all possible actions from p; call this number diff. 
                if not self.mdp.isTerminal(p):
                    values = []
                    for action in self.mdp.getPossibleActions(p):
                        q_value = self.computeQValueFromValues(p, action)
                        values.append(q_value)
                    diff = abs(max(values) - self.values[p])
                    # If diff > theta, push p into the priority queue with priority -diff, as long as it
                    # does not already exist in the priority queue with equal or lower priority. 
                    if diff > self.theta:
                        pq.update(p, -diff)
