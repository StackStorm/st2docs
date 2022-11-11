Purging Old Operational Data
============================

By default, |st2| retains all execution history indefinitely. This can lead to performance and
disk space issues for busy systems. 

|st2| has two options for bulk data purging: Automatic and manual.

1. Automatic Purging via Garbage Collector Service
--------------------------------------------------

The Garbage Collector service is designed to periodically remove old data (action executions,
live action, action execution output, and trigger instance database objects). 

The actual collection threshold is very user-specific because it depends on your requirements and
policies. Therefore garbage collection is disabled by default, with the exception of Real-Time Streaming
Action Output.

To enable it, configure a TTL (in days) for action executions and trigger instances in ``st2.conf``
as shown below:

.. sourcecode:: ini

    [garbagecollector]
    logging = st2reactor/conf/logging.garbagecollector.conf

    action_executions_ttl = 30
    action_executions_output_ttl = 10
    trigger_instances_ttl = 40
    traces_ttl = 20
    rule_enforcements_ttl = 25
    workflow_executions_ttl = 18
    task_executions_ttl = 19
    tokens_ttl = 21

In this case, the following objects will be automatically deleted:

  * action executions older than 30 days
  * action execution output objects older than 10 days
  * trigger instances older than 40 days
  * trace objects older than 20 days
  * rule enforcement objects older than 25 days
  * workflow execution objects older than 18 days
  * workflow task execution objects older than 19 days
  * token objects whose expiry was older than 21 days

The lowest supported TTL is 1 day. If you need to delete old data more frequently, check the
manual purge scripts below.

The garbage collector service also cleans up old Inquiries by marking them as "timed out".
Unlike action executions or trigger instances, each Inquiry has its own configured TTL.
Inquiries garbage collection is enabled by setting ``garbagecollector.purge_inquiries = True``. See
:doc:`Inquiries </inquiries>` for more information on garbage collection for Inquiries.

Real-time Streaming Action Output garbage collection is enabled **by default**, with an expiry period of 7 days.
See :doc:`Real-time Action Streaming Output </reference/action_output_streaming>` for more information.

2. Manual Purging Using Purge Scripts
-------------------------------------

If you need to manually purge data, you can use the scripts here.

Purging Executions Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-executions --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

The timestamp provided is interpreted as a UTC timestamp. Please perform all necessary timezone
conversions and specify time in UTC.

You can also delete executions for a particular ``action_ref`` by specifying an ``action_ref``
parameter:

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-executions --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z" --action-ref="core.localzz"

By default, only executions in completed state are deleted - i.e. ``succeeded``, ``failed``,
``canceled``, ``timeout`` and ``abandoned``. To delete all models irrespective of status, use the
``--purge-incomplete`` option:

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-executions --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z" --purge-incomplete

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-execs /opt/stackstorm/st2/bin/st2-purge-executions --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Purging Trigger Instances Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-trigger-instances --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Again, the timestamp provided is interpreted as a UTC timestamp. Please perform all necessary
timezone conversions and specify time in UTC.

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-instances /opt/stackstorm/st2/bin/st2-purge-trigger-instances --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Purging Trace Instances Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-traces --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Again, the timestamp provided is interpreted as a UTC timestamp. Please perform all necessary
timezone conversions and specify time in UTC.

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-instances /opt/stackstorm/st2/bin/st2-purge-traces --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Purging Rule Enforcement Instances Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-rule-enforcements --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Again, the timestamp provided is interpreted as a UTC timestamp. Please perform all necessary
timezone conversions and specify time in UTC.

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-instances /opt/stackstorm/st2/bin/st2-purge-rule-enforcements --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Purging Workflow Execution Instances Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-workflows --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Again, the timestamp provided is interpreted as a UTC timestamp. Please perform all necessary
timezone conversions and specify time in UTC.

By default, only executions in completed state are deleted - i.e. ``succeeded``, ``failed``,
``canceled``, ``timeout`` and ``abandoned``. To delete all models irrespective of status, use the
``--purge-incomplete`` option:

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-workflows --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z" --purge-incomplete

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-instances /opt/stackstorm/st2/bin/st2-purge-workflows --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Purging Workflow Task Execution Instances Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-task-executions --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Again, the timestamp provided is interpreted as a UTC timestamp. Please perform all necessary
timezone conversions and specify time in UTC.

By default, only executions in completed state are deleted - i.e. ``succeeded``, ``failed``,
``canceled``, ``timeout`` and ``abandoned``. To delete all models irrespective of status, use the
``--purge-incomplete`` option:

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-task-executions --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z" --purge-incomplete

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-instances /opt/stackstorm/st2/bin/st2-purge-task-executions --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Purging Token Instances whose Expiry is Older than Some Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2-purge-tokens --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"

Again, the timestamp provided is interpreted as a UTC timestamp. Please perform all necessary
timezone conversions and specify time in UTC.

This script may take some time to complete, depending on data volumes. We recommend running it
inside a screen/tmux session. For example:

.. code-block:: bash

    screen -d -m -S purge-instances /opt/stackstorm/st2/bin/st2-purge-tokens --config-file /etc/st2/st2.conf --timestamp="2015-11-25T21:45:00.000000Z"
