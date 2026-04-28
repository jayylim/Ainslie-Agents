
# Control Block
from .factory import create_environment, create_agent
import matplotlib.pyplot as plt
from decision_agent import GridEnvironment # only needed for the debugging stuff

run_config = {
    # Choose model variables
    "env_type": "grid", # grid or timeline
    "agent_type": "exponential", # exponential or hyperbolic
    
   # Parameters for each variable type (might be abstracted into a different file eventually)
    "env_params": {
        "grid":{
            "width": 10,
            "height": 10,
            "start": (1, 2),
            "rewards": {
                "SS": {
                    "position": (4, 4),
                    "value": 5
                },
                "LL": {
                    "position": (8, 1),
                    "value": 10
                }
            }
        }, # continue other model type here if necessary
        "timeline":{
            "length": 100,
            "rewards": {
                "SS": {
                    "value": 5,
                    "delay": 0
                },
                "LL": {
                    "value": 10,
                    "delay": 3
                }
            }
        
        }
    },

    "agent_params": {
        "exponential":{
            "discount_factor": 0.6 # effectively a 'value decay rate', constant in one span of time
        },
        "hyperbolic":{
            "discount_factor": 0.6 # effectively a 'value decay rate', varies at different points in one span of time
    }
    #can add override codes here, but then need merging code
    }
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


# render initial state

print("Starting...")
print(state, 0)

if hasattr(environment, "render"): # currently only grid world
    fig, axes = plt.subplots()
    plt.ion()

    environment.render(axes) # action default is None
    plt.draw()
    plt.pause(2)

# run model
while not finished:
    action, action_values = agent.choose_action(state, environment) # agent evaluates and chooses an action

    state, earned_reward, finished = environment.step(action) # update position, receive outcome of choice


    print("Current options:", action_values)
    
    # == FOR DEBUGGING: CHECKING HOW AGENT DISCOUNTS ===
    if isinstance(environment, GridEnvironment):

            # re-simulate using environment's exact design
        next_state, outcomes = environment.simulate(state,action)
        print("For this state:")   
        for name, (reward, delay) in outcomes.items():
            value = agent.value_function(reward, delay)
            print(f" {name}: reward={reward}, delay={delay}, value={value}")

    print("therefore,")
    print("Agent " + f"({run_config['agent_type']}) " + "chose " + action)
    print(state, earned_reward)


    if hasattr(environment, "render"): # currently only grid world
        environment.render(axes, action)
        axes.set_title("Agent " + f"({run_config['agent_type']}) " + "chose " + action)
        plt.draw()
        plt.pause(0.5)

plt.ioff()
plt.show()

