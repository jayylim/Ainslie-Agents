
# Control Block
from .factory import create_environment, create_agent
from .env_configs import param_config
# from .graphs import plot_value_functions
import matplotlib.pyplot as plt
from decision_agent import GridEnvironment # only needed for the debugging stuff
from .forviz import render_curves

# === Instantiate Model === 
# Choose model variables
agent_config = {
    "exponential":{
        "discount_factor": 0.6, # effectively a 'value decay rate', constant in one span of time
        "vision": "myopic" # myopic or long-sighted
    },
    "hyperbolic":{
        "discount_factor": 0.8, # effectively a 'value decay rate', varies at different points in one span of time
        "vision": "myopic"
    }
#can add override codes here, but then need merging code
}

run_config = {
    "env_type": "timeline", # grid or timeline or Rtimeline
    "agent_type": "hyperbolic", # exponential or hyperbolic  
}

step_mode = True # switch for manual stepping


# Select Parameter by Model
env_params = param_config["env_params"][run_config["env_type"]].copy()
agent_params = agent_config[run_config["agent_type"]].copy()

# instantiate
environment = create_environment(run_config["env_type"], env_params)
agent = create_agent(run_config["agent_type"], agent_params)

# === Run model ===
# (all methods and variables in this must be consistent across all enviornments and agents)
state = environment.reset()
finished = False 

# render initial state
print("Starting...")
print(state, 0)

if hasattr(environment, "render"):
    fig, (ax_env, ax_curve) = plt.subplots(1, 2, figsize = (13,5))
    plt.ion()

    environment.render(ax_env) # action default is None
    render_curves(ax_curve, environment, agent, state)
    plt.draw()
    plt.waitforbuttonpress()
 
# run model
while not finished:
    action, action_values = agent.choose_action(state, environment) # agent evaluates and chooses an action

        # == FOR DEBUGGING: CHECKING HOW AGENT DISCOUNTS ===
    if isinstance(environment, GridEnvironment):

            # re-simulate using environment's exact design
        next_state, outcomes = environment.simulate(state,action)
        print("FOR STATE " + f"{state}" + ":")   
        for name, (reward, delay) in outcomes.items():
            value = agent.value_function(reward, delay)
            print(f" {name}: reward={reward}, delay={delay}, value={value}")
    
    state, earned_reward, finished = environment.step(action) # update position, receive outcome of choice

    print("Current options:", action_values)
    print("therefore,")
    print("Agent " + f"({run_config['agent_type']}) " + "chose " + action)
    print(state, earned_reward)


    if hasattr(environment, "render"):
        environment.render(ax_env, action)
        ax_env.set_title("Agent " + f"({run_config['agent_type']}) " + "chose " + action)

    render_curves(ax_curve, environment, agent, state)

    plt.draw()
    plt.pause(1)

    if step_mode:
        cmd = input("Press Enter for next step or 'q' to quit: ")
        if cmd.lower() == "q":
            break

plt.ioff()
plt.show()
