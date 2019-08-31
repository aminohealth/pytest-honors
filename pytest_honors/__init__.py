"""The machinery behind the constraints honoring reporting and enforcement."""

import enum
from operator import attrgetter
from typing import Callable, Dict, List, Type

from .constraints import ConstraintsBase

MAGIC_MARK = "honors"
OPT_MARKDOWN_REPORT = "honors_report_markdown"

_ITEMS: Dict[
    # This is a subclass of ConstraintsBase. Putting this at the top level lets us group related
    # constraints together for reporting.
    Type[ConstraintsBase],
    Dict[
        # This is one of the members of the class,
        enum.Enum,
        # ...and this is a list of test functions marked with that member.
        List[Callable],
    ],
] = {}
_RESULTS: Dict[
    # The key of this dict is the pytest-style path to a test, like
    # `tests/test_honors.py::test_passes'.
    str,
    # Values of this dict are each test's results, like 'passed', 'failed', or 'skipped'.
    str,
] = {}


def pytest_configure(config):
    """Define the "honors" mark."""

    config.addinivalue_line(
        "markers",
        "honors(constraint1, constraint2, ...): mark tests as honoring one or more constraints.",
    )


def pytest_addoption(parser):
    """Configure options for command line and pytest.ini options."""

    help_txt = "name of the honored constraints report file to write"
    group = parser.getgroup("honors")
    group.addoption("--honors-report", action="store", dest=OPT_MARKDOWN_REPORT, help=help_txt)
    parser.addini(OPT_MARKDOWN_REPORT, help_txt)


def python_sessionstart():
    """Clear the local cache when starting a testing session."""

    _ITEMS.clear()
    _RESULTS.clear()


def pytest_itemcollected(item):
    """Build a map of all seen tests that are marked as honoring constraints."""

    for marker in item.own_markers:
        # Only look at honors markers
        if marker.name != MAGIC_MARK:
            continue

        for constraint in marker.args:
            # Fail loudly if there's something inside an honors clause but constraints
            if not isinstance(constraint, ConstraintsBase):
                raise TypeError(
                    f"Honored constraints on {item} must be instances of ConstraintsBase, not "
                    f"{constraint.__class__}."
                )
            _ITEMS.setdefault(constraint.__class__, {}).setdefault(constraint, []).append(item)


def pytest_report_teststatus(report):
    """Record the path and result of each test call."""

    # Don't log the results of setting up or tearing down a test, just of running it.
    if report.when == "call":
        _RESULTS[report.nodeid] = report.outcome


def pytest_sessionfinish(session):
    reportfile = session.config.getoption(OPT_MARKDOWN_REPORT) or session.config.getini(
        OPT_MARKDOWN_REPORT
    )
    if not reportfile:
        return

    with open(reportfile, "w") as outfile:
        for line in render_as_markdown(_ITEMS, _RESULTS):
            outfile.write(line + "\n")


def first_item_name(lst):
    """Return the name of the first item in the list."""
    return lst[0].name


def first_item__name__(lst):
    """Return the __name__ of the first item in the list."""
    return lst[0].__name__


def render_as_markdown(items, results):
    """Yield markdown lines of a report on the given items and their results."""

    for category, details in sorted(items.items(), key=first_item__name__):
        yield ""
        category_doc = category.__doc__.split("\n")[0]  # type: ignore
        yield f"# {category.__name__} - {category_doc}"

        for instance, tests in sorted(details.items(), key=first_item_name):
            yield ""
            yield f"## {instance.name}: {instance.value}"
            yield ""
            yield "Supporting evidence:"
            yield ""
            for test in sorted(tests, key=attrgetter("name")):
                result = results[test.nodeid]
                if result != "passed":
                    result = f"**{result}**"
                yield f"- Name: {test.name}"
                yield f'  Explanation: "{test.obj.__doc__}"'
                yield f"  Path: {test.nodeid}"
                yield f"  Result: {result}"
