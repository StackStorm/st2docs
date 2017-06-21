Mistral Issues
==============

This section contains information on how to troubleshoot Mistral related issues.

Troubleshooting Mistral Database Upgrade
----------------------------------------

The mistral and mistral-api services must be stopped at time of upgrading the st2mistral package
and the mistral database schema. If the st2mistral package has been upgraded and the services are
started before the ``mistral-db-manage upgrade head`` command is run, then the
``mistral-db-manage upgrade head`` command may fail. When the mistral and mistral-api services run,
SQLAlchemy automatically creates tables, relationships, and indices that do not exist. In the case
where there are new database objects in the upgraded database schema, the
``mistral-db-manage upgrade head`` command will fail because the actual schema in the database is
now different than its spec and it no longer can create the new database objects. When that happens,
the new database tables, relationships, and indices must be deleted before the
``mistral-db-manage upgrade head`` command can be re-run. For more details, review the specific
section for the version being upgraded in :doc:`/install/upgrades`.


Troubleshooting Mistral Workflow Completion Latency
---------------------------------------------------

|st2| interacts with Mistral via HTTP APIs. This is true for kicking off a workflow execution
or collecting the results for a running workflow. |st2| queries Mistral to check on workflow
execution status and the status of individual tasks. The process in |st2| that does the querying
is called ``st2resultstracker``. It saves the state of outstanding workflow executions in the
database, and once a workflow is complete, deletes the state from the database. The process uses
eventlets to simultaneously query multiple workflow results. This can consume significant CPU
cycles. There are two configurable values (as of |st2| version 2.3 onwards). These are
``thread_pool_size`` (number of eventlets) and ``query_interval`` (interval to space out the
subsequent queries to Mistral for a single execution). You can configure these values by editing
the ``results_tracker`` section in ``/etc/st2/st2.conf``:

.. sourcecode:: ini

    [results_tracker]
    query_interval = 5 # in seconds
    thread_pool_size = 10

These numbers are subject to load conditions in your infrastructure and the number of workflows
you run. The default value for ``query_interval`` is set to ``20`` (seconds). With |st2| 2.2 and
earlier, this value was ``0.1``. We've set the value to ``20`` seconds to be conservative. This
also means the time to detect a completed workflow in Mistral by |st2| could take as long as 20
seconds. If this is unacceptable for you, you can reduce the ``query_interval`` and also
simultaneously check CPU usage for the ``st2resultstracker`` process. We are reworking the design
to use HTTP callbacks from Mistral to |st2|. Until then, these tunable knobs should help.
