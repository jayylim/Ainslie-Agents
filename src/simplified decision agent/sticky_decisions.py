"""
Factoring in stickiness into the aggregated decision.

Shows the agent's computed values for the first decision node.

Snapshot compputation of t=1: Does not step the environment. 
Reuses main.py, hyperbolic.py, and timeline.py params and helpers.

Definitions and notation (see legend at bottom of this docstring):

    s   = P(a_{t+1} = a_t)                         stickiness
    stick_p_t = 1/2 + 1/2 * (2s - 1)^t                   persistence of today's action (collapses all possible trees where you arrive here)
    V_hyp(reward, delay) = reward / (1 + discount_factor * delay)
    day_t value = stick_p_t * V_hyp(reward_a, delay_a + t in days) + (1-stick_p_t) * V_hyp(reward_b, delay_b + t in days) # the value of ending on said action at day_t
    V(action) = sum_{t=0}^{horizon-1} [
             stick_p_t     * V_hyp(reward_a, delay_a + t * decision_interval)
           + (1-stick_p_t) * V_hyp(reward_b, delay_b + t * decision_interval)
           ]                                       sticky bundle value

When s = 1, V(a) matches the demonstration in main.py (pure commitment).

Run from the package root:

    python -m sticky_decisions

Legend
------
s                  stickiness; P(next decision equals current decision)
a                  candidate action being valued today (snack or resist)
b                  the other action (not a)
a_t                action on foresight day t (random under stickiness)
t                  foresight day index, t = 0 .. horizon-1 (0 = today)
sticking           probability that on day t, the agent makes the same choice as day 0
horizon            planning horizon (# of decision nodes), from get_horizon
decision_interval  hours between choice nodes (Delta)
discount_factor    k in V_hyp
reward_a, delay_a  reward magnitude and base delay for action a's offer
reward_b, delay_b  same for action b
persistence        P(a_t = a | a_0 = a); derived from s
V_hyp              hyperbolic discounted value of one (reward, delay) pair
V(a)               expected bundled value of choosing a today under s
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.hyperbolic import HypAgent
from environments.timeline import TimelineEnvironment
from main import agent_params, env_params

# === Stickiness s (edit here) ===
s = 0.8  # in [0, 1]; s = 1 recovers pure long-vision bundling

OTHER = {"snack": "resist", "resist": "snack"}  # b given a


def stick_p_t(s, t):
    # P(a_t = a | a_0 = a) = 1/2 *(1 + (2s - 1)^t)
    return 0.5 * (1 + (2 * s - 1) ** t)


def offer(agent, environment, state, action, t):
    # Hyperbolic value of `action`'s offer delayed by t decision intervals.
    _, outcomes = environment.simulate(state, action)
    decision_interval = environment.decision_interval
    total = 0.0
    for reward, delay in outcomes.values():
        total += agent.value_function(
            reward, delay + t * decision_interval
        )  # V_hyp(reward, delay + t*decision_interval)
    return total


def V(agent, environment, state, a, s):
    """
    Sticky bundle value V(a): expected sum of day-t offers under stickiness s.
    a is today's candidate; b is the other action.
    """
    horizon = agent.get_horizon(state, environment)
    b = OTHER[a]
    total = 0.0
    breakdown = []

    for t in range(horizon):
        sticking = stick_p_t(s, t)
        v_same = offer(agent, environment, state, a, t)
        v_other = offer(agent, environment, state, b, t)
        expected_day_value = sticking * v_same + (1 - sticking) * v_other
        total += expected_day_value
        breakdown.append(
            {
                "t": t,
                "sticking": sticking,
                "v_same": v_same,
                "v_other": v_other,
                "expected_day_value": expected_day_value,
            }
        )

    return total, breakdown


def greedy_from_values(action_values):
    return max(action_values, key=action_values.get)


def main():
    environment = TimelineEnvironment(**env_params)
    agent = HypAgent(**agent_params)
    state = environment.reset()
    horizon = agent.get_horizon(state, environment)
    decision_interval = environment.decision_interval
    discount_factor = agent.discount_factor

    print(f"state={state}h  horizon={horizon}  stickiness={s}")
    print(f"decision_interval={decision_interval}h  discount_factor={discount_factor}")
    print()

    V_values = {}
    for action in environment.get_actions(state):
        value, breakdown = V(agent, environment, state, action, s)
        V_values[action] = value
        b = OTHER[action]

        # print values for sanity checking
        print(f"--- Evaluating '{action}' today ---")
        print(
            f"{'t':>3}  {'sticking':>8}  {f'V_{{{action}}}':>10}  {f'V_{{{b}}}':>10}  {'EV of day':>10}"
        )
        for row in breakdown:
            print(
                f"{row['t']:3d}  {row['sticking']:8.4f}  {row['v_same']:10.4f}  "
                f"{row['v_other']:10.4f}  {row['expected_day_value']:10.4f}"
            )
        print(f"V({action}) = {value:.6f}\n")

    choice = greedy_from_values(V_values)

    # print final results
    print(
        f"Sticky V: snack={V_values['snack']:.6f}  "
        f"resist={V_values['resist']:.6f}"
    )
    print(f"Would choose {choice}")
    print()

    # Baseline (i.e. Main) pure commitment via unchanged HypAgent (implicit s = 1)
    baseline_action, baseline_values = agent.choose_action(state, environment)
    print(
        f"Baseline (agent aggregate_value, s=1): "
        f"snack={baseline_values['snack']:.6f}  "
        f"resist={baseline_values['resist']:.6f}"
    )
    print(f"Baseline would choose {baseline_action}")

    if abs(s - 1) < 1e-12:
        ok = all(
            abs(V_values[a] - baseline_values[a]) < 1e-9 for a in V_values
        )
        print(
            f"Sanity s=1 match: {'PASS' if ok else 'FAIL'} "
            f"(V(a) vs HypAgent.choose_action)"
        )


if __name__ == "__main__":
    main()
