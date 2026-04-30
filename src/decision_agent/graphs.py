# import numpy as np
# import matplotlib.pyplot as plt


# def plot_value_functions(agent, environment, state):

#     # get horizon at initial state
#     total_horizon = agent.get_horizon(state, environment)

#     # extract reward structure (assumes deterministic per action)
#     actions = environment.get_actions(state)

#     # choose one action or loop later — here we plot all
#     fig, ax = plt.subplots()

#     for action in actions:

#         _, outcomes = environment.simulate(state, action)
#         reward, base_delay = next(iter(outcomes.values()))

#         # define global domain (fixed across all steps)
#         T = base_delay
#         x_max = T + 5
#         x_vals = np.linspace(0, x_max, 100)  # creating even spaces for each time step of reward

#         # loop over real time steps
#         for s in range(total_horizon):

#             # remaining horizon
#             H_s = total_horizon - s

#             y_vals = []

#             for x in x_vals:
#                 total = 0

#                 d = T - x # copmuting time to reward
#                 # aggregate over remaining horizon
#                 for t in range(H_s):
#                     total += agent.value_function(reward, d + t)

#                 y_vals.append(max(total,0))

#             # plot curve for this timestep
#             ax.plot(
#                 x_vals,
#                 y_vals,
#                 alpha=0.5,
#                 label=f"{action}, s={s}" if s < 5 else None
#             )

#     ax.set_xlabel("Time to reward")
#     ax.set_ylabel("Aggregated value")
#     ax.set_title("Dynamic Aggregated Value Functions")


#     ax.legend()
#     plt.show()