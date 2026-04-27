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
  - Movements through a grid world, states corresponding to occupiable grid-squares, moving towards known reward
  - **Characteristics and Assumptions:** (w.r.t. IRL examples)
    - The environment is fully deterministic
    - The agent is fully aware of the rewards' positions and magnitudes
    - The agent is fully aware of the transition structure of the environment 
    - Agent will look-ahead one step
### Agents
"exponential":
  - **Characteristics and Assumptions held by Agent:**
    - Explicitly an exponential discounter
    - No memory of past experiences (Markov)
    - Non-learning (no updating beliefs)
    - Environment is remains stable/consistent
    - Fully certain and experiences no interference (from it's perspective)
    - The agent is greedy and maximises utility at all decision points
"hyperbolic":
  - **Characteristics and Assumptions held by Agent:**
    - Explicitly an exponential discounter
    - No memory of past experiences (Markov)
    - Non-learning (no updating beliefs)
    - Environment is remains stable/consistent
    - Fully certain and experiences no interference (from it's perspective)
    - The agent is greedy and maximises utility at all decision points

### Code Conventions
  - "distance" refers to distance from rewards of all modes (grid steps, time delay, etc.)
  - representations of the environment are **decoupled** from the agent's code

## To Model/Improve:
  - Hyperbolic agent in grid world
  - Decision effects in a 1d space?
    - Thinking of the homework example, where the environment is a finite-horizon MDP where actions influence future reward availability and future decision difficulty (including temptations)
  - Agent has no/graded awareness of reward position and magnitude (e.g. you don't know when your diet will show results)
  - Effects of cost in the discounting functions
 
 ## To Restructure (for future-proofing):
  1. ~~Make agent purely evaluation; agent should not know how rewards are stored, what "distance" means, what the state looks like structurally~~
  2. ~~Remove reward structure awareness in agent; agent should never access internal dictionaries into the environment~~
  3. Separate policy from the agent