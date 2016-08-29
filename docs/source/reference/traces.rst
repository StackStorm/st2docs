Traces
======

Traces are tracking entities that serve to gather all |st2| entities like ActionExecution,
TriggerInstance and Rule that originate from an event. In the |st2| context an event could be one
of the following:

* Events from an external system sent to |st2| via a Sensor or Webhook.
* Action executed via UI, CLI or API.
* Action executed via ChatOps.

Examples
--------

Let us walk through a few canonical examples:

External events
^^^^^^^^^^^^^^^

Sensors dispatch TriggerInstances into |st2| and Webhooks are also translated to TriggerInstances when posted to |st2|. Rules are written to match specific Triggers and compared against TriggerInstances.

In the canonical case, TriggerInstance(ti1) dispatched by Sensor to |st2|, matches a Rule(r1) leading to an ActionExecution(ae1). On completion of ae1 an ActionTrigger TriggerInstance(ti2) is dispatched by |st2|.

The trace created in this case contains all the entities from above since they originate from the same event i.e. TriggerInstance(ti1) dispatched into |st2|.

.. code-block:: bash

   Trace
     |- ti1
     |- r1
     |- ae1
     |- ti2

Connected flows
^^^^^^^^^^^^^^^

|st2| raises an internal Trigger called the ActionTrigger. It is possible for rules to be used in conjunction with those on completion of executions.

ActionExecution(ae1) started by user, on completion of ae1 an ActionTrigger TriggerInstance(ti1) is dispatched, Rule(r1) matches and leads to ActionExecution(ae2) another ActionTrigger TriggerInstance(ti2) is dispatched but no rule matched.

The trace created in this case contains all the entities from above since they cascade
from the same origin i.e. ActionExecution(ae1) dispatched into the system.

.. code-block:: bash

   Trace
     |- ae1
     |- ti1
     |- r1
     |- ae2
     |- ti2


Tracing Triggers and Executions
-------------------------------

It is possible for users to define identifying information for a Trace at event injection points. The injection points for |st2| where a Trace can start are:

* Dispatch a Trigger (more precisely this is dispatching a TriggerInstance) by a Sensor.
* Webhook posted to |st2|.
* Execute an Action (aka creation of an ActionExecution) via UI, CLI, API or Chat.

What is a trace_tag and trace_id?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``trace-tag`` : User specified and therefore friendly way to tag or identify a Trace. There is no requirement for this value to be unique and |st2| will not enforce this either. Whenever only a trace-tag is provided at one of the injection points a new Trace is started if one does not already exist.

* ``trace-id`` : This is a |st2| defined value and is guaranteed to be unique. Users can specify this value at the injection points as all but a Trace with the specified trace-id must already exist.

Dispatch a Trigger
^^^^^^^^^^^^^^^^^^

TriggerInstance dispatch most often happens from a Sensor. The :ref:`authoring a sensor<ref-sensors-authoring-a-sensor>` page contains information on how to introduce a Trace.

A brief snippet is included here to explain some trace specific constructs. A sensor would inject such triggers by using the sensor\_service passed into the sensor on instantiation:

.. code-block:: python

    self.sensor_service.dispatch(trigger=trigger, payload=payload, trace_tag=trace_tag)


Here the Sensor is expected to supply a meaningful value for ``trace_tag`` e.g.:

* Commit SHA of a git commit for a git commit hook trigger.
* ID of the event from a monitoring system, like Sensu or Nagios, that is relayed to |st2|.

Webhook
^^^^^^^

Both custom webhooks and generic |st2| webhooks support supplying a trace-tag via a header.

* `Header` : ``St2-Trace-Tag``

In case of a custom webhook the `curl` command will be

.. sourcecode:: bash

    curl -X POST http://127.0.0.1:9101/v1/webhooks/sample -H "X-Auth-Token: matoken" -H "Content-Type: application/json" -H "St2-Trace-Tag: webhook-1" --data '{"key1": "value1"}'

Execute an Action
^^^^^^^^^^^^^^^^^

Execution of an Action can also be associated with a Trace. Here is how this could be done from the CLI:

To start a new trace use ``trace-tag``:

.. code-block:: bash

   $ st2 run core.local date --trace-tag TraceDateAction


To associate with an existing trace use ``trace-id``:

.. code-block:: bash

   $ st2 run core.local uname --trace-id 55d505fd32ed35711522c4c8


Viewing Traces
--------------

|st2| CLI provides the ability to list and get traces.


List
^^^^

* All traces in the system:

.. code-block:: bash

    $ st2 trace list


* Filter by trace-id:

.. code-block:: bash

    $ st2 trace list --trace-tag <trace-tag>

* Filter by execution:

.. code-block:: bash

    $ st2 trace list --execution 55d505fd32ed35711522c4c7

* Filter by rule:

.. code-block:: bash

    $ st2 trace list --rule 55d5064432ed35711522c4ca

* Filter by trigger-instance:

.. code-block:: bash

    $ st2 trace list --trigger-instance 55d5069832ed35711cc4b08e


Get
^^^

* Get a specific trace:

.. code-block:: bash

    $ st2 trace get <trace-id>

* View the causation chain in a trace for an action execution. Similarly for rule and trigger-instance:

.. code-block:: bash

    $ st2 trace get <trace-id> -e

* View specific type in a trace:

.. code-block:: bash

    $ st2 trace get <trace-id> --show-executions

* Hide no-op trigger instances. These are trigger instances which do not lead to a rule enforcement:

.. code-block:: bash

    $ st2 trace get <trace-id> --hide-noop-triggers


Is everything traced?
---------------------

By default all ActionExecutions and TriggerInstances are traced. If no ``trace-tag`` is provided by a user then |st2| automatically generate a ``trace-tag`` to provide tracking.
