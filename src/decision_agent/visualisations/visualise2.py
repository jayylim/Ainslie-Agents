# Import Packages and Modules
from ..factory import create_environment, create_agent
from ..env_configs import param_config
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
import numpy as np



# === Instantiate Model Parameters and Modules === 
# Choose model variables
agent_config = {
    "exponential":{
        "discount_factor": 0.6, # effectively a 'value decay rate', constant in one span of time
        "vision": "myopic" # myopic or long-sighted
    },
    "hyperbolic":{
        "discount_factor": 0.8, # effectively a 'value decay rate', varies at different points in one span of time
        "vision": "long-sighted"
    }

    
}

run_config = { # for simple hyperbolic, timeline + hyperbolic is default
    "env_type": "timeline", # grid or timeline or Rtimeline
    "agent_type": "hyperbolic", # exponential or hyperbolic  
}

    # Select Parameter by Model
env_params = param_config["env_params"][run_config["env_type"]].copy()
agent_params = agent_config[run_config["agent_type"]].copy()

    # Instantiate
environment = create_environment(run_config["env_type"], env_params)
agent = create_agent(run_config["agent_type"], agent_params)


# === Visualisation ===
fig, axes = plt.subplots()

# boundaries based on max of entire rewards dict
x_max = max(reward["delay"] for _,reward in environment.rewards.items())  
y_max = max(reward["value"] for _,reward in environment.rewards.items()) + 1


SS = environment.rewards["SS"]
LL = environment.rewards["LL"]

# outer loop iterates through whole animation (plotting multiple frames) 

for frame in range(x_max+2):

    axes.clear()

    # Standardised axis settings
    axes.set_xlim(-1, x_max + 1) 
    axes.set_ylim(0, y_max) 
    axes.set_xlabel("Time to Reward")
    axes.set_ylabel("Perceived Value")
    axes.set_xticks(np.arange(0, x_max+1, 1))


    choices = {} # for storing agent-computed value at any time step

    # Initial Choice
    if frame == 0:
        for name, reward_type in environment.rewards.items():
            reward_value = reward_type["value"]
            reward_distance = reward_type["delay"]

            values = []
            time_step = [] 
            perceived_value = agent.value_function(reward_value, reward_distance) # agent's current value
            choices[name] = perceived_value

            for t in range(reward_distance+1):
                distance = reward_distance-t
                value = agent.value_function(reward_value, distance) # compute value with respect to the current (each) time step
                
                time_step.append(t) # marks the x-coord
                values.append(value) # marks the y-coord
        
            axes.plot(time_step, values, label=name) 
            axes.legend(loc="upper center")

            axes.axvline(reward_distance, linestyle = '--', color = "black")
            axes.scatter(0, perceived_value, s= 40, color= "black")
            axes.text(0, perceived_value + 0.2, round(perceived_value, 2), ha="center", size = 10)

        axes.set_title("Time = " + str(frame))

    # Choosing
    elif frame == 1:

        #redraw the curves
        for name, reward_type in environment.rewards.items():
            reward_value = reward_type["value"]
            reward_distance = reward_type["delay"]

            values = []
            time_step = [] 
            perceived_value = agent.value_function(reward_value, reward_distance) # agent's current value
            choices[name] = perceived_value

            for t in range(reward_distance+1):
                distance = reward_distance-t
                value = agent.value_function(reward_value, distance) # compute value with respect to the current (each) time step
                
                time_step.append(t) # marks the x-coord
                values.append(value) # marks the y-coord
        
            axes.plot(time_step, values, label=name)
            axes.set_ylim(min(choices.values())*0.5, max(choices.values())*2) #for zooming in
            axes.scatter(0, perceived_value, s= 70, color= "black")
            axes.text(0, perceived_value + 0.1, round(perceived_value, 2), ha="center", size = 10)
            axes.legend(loc="best")

        #highlight choice
        winner = "SS" if choices["SS"] > choices["LL"] else "LL"
        winner_value = choices[winner]
        axes.scatter(
            0, winner_value,s=120,
            facecolors="none",
            edgecolors="gold",
            linewidths=2.5)
    
        axes.text(0, winner_value + 0.3, f"Choose: {winner}", ha="center", size = 10)
        axes.set_title("Choosing at Time = " + str(frame-1))

    # Continue plotting chosen option
    else:
        axes.set_ylim(0, y_max) 
        step = frame - 1
        reward_distance = max(environment.rewards[winner]["delay"] - step, 0) # moving the curve towards the agent over time steps
        reward_value = environment.rewards[winner]["value"]

        values = []
        time_step = [] 
        perceived_value = agent.value_function(reward_value, reward_distance)

        for t in range(reward_distance+1):
            distance = reward_distance-t
            value = agent.value_function(reward_value, distance) # compute value with respect to the current time step
            
            time_step.append(t) # marks the x-coord
            values.append(value) # marks the y-coord

        if frame == x_max+1 :
            axes.scatter(0, perceived_value, s= 50, color= "gold")
            axes.axvline(reward_distance, linestyle = '--', color = "black", alpha = 0.3)
            axes.text(0, perceived_value + 0.5, round(perceived_value, 2), ha="center", size = 10)
            axes.set_title("Reward Reached at Time = " + str(step))
        else:
            axes.plot(time_step, values, label = name, color = "orange")
            axes.axvline(reward_distance, linestyle = '--', color = "black")
            axes.scatter(0, perceived_value, s= 50, color= "black")
            axes.text(0, perceived_value + 0.5, round(perceived_value, 2), ha="center", size = 10)
            axes.legend(loc="upper center")
            axes.set_title("Time = " + str(step))

    plt.draw() # force the curve to generate
    plt.waitforbuttonpress()
    
plt.show()


