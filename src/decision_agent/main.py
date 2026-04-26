
# Control Block
from decision_agent import GridEnvironment
from decision_agent import ExpAgent
from factory import create_environment, create_agent

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
            "discount_factor": 0.3
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
done = False 

while not done:
    action = agent.select_action(state)
    state, reward, done = environment.step(action)

    value = agent.value_function(state, environment) # get value of current position
    
    print("Agent chose " + action)
    print(state, reward, value)