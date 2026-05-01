## Main Objectives
- Demonstrate how mechanisms which can be proxies of **will-power** and **self-control** impact value-based deicions
- **Level 1**: Demonstrate the difference in behaviour of a hyperbolic discounter VS exponential discounter 
- **Level 2**: (TBC) effect of awareness of hyperbolic discounting (naive VS sophisticated)?
 
### **Level 1 Agents**
  - An agent that performs *exponential discounting* when making a value-based decision
  - An agent that performs *hyperbolic discounting* when making a value-based decision

## **Current Design Notes for the Model**

### Environments
`"grid"`:
  - Movements through a grid world, states corresponding to occupiable grid-squares, moving towards known reward
  - **Characteristics and Assumptions:** (w.r.t. IRL examples)
    - The environment is fully deterministic
    - The agent is fully aware of the rewards' positions and magnitudes
    - The agent is fully aware of the transition structure of the environment 
    - Agent will look-ahead one step
  
`"timeline"`:
- Timeline of sequential decisions, where the same decision is offered at every time step independent of the past decision
  - decision between SS action (e.g. snack) vs LL action (e.g. resist and stick to diet)
  - in `"Rtimeline"`: receiving the LL-reward is conditional on choosing LL-action until delay is over
- For observing the effects of "summed rewards" over a longer time scale
  - myopic vs long-sighted agent will have different reactions to this
  - longsighted exponential vs long-sighted hyperbolic will also have different reactions


### Agents
`"exponential"`:
  - **Characteristics and Assumptions held by Agent:**
    - Explicitly an exponential discounter
    - No memory of past experiences (Markov)
    - Non-learning (no updating beliefs)
    - Assumes environment remains stable/consistent
    - Fully certain and experiences no interference (from it's perspective)
    - The agent is greedy and maximises utility at all decision points
  
`"hyperbolic"`:
  - **Characteristics and Assumptions held by Agent:**
    - Explicitly a hyperbolic discounter
    - No memory of past experiences (Markov)
    - Non-learning (no updating beliefs)
    - Assumes nvironment remains stable/consistent
    - Fully certain and experiences no interference (from it's perspective)
    - The agent is greedy and maximises utility at all decision points
    - `"vision"` and `"horizon"` currently only binary, with long-sighted horizon equal to the full length of timeline (can be decoupled in future)

### Code Conventions
  - "distance" refers to distance from rewards of all modes (grid steps, time delay, etc.)
  - representations of the environment are **decoupled** from the agent's code
  - (For now) Every environment must have the methods: *reset*, *get_actions*, *simulate* (which has *outcomes*), *step* 
  - (For now) Every agent must have the methods: *choose_actions* 

## To Model/Improve:
  - Agent has no/graded awareness of reward position and magnitude (i.e. fog of war; e.g. not knowing when your diet will show results)
  - Effects of cost in the discounting functions?
 - **Sequential decision points and the importance of summed hyperbolic/exponential rewards**
   - ~~**[to do]: adding long-sightedness to agent + switchable parameter for vision depth**~~  
   - ~~ability to gain LL if and only if it consistently chooses resist (currently gets 188 even if switches at step 18)~~
     - self-prediction layer will tune the agent's `"belief"` to moderate its awareness of this
   - effects of using different "methods" to moderate vision depth (E.g. personal rules, emotional preparedness) -> make vision depth tunable
 - Evaluating whole **trajectories** from increasing depth (while remaining time-inconsistent), not very consistent with hyperbolic-discounters?
 - Effects of beliefs about one's preferences
   - recursion for *sophisticated* hyperbolic discounters (currently implicitly naive)

 
 ## To Restructure (for future-proofing):
  1. ~~Make agent purely evaluation; agent should not know how rewards are stored, what "distance" means, what the state looks like structurally~~
  2. ~~Remove reward structure awareness in agent; agent should never access internal dictionaries into the environment~~
  3. Separate policy greedy from the agent
  4. Make it such that for myopic agent, the environment length can be less?

## For Visualisation:
  1. What it's like for the reward to move towards the agent over time (agent's vertical position scales along the hyperbolic curve; reward represented by "wall" is coming TOWARDS you (the left))