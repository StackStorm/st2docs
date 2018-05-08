Mistral Issues
==============

This section contains information on how to troubleshoot Mistral-related issues.

Troubleshooting Mistral Database Upgrade
----------------------------------------

The ``mistral`` and ``mistral-api`` services must not be running at time of upgrading the st2mistral
package and the Mistral database schema. If the st2mistral package has been upgraded and the
services are started before the ``mistral-db-manage upgrade head`` CLI command is executed, then the
``mistral-db-manage upgrade head`` command may fail. 

When the ``mistral`` and ``mistral-api`` services run, SQLAlchemy automatically creates tables,
relationships, and indices that do not exist. If there are new database objects in the upgraded
database schema, the ``mistral-db-manage upgrade head`` command will fail because the actual schema
in the database is now different than its specifications, and it no longer can create the new database
objects. 

When that happens, the new database tables, relationships, and indices must be deleted before the
``mistral-db-manage upgrade head`` command can be re-run. For more details, review the version-specific
notes in the :doc:`/install/upgrades` documentation, for the version of Mistral and |st2| you are upgrading
too.

.. _mistral-workflows-latency:

Troubleshooting Mistral Workflow Completion Latency
---------------------------------------------------

Since v2.7, the results tracking mechanism is replaced with a callback mechanism from Mistral. Instead of |st2|
querying Mistral at regular intervals, Mistral is configured to callback |st2| on task and workflow completion.
See :ref:`mistral-workflows-completion-latency-and-performance`

Prior to v2.7, |st2| queries Mistral to check on workflow execution status and the status of individual tasks
via st2resultstracker. This ``st2resultstracker`` process saves the state of outstanding workflow executions
in the database, and once a workflow is complete, deletes the state from the database. The process uses
eventlets to simultaneously query multiple workflow results. This can consume significant CPU cycles. 

There are two configurable values for controlling this. These are ``thread_pool_size`` (number of eventlets)
and ``query_interval`` (interval to space out the subsequent queries to Mistral for a single execution). You
can configure these values by editing the ``results_tracker`` section in ``/etc/st2/st2.conf``:

.. sourcecode:: ini

    [resultstracker]
    query_interval = 5 # in seconds
    thread_pool_size = 10

These values are subject to load conditions in your infrastructure and the number of workflows
you are running. The default value for ``query_interval`` is set to ``5`` (seconds) which is a balance
between the workflow speed and the CPU overhead. With |st2| 2.2 and earlier, this value was ``0.1``.
We have now set the default value to ``5`` seconds to be conservative. This also means the time to detect
a completed workflow in Mistral by |st2| could take as long as 5 seconds.

If this is unacceptable for you, you can reduce the ``query_interval`` and also
simultaneously check CPU usage for the ``st2resultstracker`` process.
