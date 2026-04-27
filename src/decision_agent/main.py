
# Control Block
from .factory import create_environment, create_agent
import matplotlib.pyplot as plt

run_config = {
    # Choose model variables
    "env_type": "grid", # or 2nd type
    "agent_type": "exponential", # or hyperbolic
   

   # Parameters for each variable type (might be abstracted into a different file eventually)
    "env_params": {
        "grid":{
            "width": 10,
            "height": 10,
            "start": (2, 8),
            "reward_position": (7, 1),
            "reward": 10,
        } # continue other model type here if necessary
    },

    "agent_params": {
        "exponential":{
            "discount_factor": 0.8
        },
        "hyperbolic":{
            "k": 0.2
        }
    }
    #can add override codes here, but then need merging code
}

# Select Parameter by Model
env_params = run_config["env_params"][run_config["env_type"]].copy()
agent_params = run_config["agent_params"][run_config["agent_type"]].copy()

# Instantiate Model
environment = create_environment(run_config["env_type"], env_params)
agent = create_agent(run_config["agent_type"], agent_params)

# Run model (all methods and variables in this must be consistent across all enviornments and agents)
state = environment.reset()
finished = False 

fig, axes = plt.subplots()
plt.ion()

# render initial state
distance = environment.distance(state)
value = agent.value_function(environment.reward, distance) # get value of current position

print("Starting...")
print(state, 0, value, distance)

if hasattr(environment, "render"):
    environment.render(axes) # action default is None
    plt.draw()
    plt.pause(2)

# run model
while not finished:
    action = agent.choose_action(state, environment)
    state, reward, finished = environment.step(action)
    
    # compute current state value
    distance = environment.distance(state)
    value = agent.value_function(reward, distance) # get value of current position
    
    print("Agent chose " + action)
    print(state, reward, value, distance)

    if hasattr(environment, "render"):
        environment.render(axes, action)
        plt.draw()
        plt.pause(0.5)

plt.ioff()
plt.show()

