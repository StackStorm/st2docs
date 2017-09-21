Real-time Action Output Streaming
=================================

.. note::

  This feature is experimental. It is available in |st2| v2.5.0 and above. Because it is
  experimental, it is disabled by default, and must be explicitly enabled (opt-in). To enable it,
  set the ``actionrunner.stream_output`` config option to ``True`` in ``st2.conf`` and restart all
  services (``sudo st2ctl restart``).

How it Works
------------

By default when a user runs a |st2| action, they don't see the actual output produced by the action
until the execution has finished (either failed, succeeded or timed out).

In v2.5.0 we introduced new functionality which allows users to see output in real-time, as it is
produced by the action. This is especially useful with long running actions and in CI/CD
scenarios where you want to see the output in an incremental manner as soon as it's available.

Output streaming functionality is currently available for the following runners:

* local command runner
* local script runner
* remote command runner
* remote script runner
* python runner

.. note::

  Output streaming only works with the remote runner when you run the command/script on a single host
  at once (when you pass a single host for the ``host`` parameter - one host per action execution).

  If you want to run a command/script on multiple hosts and you want real-time action output, you
  should create one execution per host as shown below:

  .. code-block:: bash

    st2 run examples.my_remote_action host=host1
    st2 run examples.my_remote_action host=host2
    st2 run examples.my_remote_action host=host3

    # instead of
    st2 run examples.my_remote_action host=host1,host2,host3


Inside the runners we explicitly disable stdout and stderr output buffering. Some scripts
and programs use their own internal buffer which means that in some cases output might be slightly
delayed, depending on the size of the buffer used by the underlying script/program.

Accessing Real-time Action Output
---------------------------------

Real-time streaming action output can be accessed using one of the approaches described below,
after an execution has been scheduled.

1. Via CLI
~~~~~~~~~~

The easiest way to access the output is to use the ``st2 execution tail <execution id>`` command:

.. code-block:: bash

    st2 execution tail <execution id> [--type=stdout/stderr/other]
    st2 execution tail last  # "last" is a special convenience keyword which will automatically
                             # retrieve and use ID of the last execution which has been scheduled.

This command listens for new data on the StackStorm event stream API and prints it as it becomes
available.

.. note::

  ``st2 execution tail`` Only displays output for simple actions and workflows which are not
  nested (e.g. workflow which calls a simple action).

  If you have multiple levels of nested workflows (e.g. workflow which calls a workflow which
  calls an action) and you want to see output of an action which is called by a nested workflow,
  you need to directly tail execution of a nested workflow.

Keep in mind that this command utilizes the stream API endpoint so it will only print any new data
which comes in after you ran the command.

If you want to view output of an execution which has completed, you can use the execution output
API endpoint (see below) or use the executions API endpoint
(``GET /v1/executions/<execution id>``) and access the ``result`` attribute on the returned object.

.. code-block:: bash

    # Tailing running execution
    $ st2 execution tail last
    stderr -> Line: 7
    stdout -> Line: 8
    stderr -> Line: 9

    $ st2 execution tail last --include-metadata
    [2017-08-31T11:51:06.961844Z][stderr] stderr -> Line: 7
    [2017-08-31T11:51:07.462199Z][stdout] stdout -> Line: 8
    [2017-08-31T11:51:07.963102Z][stderr] stderr -> Line: 9

    # Tailing execution which has finished
    stderr -> Line: 7
    stdout -> Line: 8
    stderr -> Line: 9
    stdout -> Line: 10

    Execution 59a7f8260640fd686303e628 has completed.

2. Via the StackStorm API
~~~~~~~~~~~~~~~~~~~~~~~~~

Output can also be accessed in real-time using the |st2| API:

* ``GET /v1/executions/<execution id>/output[?type=stdout/stderr/other]``

.. code-block:: bash

    $ curl "http://127.0.0.1:9101/v1/executions/last/output"
    stderr -> Line: 1
    stdout -> Line: 2
    stderr -> Line: 3
    stdout -> Line: 4
    stderr -> Line: 5
    stdout -> Line: 6
    stderr -> Line: 7
    stdout -> Line: 8
    stderr -> Line: 9
    stdout -> Line: 10

The API endpoints keep a long running connection open until the execution completes or the user
closes the connection.

Once requested, the API endpoint returns any data which has been produced so far and after that,
any new data as it becomes available.

Similar to the CLI command, you can also use ``last`` for the execution id, and the ID of the 
execution which has been scheduled last will be used.

3. Via the StackStorm Stream API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-

In addition to the |st2| API above, output can also be accessed using the event stream API.

This API endpoint follows the server-sent event specification (JSON messages delimited by a new line
- ``\n``) and is also used for other events. The name of the event is
``st2.execution.output__create``:

.. code-block:: bash

    $ curl http://127.0.0.1:9102/v1/stream?events=st2.execution.output__create

    event: st2.execution.output__create
    data: {"timestamp": "2017-09-12T13:31:28.608095Z", "runner_ref": "remote-shell-cmd", "output_type": "stderr", "action_ref": "examples.remote_command_runner_print_to_stdout_and_stderr", "data": "stderr line 1\n", "id": "59b7e1b00640fd119d798359", "execution_id": "59b7e1ae0640fd0f72fdc746"}

    event: st2.execution.output__create
    data: {"timestamp": "2017-09-12T13:31:28.836387Z", "runner_ref": "remote-shell-cmd", "output_type": "stdout", "action_ref": "examples.remote_command_runner_print_to_stdout_and_stderr", "data": "stdout line 2\n", "id": "59b7e1b00640fd119d79835a", "execution_id": "59b7e1ae0640fd0f72fdc746"}

    event: st2.execution.output__create
    data: {"timestamp": "2017-09-12T13:31:28.863368Z", "runner_ref": "remote-shell-cmd", "output_type": "stderr", "action_ref": "examples.remote_command_runner_print_to_stdout_and_stderr", "data": "stderr line 3\n", "id": "59b7e1b00640fd119d79835b", "execution_id": "59b7e1ae0640fd0f72fdc746"}

    event: st2.execution.output__create
    data: {"timestamp": "2017-09-12T13:31:29.100242Z", "runner_ref": "remote-shell-cmd", "output_type": "stdout", "action_ref": "examples.remote_command_runner_print_to_stdout_and_stderr", "data": "stdout line 4\n", "id": "59b7e1b10640fd119d79835c", "execution_id": "59b7e1ae0640fd0f72fdc746"}

Keep in mind that this feature is still behind a feature flag and that's why you need to explicitly
pass ``?events=st2.execution.output__create`` query param to the API endpoint to make sure you also
receive these events.

Security Implications
---------------------

This functionality can be restricted via RBAC. To access the execution stdout and stderr API
endpoint, ``EXECUTION_VIEW`` permission type is required.

Depending on your actions and what kind of output they produce, the output may contain sensitive
data. Because of that you are strongly encouraged to only grant this permission to users who explicitly
require it. In addition to that, you are also strongly encouraged to modify your actions to mask/hide
any potentially sensitive data inside the action output if it's not needed for further
processing inside |st2|.

For more information about masking and securely passing secrets between the actions, please see
:doc:`Secrets Masking </reference/secrets_masking>` page.

Keep in mind that action output data is the same data which is available via execution
``result`` attribute through ``/v1/executions/<execution id>`` API endpoint (this API endpoint
also requires ``EXECUTION_VIEW`` RBAC permission).

Garbage Collection
------------------

If your actions produce a lot of output, enabling real-time output streaming for each action execution
can result large amounts of data being passed around and stored in the database. This data is stored
in the special write ahead database collections (``action_execution_stdout_output_d_b``,
``action_execution_stderr_output_d_b``).

Because of that, garbage collection is enabled by default for execution stdout and stderr objects
- they are deleted automatically after 7 days.

If you want to disable garbage collection for those objects (unwise) or change the default TTL, you can
do that by setting the ``garbagecollector.action_executions_ttl`` config option. This option is the TTL
in days. Setting it to ``0`` disables garbage collection.

For more information on setting up garbage collection, please refer to the
:doc:`Purging Old Operational Data </troubleshooting/purging_old_data>` documentation page.
