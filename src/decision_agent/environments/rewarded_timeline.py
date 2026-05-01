'''
A one-dimensional timeline with decision nodes at different points in time across a horizon
Currently a binary choice
'''
import matplotlib.pyplot as plt


class RTimelineEnvironment:
    def __init__(self, rewards, length=20, start=0): 
        self.rewards = rewards # this will be a dictionary that stores the rewards for each choice
        self.length = length if length is not None else 20# this will be a variable that controls the length of the choice horizon
        self.start = start # starting of whole simulation (e.g. day 0)
        self.time_step = start # the current time step along the horizon; effectively "agent_position"
        self.pending_rewards = [] # to store chosen LL
        self.total_reward = 0

# === Agent-facing layer ===
    def get_actions(self, state=None):
        return ["snack", "resist"]
    
    def simulate(self, state, action): # this is a one-time-step stimulation
        next_state = state + 1
        
        reward_type, reward_info = self.get_reward(action) # extracts info for the reward correspodning to the chosen action
        
        # compute remaining delay relative to current simulated state
        r_delay = max(reward_info["delay"]-(next_state - self.time_step), 0)

       # stores outcome of all actions in the form of "rewards"
        outcomes = {
            reward_type: (reward_info["value"], r_delay) 
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

        reward_type, reward_info = self.get_reward(action) # extract reward info based on action selected
        earned_reward = 0

        if action != "resist":
            self.pending_rewards = [] # lose all pending rewards if break streak

        # update incoming rewards based on reward info selected
        if action == "snack":
            earned_reward = reward_info["value"] 
        if action == "resist":
            self.pending_rewards.append({
                "type": reward_type,
                "value": reward_info["value"],
                "time_to": reward_info["delay"]
            })
            
        # update all pending rewards
        currently_pending = [] # buffer for updating rewards
        for r in self.pending_rewards: # iterates through all stored pending_reward dicts
            r["time_to"] -= 1

            if r["time_to"] == 0:
                earned_reward += r["value"] # earn the delayed reward
            else:
                currently_pending.append(r)
        self.pending_rewards = currently_pending # update the pending_rewards array

        # update agent's position
        self.time_step += 1
        self.total_reward += earned_reward # update total reward

        # check finished
        if self.time_step >= self.length:
            finished = True
        else:
            finished = False
        

        return self.time_step, earned_reward, finished

    # render a visualisation of the enviornment       
    def render(self, axes, action=None):
        axes.clear()

        # create two horiontal timelines
        y_SS = 0.05
        y_LL = -0.05
        axes.plot([0, self.length], [y_SS, y_SS], color = "red")
        axes.plot([0, self.length], [y_LL, y_LL], color ="blue")
        axes.text(-2, y_SS, "snack", va="center")
        axes.text(-2, y_LL, "diet (resist)", va="center")
        
        # tracking progress, horizon and reward
        axes.text(
            -1, # x position
            y_LL-0.1,
            f"Progress: {self.time_step} step(s)",
            ha="left",
            fontsize=10,
            color="black"
            )
        axes.text(
            -1, # x position
            y_LL-0.15,
            f"Horizon: {self.length-self.time_step} time step(s)",
            ha="left",
            fontsize=10,
            color="black"
            )
        axes.text(
            -1, # x position
            y_LL-0.2,
            f"Total Reward: {self.total_reward}",
            ha="left",
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
                    axes.scatter(reward_time, y_SS, s =50, color = "gold")
                    axes.text(
                        reward_time,
                        y_SS + 0.03,
                        f"{name}\n({reward['value']})",
                        ha="center"
                    )
                if name == "LL":
                    axes.scatter(reward_time, y_LL, s =50, color = "gold")
                    axes.text(
                        reward_time,
                        y_LL + 0.03,
                        f"{name}\n({reward['value']})",
                        ha="center"
                    )
        # tracking pending rewards
        for r in self.pending_rewards:
            reward_spot = self.time_step + r["time_to"]
            if reward_spot <= self.length:
                axes.scatter(reward_spot, y_LL, s = 40, color = "green")
                axes.text(
                        reward_spot,
                        y_LL - 0.05,
                        f"{reward['value']}",
                        ha="center",
                        color = "green"
                    )
                

        # formatting
        axes.set_ylim(-0.3, 0.3)
        axes.axis("off")
            