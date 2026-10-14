"""
Run a hyperbolic agent on the memoryless SS/LL timeline.
Edit the params below, then run from this directory:

    python main.py

Units are hours. One choice per day (decision_interval=24).
LL delay is hours after the choice (e.g. 12 ≈ next morning).
"""

from agents.hyperbolic import HypAgent
from environments.timeline import TimelineEnvironment

# === Params ===
env_params = {
    "length": None,  # 10 days (240 hours); or None for infinite
    "start": 0,
    "decision_interval": 24,  # hours between decisions
    "rewards": {
        "SS": {"value": 5, "delay": 0},   # snack now
        "LL": {"value": 15, "delay": 12},  # hours after choice until weigh-in
    },
}

agent_params = {
    "discount_factor": 0.8,
    "vision": "long",  # "short" or "long"
    "horizon": None,  # max # of decisions to plan; capped by remaining env decisions, includes the current day (min. 1)
}

max_steps = 10  # used when env length is None; also caps the run as a safety stop

# === Instantiate ===
environment = TimelineEnvironment(**env_params)
agent = HypAgent(**agent_params)

# === Run ===
state = environment.reset()
finished = False
steps = 0

print("Starting...")
print(f"state={state}h (interval={environment.decision_interval}h)")

while not finished and steps < max_steps:
    action, action_values = agent.choose_action(state, environment)
    # earned_reward = environment.payout(action) ## only if tracking payouts
    state, finished = environment.step(action)
    steps += 1

    print(f"Day {steps}: options={action_values}")
    print(f"  Chose {action}")

print("Done.")
