'''
A one-dimensional timeline with decision nodes at different points in time across a horizon
Currently a binary choice
'''
import matplotlib.pyplot as plt


class TimelineEnvironment:
    def __init__(self, rewards, length=20, start=0): 
        self.rewards = rewards # this will be a dictionary that stores the rewards for each choice
        self.length = length if length is not None else 20# this will be a variable that controls the length of the choice horizon
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

        if self.time_step >= self.length:
            finished = True
        else:
            finished = False

        return self.time_step, earned_reward, finished

    # render a visualisation of the enviornment       
    def render(self, axes, action=None):
        axes.clear()

        # create two horiontal timelines
        y_SS = 0.1
        y_LL = -0.1
        axes.plot([0, self.length], [y_SS, y_SS], color = "red")
        axes.plot([0, self.length], [y_LL, y_LL], color ="blue")
        axes.text(-3, y_SS, "snack", va="center")
        axes.text(-3, y_LL, "diet", va="center")
        
        # tracking horizon
        axes.text(
            0, # x position
            y_LL-0.1,
            f"Horizon: {self.length-self.time_step} time steps",
            ha="center",
            fontsize=10,
            color="black"
            )
        
        # tracking time step
        axes.text(
            0, # x position
            y_LL-0.15,
            f"Time step: {self.time_step}",
            ha="right",
            fontsize=10,
            color="black"
            )

        # drawing ticks
        for t in range(1, self.length +1):
            axes.plot([t,t], [y_SS+0.02, y_SS-0.02], color = "red")
            axes.plot([t,t], [y_LL+0.02, y_LL-0.02], color = "blue")

        # drawing agent
        if action == "snack":
            y_agent = y_SS
        elif action == "resist":
            y_agent = y_LL
        else:
            y_agent = 0

        axes.scatter(self.time_step, y_agent, s = 100, color = "black")

        # tracking position of current rewards
        for name, reward in self.rewards.items():
            d = reward["delay"]

            # visualize reward arrival from current position
            reward_time = self.time_step + d

            if reward_time <= self.length:
                if name == "SS":
                    axes.scatter(reward_time, y_SS, s =30, color = "gold")
                    axes.text(
                        reward_time,
                        y_SS + 0.05,
                        f"{name}\n({reward['value']})",
                        ha="center"
                    )
                if name == "LL":
                    axes.scatter(reward_time, y_LL, s =30, color = "gold")
                    axes.text(
                        reward_time,
                        y_LL + 0.05,
                        f"{name}\n({reward['value']})",
                        ha="center"
                    )

        # formatting
        axes.set_ylim(-0.3, 0.3)
        axes.axis("off")
            