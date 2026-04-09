"""
Launching runs
"""

from decision_agent import Environment


environment = Environment(
    width = 5,
    height = 5,
    start = (2, 4),
    rewardPosition = (4, 3)
)

environment.display()