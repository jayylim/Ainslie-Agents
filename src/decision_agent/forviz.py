
import numpy as np

def render_curves(axes, environment, agent, state):

    axes.clear()

    x_max = environment.length
    y_max = max(rewards["value"] for rewards in environment.rewards.values()) + 1


    # Standardised axis settings
    axes.set_xlim(-1, x_max + 1) 
    axes.set_ylim(0, y_max) 
    axes.set_xlabel("Time to Reward")
    axes.set_ylabel("Perceived Value")
    axes.set_xticks(np.arange(0, x_max+1, 1))

    choices = {} # for storing agent-computed value at any time step

    for name, rewards in environment.rewards.items():
        distance = max(rewards["delay"] - state, 0) # state is the current step of agent updated in main.py

        values = [] # y values
        time_step = [] # x values
        perceived_value = agent.value_function(rewards["value"], distance) # agent's current value
        choices[name] = perceived_value

        for t in range(distance+1):
            value = agent.value_function(rewards["value"], distance - t) # compute value at each subsequent step with respect to the current time step
            time_step.append(t) # fills the corresponding x-coord
            values.append(value) # fills the corresponding y-coord


        axes.plot(time_step, values, label=name) 
        axes.legend(loc="upper center")


        if distance == 0:
            axes.scatter(0, perceived_value, s= 40, color= "gold")
            axes.axvline(distance, linestyle = '--', color = "black", alpha = 0.3)
            axes.text(0, perceived_value + 0.2, round(perceived_value, 2), ha="center", size = 10)
        else:
            axes.axvline(distance, linestyle = '--', color = "black")
            axes.scatter(0, perceived_value, s= 40, color= "black")
            axes.text(0, perceived_value + 0.2, round(perceived_value, 2), ha="center", size = 10)

        axes.set_title("Value Curves of Current Choice")



