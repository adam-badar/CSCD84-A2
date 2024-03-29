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
from game import Actions, Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
        # check if the len of the food list is less for an index => pacman eats the food
        for i in range(len(legalMoves)):
            if (legalMoves[i] == Directions.STOP):
                continue
            # ensure that the pacman does not end up in a loop (ie it eats the food if available)
            if (gameState.generatePacmanSuccessor(legalMoves[i]).getFood().count() < gameState.getFood().count()):
                #ensure that the pacman does not go to a position where the ghost is (float -inf in scores)
                if (self.evaluationFunction(gameState, legalMoves[i]) != -float('inf')):
                    return legalMoves[i]
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        if (self.euclideanDistance(newPos, newGhostStates[0].getPosition()) < 1):
            return -float('inf')
        if (action == Directions.STOP):
            return -float('inf')
        return -self.closestFood(newPos, newFood)


    def euclideanDistance(self, pos1, pos2):
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5


    def closestFood(self, pos, food):
        if len(food) == 0:
            return 0
        for i in range(len(food)):
            food[i] = self.euclideanDistance(pos, food[i])
        return min(food)


def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        arr = self.Minimax(gameState, 0, 0, None)
        return arr[1]


    def Minimax(self, gameState: GameState, depth, agentIndex, action):
        # Check if terminal state or maximum depth reached
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return [self.evaluationFunction(gameState), action]
        # Only decrement depth if all agents have moved
        if agentIndex == gameState.getNumAgents() - 1:
                depth += 1
        # If agent is max (pacman) since we are tyring to maximize the score (evalutaion f'n)
        if agentIndex == 0:
            actions = gameState.getLegalActions(0)
            v = -float("inf")
            best_act = None
            for action in actions:
                temp = self.Minimax(gameState.generateSuccessor(0, action), depth, 1, action)[0]
                #can't use max() since we need to keep track of the action that led to the max value
                if temp > v:
                    v = temp
                    best_act = action
            return [v, best_act]
        # If agent is min (ghost)
        else:
            actions = gameState.getLegalActions(agentIndex)
            v = float("inf")
            best_act = None
            for action in actions:
                if agentIndex == gameState.getNumAgents() - 1:
                    temp = self.Minimax(gameState.generateSuccessor(agentIndex, action), depth, 0, action)[0]
                else:
                    temp = self.Minimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, action)[0]
                #can't use min() since we need to keep track of the action that led to the min value
                if temp < v:
                    v = temp
                    best_act = action
            return [v, best_act]




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        arr = self.AlphaBeta(gameState, 0, 0, None, -float("inf"), float("inf"))
        return arr[1]


    def AlphaBeta(self, gameState: GameState, depth, agentIndex, action, alpha, beta):
        # Check if terminal state or maximum depth reached
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return [self.evaluationFunction(gameState), action]
        # Only decrement depth if all agents have moved
        if agentIndex == gameState.getNumAgents() - 1:
                depth += 1
        # If agent is max (pacman) since we are tyring to maximize the score (evalutaion f'n)
        if agentIndex == 0:
            actions = gameState.getLegalActions(0)
            v = -float("inf")
            best_act = None
            for action in actions:
                temp = self.AlphaBeta(gameState.generateSuccessor(0, action), depth, 1, action, alpha, beta)[0]
                #can't use max() since we need to keep track of the action that led to the max value
                if temp > v:
                    v = temp
                    best_act = action
                #prune the tree
                if temp > beta:
                    return [v, best_act]
                alpha = max(alpha, v)
            return [v, best_act]
        # If agent is min (ghost)
        else:
            actions = gameState.getLegalActions(agentIndex)
            v = float("inf")
            best_act = None
            for action in actions:
                if agentIndex == gameState.getNumAgents() - 1:
                    temp = self.AlphaBeta(gameState.generateSuccessor(agentIndex, action), depth, 0, action, alpha, beta)[0]
                else:
                    temp = self.AlphaBeta(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, action, alpha, beta)[0]
                #can't use min() since we need to keep track of the action that led to the min value
                if temp < v:
                    v = temp
                    best_act = action
                #prune the tree
                if temp < alpha:
                    return [v, best_act]
                beta = min(beta, v)
            return [v, best_act]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        arr = self.Expectimax(gameState, 0, 0, None)
        return arr[1]


    def Expectimax(self, gameState: GameState, depth, agentIndex, action):
        # Check if terminal state or maximum depth reached
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return [self.evaluationFunction(gameState), action]
        # Only decrement depth if all agents have moved
        if agentIndex == gameState.getNumAgents() - 1:
                depth += 1
        # If agent is max (pacman) since we are tyring to maximize the score (evalutaion f'n)
        if agentIndex == 0:
            actions = gameState.getLegalActions(0)
            v = -float("inf")
            best_act = None
            for action in actions:
                temp = self.Expectimax(gameState.generateSuccessor(0, action), depth, 1, action)[0]
                #can't use max() since we need to keep track of the action that led to the max value
                if temp > v:
                    v = temp
                    best_act = action
            return [v, best_act]
        # If agent is min (ghost)
        else:
            actions = gameState.getLegalActions(agentIndex)
            v = 0
            best_act = None
            for action in actions:
                p = 1 / len(actions)
                if agentIndex == gameState.getNumAgents() - 1:
                    v += self.Expectimax(gameState.generateSuccessor(agentIndex, action), depth, 0, action)[0] * p
                else:
                    v += self.Expectimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, action)[0] * p
            return [v, best_act]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
