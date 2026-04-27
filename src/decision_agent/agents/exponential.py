
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
    def choose_action(self, state, environment):

        # no initial bias towards any action
        best_action = None 
        best_value = float("-inf") # first action will replace this

        # evaluate all actions (model-based, aware of reward position)
        for action in environment.get_actions(state):
            
            next_state, outcomes = environment.simulate(state, action)

            action_value = max( # iterating the value function through all simulated outcomes, and computing the max
                self.value_function(reward, distance)
                for reward, distance in outcomes.values()
            )

            if action_value > best_value:
                best_value = action_value
                best_action = action

        return best_action


