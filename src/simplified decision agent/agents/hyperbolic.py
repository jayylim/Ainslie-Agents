"""
Hyperbolic discounter with a greedy policy.
Acts only through the environment interface (simulate / get_actions).

Distances are in environment units (hours). Future choice nodes are spaced
decision_interval hours apart when aggregating.
"""


class HypAgent:
    def __init__(self, discount_factor=0.8, vision="short", horizon=None):
        self.discount_factor = discount_factor
        self.vision = vision  # "short" or "long"
        self.horizon = horizon  # max # of decisions to plan; None => all remaining if finite

    def value_function(self, reward, distance):
        return reward / (1 + self.discount_factor * distance) # hyperbolic discounting formula

    def get_horizon(self, state, environment):
        """Number of decision nodes counted from `state` (inclusive).
        short vision => always 1 
        long vision  => self.horizon, capped by remaining env decisions if finite.
        """
        if self.vision == "short":
            return 1

        if self.horizon == 0:
            raise ValueError("Horizon cannot be 0")

        interval = getattr(environment, "decision_interval", 1)

        # Finite env: never plan past the last real choice node
        if environment.length is not None:
            remaining_hours = max(environment.length - state, 0)
            remaining_decisions = max(
                (remaining_hours + interval - 1) // interval, 1
            )
            if self.horizon is not None:
                return min(self.horizon, remaining_decisions)
            return remaining_decisions

        if self.horizon is not None:
            return self.horizon

        raise ValueError("Horizon must be set as timeline is infinite") # if the horizon is not set and the environment is infinite, raise an error

    # Array for the horizon of choices agent can simulate
    def choice_horizon(self, state, action, environment):
        """(effective_delay, reward) pairs counted from each `state` (decision node) over the vision horizon.

        Delays are relative to the current decision (same terms as aggregate_value).
        """
        events = []
        current_state = state
        horizon = self.get_horizon(state, environment)
        interval = getattr(environment, "decision_interval", 1)

        for t in range(horizon):
            next_state, outcomes = environment.simulate(current_state, action)
            for reward, delay in outcomes.values():
                events.append((delay + t * interval, reward))
            current_state = next_state

        return events

    # making a bundled choice across the horizon
    def aggregate_value(self, state, action, environment):
        """Sum discounted value of repeating `action` over the vision horizon."""
        return sum(
            self.value_function(reward, delay)
            for delay, reward in self.choice_horizon(state, action, environment)
        )

    def evaluate_action(self, state, action, environment):
        # short vision: evaluate the immediate reward and skip aggregate
        if self.vision == "short":
            _, outcomes = environment.simulate(state, action)
            return max(
                self.value_function(reward, distance)
                for reward, distance in outcomes.values()
            )
        if self.vision == "long":
            return self.aggregate_value(state, action, environment)
        raise ValueError(f"Unknown vision: {self.vision}")

    def choose_action(self, state, environment):
        best_action = None
        best_value = float("-inf")
        action_values = {}

        # loop through all actions and evaluate them
        for action in environment.get_actions(state):
            value = self.evaluate_action(state, action, environment)
            action_values[action] = float(value)
            if value > best_value:
                best_value = value
                best_action = action

        return best_action, action_values
