import enum
from operator import attrgetter

MAGIC_MARK = "honors"
REPORT_CONFIG = "honors_report"

_ITEMS = {}
_RESULTS = {}


def pytest_configure(config):
    """Define the "honors" mark."""

    config.addinivalue_line(
        "markers",
        "honors(constraint1, constraint2, ...): mark tests as honoring one or more constraints.",
    )


def pytest_addoption(parser):
    help_txt = "name of the honored constraints report file to write"
    group = parser.getgroup("honors")
    group.addoption("--honors-report", action="store", dest=REPORT_CONFIG, help=help_txt)
    parser.addini(REPORT_CONFIG, help_txt)


def pytest_itemcollected(item):
    for marker in item.own_markers:
        # This shouldn't happen if we're only looking at interesting marks, but it's cheap.
        if marker.name != MAGIC_MARK:
            continue

        for constraint in marker.args:
            if not isinstance(constraint, enum.Enum):
                raise TypeError(
                    f"Honored constraints on {item} must be instances of Enum, not "
                    f"{constraint.__class__}."
                )
            _ITEMS.setdefault(constraint.__class__, {}).setdefault(constraint, []).append(item)


def pytest_report_teststatus(report):
    if report.when == "call":
        _RESULTS[report.nodeid] = report.outcome


def python_sessionstart():
    _ITEMS.clear()
    _RESULTS.clear()


def pytest_sessionfinish(session):
    reportfile = session.config.getoption(REPORT_CONFIG) or session.config.getini(REPORT_CONFIG)
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
