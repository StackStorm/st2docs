Sensors and Triggers
====================

Sensors
-------

Sensors are a way to integrate external systems and events with |st2|. Sensors are pieces of
Python code that either periodically poll some external system, or passively wait for inbound
events. They then inject triggers into |st2|, which can be matched by rules, for potential action
execution.

Sensors are written in Python, and must follow the |st2|-defined sensor interface requirements.

Triggers
--------

Triggers are |st2| constructs that identify the incoming events to |st2|. A trigger is a tuple of
type (string) and optional parameters (object). Rules are written to work with triggers. Sensors
typically register triggers though this is not strictly required. For example, there is a generic
:doc:`webhooks</webhooks>` trigger registered with |st2|, which does not require a custom sensor.

Internal Triggers
-----------------

By default |st2| emits some internal triggers which you can leverage in rules. Those triggers can
be distinguished from non-system triggers since they are prefixed with ``st2.``.

A list of available triggers for each resource is included below:

.. include:: _includes/internal_trigger_types.rst

.. _ref-sensors-authoring-a-sensor:

Creating a Sensor
-----------------

Creating a sensor involves writing a Python file and a YAML metadata file that defines the sensor.
Here's a minimal skeleton example. This is the metadata file:

.. literalinclude:: ../../st2/contrib/examples/sensors/sample_sensor.yaml
   :language: yaml

And this is the corresponding Python skeleton:

.. literalinclude:: ../../st2/contrib/examples/sensors/sample_sensor.py
   :language: python

This is a bare minimum version of what a sensor looks like. For a more complete implementation of
a sensor that actually injects triggers into the system, look at the `examples <#examples>`__
section below.

Your sensor should generate triggers in Python dict form:

.. code-block:: python

    trigger = 'pack.name'
    payload = {
        'executed_at': '2014-08-01T00:00:00.000000Z'
    }
    trace_tag = external_event_id


The sensor injects such triggers by using the sensor\_service passed into the sensor on
instantiation.

.. code-block:: python

    self.sensor_service.dispatch(trigger=trigger, payload=payload, trace_tag=trace_tag)

If you want a sensor that polls an external system at regular intervals, you can use a
PollingSensor instead of Sensor as the base class.

.. literalinclude:: ../../st2/contrib/examples/sensors/sample_polling_sensor.py
   :language: python

Polling Sensors also require a ``poll_interval`` parameter in the metadata file. This defines
(in seconds) how frequently the ``poll()`` method is called.

How Sensors are Run
-------------------

Each sensor runs as a separate process. The ``st2sensorcontainer`` (see
:doc:`Overview </install/overview>`) starts ``sensor_wrapper.py`` which wraps your Sensor class
(such as ``SampleSensor`` or ``SamplePollingSensor`` above) in a
:ref:`st2reactor.container.sensor_wrapper.SensorWrapper<ref-sensors-authoring-a-sensor>`.

Sensor Service
--------------

As you can see in the example above, a ``sensor_service`` is passed to each sensor class
constructor on instantiation.

The Sensor service provides different services to the sensor via public methods. The most
important one is the ``dispatch`` method which allows sensors to inject triggers into the system.

All public methods are described below:

Common Operations
-----------------

1. dispatch(trigger, payload, trace_tag)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method allows the sensor to inject triggers into the system.

For example:

.. code-block:: python

    trigger = 'pack.name'
    payload = {
        'executed_at': '2014-08-01T00:00:00.000000Z'
    }
    trace_tag = uuid.uuid4().hex

    self.sensor_service.dispatch(trigger=trigger, payload=payload, trace_tag=trace_tag)

2. get_logger(name)
~~~~~~~~~~~~~~~~~~~

This method allows the sensor instance to retrieve the logger instance which is specific
to that sensor.

For example:

.. code-block:: python

    self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
    self._logger.debug('Polling 3rd party system for information')

.. _ref-sensors-datastore-management-operations:

Datastore Management Operations
-------------------------------

In addition to the trigger injection, the sensor service also provides functionality for reading
and manipulating the :doc:`datastore <datastore>`.

Each sensor has a namespace which is local to it and by default, all the datastore operations
operate on the keys in that sensor-local namespace. If you want to operate on a global namespace,
you need to pass the ``local=False`` argument to the datastore manipulation method.

Among other reasons, this functionality is useful if you want to persist temporary data between
sensor runs.

A good example of this functionality in action is ``TwitterSensor``. The Twitter sensor persists
the ID of the last processed tweet after every poll in the datastore. This way if the sensor is
restarted or if it crashes, the sensor can resume from where it left off without injecting
duplicate triggers into the system.

For the implementation, see :github_exchange:`twitter_search_sensor.py in
StackStorm Exchange<twitter/tree/master/sensors/twitter_search_sensor.py>`

1. list_values(local=True, prefix=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method allows you to list the values in the datastore. You can also filter by key name prefix
(key name starts with) by passing ``prefix`` argument to the method:

.. code-block:: python

    kvps = self.sensor_service.list_values(local=False, prefix='cmdb.')

    for kvp in kvps:
        print(kvp.name)
        print(kvp.value)

2. get_value(name, local=True, decrypt=False)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method allows you to retrieve a single value from the datastore:

.. code-block:: python

    kvp = self.sensor_service.get_value('cmdb.api_host')
    print(kvp.name)

If the value is encrypted, you can decrypt it with this:

.. code-block:: python

    kvp = self.sensor_service.get_value('cmdb.api_password', decrypt=True)
    print(kvp.name)

3. set_value(name, value, ttl=None, local=True, encrypt=False)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method allows you to store (set) a value in the datastore. Optionally you can also specify
time to live (TTL) for the stored value:

.. code-block:: python

    last_id = 12345
    self.sensor_service.set_value(name='last_id', value=str(last_id))

Secret values can be encrypted in the datastore:

.. code-block:: python

    ma_password = 'Sup3rS34et'
    self.sensor_service.set_value(name='ma_password', value=ma_password, encrypt=True)


4. delete_value(name, local=True)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method allows you to delete an existing value from the datastore. If a value is not found this
method will return ``False``, ``True`` otherwise.

.. code-block:: python

    self.sensor_service.delete_value(name='my_key')

.. _ref-sensors-api-docs:

API Docs
~~~~~~~~

.. autoclass:: st2reactor.container.sensor_wrapper.SensorService
    :members:

Running Your First Sensor
-------------------------

Once you write your own sensor, the following steps can be used to run your sensor for the first
time:

1. Place the sensor Python file and YAML metadata in the ``default`` pack in
   ``/opt/stackstorm/packs/default/sensors/``. Alternatively, you can create a custom
   pack in ``/opt/stackstorm/packs/`` with the appropriate pack structure (see
   :doc:`/reference/packs`) and place the sensor artifacts there.

2. Register the sensor with ``st2ctl``. Watch for any errors in sensor registration:

   .. code-block:: bash

      st2ctl reload --register-all

   If there are errors in registration, fix the errors and re-register them using
   ``st2ctl reload --register-all``.

3. If registration is successful, the sensor will run automatically.

Once you like your sensor, you can promote it to a pack (if required) by creating a pack in
``/opt/stackstorm/packs/${pack_name}`` and moving the sensor artifacts (YAML and Python) to
``/opt/stackstorm/packs/${pack_name}/sensors/``. See :doc:`/reference/packs` for how to create a pack.


Examples
--------

This is a working example of a simple sensor that injects a trigger every 10 seconds.

Metadata:

.. literalinclude:: /../../st2/contrib/hello_st2/sensors/sensor1.yaml
   :language: yaml

Python code:

.. literalinclude:: /../../st2/contrib/hello_st2/sensors/sensor1.py
   :language: python

The `StackStorm Exchange <https://exchange.stackstorm.org>`__ has many more examples.
Here's just a few:


Passive Sensors
~~~~~~~~~~~~~~~

* :github_exchange:`IRC<irc/tree/master/sensors/irc_sensor.py>`

* :github_exchange:`Kafka Messages<kafka/tree/master/sensors/message_sensor.py>`

* :github_exchange:`RabbitMQ Queues<rabbitmq/tree/master/sensors/queues_sensor.py>`

Polling Sensors
~~~~~~~~~~~~~~~

* :github_exchange:`Github repository monitoring<github/tree/master/sensors/github_repository_sensor.py>`

* :github_exchange:`Jira issues<jira/tree/master/sensors/jira_sensor.py>`

* :github_exchange:`Twitter search<twitter/tree/master/sensors/twitter_search_sensor.py>`


Debugging a Sensor From a Pack
------------------------------

If you just want to run a single sensor from a pack and the sensor is already registered, you can
use the ``st2sensorcontainer`` to run just that single sensor:

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2sensorcontainer --config-file=/etc/st2/st2.conf --sensor-ref=pack.SensorClassName

For example:

.. code-block:: bash

    /opt/stackstorm/st2/bin/st2sensorcontainer --config-file=/etc/st2/st2.conf --sensor-ref=git.GitCommitSensor

Sharing code between Python Sensors and Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Refer to :ref:`documentation <ref-shared-libs-python-sensors-actions>` on sharing common code
between python actions and sensors.
