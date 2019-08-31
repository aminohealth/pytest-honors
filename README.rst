=============
pytest-honors
=============

.. image:: https://img.shields.io/pypi/v/pytest-honors.svg
    :target: https://pypi.org/project/pytest-honors
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-honors.svg
    :target: https://pypi.org/project/pytest-honors
    :alt: Python versions

.. image:: https://travis-ci.org/kstrauser/pytest-honors.svg?branch=master
    :target: https://travis-ci.org/kstrauser/pytest-honors
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/kstrauser/pytest-honors?branch=master
    :target: https://ci.appveyor.com/project/kstrauser/pytest-honors/branch/master
    :alt: See Build Status on AppVeyor

Enforce coverage and report on tests that honor constraints

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* TODO


Requirements
------------

* TODO


Installation
------------

You can install "pytest-honors" via `pip`_ from `PyPI`_::

    $ pip install pytest-honors


Usage
-----

You've written several thousand unit tests, but you don't know which are actually *important* to you. Your team could laboriously struggle to keep docs up to date, but realistically that almost never works out as hoped. Even if your documentation is perfect, develops in the middle of a large refactoring don't want to flip between static text and their code.

pytest-honors wants to help you. For example, given this code::

    import pytest
    from pytest_honors.constraints import ConstraintsBase

    class MyControls(ConstraintsBase):
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

In the language of pytest-honors, we say that ``test_password_string`` "honors" the PasswordsMustBeGood constraint and that ``test_unique_email`` honors the EmailAddressesMustBeUnique constraint. This is valuable on its own, as developers can tell at a glance that each test actually matters to the overall design of the system and they're not just there because a new boss wants everyone to reach 100% test coverage.But pytest-honors gives you some very important tools. By moving important documentation to a machine-readable, we can put that information to work.

When run like ``pytest --honors-report-markdown report.md``, we can get nice, human-readable documentation like:

.. code-block:: markdown

    # MyControls - An enumeration.

    ## EmailAddressesMustBeUnique: No two users may have the same email

    Supporting evidence:

    - Name: test_unique_email
      Explanation: "None"
      Path: tests/test_meat.py::test_unique_email
      Result: passed

    ## PasswordsMustBeGood: We don't want bad passwords

    Supporting evidence:

    - Name: test_password_strength
      Explanation: "None"
      Path: tests/test_meat.py::test_password_strength
      Result: passed

This shows us all controls that are honored by the tests that we ran. Want to show your auditor that you're checking important controls in your code? Now you have evidence.

When run like ``pytest --honors-regression-fail``, if the coverage for any controls has decreased since the last test run, the pytest-honors fails. Suppose an intern deletes the ``test_unique_email`` unit test. That results in the error::

    ValueError: ['Constraint MyControls.EmailAddressesMustBeUnique count dropped from 1 to 0']

You can integrate this in your CI pipeline and know that a rogue developer isn't deleting the constraints you care about.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-honors" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/kstrauser/pytest-honors/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
