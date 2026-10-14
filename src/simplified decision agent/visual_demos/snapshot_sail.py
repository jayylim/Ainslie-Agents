"""
Classic Ainslie sail from day-1 horizon aggregates.

The agent still plans over its vision horizon from day 1. Those outcomes are
collapsed into two magnitudes for a simple comparison:

  - resist (LL): one hyperbolic curve whose peak is the value of the whole
    LL bundle at the first LL delivery (≈15 + residual later LLs)
  - snack (SS): one dot at t=0 with height = aggregated SS value

No stepping through the environment.

Run from the package root:

    python -m visual_demos.snapshot_sail
"""

import matplotlib
import matplotlib.pyplot as plt

import sys
from pathlib import Path

# Debugger / direct run put visual_demos/ on sys.path; package root is one up
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    matplotlib.use("MacOSX")
except Exception:
    pass

from agents.hyperbolic import HypAgent
from environments.timeline import TimelineEnvironment
from main import agent_params, env_params

COLORS = {"snack": "#c44e52", "resist": "#4c72b0"}


def horizon_events(agent, environment, state, action):
    """(delay, reward) pairs the agent counts for this action from day 1."""
    if agent.vision == "short":
        _, outcomes = environment.simulate(state, action)
        return [(delay, reward) for reward, delay in outcomes.values()]

    events = []
    horizon = agent.get_horizon(state, environment)
    interval = environment.decision_interval
    for t in range(horizon):
        _, outcomes = environment.simulate(state, action)
        for reward, delay in outcomes.values():
            events.append((delay + t * interval, reward))
    return events


def bundle_value_at(agent, events, at_time):
    """Sum of hyperbolic values of rewards still outstanding at `at_time`."""
    return sum(
        agent.value_function(reward, delay - at_time)
        for delay, reward in events
        if delay >= at_time
    )


environment = TimelineEnvironment(**env_params)
agent = HypAgent(**agent_params)
state = environment.reset()

action, action_values = agent.choose_action(state, environment)

ss_events = horizon_events(agent, environment, state, "snack")
ll_events = horizon_events(agent, environment, state, "resist")

ll_delay = environment.rewards["LL"]["delay"]
# Peak of the classic sail = whole LL bundle valued when the first LL arrives
ll_value = bundle_value_at(agent, ll_events, ll_delay)
# SS is immediate: day-1 aggregate (same as action_values["snack"])
ss_value = bundle_value_at(agent, ss_events, 0)

fig, axes = plt.subplots()

# LL sail: treat that bundle peak as a single delayed reward
xs, ys = [], []
for t in range(ll_delay + 1):
    distance = ll_delay - t
    value = agent.value_function(ll_value, distance)
    xs.append(t)
    ys.append(value)

axes.plot(xs, ys, color=COLORS["resist"], label="resist")
axes.axvline(ll_delay, linestyle=":", color=COLORS["resist"], alpha=0.5)

perceived_ll = ys[0]
axes.scatter(0, perceived_ll, s=50, color=COLORS["resist"], zorder=5)
axes.text(-1, perceived_ll, f"{perceived_ll:.2f}", color=COLORS["resist"],
          va="bottom", ha="right", size=12)
axes.scatter(ll_delay, ys[-1], s=50, color=COLORS["resist"], zorder=5)
axes.text(ll_delay, ys[-1], f"  {ys[-1]:.2f}", color=COLORS["resist"],
          va="bottom", ha="left", size=12)

# SS: single dot at the day-1 aggregate
axes.scatter(0, ss_value, s=50, color=COLORS["snack"], zorder=5, label="snack")
axes.text(-1, ss_value, f"{ss_value:.2f}", color=COLORS["snack"],
          va="bottom", ha="right", size=12)

y_max = max(ll_value, ss_value)
axes.set_xlim(-max(2, ll_delay * 0.2), ll_delay + max(1, ll_delay * 0.15))
axes.set_ylim(0, y_max * 1.15 if y_max else 1)
axes.set_xlabel("Hours from now")
axes.set_ylabel("Perceived value")
axes.set_title(f"Bundled value on day 1 |  Agent would choose {action}")
axes.legend(loc="upper left")

print(f"Perceived values on day 1: snack={action_values['snack']:.4f}  "
      f"resist={action_values['resist']:.4f}")
print(f"Aggregated valuesof each option on day 1:    snack={ss_value:.4f}  resist peak={ll_value:.4f}")
print(f"Would choose {action}")

plt.show()

