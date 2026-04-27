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

## **Current Design Notes for the Model**
### Environments
"grid":
  - Movements through a grid world towards a known reward
    - The multiple-option action space will eventually be important in considering multiple reward options
  - **Characteristics and Assumptions:** (w.r.t. IRL examples)
    - The environment is fully deterministic
    - The agent is fully aware of the reward's position(s)
    - The agent is fully aware of the transition structure of the environment 
### Agents
"exponential":
  - **Characteristics and Assumptions held by Agent:**
    - Explicitly an exponential discounter
    - No memory of past experiences (Markov)
    - Non-learning (no updating beliefs)
    - Environment is remains stable/consistent
    - Only plans 1 step ahead
    - Fully certain and experiences no interference (from it's perspective)
    - The agent is greedy and maximises utility at all decision points

## To model:
  - Hyperbolic agent in grid world
  - Decision effects in a 1d space?
    - Thinking of the homework example, where the environment is a finite-horizon MDP where actions influence future reward availability and future decision difficulty (including temptations)
  - Agent has no/graded awareness of reward position and magnitude (e.g. you don't know when your diet will show results)
  - Effects of cost in the discounting functions
  - Incorporate multiple rewards (to simulate bandit-task like options?) + opportunity costs in the value functions

  
