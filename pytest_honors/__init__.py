import enum

import pytest

MAGIC_MARK = "honors"


def pytest_configure(config):
    """Define the "honors" mark."""

    config.addinivalue_line(
        "markers",
        "honors(constraint1, constraint2, ...): mark tests as honoring one or more constraints.",
    )


def pytest_addoption(parser):
    group = parser.getgroup("honors")
    group.addoption(
        "--honors-report",
        action="store",
        dest="honors_report",
        help="write a report of honored constraints to the named file.",
    )


_ITEMS = {}
_RESULTS = {}


def pytest_itemcollected(item):
    markers = item.own_markers
    # if issubclass(markers.__class__, enum.Enum):
    #     markers = [markers]

    for marker in markers:
        # This shouldn't happen if we're only looking at interesting marks, but it's cheap.
        if marker.name != MAGIC_MARK:
            continue

        for constraint in marker.args:
            if not isinstance(constraint, enum.Enum):
                raise TypeError(
                    f"Honored constraints on {item} must be instances of Enum, not {constraint.__class__}."
                )
            _ITEMS.setdefault(constraint.__class__, {}).setdefault(constraint, []).append(item)


def pytest_report_teststatus(report):
    if report.when == "call":
        _RESULTS[report.nodeid] = report.outcome


def python_sessionstart():
    _ITEMS.clear()
    _RESULTS.clear()


def pytest_sessionfinish(session, exitstatus):
    reportfile = "foo.md"

    with open(reportfile, "w") as outfile:
        for line in render_as_markdown():
            outfile.write(line + "\n")


def first_item_name(lst):
    """Return the name of the first item in the list."""
    return lst[0].name


def render_as_markdown():
    for category, details in sorted(_ITEMS.items(), key=lambda x: (x[0].__name__)):
        yield ""
        category_doc = category.__doc__.split("\n")[0]  # type: ignore
        yield f"# {category.__name__} - {category_doc}"

        for instance, tests in sorted(details.items(), key=first_item_name):
            yield ""
            yield f"## {instance.name}: {instance.value}"
            yield ""
            yield "Supporting evidence:"
            yield ""
            for test in sorted(tests, key=lambda x: x.name):
                result = _RESULTS[test.nodeid]
                if result != "passed":
                    result = f"**{result}**"
                yield f"- Name: {test.name}"
                yield f'  Explanation: "{test.obj.__doc__}"'
                yield f"  Path: {test.nodeid}"
                yield f"  Result: {result}"
