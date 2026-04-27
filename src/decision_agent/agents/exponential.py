
""" 
Agent characterised by exponential discounting and greedy policy. Acts based on the environment interface
"""


class ExpAgent:
    def __init__(self, discount_factor=0.8): # set default discount arbitrarily to 0.8
        self.discount_factor = discount_factor
    
    # the value function
    def value_function(self, reward, distance): ## might change in the future to limit agent's knowledge of the environment class
        value = reward * (self.discount_factor ** distance) # exponentially discounting reward based on number of steps
        return value

    # setting a GREEDY policy for the agent
    def choose_action(self, state, environment):

        # no initial bias towards any action
        best_action = None 
        best_value = float("-inf") # first action will replace this

        # evaluate all actions (model-based, aware of reward position)
        for action in environment.get_actions(state):
            predicted_position = environment.transitions(state, action) # simulating next position using an internal model
            
            distance = environment.distance(predicted_position)
            reward = environment.reward
            predicted_value = self.value_function(reward, distance) # determine value of simulated position using value function

            if predicted_value > best_value:
                best_value = predicted_value
                best_action = action

        return best_action

