
""" 
Agent characterised by exponential discounting and greedy policy. Acts based on the environment interface
"""
import numpy as np

class ExpAgent:
    def __init__(self, discount_factor=0.8): # set default discount arbitrarily to 0.8
        self.discount_factor = discount_factor
    
    # the value function
    def value_function(self, reward, distance): ## might change in the future to limit agent's knowledge of the environment class
        utility = reward * (np.exp(-self.discount_factor * distance)) # exponentially discounting reward on distance from reward
        return utility

   # setting a GREEDY policy for the agent
    def evaluate_action(self, state, action, environment):
            # determines how a given action is evaluated (model-based, myopic, aware of reward position)
            _, outcomes = environment.simulate(state, action)

            value = max( # iterating the value function through all simulated outcomes, and computing the max
                self.value_function(reward, distance)
                for reward, distance in outcomes.values()
            )
            return value
    
    def choose_action(self, state, environment):

        # no initial bias towards any action
        best_action = None 
        best_value = float("-inf") # first action will replace this

        action_values = {} # for tracking action values, for debugging

         # iterate through all actions and evaluate
        for action in environment.get_actions(state):

            value = self.evaluate_action(state, action, environment)
            action_values[action] = float(value) # store in dict

            # compute the argmax over actions
            if value > best_value:
                best_value = value
                best_action = action

        return best_action, action_values
