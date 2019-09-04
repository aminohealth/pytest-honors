"""Test the pytest_honors package."""

from typing import NamedTuple
from unittest import mock

import pytest

import pytest_honors
from pytest_honors.constraints import ConstraintsGroup


class SomeControls(ConstraintsGroup):
    """Some things are here."""

    spam = "Spam"
    eggs = "Eggs"


class OtherControls(ConstraintsGroup):
    """Other things are here."""

    favorite_color = "blue"


class Func1:
    """Function one."""

    nodeid = "::func1"
    name = "Func uno"

    def obj(self):
        """Func1's docs"""


class Func2:
    """Function two."""

    nodeid = "::func2"
    name = "Func dos"

    def obj(self):
        """Func2's docs"""


class MockReport(NamedTuple):
    nodeid: str
    when: str
    outcome: str


@pytest.mark.parametrize(
    "nodeid,when,outcome,save",
    [
        ("test1", "setup", "passed", False),
        ("test2", "call", "skipped", True),
        ("test3", "teardown", "failed", False),
    ],
)
def test_pytest_report_teststatus(nodeid, when, outcome, save):
    """Test statuses are recorded after call."""

    expected = {None: None}
    with mock.patch.dict(pytest_honors._RESULTS, expected, clear=True):
        pytest_honors.pytest_report_teststatus(MockReport(nodeid, when, outcome))
        if save:
            expected[nodeid] = outcome
        assert pytest_honors._RESULTS == expected


def test_make_counts():
    """make_counts summarizes control honorer counts correctly."""

    items = {
        SomeControls: {
            SomeControls.spam: ["test_one", "test_two"],
            SomeControls.eggs: ["test_three"],
        },
        OtherControls: {OtherControls.favorite_color: ["test_one", "test_three"]},
    }

    assert pytest_honors.make_counts(items) == {
        "SomeControls.spam": 2,
        "SomeControls.eggs": 1,
        "OtherControls.favorite_color": 2,
    }


def test_fail_on_regression():
    """Decreasing honorers counts gives the expected error."""

    old_results = {"spam": 10, "eggs": 10}
    new_results = {"spam": 9, "eggs": 8}

    with pytest.raises(ValueError) as error:
        pytest_honors.fail_on_regressions(old_results, new_results)

    assert error.value.args == (
        [
            "Constraint 'eggs' honorers count dropped from 10 to 8",
            "Constraint 'spam' honorers count dropped from 10 to 9",
        ],
    )


def test_render_as_markdown():
    """Known results yield the expected report."""

    items = {
        SomeControls: {SomeControls.spam: [Func1], SomeControls.eggs: [Func2]},
        OtherControls: {OtherControls.favorite_color: [Func2, Func1]},
    }

    results = {"::func1": "passed", "::func2": "absconded"}

    report = list(pytest_honors.render_as_markdown(items, results))

    assert (
        "\n".join(report)
        == """
# OtherControls - Other things are here.

## favorite_color: blue

Supporting evidence:

- Name: Func dos
  Explanation: "Func2's docs"
  Path: ::func2
  Result: **absconded**
- Name: Func uno
  Explanation: "Func1's docs"
  Path: ::func1
  Result: passed

---

# SomeControls - Some things are here.

## eggs: Eggs

Supporting evidence:

- Name: Func dos
  Explanation: "Func2's docs"
  Path: ::func2
  Result: **absconded**

## spam: Spam

Supporting evidence:

- Name: Func uno
  Explanation: "Func1's docs"
  Path: ::func1
  Result: passed"""
    )
