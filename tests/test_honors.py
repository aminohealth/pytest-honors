"""Test the pytest_honors package."""

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


def test_render_as_markdown():
    """No two keys may have the same values."""

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
