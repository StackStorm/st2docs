Testing
=======

|st2| has multiple types of tests. To run a particular test suite we use Makefile targets.
Underneath, those make targets create a virtual environment, install the required Python
dependencies and use ``nose`` Python test runner to run the tests.

Unit tests
----------

Unit tests exercise small units/pieces of code (usually those are functions) and don't require
any services or 3rd party dependencies to run. Besides manipulating the state in memory, they
usually have no other side affects.

In cases where a unit you are testing requires a service to run, you should use the ``mock``
library to mock the service and the result.

Note: Currently some of the unit tests require database (MongoDB) and message bus (RabbitMQ) to
run. We are in process of moving those tests to the integration test suite.

Unit tests are located in ``<component>/tests/unit/``, e.g. ``st2api/tests/unit/``.

Integration tests
-----------------

Integration tests exercise small pieces of code which require some |st2| services such as a
database and message bus to run. Usually they have side affects (e.g. changing the state in
the db, etc.).

Integration tests are located in ``<component>/tests/integration``, e.g.
``st2actions/tests/integration/``.

End-to-end tests
----------------

End-to-end tests exercise the system as a whole, and require all the |st2| services and
dependencies (database, message bus, etc.) to run.

Usually they exercise the API and the system using the CLI and/or the Python
API client.

Running all Tests
-----------------

To run all tests, run the following command:

.. sourcecode:: bash

    make pytests

Running all Unit Tests
----------------------

To run all unit tests, run the following command:

.. sourcecode:: bash

    make unit-tests

Running all Integration Tests
-----------------------------

To run all integration tests, run the following command:

.. sourcecode:: bash

    make itests

Running all Tests in a Test File
---------------------------------

To run all the tests located in a single test file, move to the root of the
repository and run the following command:

.. sourcecode:: bash

    nosetests --nocapture <path to the test file>

For example:

.. sourcecode:: bash

    nosetests --nocapture st2reactor/tests/unit/test_enforce.py

The ``--nocapture`` flag tells the nose test runner to directly output any stdout and stderr
generated during the test execution instead of capturing and ignoring it.
