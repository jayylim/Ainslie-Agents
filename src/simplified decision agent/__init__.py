"""Simplified hyperbolic discounting demo on a memoryless SS/LL timeline."""

from .environments.timeline import TimelineEnvironment
from .agents.hyperbolic import HypAgent

__all__ = ["TimelineEnvironment", "HypAgent"]
