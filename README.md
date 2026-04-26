# Developing Ainslie Agents


## Total Objective (Project Premise)
Does a mechanism for predicting your own future behaviour compound into the value of current choices

## Structure
```
ainslie-agents/
├──src/ # contains core code
│   └──decision_agent/
│        └──agents/
│            └── exponential.py # exponential agent
│            └── hyperbolic.py # hyperbolic agent
│        └──environments/
│            └── grid.py # grid world environment
│        ├── __init__.py # initialisation code
│        ├── factory.py  # for holding agent/environment configs
│        ├── main.py # for running the model
│        └── utils.py # for convenience functions
└── README.md
```
## Choosing a model
Under run_config, choose:
- Environment type
- Agent type
- Initialisation parameters for each
- Run runner/main.py

## Run
cd src
python -m decision_agent.main
 
 ## Main Objectives
- Demonstrate how mechanisms which can be proxies of **will-power** and **self-control** impact value-based deicions
- **Level 1**: Demonstrate the difference in behaviour of a hyperbolic discounter VS exponential discounter 
- **Level 2**: (TBC) effect of awareness of hyperbolic discounting (naive VS sophisticated)?
 
### **Level 1 Agents**
  - An agent that performs *exponential discounting* when making a value-based decision
  - An agent that performs *hyperbolic discounting* when making a value-based decision

## **General Environment and Model**
  - Movements through a grid world towards squares with varying amounts of reward
    - The multiple-option action space will eventually be important in considering multiple reward options
  - Assumptions of the model (in line with the IRL examples)
    - The environment is deterministic
    - The agent is aware of the rewards' positions


## To model:
  - Decision effects in a 1d space?
    - Thinking of the homework example, where the environment is a finite-horizon MDP where actions influence future reward availability and future decision difficulty (including temptations)
  - Effects of cost in the discounting functions
  - Incorporate multiple rewards (to simulate bandit-task like options?) + opportunity costs in the value functions

## To structure project
  - Making it more 'playable' by reorganising files and agenets and environments
  - need to fix agent dynamics being dependent on the environment
  
