Webhooks
========

Webhooks allow you to integrate external systems with |st2| using HTTP
webhooks. Unlike sensors which use a "pull" approach, webhooks use a "push"
approach. This means they work by you pushing triggers directly to the |st2|
API using HTTP POST requests.

Sensors vs Webhooks
-------------------

Sensors integrate with external systems and services using a poll approach
(sensors periodically reach out to an external system to retrieve data you are
interested in) and webhooks use a push approach (your systems push data to the
|st2| API when an event you are interested in occurs).

Sensors are the preferred integration method since they offer a more granular and
tighter integration.

On the other hand, webhooks come in handy when you have an existing script or
software which you can easily modify to send a webhook to the |st2| API when an
event you are interested in occurs.

Another example where webhooks come handy is when you want to consume events
from a 3rd party service which already offer webhooks integration - e.g. GitHub

Authentication
--------------

All the requests to the /webhooks endpoints needs to be authenticated in the
same way as other API requests. There are two possible authentication approaches - 
`API keys <authentication-apikeys>` and tokens. API keys are recommended for webhooks,
as they do not expire. Tokens have a fixed expiry.

API key-based
~~~~~~~~~~~~~

* `Header` : ``St2-Api-Key``
* `Query parameter` : ``?st2-api-key``

Token-based
~~~~~~~~~~~

* `Header` : ``X-Auth-Token``
* `Query parameter` : ``?x-auth-token``


Both methods above support providing the authentication material as a header or query parameter.
A header is usually used with your scripts where you can control request headers while query
parameters are used with 3rd party services such as GitHub where you can only specify a URL.

Request Body
------------

The request body or so called trigger payload can be either JSON or URL encoded form data. The body type
is determined based on the value of the ``Content-Type`` header (``application/json`` for JSON and
``application/x-www-form-urlencoded`` for URL encoded form data).

All the examples below assume JSON and as such, provide ``application/json`` for the
``Content-Type`` header value.

Registering a Webhook
---------------------

You can register a webhook in |st2| by specifying ``core.st2.webhook``
trigger inside a rule definition.

Here is an excerpt from a rule which registers a new webhook named ``sample``:

.. sourcecode:: yaml

    ...
    trigger:
            type: "core.st2.webhook"
            parameters:
                url: "sample"
    ...

Once this rule is created, you can use this webhook by POST-ing data to
``/v1/webhooks/sample``. The request body needs to be JSON and can contain
arbitrary data which you can match against in the rule criteria.

Note that all trailing and leading ``/`` of the ``url`` parameter are ignored by
|st2|. e.g. a value of ``/sample``, ``sample/``, ``/sample/`` and ``sample`` are
all treated the same i.e. considered identical.

POST-ing data to a custom webhook will cause a trigger with the following
attributes to be dispatched:

* ``trigger`` - Trigger name.
* ``trigger.headers`` - Dictionary containing the request headers.
* ``trigger.body`` - Dictionary containing the request body.

This example shows how to send data to a custom webhook using
cURL and how to match on this data using rule criteria:

.. sourcecode:: bash

    curl -X POST https://localhost/api/v1/webhooks/sample -H "X-Auth-Token: matoken" -H "Content-Type: application/json" --data '{"key1": "value1"}'

Rule:

.. sourcecode:: yaml

    ...
    trigger:
            type: "core.st2.webhook"
            parameters:
                url: "sample"

    criteria:
        trigger.body.key1:
            type: "equals"
            pattern: "value1"

    action:
        ref: "mypack.myaction"
        parameters:
    ...

Using a Generic Webhook
-----------------------

By default, a special-purpose webhook with the name ``st2`` is already registered. Instead
of using ``st2.core.webhook``, it allows you to specify any trigger that is known to |st2|
(either by default or from custom sensors and triggers in packs), so you can use it to
trigger rules that aren’t explicitly set up to be triggered by webhooks.

The body of this request needs to be JSON and must contain the following attributes:

* ``trigger`` - Name of the trigger (e.g. ``mypack.mytrigger``)
* ``payload`` - Object with a trigger payload.

This example shows how to send data to the generic webhook using
cURL, and how to match this data using rule criteria (replace ``localhost`` with your st2 host if call remotely):

.. sourcecode:: bash

    curl -X POST https://localhost/api/v1/webhooks/st2 -H "X-Auth-Token: matoken" -H "Content-Type: application/json" --data '{"trigger": "mypack.mytrigger", "payload": {"attribute1": "value1"}}'

Rule:

.. sourcecode:: yaml

    ...
    trigger:
        type: "mypack.mytrigger"

    criteria:
        trigger.attribute1:
            type: "equals"
            pattern: "value1"

    action:
        ref: "mypack.myaction"
        parameters:
    ...

Keep in mind that the ``trigger.type`` attribute inside the rule definition
needs to be the same as the trigger name defined in the webhook payload body.

Listing Registered Webhooks
---------------------------

To list all registered webhooks, run:

::

    st2 webhook list

When Not to Use Webhooks
------------------------

While webhooks are useful, they do have two drawbacks:

* **Not Bidirectional**  - Webhooks simply submit data into |st2|. So if you want data back from |st2|,
  or an action execution ID, you'll have to get that data in an asynchronous fashion.
* **No Guarantee of Execution** - Webhooks in |st2| do not guarantee an execution. It depends on
  the configuration of the rule that registered the webhook - based upon the webhook contents, it may
  not execute any action, or may execute multiple actions.

If you always want to execute a specific action or workflow, and/or you're looking for guaranteed response,
you could leverage the ``/v1/executions`` API. This is the same as running an action from the CLI with
``st2 run <mypack>.<myaction>``. We can get a little insight into this using the ``--debug`` flag:

.. sourcecode:: bash

    st2 --debug run core.local "date"
    2017-03-31 08:21:18,706  DEBUG - Using cached token from file "/home/ubuntu/.st2/token-st2admin"
    # -------- begin 140183979680208 request ----------
    curl -X GET -H  'Connection: keep-alive' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'User-Agent: python-requests/2.11.1' -H  'X-Auth-Token: da5ecf3b0ab841008d663052fe95cddd' http://127.0.0.1:9101/v1/actions/core.local
    # -------- begin 140183979680208 response ----------
    {"name": "local", "parameters": {"cmd": {"required": true, "type": "string", "description": "Arbitrary Linux command to be executed on the local host."}, "sudo": {"immutable": true}}, "tags": [], "description": "Action that executes an arbitrary Linux command on the localhost.", "enabled": true, "entry_point": "", "notify": {}, "uid": "action:core:local", "pack": "core", "ref": "core.local", "id": "58c9663a49d4af4cbd56f84d", "runner_type": "local-shell-cmd"}
    # -------- end 140183979680208 response ------------

    # -------- begin 140183979680080 request ----------
    curl -X GET -H  'Connection: keep-alive' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'User-Agent: python-requests/2.11.1' -H  'X-Auth-Token: da5ecf3b0ab841008d663052fe95cddd' 'http://127.0.0.1:9101/v1/runnertypes/?name=local-shell-cmd'
    # -------- begin 140183979680080 response ----------
    [{"runner_module": "local_runner", "uid": "runner_type:local-shell-cmd", "description": "A runner to execute local actions as a fixed user.", "enabled": true, "runner_parameters": {"sudo": {"default": false, "type": "boolean", "description": "The command will be executed with sudo."}, "timeout": {"default": 60, "type": "integer", "description": "Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds."}, "cmd": {"type": "string", "description": "Arbitrary Linux command to be executed on the host."}, "kwarg_op": {"default": "--", "type": "string", "description": "Operator to use in front of keyword args i.e. \"--\" or \"-\"."}, "env": {"type": "object", "description": "Environment variables which will be available to the command(e.g. key1=val1,key2=val2)"}, "cwd": {"type": "string", "description": "Working directory where the command will be executed in"}}, "id": "58c9663a49d4af4cbd56f847", "name": "local-shell-cmd"}]
    # -------- end 140183979680080 response ------------

    # -------- begin 140183979680976 request ----------
    curl -X POST -H  'Connection: keep-alive' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'User-Agent: python-requests/2.11.1' -H  'content-type: application/json' -H  'X-Auth-Token: da5ecf3b0ab841008d663052fe95cddd' -H  'Content-Length: 69' --data-binary '{"action": "core.local", "user": null, "parameters": {"cmd": "date"}}' http://127.0.0.1:9101/v1/executions
    # -------- begin 140183979680976 response ----------
    {"status": "requested", "start_timestamp": "2017-03-31T08:21:18.828620Z", "log": [{"status": "requested", "timestamp": "2017-03-31T08:21:18.843043Z"}], "parameters": {"cmd": "date"}, "runner": {"runner_module": "local_runner", "uid": "runner_type:local-shell-cmd", "description": "A runner to execute local actions as a fixed user.", "enabled": true, "runner_parameters": {"sudo": {"default": false, "type": "boolean", "description": "The command will be executed with sudo."}, "timeout": {"default": 60, "type": "integer", "description": "Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds."}, "cmd": {"type": "string", "description": "Arbitrary Linux command to be executed on the host."}, "kwarg_op": {"default": "--", "type": "string", "description": "Operator to use in front of keyword args i.e. \"--\" or \"-\"."}, "env": {"type": "object", "description": "Environment variables which will be available to the command(e.g. key1=val1,key2=val2)"}, "cwd": {"type": "string", "description": "Working directory where the command will be executed in"}}, "id": "58c9663a49d4af4cbd56f847", "name": "local-shell-cmd"}, "web_url": "https://st2expect/#/history/58de117e49d4af083399181c/general", "context": {"user": "st2admin"}, "action": {"description": "Action that executes an arbitrary Linux command on the localhost.", "runner_type": "local-shell-cmd", "tags": [], "enabled": true, "pack": "core", "entry_point": "", "notify": {}, "uid": "action:core:local", "parameters": {"cmd": {"required": true, "type": "string", "description": "Arbitrary Linux command to be executed on the local host."}, "sudo": {"immutable": true}}, "ref": "core.local", "id": "58c9663a49d4af4cbd56f84d", "name": "local"}, "liveaction": {"runner_info": {}, "parameters": {"cmd": "date"}, "action_is_workflow": false, "callback": {}, "action": "core.local", "id": "58de117e49d4af083399181b"}, "id": "58de117e49d4af083399181c"}
    # -------- end 140183979680976 response ------------

    # -------- begin 140183979680976 request ----------
    curl -X GET -H  'Connection: keep-alive' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'User-Agent: python-requests/2.11.1' -H  'X-Auth-Token: da5ecf3b0ab841008d663052fe95cddd' http://127.0.0.1:9101/v1/executions/58de117e49d4af083399181c
    # -------- begin 140183979680976 response ----------
    {"status": "succeeded", "start_timestamp": "2017-03-31T08:21:18.828620Z", "log": [{"status": "requested", "timestamp": "2017-03-31T08:21:18.843000Z"}, {"status": "scheduled", "timestamp": "2017-03-31T08:21:18.943000Z"}, {"status": "running", "timestamp": "2017-03-31T08:21:19.041000Z"}, {"status": "succeeded", "timestamp": "2017-03-31T08:21:19.242000Z"}], "parameters": {"cmd": "date"}, "runner": {"runner_module": "local_runner", "uid": "runner_type:local-shell-cmd", "enabled": true, "name": "local-shell-cmd", "runner_parameters": {"sudo": {"default": false, "type": "boolean", "description": "The command will be executed with sudo."}, "timeout": {"default": 60, "type": "integer", "description": "Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds."}, "cmd": {"type": "string", "description": "Arbitrary Linux command to be executed on the host."}, "kwarg_op": {"default": "--", "type": "string", "description": "Operator to use in front of keyword args i.e. \"--\" or \"-\"."}, "env": {"type": "object", "description": "Environment variables which will be available to the command(e.g. key1=val1,key2=val2)"}, "cwd": {"type": "string", "description": "Working directory where the command will be executed in"}}, "id": "58c9663a49d4af4cbd56f847", "description": "A runner to execute local actions as a fixed user."}, "elapsed_seconds": 0.378813, "web_url": "https://st2expect/#/history/58de117e49d4af083399181c/general", "result": {"failed": false, "stderr": "", "return_code": 0, "succeeded": true, "stdout": "Fri Mar 31 08:21:19 UTC 2017"}, "context": {"user": "st2admin"}, "action": {"runner_type": "local-shell-cmd", "name": "local", "parameters": {"cmd": {"required": true, "type": "string", "description": "Arbitrary Linux command to be executed on the local host."}, "sudo": {"immutable": true}}, "tags": [], "enabled": true, "entry_point": "", "notify": {}, "uid": "action:core:local", "pack": "core", "ref": "core.local", "id": "58c9663a49d4af4cbd56f84d", "description": "Action that executes an arbitrary Linux command on the localhost."}, "liveaction": {"runner_info": {"hostname": "st2expect", "pid": 1657}, "parameters": {"cmd": "date"}, "action_is_workflow": false, "callback": {}, "action": "core.local", "id": "58de117e49d4af083399181b"}, "id": "58de117e49d4af083399181c", "end_timestamp": "2017-03-31T08:21:19.207433Z"}
    # -------- end 140183979680976 response -----------

    id: 58de117e49d4af083399181c
    status: succeeded
    parameters:
      cmd: date
    result:
      failed: false
      return_code: 0
      stderr: ''
      stdout: Fri Mar 31 08:21:19 UTC 2017
      succeeded: true

In addition to the "usual" output that shows the result of the execution, the ``--debug`` flag also
shows all the API calls made during the course of the entire interaction, in the form of ``curl``
commands.

The above output shows the API calls made when executing the command from the |st2| host. If you are accessing the
API from a remote system, it will be proxied through nginx, using the ``/api`` URI (see :doc:`/reference/ha` for
more information). So remote calls will take this form:

.. sourcecode:: bash

    curl -X POST https://[ST2_IP]/v1/executions -H  'Connection: keep-alive' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'User-Agent: python-requests/2.11.1' -H  'content-type: application/json' -H  'X-Auth-Token: matoken' -H  'Content-Length: 69' --data-binary '{"action": "core.local", "user": null, "parameters": {"cmd": "date"}}'
