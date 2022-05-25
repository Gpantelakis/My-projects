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
        # Collect legal moves and child states
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

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        

        "*** YOUR CODE HERE ***"
        
        new_food_L=newFood.asList()
        new_ghost_positions = childGameState.getGhostPositions()
        current_food=currentGameState.getFood()
        current_food_L=current_food.asList()
        score=0
        c_food=100000000
        c_ghost=100000000
        distancef=[]
        distanceg=[]

        if newPos in current_food_L:
            score+=10
        for foodpos in new_food_L:
            distancef.append(manhattanDistance(newPos,foodpos))
        if len(distancef)>0:
            c_food=min(distancef)
        score=10.0/c_food-3*len(distancef)

        for ghostp in new_ghost_positions:
            distanceg=manhattanDistance(newPos,ghostp)
            c_ghost=min(c_ghost,distanceg)

        if c_ghost<2:
            score-=30

        return childGameState.getScore()+score

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

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        best_action = self.max_v(gameState=gameState, depth=0, agent_num=0)[1]
        return best_action

        util.raiseNotDefined()
    def max_v(self,gameState,depth,agent_num):

        value=(float('-Inf'),None)      #Initialize the value which is a tuple of the best value of a state and the action
        l_actions=gameState.getLegalActions(agent_num)
        for action in l_actions:
            next_state=gameState.getNextState(agent_num,action)
            number_of_Agents=gameState.getNumAgents()
            expand_depth=depth+1
            current_agent=expand_depth % number_of_Agents
            value2=self.choice_value(gameState=next_state,depth=expand_depth,agent_num=current_agent),action
            value=max([value,value2],key=lambda val :val[0])
            
        return value
    
    def min_v(self,gameState,depth,agent_num):

        value=(float('+Inf'),None)      #Initialize the value which is a tuple of the best value of a state and the action
        l_actions=gameState.getLegalActions(agent_num)
        for action in l_actions:
            next_state=gameState.getNextState(agent_num,action)
            number_of_Agents=gameState.getNumAgents()
            expand_depth=depth+1
            current_agent=expand_depth % number_of_Agents
            value2=self.choice_value(gameState=next_state,depth=expand_depth,agent_num=current_agent),action
            value=min([value,value2],key=lambda val :val[0])
            
        return value
    
    def is_leaf_node(self,gameState,depth,agent_num):

        if gameState.isWin():
            return gameState.isWin()
        elif gameState.isLose():
            return gameState.isLose()
        elif gameState.getLegalActions(agent_num) is 0:  
            return gameState.getLegalActions(agent_num)
        elif depth >= self.depth * gameState.getNumAgents():
            return self.depth
    
    def choice_value(self,gameState,depth,agent_num):


        if self.is_leaf_node(gameState=gameState,depth=depth,agent_num=agent_num):
            return self.evaluationFunction(gameState)
        elif agent_num == 0:
            return self.max_v(gameState=gameState,depth=depth,agent_num=agent_num)[0]
        else:
            return self.min_v(gameState=gameState,depth=depth,agent_num=agent_num)[0]



        

        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha=float('-Inf')
        beta=float('+Inf')
        best_action = self.max_v(gameState=gameState, depth=0, agent_num=0,alpha=alpha,beta=beta)[1]
        return best_action

    def max_v(self,gameState,depth,agent_num,alpha,beta):

        value=(float('-Inf'),None)      #Initialize the value which is a tuple of the best value of a state and the action
        l_actions=gameState.getLegalActions(agent_num)
        for action in l_actions:
            next_state=gameState.getNextState(agent_num,action)
            number_of_Agents=gameState.getNumAgents()
            expand_depth=depth+1
            current_agent=expand_depth % number_of_Agents
            value2=self.choice_value(gameState=next_state,depth=expand_depth,agent_num=current_agent,alpha=alpha,beta=beta),action
            value=max([value,value2],key=lambda val :val[0])
            if value[0]>beta:
                return value
            alpha=max(alpha,value[0])
        return value    
        
        util.raiseNotDefined()
    def min_v(self,gameState,depth,agent_num,alpha,beta):

        value=(float('+Inf'),None)      #Initialize the value which is a tuple of the best value of a state and the action
        l_actions=gameState.getLegalActions(agent_num)
        for action in l_actions:
            next_state=gameState.getNextState(agent_num,action)
            number_of_Agents=gameState.getNumAgents()
            expand_depth=depth+1
            current_agent=expand_depth % number_of_Agents
            value2=self.choice_value(gameState=next_state,depth=expand_depth,agent_num=current_agent,alpha=alpha,beta=beta),action
            value=min([value,value2],key=lambda val :val[0])
            if value[0]<alpha:
                return value
            beta=max(alpha,value[0])

        return value
    
    def is_leaf_node(self,gameState,depth,agent_num):

        if gameState.isWin():
            return gameState.isWin()
        elif gameState.isLose():
            return gameState.isLose()
        elif gameState.getLegalActions(agent_num) is 0:
            return gameState.getLegalActions(agent_num)
        elif depth >= self.depth * gameState.getNumAgents():
            return self.depth
    
    def choice_value(self,gameState,depth,agent_num,alpha,beta):


        if self.is_leaf_node(gameState=gameState,depth=depth,agent_num=agent_num):
            return self.evaluationFunction(gameState)
        elif agent_num == 0:
            return self.max_v(gameState=gameState,depth=depth,agent_num=agent_num,alpha=alpha,beta=beta)[0]
        else:
            return self.min_v(gameState=gameState,depth=depth,agent_num=agent_num,alpha=alpha,beta=beta)[0]


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
        best_action = self.max_v(gameState=gameState, depth=0, agent_num=0)[1]
        return best_action
        util.raiseNotDefined()

    def max_v(self,gameState,depth,agent_num):

        value=(float('-Inf'),None)      #Initialize the value which is a tuple of the best value of a state and the action
        l_actions=gameState.getLegalActions(agent_num)
        for action in l_actions:
            next_state=gameState.getNextState(agent_num,action)
            number_of_Agents=gameState.getNumAgents()
            expand_depth=depth+1
            current_agent=expand_depth % number_of_Agents
            value2=self.choice_value(gameState=next_state,depth=expand_depth,agent_num=current_agent),action
            value=max([value,value2],key=lambda val :val[0])
            
        return value

    def expected_v(self,gameState,depth,agent_num):
        
        value=[]      #Initialize the value which is a tuple of the best value of a state and the action
        l_actions=gameState.getLegalActions(agent_num)
        for action in l_actions:
            next_state=gameState.getNextState(agent_num,action)
            number_of_Agents=gameState.getNumAgents()
            expand_depth=depth+1
            current_agent=expand_depth % number_of_Agents
            value.append(self.choice_value(gameState=next_state,depth=expand_depth,agent_num=current_agent))
        expected_value=sum(value)/len(value)   
            
        return expected_value
        


    def is_leaf_node(self,gameState,depth,agent_num):

        if gameState.isWin():
            return gameState.isWin()
        elif gameState.isLose():
            return gameState.isLose()
        elif gameState.getLegalActions(agent_num) is 0:
            return gameState.getLegalActions(agent_num)
        elif depth >= self.depth * gameState.getNumAgents():
            return self.depth    

       
    
    def choice_value(self,gameState,depth,agent_num):


        if self.is_leaf_node(gameState=gameState,depth=depth,agent_num=agent_num):
            return self.evaluationFunction(gameState)
        elif agent_num == 0:
            return self.max_v(gameState=gameState,depth=depth,agent_num=agent_num)[0]
        else:
            return self.expected_v(gameState=gameState,depth=depth,agent_num=agent_num)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    """
    1.At First we must find the closest food from the pacman and i subtract 
    from the value.So the closer food we find,the bigger score we will have 
    
    2.After we put in a list the the enemy ghosts an the scared ghosts.

    3.For the closest ghost in pacman we subtract from the score the inverse distance multiplied by 4.
    So the further ghost the algorithm choose,the less subtraction will be.

    4.After we find the closest scared ghost and we subtract from the score its distance multiplied by 2.
    So the closest scared ghost will subtract the least points from score.

    In the end we subtract the remainnig food multiplied by 3,to find a way the algorithm to minimize this and win. 
    
    """

    

    "*** YOUR CODE HERE ***"

    pacman_pos=currentGameState.getPacmanPosition()
    food_pos=currentGameState.getFood()
    food_posL=food_pos.asList()
    ghost_states=currentGameState.getGhostStates()
    score=currentGameState.getScore()
    
    c_food=float('+Inf')
    c_ghost=float('+Inf')
    c_scared_ghost=float('+Inf')

    distancef=[]
    for food in food_posL:
        distancef.append(manhattanDistance(pacman_pos,food))
    if len(distancef)>0:
        c_food=min(distancef)
        score-=c_food
    
    scared_ghosts=[]
    ghosts=[]
    for ghost in ghost_states:
        if ghost.scaredTimer>0:
            ghosts.append(ghost)
        else:
            scared_ghosts.append(ghost)
    
    ghostpos=[]
    for ghost in ghosts:
        ghostpos.append(ghost.getPosition())

    distance_g=[]
    if len(ghostpos)>0:
        for ghostp in ghostpos:
            distance_g.append(manhattanDistance(pacman_pos,ghostp))
        c_ghost=min(distance_g)
        score-=4*(1/c_ghost)
    
    scared_ghost_p=[]
    for s_ghost in scared_ghosts:
        scared_ghost_p.append(s_ghost.getPosition())
    
    if len(scared_ghost_p)>0:
        distane_s_g=[]
        for sc_ghost in scared_ghost_p:
            distane_s_g.append(manhattanDistance(pacman_pos,sc_ghost))
        c_s_ghost=min(distane_s_g)   
        score-=2*c_s_ghost
    

    score-=3*len(food_posL)
    return score

    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
