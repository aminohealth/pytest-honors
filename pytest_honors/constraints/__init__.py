"""Constraints definitions."""

import enum


class ConstraintsBase(enum.Enum):
    """Base class for describing Constraints.

    Although this is currently just an Enum, always inherit from this class instead of directly
    from Enum. It is very likely that new behavior will be added here in the near future."""
