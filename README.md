# Developing Ainslie Agents


## Total Objective (Project Premise)
Does a mechanism for predicting your own future behaviour compound into the value of current choices

## Repo Structure
- `src/decision_agent/` : contains core code
- `tests/`: for running tests
- `docs/`: project and design notes

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
  - The environment is deterministic?

