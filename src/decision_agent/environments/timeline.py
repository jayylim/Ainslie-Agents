'''
A one-dimensional timeline with decision nodes at different points in time across a horizon
Currently a binary choice
'''


class TimelineEnvironment:
    def __init__(self, rewards, length=20, start =0): 
        self.rewards = rewards # this will be a dictionary that stores the rewards for each choice
        self.length = length # this will be a variable that controls the length of the choice horizon
        self.start = start # starting of whole simulation (e.g. day 0)
        self.time_step = start # the current time step along the horizon; effectively "agent_position"


# === Agent-facing layer ===
    def get_actions(self, state=None):
        return ["snack", "resist"]
    
    def simulate(self, state, action): # this is a one-time-step stimulation
        next_state = state + 1
        
        reward_type, reward_info = self.get_reward(action) # extracts info for the reward correspodning to the chosen action
       
       # stores outcome of all actions in the form of "rewards"
        outcomes = {
            reward_type: (reward_info["value"], reward_info["delay"]) 
        }
        return next_state, outcomes
        
# === Environment Specific Methods ===
    def reset(self):
        self.time_step = self.start
        return self.time_step
    
    def get_reward(self, action):
        self.action_map = { # mapping actions to each reward type in environment_parameters
            "snack": "SS",
            "resist": "LL"
        }
        reward_type = self.action_map[action] # select the right reward type
        return reward_type, self.rewards[reward_type] # returns the reward tuple based on action

    def step(self, action):          
        _, reward_info = self.get_reward(action) # extract reward info based on action selected

        # only get reward if delay = 0
        if reward_info["delay"] == 0:
            earned_reward = reward_info["value"] 
        else: 
            earned_reward = 0

        self.time_step += 1
        finished = True

        return self.time_step, earned_reward, finished
            
        
        
            
    
