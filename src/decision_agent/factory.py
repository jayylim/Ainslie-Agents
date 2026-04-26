''' 
For compiling configurations into variables that can be called by model setup
'''

from environment.grid import GridEnvironment
from agents.exponential import ExpAgent
from agents.hyperbolic import HypAgent


def create_environment(env_type, params):
    if env_type == "grid":
        return GridEnvironment(**params)
    elif env_type == # 2nd env
        return # class of second env(**params)
    else:
        raise ValueError("Unkown environment type")
    
def create_agent(agent_type, params):
    if agent_type == "exponential":
        return ExpAgent(**params)
    elif agent_type == "hyperbolic":
        return HypAgent(**params)
    else:
        raise ValueError("Unknown agent type")





