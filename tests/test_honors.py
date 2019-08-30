import enum

import pytest


class MyConstraints(enum.Enum):
    """Sample constraints for test purposes."""

    spam = "Does a thing"
    eggs = "Another thing"
    walk = "Funnily"


@pytest.mark.honors(MyConstraints.spam, MyConstraints.eggs)
def test_passes():
    """This test always passes."""


@pytest.mark.honors(MyConstraints.eggs, MyConstraints.walk)
def test_fails():
    """This test always fails."""
    assert False
