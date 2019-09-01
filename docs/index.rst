.. pytest-honors documentation master file, created by
   sphinx-quickstart on Thu Oct  1 00:43:18 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pytest-honors
=============

pytest-honors reports on tests that honor constraints and guards against regressions. It's a `pytest`_ plugin for automatically generating reports showing which of your project's unit tests "honor" (or "prove" or "demonstrate" or "support") various constraints that you care about. It can also be integrated with your build pipeline to make sure that you never accidentally remove the tests that are most important to you.

What it does
============

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


Terminology
===========

For explicitness:

constraint
  A condition -- maybe a design requirement, or a security control, or a contractual obligation -- that must be met at all times.

constraint group
  A namespace of constraints that logically belong together.

honors
  A test "honors" a constraint when it can be used to demonstrate that a constraint is being met.

honorers
  The collection of tests that honor a particular constraint or constraint group.


Code usage
==========

To build your own collections of constraints, import and subclass ``pytest_honors.constraints.ConstraintsGroup`` as in the `What it does`_ example above::

  from pytest_honors.constraints import ConstraintsGroup

  class MyControls(ConstraintsGroup):
      PasswordsMustBeGood = "We don't want bad passwords"
      EmailAddressesMustBeUnique = "No two users may have the same email"

pytest-honors adds a new ``honors`` marker that you can use to add one or more constraints to a test::

  @pytest.mark.honors(
      MyControls.PasswordsMustBeGood,
      MyControls.EmailAddressesMustBeUnique
  )
  def test_everything():
      assert check_password(...)
      assert multiple_accounts_with_same_email_fail()

That's it! Again, even if you don't use any other pytest-honors features, now you have a consistent, easily searchable way of marking your most important tests. Perhaps these are the ones that demonstrate the underlying foundation of your whole project, or they identify security requirements that can't ever be casually dismissed without significant planning, or they prove that a serious bug has been fixed and can't recur. In any case, it would be bad if a well-meaning developer removed those tests, especially during a large refactoring where the changes might get lost in the shuffle.


Command line usage
==================

Once you've annotated your tests, use the pytest-honors pytest plugin to make them work for you. It adds three new options to your pytest command line (or `pytest.ini`_):

Reporting
---------

``pytest --honors-report-markdown report.md`` generates human-readable documentation like:

.. code-block:: markdown

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

Remembering what it found
-------------------------

``pytest --honors-store-counts`` causes pytest-honors to store information about the number of tests honoring each constraint so that it can compare the results to future runs. pytest-honors will only write the information at the end of a test run that finishes successfully (even if some tests fail). If the testing session ends unexpectedly -- perhaps you hit ctrl-C to stop a test run that has gone horribly wrong -- then it won't store the possibly-corrupt results.

Note that you probably don't want to do this during regular development if you're only executing a few specific tests for code you're actively working on. You'd most likely want to use this option when you're running *all* of your normal tests, perhaps as part of your CI process.

Keeping fixed things fixed
--------------------------

``pytest --honors-regression-fail`` uses the count information from a previous pytest run to compare against the current testing session. If the coverage for any controls has decreased since the last test run, then pytest fails. Suppose an intern deletes the ``test_unique_email`` unit test. That results in the error::

  ValueError: [
      'Constraint MyControls.EmailAddressesMustBeUnique honorers count dropped from 1 to 0'
  ]

You can integrate this in your CI pipeline and know that a rogue developer isn't deleting the constraints you care about.


Installation
============

Install with `pip`_ (package on `PyPI`_; source at `GitHub`_)::

  $ pip install pytest-honors


Built-in constraint groups
==========================

pytest-honors comes with a set of ISO 27001 control definitions. A long-term goal of the project is to serve as a convenient collection of standard constraints.


Contributing
============

Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

Especially appreciated, and requiring the least amount of coding experience, would be other constraint definitions so that new users have a pleasant "batteries included" experience.

All code is formatted with `Black`_.


Copyright
=========

pytest-honors is a project of (and copyright 2019 by) `Amino`_.

Standards referenced by constraints included in the project are owned by their respective authors.


License
=======

Distributed under the terms of the `MIT`_ license, "pytest-honors" is free and open source software.


History
=======

v0.1.2, 2019-09-01: Cleanup and more documentation.

v0.1.0 / v0.1.1, 2019-08-31: Initial public releases.

.. Contents:

.. .. toctree::
..    :maxdepth: 2

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

.. _`Amino`: https://amino.com/
.. _`Black`: https://github.com/psf/black
.. _`GitHub`: https://github.com/aminohealth/pytest-honors
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project/pytest-honors/
.. _`pytest.ini`: https://docs.pytest.org/en/latest/customize.html
.. _`pytest`: https://github.com/pytest-dev/pytest
