=============
pytest-honors
=============

.. image:: https://img.shields.io/pypi/v/pytest-honors.svg
    :target: https://pypi.org/project/pytest-honors
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-honors.svg
    :target: https://pypi.org/project/pytest-honors
    :alt: Python versions

.. image:: https://travis-ci.org/aminohealth/pytest-honors.svg?branch=master
    :target: https://travis-ci.org/aminohealth/pytest-honors
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/5qaiatbjd76fxrxk/branch/master?svg=true
    :target: https://ci.appveyor.com/project/kstrauser/pytest-honors-p7p8g/branch/master
    :alt: See Build Status on AppVeyor

.. image:: https://readthedocs.org/projects/pytest-honors/badge/?version=latest
    :target: https://pytest-honors.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Report on tests that honor constraints, and guard against regressions

----

Intro
-----

pytest-honors is a `pytest`_ plugin for automatically generating reports showing which of your project's unit tests "honor" (or "prove" or "demonstrate" or "support") various constraints that you care about. It can also be integrated with your build pipeline to make sure that you never accidentally remove the tests that are most important to you.

Below is a summary of features. More information is available at the `pytest-honors documentation`_ page.

Features
--------

* Lightning fast! Since it piggybacks onto pytest's own test discovery and reporting system, it adds almost no measurable overhead to your testing process.
* Generate nicely human-readable Markdown reports, suitable for handing to an auditor.
* Automatically ensure that your test coverage only ever increases with time. Fixed things stay fixed!
* Comes with ISO 27001 control definitions (but it's super easy to add your own).


Requirements
------------

* pytest 3.5.0 or newer.


Installation
------------

You can install "pytest-honors" via `pip`_ from `PyPI`_::

    $ pip install pytest-honors


Usage
-----

You've written several thousand unit tests, but you don't know which are actually *important* to you. Your team could laboriously struggle to keep docs up to date, but realistically that almost never works out as hoped. Even if your documentation is perfect, developers in the middle of a large refactoring project don't want to flip between static text and their code.

pytest-honors wants to help you. For example, given this code::

    import pytest
    from pytest_honors.constraints import ConstraintsGroup

    class MyControls(ConstraintsGroup):
        PasswordsMustBeGood = "We don't want bad passwords"
        EmailAddressesMustBeUnique = "No two users may have the same email"

    @pytest.mark.honors(MyControls.PasswordsMustBeGood)
    def test_password_strength():
        with pytest.raises(ValueError):
            check_password("12345")

    @pytest.mark.honors(MyControls.EmailAddressesMustBeUnique)
    def test_unique_email():
        add_account("User One", "spam@example.com")
        with pytest.raises(ValueError):
            add_account("User Two", "spam@example.com")

In the language of pytest-honors, we say that ``test_password_string`` "honors" the PasswordsMustBeGood constraint and that ``test_unique_email`` honors the EmailAddressesMustBeUnique constraint. This is valuable on its own as developers can tell at a glance that each test actually matters to the overall design of the system, and they're not just there because a new boss wants everyone to reach 100% test coverage. By moving important documentation to a machine-readable format that lives next to the code, we can put that information to work to give you some very useful tools.

When run like ``pytest --honors-report-markdown report.md``, we can get nice, human-readable documentation like:

.. code-block:: text

    # MyControls - An enumeration.

    ## EmailAddressesMustBeUnique: No two users may have the same email

    Supporting evidence:

    - Name: test_unique_email
      Explanation: "None"
      Path: tests/test_important_stuff.py::test_unique_email
      Result: passed

    ## PasswordsMustBeGood: We don't want bad passwords

    Supporting evidence:

    - Name: test_password_strength
      Explanation: "None"
      Path: tests/test_important_stuff.py::test_password_strength
      Result: passed

This shows us all controls that are honored by the tests that we ran. Want to show your auditor that you're checking important controls in your code? Now you have evidence.

When run like ``pytest --honors-store-counts``, pytest-honors saves the number of tests honoring each constraint. Later you can run ``pytest --honors-regression-fail``, and if the coverage for any controls has decreased since the last test run, then pytest fails. Suppose an intern deletes the ``test_unique_email`` unit test. That results in the error::

  ValueError: ['Constraint MyControls.EmailAddressesMustBeUnique honorers count dropped from 1 to 0']

You can integrate this in your CI pipeline and know that a rogue developer isn't deleting the constraints you care about.


Contributing
------------

Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

Especially appreciated, and requiring the least amount of coding experience, would be other constraint definitions so that new users have a pleasant "batteries included" experience.


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-honors" is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/aminohealth/pytest-honors/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project/pytest-honors/
.. _`pytest-honors documentation`: https://pytest-honors.readthedocs.io/en/latest/
