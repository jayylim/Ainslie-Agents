"""
Plot the hyperbolic value curve at each decision from main.py.

Same params / agent / environment as main. At each decision point, draws the
sail for snack (SS) and resist (LL) — one curve per option, already aggregated
over the agent's horizon when vision is long.

Run from the package root:

    python -m visual_demos.visualize_main

Or use the "visualize_main" launch config in .vscode/launch.json.

Click / keypress to advance to the next decision.
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
from main import agent_params, env_params, max_steps

COLORS = {"snack": "#c44e52", "resist": "#4c72b0"}


def decision_events(agent, environment, state, action):
    """(delay, reward) pairs behind the agent's value for this action."""
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


def mark_point(axes, x, y, color, *, text_x=None, ha="left"):
    """Scatter + value label at a sail landmark."""
    axes.scatter(x, y, s=50, color=color, zorder=5)
    tx = x if text_x is None else text_x
    prefix = "" if ha == "right" else "  "
    axes.text(tx, y, f"{prefix}{y:.2f}", color=color, va="bottom", ha=ha, size=12)


def plot_sail(axes, agent, events, color, label, perceived):
    """One simple_hyperbolic-style sail for the current decision."""
    t_max = max((delay for delay, _ in events), default=0)
    t_max = max(t_max, 1)

    xs, ys = [], []
    for t in range(t_max + 1):
        value = sum(
            agent.value_function(reward, delay - t)
            for delay, reward in events
            if delay >= t
        )
        xs.append(t)
        ys.append(value)

    axes.plot(xs, ys, color=color, label=label)

    # Dotted lines at each LL delivery
    if label == "resist":
        for delay, _ in events:
            axes.axvline(delay, linestyle=":", color=color, alpha=0.5)

    mark_point(axes, 0, perceived, color, text_x=-10, ha="right")

    # Furthermost tip of the sail (both SS and LL)
    if ys:
        mark_point(axes, xs[-1], ys[-1], color)

    # Nearest LL delivery tip (skip if it coincides with t=0 or the far tip)
    if label == "resist" and events:
        near_x = min(delay for delay, _ in events)
        if 0 < near_x < xs[-1]:
            mark_point(axes, near_x, ys[near_x], color)

    return max(ys) if ys else perceived


environment = TimelineEnvironment(**env_params)
agent = HypAgent(**agent_params)

state = environment.reset()
finished = False
steps = 0

# Getting x-max
horizon_decisions = agent.get_horizon(state, environment)
interval = environment.decision_interval
max_reward_delay = max(r["delay"] for r in environment.rewards.values())
x_max = max_reward_delay + (horizon_decisions - 1) * interval

# Plotting while running
fig, axes = plt.subplots()
print("Starting visualisation (click / keypress to advance)...")

while not finished and (max_steps is None or steps < max_steps): 
    action, action_values = agent.choose_action(state, environment)
    steps += 1

    axes.clear()
    y_max = 0
    for option in environment.get_actions(state):
        events = decision_events(agent, environment, state, option)
        peak = plot_sail(
            axes,
            agent,
            events,
            COLORS[option],
            option,
            action_values[option],
        )
        y_max = max(y_max, peak)

    axes.set_xlim(-28, x_max+10)
    axes.set_ylim(0, y_max * 1.15 if y_max else 1)
    # Tick every 12h; label only every 24h, shown in days
    xticks = list(range(0, x_max + 1, 12))
    axes.set_xticks(xticks)
    axes.set_xticklabels(
        [str(t // 24) if t % 24 == 0 else "" for t in xticks]
    )
    axes.set_xlabel("Days from now")
    axes.set_ylabel("Perceived value")
    axes.set_title(f"Day {steps}  |  chose {action}")
    axes.legend(loc="upper right")

    print(f"Day {steps}: options={action_values}")
    print(f"  Chose {action}")

    state, finished = environment.step(action)
    plt.pause(0.05)
    plt.waitforbuttonpress()

print("Done.")
plt.show()
