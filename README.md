# Developing Ainslie Agents


## Total Objective (Project Premise)
Does a mechanism for predicting your own future behaviour compound into the value of current choices

## Structure
```
ainslie-agents/
├──src/ # contains core code
│   └──decision_agent/
│        ├── __init__.py
│        ├── config.py
│        ├── utils.py # for convenience functions
│        ├── environment.py
│        ├── agents.py
│        └── main.py
├── tests/  # for running tests
├── docs/ # project and design notes
└── README.md
```
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
  - Effects of cost in the discounting functions
  - Incorporate multiple rewards (to simulate bandit-task like options?) + opportunity costs in the value functions

