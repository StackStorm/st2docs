Purging Old Operational Data
============================

By default, |st2| retains all execution history indefinitely. This can lead to performance and
disk space issues for busy systems. 

|st2| has two options for bulk data purging: Automatic and manual.

1. Automatic Purging via Garbage Collector Service
--------------------------------------------------

The Garbage Collector service is designed to periodically remove old data (action executions,
live action, trigger instance database objects). 

The actual collection threshold is very user-specific - it depends on your requirements and
policies. Therefore garbage collection is disabled by default.

To enable it, configure a TTL (in days) for action executions and trigger instances in ``st2.conf``
as shown below:

.. sourcecode:: ini

    [garbagecollector]
    logging = st2reactor/conf/logging.garbagecollector.conf

    action_executions_ttl = 30
    trigger_instances_ttl = 30

In this case action executions and trigger instances older than 30 days will be
automatically deleted.

The lowest supported TTL is 7 days. If you need to delete old data more frequently, check the
manual purge scripts below.

2. Manual Purging Using Purge Scripts
-------------------------------------

If you need to manually purge data, you can use the scripts here.

Purging Executions Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    st2-purge-executions --timestamp="2015-11-25T21:45:00.000000Z"

The timestamp provided is interpreted as a UTC timestamp. Please perform all necessary timezone
conversions and specify time in UTC.

You can also delete executions for a particular ``action_ref`` by specifying an ``action_ref``
parameter:

.. code-block:: bash

    st2-purge-executions --timestamp="2015-11-25T21:45:00.000000Z" --action-ref="core.localzz"

By default, only executions in completed state are deleted - i.e. ``succeeded``, ``failed``,
``canceled``, ``timeout`` and ``abandoned``. To delete all models irrespective of status, use the
``--purge-incomplete`` option:

.. code-block:: bash

    st2-purge-executions --timestamp="2015-11-25T21:45:00.000000Z" --purge-incomplete

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-execs st2-purge-executions --timestamp="2015-11-25T21:45:00.000000Z"

Purging Trigger Instances Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    st2-purge-trigger-instances --timestamp="2015-11-25T21:45:00.000000Z"

Again, the timestamp provided is interpreted as a UTC timestamp. Please perform all necessary
timezone conversions and specify time in UTC.

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-instances st2-purge-trigger-instances --timestamp="2015-11-25T21:45:00.000000Z"
