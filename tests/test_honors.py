from pytest_honors.constraints import ConstraintsBase
from pytest_honors.constraints.iso27001 import ISO27001Controls

import pytest


class MyConstraints(ConstraintsBase):
    """Sample constraints for test purposes."""

    spam = "Does a thing"
    eggs = "Another thing"
    walk = "Funnily"


@pytest.mark.honors(MyConstraints.spam, MyConstraints.eggs, ISO27001Controls.A_12_5_3)
def test_passes():
    """This test always passes."""


@pytest.mark.honors(MyConstraints.eggs, MyConstraints.walk)
@pytest.mark.xfail(strict=True)
def test_fails():
    """This test always fails."""
    assert False
