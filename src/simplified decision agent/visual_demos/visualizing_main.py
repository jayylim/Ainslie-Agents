'''
Live run of the multi-sail view from visualise_sails.

At each decision: one sail per foreseeable LL, one scatter per foreseeable SS,
with black dotted lines at decision nodes. Click / keypress advances to the
next day (same stepping loop as visualize_main).

Run from the package root:

    python -m visual_demos.visualizing_main
'''

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


def foreseeable_events(agent, environment, state):
    """Indexed (delay, reward) for each SS / LL in the planning horizon."""
    horizon = agent.get_horizon(state, environment)
    interval = environment.decision_interval
    ss_events = []
    ll_events = []

    for step in range(horizon):
        _, ss_outcomes = environment.simulate(state, "snack")
        for reward, delay in ss_outcomes.values():
            ss_events.append((delay + step * interval, reward))

        _, ll_outcomes = environment.simulate(state, "resist")
        for reward, delay in ll_outcomes.values():
            ll_events.append((delay + step * interval, reward))

    return ss_events, ll_events


def bundle_value_at(agent, events, at_time):
    """Sum of hyperbolic values of rewards still outstanding at `at_time`."""
    return sum(
        agent.value_function(reward, delay - at_time)
        for delay, reward in events
        if delay >= at_time
    )


def plot_ll_sail(axes, agent, delay, aggregate, decision_t, color, *, label=None):
    xs, ys = [], []
    for t in range(decision_t, delay + 1):
        xs.append(t)
        ys.append(agent.value_function(aggregate, delay - t))

    axes.plot(xs, ys, color=color, label=label)
    axes.axvline(delay, linestyle=":", color=color, alpha=0.45)
    axes.axvline(decision_t, linestyle=":", color="black", alpha=0.55)

    tip = ys[-1]
    axes.scatter(delay, tip, s=50, color=color, zorder=5)
    axes.text(delay, tip, f"  {tip:.2f}", color=color, va="bottom", ha="left", size=11)

    left_val = ys[0]
    axes.scatter(decision_t, left_val, s=40, color=color, zorder=5)
    ha = "right" if decision_t == 0 else "left"
    prefix = "" if ha == "right" else "  "
    offset = -1 if ha == "right" else 0
    axes.text(
        decision_t + offset,
        left_val,
        f"{prefix}{left_val:.2f}",
        color=color,
        va="bottom",
        ha=ha,
        size=11,
    )

    return max(ys) if ys else 0


def plot_ss_points(axes, ss_points, color):
    """One scatter per foreseeable SS, height = remaining bundle aggregate."""
    y_max = 0
    for i, (delay, aggregate) in enumerate(ss_points):
        y_max = max(y_max, aggregate)
        label = "snack" if i == 0 else None
        axes.scatter(delay, aggregate, s=55, color=color, zorder=6, label=label)
        axes.text(
            delay,
            aggregate,
            f"  {aggregate:.2f}",
            color=color,
            va="bottom",
            ha="left",
            size=11,
        )
    return y_max


environment = TimelineEnvironment(**env_params)
agent = HypAgent(**agent_params)

state = environment.reset()
finished = False
steps = 0

fig, axes = plt.subplots(figsize=(10, 5))
print("Starting visualisation (click / keypress to advance)...")

while not finished and (max_steps is None or steps < max_steps):
    action, action_values = agent.choose_action(state, environment)
    steps += 1

    ss_events, ll_events = foreseeable_events(agent, environment, state)
    n = len(ll_events)

    ll_sails = [
        (delay, bundle_value_at(agent, ll_events, delay))
        for delay, _ in ll_events
    ]
    ss_points = [
        (delay, bundle_value_at(agent, ss_events, delay))
        for delay, _ in ss_events
    ]

    axes.clear()
    y_max = 0

    for i, (delay, aggregate) in enumerate(ll_sails):
        decision_t = ss_points[i][0]
        peak = plot_ll_sail(
            axes,
            agent,
            delay,
            aggregate,
            decision_t,
            COLORS["resist"],
            label="resist" if i == 0 else None,
        )
        y_max = max(y_max, peak)

    y_max = max(y_max, plot_ss_points(axes, ss_points, COLORS["snack"]))

    x_max = max(
        max((d for d, _ in ll_sails), default=1),
        max((d for d, _ in ss_points), default=1),
    )
    axes.set_xlim(-max(4, x_max * 0.08), x_max + max(4, x_max * 0.08))
    axes.set_ylim(0, y_max * 1.15 if y_max else 1)

    xticks = list(range(0, x_max + 1, 12))
    axes.set_xticks(xticks)
    axes.set_xticklabels([str(t // 24) if t % 24 == 0 else "" for t in xticks])
    axes.set_xlabel("Days from now")
    axes.set_ylabel("Perceived value")
    axes.set_title(
        f"Day {steps}  |  horizon {n}  |  chose {action}"
    )
    axes.legend(loc="upper right")

    print(f"Day {steps}: options={action_values}")
    print(f"  Chose {action}")

    state, finished = environment.step(action)
    plt.pause(0.05)
    plt.waitforbuttonpress()

print("Done.")
plt.show()
