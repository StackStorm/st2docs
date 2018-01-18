Development
===========

This page describes the |st2| development processes and contains general
guidelines and information on how to contribute to the project.

Contributing
------------

We welcome and appreciate contributions of any kind (code, tests, documentation,
examples, use cases, ...).

If you need help or get stuck at any point during this process, stop by on our
`Slack Community <https://stackstorm.com/community-signup>`_ and we will do our best to
assist you.

For information on contributing an integration pack, please refer to the
:doc:`Create and Contribute a Pack </reference/packs>` page.

For an overview of core StackStorm code structure, please refer to
:doc:`Code structure </development/code_structure>`.

Setting up a Development Environment
------------------------------------

There are multiple ways for you to set up a development environment and get started with |st2|
development.

The easiest approach is to use our Vagrant images which contain all the dependencies you need to
get started. For more information, see `st2vagrant <https://github.com/StackStorm/st2vagrant>`_.

Another approach is to install StackStorm and all the dependencies from source on a server or VM
of your liking. For more information about this approach, see
:doc:`Installing StackStorm from sources </development/sources>`.

General Contribution Guidelines
-------------------------------

* Any non-trivial change must contain corresponding tests. For more information, refer to the
  :doc:`Testing page</development/testing>` (or the :doc:`Pack Testing</development/pack_testing>`
  page for pack development).
* All the functions and methods must contain Sphinx docstrings which are used to generate the API
  documentation. We follow the Apache Libcloud project docstrings conventions. For more
  information, refer to the `Docstring conventions`_ page.
* If you are adding a new feature, make sure to add corresponding documentation and examples.

Code Style Guide
----------------

* We follow `PEP8 Python Style Guide`_.
* Use 4 spaces for a tab.
* Use 100 characters in a line.
* Make sure edited files don't contain any trailing whitespace.
* Make sure that all the source files contain an Apache 2.0 license header. For an example, see one
  of the existing Python files.
* You can verify that your modifications don't break any rules by running the lint script -
  ``make flake8``

Most |st2| repositories use shared Flake8 and PyLint configuration files, which you can get from
the `lint-configs repo <https://github.com/StackStorm/lint-configs>`_.

And most importantly, follow the existing style in the file you are editing and **be consistent**.

Deprecation Policy
------------------

Sometimes we need to deprecate features. Usually this is because there is now a much better way of
doing something. Where these changes affect users, we must ensure that we give ample warning, and
a chance to migrate, before we remove the old features completely.

Our general deprecation policy is to provide notice for at least two major (`x.y`) versions,
before a feature is removed. 

This is an example of a typical deprecation timeline:

* **2.0:** New configuration format introduced. Documentation updated to refer to both old and new
  versions, with information on migration.
* **2.1:** ``WARNING`` logs generated on use of old-style configuration, e.g. at time of pack
  registration. Changelog to include note in "Deprecated" section. Documentation should focus on
  new style, with reference information on migration. Users can keep using the older configuration.
* **2.2:** Continue with previous ``WARNING`` logs. Users may still keep the older configuration.
* **2.3:** Fatal ``ERROR`` logs generated on use of old-style configuration. Documentation should
  only refer to new style. Changelog entry added in "Removed" section. At this point the feature
  is no longer supported, and users **must** migrate.

We may choose to have a longer notice period, but in general this will not be more than 4 major
versions. There is a cost to maintaining legacy features.

General Coding Guidelines
-------------------------

Logging
~~~~~~~

Logging is important because it increases the visibility and makes the project easier to debug
and support.

You are encouraged to generously use the log statements across the code base. You should log every
event which increases the visibility and/or makes the product easier to debug and support.

Every log statement should also include as much as useful additional context as possible. This
context should be included in the dictionary which is passed via the ``extra`` keyword argument
to the logger method as shown below.

Default log formatters we use include this additional context as part of the message which makes
it easier for users to find the relevant information.

On top of that, we also offer `GELF <http://docs.graylog.org/en/2.3/pages/gelf.html#gelf-payload-specification>`_
log formatters which outputs log messages in GELF format (structured JSON). This formatter can be
used to ship structured logs to Graylog2, loggly, logstash or a similar service.

Obtaining a Reference to the Logger Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To obtain a reference to the logger instance you should use the ``st2common.log.getLogger``
function as shown below. You should use this function, and not the one from the ``stdlib`` logging
module because we declare a custom log level and do a couple of other things which are only
available on loggers which are obtained through our version of ``getLogger``.

In most cases, you should do this at the top of the module after the imports
and reuse this logger throughout that module:

.. sourcecode:: python

    from st2common import log as logging

    LOG = logging.getLogger(__name__)
    LOG.debug('....')

Passing Context to the Logger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As noted above, you should always include as much context as possible in the log messages.
Context is provided by passing a dictionary via the ``extra`` keyword argument to the logger
method.

This dictionary should contain values which are relevant to the log message in question
(e.g. created/modified database object, user who performed the action, etc.).

If you are passing an instance of a custom class as a value, you should implement the ``to_dict``
method on that class. This method is responsible for returning a dictionary representation of
this object which can be serialized as JSON.

Keep in mind that this method is already implemented for all of the StackStorm
database objects (``ActionDB``, ``RunnerTypeDB``, etc.).

.. sourcecode:: python

    action_db = ...
    user_db = ...
    remote_addr = ...

    extra = {'action_db': action_db, 'user_db': user_db, 'remote_addr': remote_addr}
    LOG.debug('New action has been created. ActionDB.id=%s' % (action_db.id),
              extra=extra)

Using the AUDIT Log Level
^^^^^^^^^^^^^^^^^^^^^^^^^

StackStorm code declares a custom ``AUDIT`` log level. This log level is to be used when recording
CRUD operations on resources and when performing other actions that need to be logged in the audit
log.

For example:

.. sourcecode:: python

    LOG.audit('KeyValuePair updated. KeyValuePair.id=%s' % (kvp_db.id), extra=extra)

Dealing with Dates and Datetime Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All the ``datetime`` objects used in the codebase should be timezone-aware and represented in UTC.
The same applies to storing dates in the database - timestamps are preferred, but if you can't use
a timestamp, stored dates should be represented in UTC.

If you want to store a timestamp with microsecond precision you should use the
``st2common.fields.ComplexDateTimeField`` field class.

If you want to retrieve a ``datetime`` object for the current time, you should use
``st2common.util.date.get_datetime_utc_now`` which returns a timezone-aware ``datetime`` object
in UTC. ``st2common.util.date`` also contains other date- and time-related utility functions.

Instantiating Model Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When instantiating ``mongoengine`` model classes (e.g. ``ActionDB``, ``RuleDB``, ``SensorTypeDB``,
etc.), make sure to pass all the field values as arguments to the model constructor, instead of
performing a late assignment of variables on the class instance.

Good:

.. sourcecode:: python

    action_db = ActionDB(pack='mypack', name='myaction', enabled=True)

Bad:

.. sourcecode:: python

    action_db = ActionDB()
    action_db.pack = 'mypack'
    action_db.name = 'myaction'
    action_db.enabled = True

Passing all the fields as keyword arguments to the constructor means we can preserve the
constructor functionality. On top of that it also makes it more clear and obvious to the
developers when the values are available and allows us to perform basic "static" analysis on the
code.

.. _`PEP8 Python Style Guide`: http://www.python.org/dev/peps/pep-0008/
.. _`Docstring conventions`: https://libcloud.readthedocs.org/en/latest/development.html#docstring-conventions

.. toctree::
    :maxdepth: 1

    Code Structure <code_structure>
    testing
    Pack Testing <pack_testing>
