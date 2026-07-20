# Import Packages and Modules
from .factory import create_environment, create_agent
from .env_configs import param_config
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
x_max = max(reward["delay"] for _, reward in environment.rewards.items())
y_max = max(reward["value"] for _, reward in environment.rewards.items()) + 1

# outer loop iterates through whole animation
for frame in range(x_max + 1):

    axes.clear()

    # Standardised axis settings
    axes.set_xlim(-1, x_max + 1)
    axes.set_ylim(0, y_max)
    axes.set_xlabel("Time to Reward")
    axes.set_ylabel("Perceived Value")
    axes.set_xticks(np.arange(0, x_max + 1, 1))

    choices = {}

    # First pass: compute current perceived values for each reward
    for name, reward_type in environment.rewards.items():
        reward_value = reward_type["value"]

        # remaining delay as time progresses
        reward_distance = max(reward_type["delay"] - frame, 0)

        perceived_value = agent.value_function(reward_value, reward_distance)
        choices[name] = perceived_value

    # Winner at this time step
    winner = "SS" if choices["SS"] > choices["LL"] else "LL"

    # Second pass: plot all reward curves
    for name, reward_type in environment.rewards.items():
        reward_value = reward_type["value"]
        reward_distance = max(reward_type["delay"] - frame, 0)

        values = []
        time_step = []

        for t in range(reward_distance + 1):
            distance = reward_distance - t
            value = agent.value_function(reward_value, distance)

            time_step.append(t)
            values.append(value)

        perceived_value = choices[name]

        # Plot curve
        axes.plot(time_step, values, label=name)

        # Reward arrival marker
        axes.axvline(reward_distance, linestyle="--", color="black", alpha=0.3)

        # Plot current perceived value
        axes.scatter(0, perceived_value, s=50, color="black")
        axes.text(
            0,
            perceived_value + 0.2,
            round(perceived_value, 2),
            ha="center",
            size=10
        )

        # Highlight the winner for this frame
        if name == winner:
            axes.scatter(
                0,
                perceived_value,
                s=130,
                facecolors="none",
                edgecolors="gold",
                linewidths=2.5
            )

            axes.text(
                0,
                perceived_value + 0.5,
                f"Winner: {winner}",
                ha="center",
                size=10
            )

    axes.legend(loc="upper center")
    axes.set_title(f"Time = {frame}")

    plt.draw()
    plt.waitforbuttonpress()

plt.show()

