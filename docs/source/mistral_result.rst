.. _mistral-workflows-completion-latency-and-performance:

Mistral Workflows Completion, Latency, and Performance
======================================================

During the workflow runtime, |st2| and Mistral handshake multiple times over HTTP. This applies when launching
the workflow execution, completing a task, or completing the workflow.

Prior to v2.7, |st2| queries Mistral to check on workflow execution status and the status of individual tasks
via ``st2resultstracker``. This mechanism has a number of configuration settings. See :ref:`mistral-workflows-latency`
section about how to fine-tune the Mistral workflows completion time vs CPU consumption.

Since v2.7, the results tracking mechanism is replaced with a callback mechanism from Mistral. Instead of |st2|
querying Mistral at regular interval, Mistral is configured to callback |st2| on task and workflow completion.
With the callback mechanism, it is possible to trace the events sent to |st2|.

.. code-block:: bash

    # Identify the Mistral workflow execution ID which is different
    st2 execution get <st2-action-execution-id> -dj | grep workflow_execution_id

    # Grep the log entries from the Mistral log, typically at /var/log/mistral/mistral-server.log
    sudo tail -n 1000 /var/log/mistral/mistral-server.log | grep stackstorm_notifier | grep <mistral-wf-ex-id>

The returned list of log entries will look similar to the following:

::

    2018-03-28 22:40:05,811 140124959618704 INFO stackstorm_notifier [-] [839925d9-02c7-47be-ad8e-ce0943749a7b] The workflow event WORKFLOW_LAUNCHED for 839925d9-02c7-47be-ad8e-ce0943749a7b will be published to st2.
    2018-03-28 22:40:05,844 140124959618704 INFO stackstorm_notifier [-] [839925d9-02c7-47be-ad8e-ce0943749a7b] The workflow event WORKFLOW_LAUNCHED for 839925d9-02c7-47be-ad8e-ce0943749a7b is published to st2.
    2018-03-28 22:40:06,492 140124958584912 INFO stackstorm_notifier [-] [839925d9-02c7-47be-ad8e-ce0943749a7b] The task event TASK_SUCCEEDED for c8731e6a-2464-4a59-bf46-501a80215298 will be processed for st2.
    2018-03-28 22:40:06,492 140124958584912 INFO stackstorm_notifier [-] [839925d9-02c7-47be-ad8e-ce0943749a7b] The task event TASK_SUCCEEDED for c8731e6a-2464-4a59-bf46-501a80215298 is processed for st2.
    2018-03-28 22:40:07,195 140124956804432 INFO stackstorm_notifier [-] [839925d9-02c7-47be-ad8e-ce0943749a7b] The workflow event WORKFLOW_SUCCEEDED for 839925d9-02c7-47be-ad8e-ce0943749a7b will be published to st2.
    2018-03-28 22:40:07,371 140124956804432 INFO stackstorm_notifier [-] [839925d9-02c7-47be-ad8e-ce0943749a7b] The workflow event WORKFLOW_SUCCEEDED for 839925d9-02c7-47be-ad8e-ce0943749a7b is published to st2.

The results tracking mechanism is still available for manual intervention and can be enabled on an individual workflow
basis in case |st2| or Mistral services are offline during a callback operation.

.. code-block:: bash

    # Enable the results tracking for an individual workflow execution
    st2-track-result <st2-action-execution-id> --config-dir /etc/st2

    # Disable the results tracking for an individual workflow execution
    st2-track-result <st2-action-execution-id> --config-dir /etc/st2 --delete
