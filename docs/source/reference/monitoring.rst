System Monitoring
=================

An event-based automation & remediation platform should heal itself, right? Sure - but it's still
important to monitor your system to validate that everything is working as expected. Monitoring is
not just about faults either. It can help you understand how much the system is being used, and
when you need to scale it out.

These guidelines should help you understand what services, metrics and logs to monitor. They can be
implemented using any combination of common monitoring tools.

.. note::

    These monitoring guidelines are just that: guidelines. You will need to modify them to suit
    your specific environment. They are still a work in progress, and we welcome feedback on ways
    to improve them, and suggestions for specific monitoring system integration details.

Service Testing
^^^^^^^^^^^^^^^

|st2| does not have one single API endpoint for checking system health. You can make a reasonable
assumption about current system status by using the API to execute a simple action, and then
checking the response:

.. code-block:: bash

    ## Execute "date -R" using the core.local action:
    curl -X POST 'content-type: application/json' -H  'St2-Api-Key: my_api_key' --data-binary '{"action": "core.local", "user": null, "parameters": {"cmd": "date -R"}}' -k https://192.0.2.1/api/v1/executions
    {"status": "requested", "start_timestamp": "2016-10-10T01:37:45.937153Z", "log": [{"status": "requested", "timestamp": "2016-10-10T01:37:45.950751Z"}], "parameters": {"cmd": "date -R"}, "runner": {"runner_module": "st2actions.runners.localrunner", "uid": "runner_type:local-shell-cmd", "description": "A runner to execute local actions as a fixed user.", "enabled": true, "runner_parameters": {"sudo": {"default": false, "type": "boolean", "description": "The command will be executed with sudo."}, "env": {"type": "object", "description": "Environment variables which will be available to the command(e.g. key1=val1,key2=val2)"}, "cmd": {"type": "string", "description": "Arbitrary Linux command to be executed on the host."}, "kwarg_op": {"default": "--", "type": "string", "description": "Operator to use in front of keyword args i.e. \"--\" or \"-\"."}, "timeout": {"default": 60, "type": "integer", "description": "Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds."}, "cwd": {"type": "string", "description": "Working directory where the command will be executed in"}}, "id": "57fa74ad1d41c8249e5664f4", "name": "local-shell-cmd"}, "web_url": "https://ubuntu/#/history/57faf0e91d41c805055a1110/general", "context": {"user": "st2admin"}, "action": {"description": "Action that executes an arbitrary Linux command on the localhost.", "runner_type": "local-shell-cmd", "tags": [], "enabled": true, "pack": "core", "entry_point": "", "notify": {}, "uid": "action:core:local", "parameters": {"cmd": {"required": true, "type": "string", "description": "Arbitrary Linux command to be executed on the remote host(s)."}, "sudo": {"immutable": true}}, "ref": "core.local", "id": "57fa74ae1d41c8249e566509", "name": "local"}, "liveaction": {"runner_info": {}, "parameters": {"cmd": "date -R"}, "action_is_workflow": false, "callback": {}, "action": "core.local", "id": "57faf0e91d41c805055a110f"}, "id": "57faf0e91d41c805055a1110"}

    ## Check the execution status using the id from above:
    $ curl -X GET -H  St2-Api-Key: my_api_key' -k https://192.0.2.1/api/v1/executions/57faf0e91d41c805055a1110
    {"status": "succeeded", "start_timestamp": "2016-10-10T01:37:45.937153Z", "log": [{"status": "requested", "timestamp": "2016-10-10T01:37:45.950000Z"}, {"status": "scheduled", "timestamp": "2016-10-10T01:37:46.039000Z"}, {"status": "running", "timestamp": "2016-10-10T01:37:46.157000Z"}, {"status": "succeeded", "timestamp": "2016-10-10T01:37:46.305000Z"}], "parameters": {"cmd": "date -R"}, "runner": {"runner_module": "st2actions.runners.localrunner", "uid": "runner_type:local-shell-cmd", "enabled": true, "name": "local-shell-cmd", "runner_parameters": {"sudo": {"default": false, "type": "boolean", "description": "The command will be executed with sudo."}, "env": {"type": "object", "description": "Environment variables which will be available to the command(e.g. key1=val1,key2=val2)"}, "cmd": {"type": "string", "description": "Arbitrary Linux command to be executed on the host."}, "kwarg_op": {"default": "--", "type": "string", "description": "Operator to use in front of keyword args i.e. \"--\" or \"-\"."}, "timeout": {"default": 60, "type": "integer", "description": "Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds."}, "cwd": {"type": "string", "description": "Working directory where the command will be executed in"}}, "id": "57fa74ad1d41c8249e5664f4", "description": "A runner to execute local actions as a fixed user."}, "elapsed_seconds": 0.339103, "web_url": "https://ubuntu/#/history/57faf0e91d41c805055a1110/general", "result": {"failed": false, "stderr": "", "return_code": 0, "succeeded": true, "stdout": "Sun, 09 Oct 2016 18:37:46 -0700"}, "context": {"user": "st2admin"}, "action": {"runner_type": "local-shell-cmd", "name": "local", "parameters": {"cmd": {"required": true, "type": "string", "description": "Arbitrary Linux command to be executed on the remote host(s)."}, "sudo": {"immutable": true}}, "tags": [], "enabled": true, "entry_point": "", "notify": {}, "uid": "action:core:local", "pack": "core", "ref": "core.local", "id": "57fa74ae1d41c8249e566509", "description": "Action that executes an arbitrary Linux command on the localhost."}, "liveaction": {"runner_info": {"hostname": "ubuntu", "pid": 1014}, "parameters": {"cmd": "date -R"}, "action_is_workflow": false, "callback": {}, "action": "core.local", "id": "57faf0e91d41c805055a110f"}, "id": "57faf0e91d41c805055a1110", "end_timestamp": "2016-10-10T01:37:46.276256Z"}

Look for ``failed: false`` in the result above. This process will exercise the core parts of |st2|.
If it succeeds, then the system is correctly configured and working.

Processes
^^^^^^^^^

You can use ``sudo st2ctl status`` to get a quick overview of current process status:

.. code-block:: bash

    $ sudo st2ctl status
    ##### st2 components status #####
    st2actionrunner PID: 1014
    st2api PID: 921
    st2api PID: 1285
    st2stream PID: 922
    st2stream PID: 1287
    st2auth PID: 912
    st2auth PID: 1286
    st2garbagecollector PID: 910
    st2notifier PID: 916
    st2resultstracker PID: 913
    st2rulesengine PID: 920
    st2timersengine PID: 925
    st2sensorcontainer PID: 907
    st2chatops is not running.
    $

In a distributed system, only some of these processes will be running on each system. In the
example here ``st2chatops`` is not configured on this system.

Tools such as nagios or check_mk can be used to monitor the process list. Some services spawn more
than one process. The exact number will depend upon your system configuration - e.g.
``st2actionrunner`` will spawn additional processes on a multi-core system.

Some of the processes such as ``st2timersengine`` do not run always. For example, when timer
service is disable by configuration, then the process exits with exit code 0. The monitoring
system should account for this behavior.

Additional processes to monitor:

* RabbitMQ - ``rabbitmq-server``
* MongoDB - ``mongod``
* Nginx (if used for web/API frontend) - ``nginx``
* Postfix/Sendmail (if local mail relay configured)
* rsyslog/logstash/splunk-agent (if used)


Metrics
^^^^^^^

Key metrics for |st2| administrators to watch are the number of running and scheduled actions, and
the average execution time. Busy systems will need to scale out the number of ``st2actionrunner``
processes.

|st2| exposes some of those metrics via statsd using the metrics framework. For more information,
please refer to :doc:`/reference/metrics` section.

MongoDB
-------

MongoDB holds state for all currently scheduled and running actions. Use these queries to monitor
current numbers:

* Scheduled actions: ``db.live_action_d_b.find({"status":"scheduled"})``
* Running actions: ``db.live_action_d_b.find({"status":"running"})``

Monitor these values over time to detect trends, and abnormal activity. Increasing numbers of
scheduled actions may indicate insufficient ``st2actionrunner`` capacity. These queues can be
monitored using:

.. code-block:: bash

    mongo st2 --eval \'rs.slaveOk(); db.live_action_d_b.find({\"status\":\"scheduled\"}).count()\' | tail -1
    mongo st2 --eval \'rs.slaveOk(); db.live_action_d_b.find({\"status\":\"running\"}).count()\' | tail -1

RabbitMQ
--------

These RabbitMQ queue lengths should be monitored:

* ``st2.actionrunner.cancel``
* ``st2.actionrunner.req``
* ``st2.actionrunner.work``

You can obtain these values using ``sudo rabbitmqctl list_queues | fgrep st2.actionrunner.``

For most systems, these queue lengths should be < 10.

Completed Actions
-----------------

The |st2| audit logs record all executed actions, execution time and result. These logs should be
stored in a system like Splunk or Elasticsearch that allows for extraction of average run time and
execution count.

Interesting metrics to monitor:

* Completed actions count over time
* Average execution time - watch for outliers
* Action frequency by pack, and by individual action

See below for more details on logfile monitoring.

Logs
^^^^

By default, all |st2| logs are stored in the ``/var/log/st2/`` directory. See the :ref:`Configure
Logging<config-logging>` section for more information about logfile location, configuration and
using syslog.

.. note::

    We **strongly** recommend storing all |st2| logs in a dedicated log management tool, such as
    `Splunk <https://www.splunk.com>`_, `Graylog <http://www.graylog.org>`_ or the `ELK stack
    <https://elastic.co>`_. You can also see some examples of Logstash configuration and Kibana
    dashboards here: :github_exchange:`exchange-misc/logstash <exchange-misc/tree/master/logstash>`.

All log messages include a log level - DEBUG, INFO, WARNING, ERROR, CRITICAL. All messages at
WARNING and above should be escalated for investigation.

Most organizations will want to investigate failed action executions. This is an example of a
failed execution in the ``st2actionrunner`` logs:

.. code-block:: bash

    2017-03-15 23:53:46,833 70846416 AUDIT base [-] Liveaction completed (liveaction_db={'status': 'failed', 'runner_info': {u'hostname': u'st2vagrant', u'pid': 1199}, 'parameters': {u'cmd': u'foo'}, 'action_is_workflow': False, 'start_timestamp': '2017-03-15 23:53:46.439855+00:00', 'callback': {}, 'notify': None, 'result': {'succeeded': False, 'failed': True, 'return_code': 127, 'stderr': 'bash: foo: command not found', 'stdout': ''}, 'context': {u'user': u'st2admin'}, 'action': u'core.local', 'id': '58c9d40ac4da5f0737cd86f0', 'end_timestamp': '2017-03-15 23:53:46.792152+00:00'})

Note the ``'status': 'failed'`` section.
