# Import Packages and Modules
from ..factory import create_environment, create_agent
from ..env_configs import param_config
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('MacOSX')

# === Instantiate Model === 
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

# step_mode = True # switch for manual stepping

# Select Parameter by Model
env_params = param_config["env_params"][run_config["env_type"]].copy()
agent_params = agent_config[run_config["agent_type"]].copy()

# instantiate
environment = create_environment(run_config["env_type"], env_params)
agent = create_agent(run_config["agent_type"], agent_params)

# choose reward type and setup reward info
reward_type = "LL" # or "SS"

rewards = environment.rewards[reward_type]
reward_value = rewards["value"]
reward_distance = rewards["delay"]


# === Running Viz ===
fig, axes = plt.subplots()

x_max = reward_distance #set outside the loop for desired visual and prevent adjusting to value
y_max = reward_value+1


# outer loop iterates through whole animation (plotting multiple frames) 

for frame in range(reward_distance+1):

    axes.clear()
    axes.set_xlim(-0.2, x_max) 
    axes.set_ylim(0, y_max) 

    values = []
    time_step = [] 
    perceived_value = agent.value_function(reward_value, reward_distance)

    # each iteration of inner loop plots the graph for remaining horizon

    for t in range(reward_distance+1):
        distance = reward_distance-t
        value = agent.value_function(reward_value, distance) # compute value with respect to the current time step
        
        time_step.append(t) # marks the x-coord
        values.append(value) # marks the y-coord

    axes.plot(time_step, values)
    axes.axvline(reward_distance, linestyle = '--')
    axes.scatter(0, perceived_value, s= 50, color= "black")
    axes.text(0, perceived_value - 1, round(perceived_value, 2), ha="left", size = 13)
    axes.set_title("time = " + str(frame))
    
    reward_distance -= 1
    plt.pause(0.5)
    input()

plt.show()


