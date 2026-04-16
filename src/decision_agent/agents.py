"""
Overall decision-making logic of the baseline agent
"""


""" 
Exponentially discounting agent, where agent is AWARE of the reward position
"""

# currently only 1 reward, no interaction between choices


class ExpAgent:
    def __init__(self, discount_factor=0.8): # set default discount arbitrarily to 0.8
        self.discount_factor = discount_factor
        self.actions  = ["up", "down", "left", "right"]
    
    # the value function
    def value_function(self, state_position, environment): ## might change in the future to limit agent's knowledge of the environment class
        state_row, state_col = state_position
        goal_row, goal_col = environment.reward_position

        reward = environment.reward

        distance = abs(state_row - goal_row) + abs (state_col - goal_col) # absolute manhattan distance from reward
        
        value = reward * (self.discount_factor ** distance) # exponentially discounting reward based on number of steps

        return value

    # position updating rules for internal model simulation; must be same as environment's rules
    def simulate(self, current_position, action, environment):
        row, col = current_position

        # Updating position by action
        if action == "up":
            row += -1
        elif action == "down":
            row += +1
        elif action == "left":
            col += -1 
        elif action == "right":
            col += +1 
        
        col = max(0, min(environment.width -1, col)) # clamps columns to be between grid width-1 and 0
        row = max(0, min(environment.height -1, row)) # clamps rows to be between grid height-1 and 0
    
        return (row, col) # return new position

    # setting the policy for the agent
    def choose_action(self, current_position, environment):
        reward_position = environment.reward_position

        # no initial bias towards any action
        best_action = None 
        best_value = float("-inf") # first action will replace this

        for action in self.actions:
            predicted_position = self.simulate(current_position, action, environment) # simulating next position using an internal model
            predicted_value = self.value_function(predicted_position, environment) # determine value of simulated position using value function

            if predicted_value > best_value:
                best_value = predicted_value
                best_action = action

        return best_action

