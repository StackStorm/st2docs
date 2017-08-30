Real-time Action Output Streaming
=================================

.. note::

  This feature is still experimental and available in |st2| v1.5.0 and above. Because it's
  experimental, it's behind a feature flag and disabled by default (opt-int). To enable it,
  set ``actionrunner.stream_output`` ``st2.conf`` config option to ``True`` and restart all
  the services (``sudo st2ctl restart``).

How it works
------------

By default when user runs a |st2| action, they don't see the actual output produced by the action
until the execution has finished (either failed, succeeded or timed out).

In v2.5.0 we introduced new functionality which allows users to see output in real-time as it is
produced by the action. This comes especially handy with long running actions and in CI / CD
scenarios where you want to see the output in an incremental manner as soon as it's available.

Right now output streaming functionality is available for the following runners:

* local command runner
* local script runner
* remote command runner
* remote script runner
* python runner

The protocol is line oriented 

The whole protocol is line oriented which means 
some scripts buffrer the output

Accessing real-time action output
---------------------------------

Real-time streaming action output can be accessed using one of the approaches described below
after an execution has been scheduled.

1. Using CLI
~~~~~~~~~~~~

The easiest way to access the output is to use ``st2 execution tail <execution id>`` CLI command.

.. code-block:: bash

    st2 execution tail <execution id>
    st2 execution tail last  # "last" is a special convenience keyword which will automatically
                             # retrieve and use ID of the last execution which has been scheduled.

This command listens for new data on the StackStorm event stream API and prints it once it's
available.

Keep in mind that this command utilizes the stream API endpoint so it will only print any new data
which comes in after you ran the command.

TODO example output

2. Via the StackStorm API
~~~~~~~~~~~~~~~~~~~~~~~~~

Output can also be accessed in real-time using two |st2| API endpoints described below:

* ``/v1/executions/<execution id>/stdout``
* ``/v1/executions/<execution id>/stderr``

Both of those API endpoints keep a long running connection open until the execution completes or
user closes the connection.

Once requested, those API endpoints return any data which has been produced so far and after that,
any new data which comes in when it's available.

2. Via the StackStorm Stream API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to |st2| API endpoint, output can also be accessed using the |st2| event stream API.

This API endpoint follows server-sent event specification (JSON messages delimited by a new line
- ``\n``) and is also used for other events.

Gargage Collection
------------------

In case your actions produce a lot of output, enabling real-time output streaming for each
action execution can result a lot of data being passed around and stored in the database. This
data is stored in special write ahead only database collections (
``action_execution_stdout_output_d_b``, ``action_execution_stderr_output_d_b``).

In case you encounter performance issues or those two collections / database grows too large,
you are encouraged to enable periodic garbage collection.

Each output object belongs to a particular execution so by default, they are deleted as part
of executions and related objects purge when ``garbagecollector.action_executions_ttl``
config option is set.

If for some reason, you want to delete output objects, but not parent execution objects themselves
(e.g. you care about action execution metadata, but not about the action execution output objects
itself), you can achieve that by setting ``garbagecollector.action_executions_output_ttl`` config
option.

For more information on setting up garbage collection, please refer to please refer to the
:doc:`Purging Old Operational Data </troubleshooting/purging_old_data>` documentation page.
