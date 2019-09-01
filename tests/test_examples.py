"""Examples of tests written with honors marks."""

from pytest import mark

from pytest_honors.constraints import ConstraintsGroup
from pytest_honors.constraints.iso27001 import ISO27001Controls


class MyConstraints(ConstraintsGroup):
    """Sample constraints for test purposes."""

    spam = "Does a thing"
    eggs = "Another thing"
    walk = "Funnily"


@mark.honors(MyConstraints.spam, MyConstraints.eggs, ISO27001Controls.A_12_5_3)
def test_passes():
    """This test always passes."""


@mark.honors(MyConstraints.eggs, MyConstraints.walk)
@mark.xfail(strict=True)
def test_fails():
    """This test always fails."""
    assert False
