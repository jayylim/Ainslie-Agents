# Developing Ainslie Agents


## Total Objective (Project Premise)
Does a mechanism for predicting your own future behaviour compound into the value of current choices

## Structure
```
ainslie-agents/
├──src/ # contains core code
│   └──decision_agent/
│        └──agents/
│            └── exponential.py # exponential-discounting agent
│            └── hyperbolic.py # hyperbolic-discounting agent
│        └──environments/
│            └── grid.py # grid world environment
│            └── timeline.py # sequential decision-making environment
│            └── rewarded_timeline.py # testing upgrades to timeline.py
│        ├── __init__.py # initialisation code
│        ├── factory.py  # for holding agent/environment configs
│        ├── main.py # for running the model
│        └── utils.py # for convenience functions
│        └── visualise.py # separate visualisation code
└── README.md
```
## Running a Model
In `main.py`, under `run_config` , choose:
- Environment type
- Agent type
- Initialisation parameters for each
- Select correct debugger
- Run main.py

## Run
cd src
python -m decision_agent.main
 


  
