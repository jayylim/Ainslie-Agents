"""
Launching runs
"""

# import relevant variables
from decision_agent import Environment
from decision_agent import ExpAgent

#setting up environment
environment = Environment(
    width = 10,
    height = 10,
    start = (2, 8),
    reward_position = (9, 4),
    reward = 10
)


# setting up agent
agent = ExpAgent()
state = environment.reset() 
finished = False

environment.display()

while not finished: # runs a loop until done = True
    action = agent.choose_action(state, environment) # selection action based on policy and value function, etc.
    state, reward, finished = environment.step(action) # apply action to environment
    
    value = agent.value_function(state, environment) # get value of current position
    print("Agent moved " + action)
    print(state, reward, value)
    environment.display()
 
  