
""" 
Agent characterised by hyperbolic discounting and greedy policy. Acts based on the environment interface
"""

import numpy as np

class HypAgent:
    def __init__(self, discount_factor=0.8, vision="myopic", horizon=None): # set default discount arbitrarily to 0.8
        self.discount_factor = discount_factor
        self.vision = vision # categorical to be tunable in future
        self.horizon = horizon # to infer form environment
    
    # the value function
    def value_function(self, reward, distance): ## might change in the future to limit agent's knowledge of the environment class
        utility = reward / (1 + self.discount_factor * distance) # hyperbolically discounting reward on distance from reward
        return utility
    
    # checks environment for certain characteristics, then adopts necessary characteristics
    def get_horizon(self, state, environment):
        if self.horizon is not None:
            return self.horizon
        
        # use remaining horizon
        if hasattr(environment, "length") and hasattr(environment, "time_step"):
            return environment.length - environment.time_step   
            
        # fallback
        return 1

    # sampling the decision node at every future time step, and summing discounted value for the same repeated action
    def long_value(self, state, action, environment):
         total_value = 0
         current_state = state # the current time step of agent

         horizon = self.get_horizon(state, environment)
         
         for t in range(horizon): # iterate through all future time steps
            next_state, outcomes = environment.simulate(current_state, action)
              # the value of this future time step
            for reward, delay in outcomes.values():
                effective_delay = delay + t
                total_value += self.value_function(reward, effective_delay)

            current_state = next_state # updates the state by 1

         return total_value  
              
    # setting a GREEDY policy for the agent
    def evaluate_action(self, state, action, environment):
            
            if self.vision == "myopic":
            # determines how a given action is evaluated (model-based, myopic, aware of reward position)
                _, outcomes = environment.simulate(state, action)
                value = max( # iterating the value function through all simulated outcomes, and computing the max
                    self.value_function(reward, distance)
                    for reward, distance in outcomes.values()
                )
                return value
            elif self.vision == "long-sighted":
                return self.long_value(state, action, environment)
    
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
