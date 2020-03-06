"""The machinery behind the constraints honoring reporting and enforcement."""

import enum
from operator import attrgetter
from typing import Callable, Dict, List, Type

from pytest import ExitCode, PytestWarning

from .constraints import ConstraintsGroup

MAGIC_MARK = "honors"
OPT_MARKDOWN_REPORT = "honors_report_markdown"
OPT_REGRESSION_FAIL = "honors_regression_fail"
OPT_STORE_COUNTS = "honors_store_counts"
CACHE_KEY_COUNTS = "honors/counts"

_ITEMS: Dict[
    # This is a subclass of ConstraintsGroup. Putting this at the top level lets us group related
    # constraints together for reporting.
    Type[ConstraintsGroup],
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


# pytest hooks

# pytest inspects its plugins for functions with specific names. If it finds them, it calls
# those functions at the appropriate point in its processing flow. For a full explanation of these
# "hooks", see https://doc.pytest.org/en/latest/reference.html


def pytest_configure(config):
    """Define the "honors" mark."""

    config.addinivalue_line(
        "markers",
        "honors(constraint1, constraint2, ...): mark tests as honoring one or more constraints.",
    )


def pytest_addoption(parser):
    """Configure options for command line and pytest.ini options."""

    group = parser.getgroup("honors")

    report_help = "name of the honored constraints report file to write"
    group.addoption(
        "--honors-report-markdown", action="store", dest=OPT_MARKDOWN_REPORT, help=report_help
    )
    parser.addini(OPT_MARKDOWN_REPORT, report_help)

    fail_help = "if set, fail tests when any constraint counts decrease"
    group.addoption(
        "--honors-regression-fail", action="store_true", dest=OPT_REGRESSION_FAIL, help=fail_help
    )
    parser.addini(OPT_REGRESSION_FAIL, fail_help, type="bool", default=False)

    write_help = "if set, store honorers counts for later comparison"
    group.addoption(
        "--honors-store-counts", action="store_true", dest=OPT_STORE_COUNTS, help=write_help
    )
    parser.addini(OPT_STORE_COUNTS, write_help, type="bool", default=False)


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

        for arg in marker.args:
            # Fail loudly if there's something inside an honors clause but constraints
            if not isinstance(arg, ConstraintsGroup):
                raise TypeError(
                    f"Honored constraints on {item} must be instances of ConstraintsGroup, not "
                    f"{arg.__class__}."
                )
            _ITEMS.setdefault(arg.__class__, {}).setdefault(arg, []).append(item)


def pytest_report_teststatus(report):
    """Record the path and result of each test call."""

    # Don't log the results of setting up or tearing down a test, just of running it.
    if report.when == "call":
        _RESULTS[report.nodeid] = report.outcome


def pytest_sessionfinish(session, exitstatus):
    """Report on or validate constraints coverage."""

    if exitstatus not in {ExitCode.OK, ExitCode.TESTS_FAILED}:
        return

    reportfile = get_config_item(session, OPT_MARKDOWN_REPORT)
    if reportfile:
        with open(reportfile, "w") as outfile:
            for line in render_as_markdown(_ITEMS, _RESULTS):
                outfile.write(line + "\n")

    new_counts = make_counts(_ITEMS)
    if get_config_item(session, OPT_REGRESSION_FAIL):
        old_counts = get_old_counts(session)
        fail_on_regressions(old_counts, new_counts)

    if get_config_item(session, OPT_STORE_COUNTS):
        session.config.cache.set(CACHE_KEY_COUNTS, new_counts)


def get_old_counts(session):
    """Return the previously saved honorers counts."""

    return session.config.cache.get(CACHE_KEY_COUNTS, {})


def make_counts(items):
    """Return a dict of string constraint names to the count of their honorers."""

    return {
        f"{constraint.__class__.__name__}.{constraint.name}": len(tests)
        for group_members in items.values()
        for constraint, tests in group_members.items()
    }


def fail_on_regressions(old_counts, new_counts):
    """Raise a ValueError if any constraint's honorers count decreased from the previous run."""

    errors = []
    for key, old_count in old_counts.items():
        new_count = new_counts.get(key, 0)
        if new_count < old_count:
            errors.append(
                f"Constraint {key!r} honorers count dropped from {old_count} to {new_count}"
            )
    if errors:
        raise ValueError(sorted(errors))


def render_as_markdown(items, results):
    """Yield markdown lines of a report on the given items and their results."""

    first = True
    for constraint_group, group_members in sorted(items.items(), key=key__name__):
        if first:
            first = False
        else:
            yield ""
            yield "---"
        yield ""
        constraint_group_doc = constraint_group.__doc__.split("\n")[0]  # type: ignore
        yield f"# {constraint_group.__name__} - {constraint_group_doc}"

        for constraint, tests in sorted(group_members.items(), key=key_name):
            yield ""
            yield f"## {constraint.name}: {constraint.value}"
            yield ""
            yield "Supporting evidence:"
            yield ""
            for test in sorted(tests, key=attrgetter("name")):
                try:
                    result = results[test.nodeid]
                except KeyError:
                    test.warn(
                        PytestWarning(
                            "An honoring node can't be included in the report because it failed."
                        )
                    )
                    continue
                if result != "passed":
                    result = f"**{result}**"
                yield f"- Name: {test.name}"
                yield f'  Explanation: "{test.obj.__doc__}"'
                yield f"  Path: {test.nodeid}"
                yield f"  Result: {result}"


# Helpers


def get_config_item(session, name):
    """Return the given config item from either the command line or pytest.ini"""

    value = session.config.getoption(name)
    if value is None:
        value = session.config.getini(name)
    return value


def key_name(tpl):
    """Return the name of the first item in the tuple."""

    return tpl[0].name


def key__name__(tpl):
    """Return the __name__ of the first item in the tuple."""

    return tpl[0].__name__
