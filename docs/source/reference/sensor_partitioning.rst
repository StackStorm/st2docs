Partitioning Sensors
====================

.. note::

   If the life-cycle of your |st2| services is handled by a third party orchestrator such as
   Kubernetes, you will likely need to manually create sensor node assignments (single sensor
   running inside a single sensor container) for all the running / configured sensors.
   For more information, please refer to the :ref:`st2sensorcontainer single sensor mode
   <st2sensorcontainer-single-sensor-mode>`.

It may be desirable to partition sensors across multiple sensor nodes, either for load management
or security purposes. |st2| offers several ways of doing this.

.. contents:: :local:

Each sensor node is identified by a name. The sensor nodename can be provided via a config
property ``sensor_node_name`` as follows:

.. code-block:: ini

    [sensorcontainer]
    ...
    sensor_node_name = sensornode.example.net_f7aeb3ed

1. Default
~~~~~~~~~~

In the default scheme all sensors are run on a particular node. As the name suggests it is the
default configuration. It is useful when you have a single sensor node.

No change is required to the config file but for completeness the config would be:

.. code-block:: ini

    [sensorcontainer]
    ...
    sensor_node_name = sensornode.example.net_f7aeb3ed
    partition_provider = name:default

2. Key-Value Store
~~~~~~~~~~~~~~~~~~

In this scheme the partition map is stored in the key-value store under a special sensor
node name scoped key. This is a way to provide a fixed map and does not help with any
dynamic mapping of sensors to sensor nodes.

.. code-block:: ini

    [sensorcontainer]
    ...
    sensor_node_name = sensornode.example.net_f7aeb3ed
    partition_provider = name:kvstore


To update the key value store use the following command:

.. code-block:: bash

    st2 key set sensornode.example.net_f7aeb3ed.sensor_partition "examples.SampleSensor, examples.SamplePollingSensor"


The key format is: ``{sensor_node_name}.sensor_partition``

3. File
~~~~~~~

In this scheme the partition map is stored in a file. This is a way to provide a fixed map and
does not help with any dynamic mapping of sensors to sensor nodes.

.. code-block:: ini

    [sensorcontainer]
    ...
    sensor_node_name = sensornode.example.net_f7aeb3ed
    partition_provider = name:file, partition_file:/etc/st2/partition_file.yaml


File content is as follows:

.. code-block:: yaml

    # /etc/st2/partition_file.yaml
    ---
    sensornode.example.net_f7aeb3ed:
        - examples.SamplePollingSensor
        - examples.SampleSensor


The key format is: ``{sensor_node_name}.sensor_partition``

4. Hash
~~~~~~~

This is a dynamic scheme where each sensor node is assigned one or more hash ranges. Each sensor itself
is hashed. and depending on which bucket of the range it fits into a sensornode runs the sensor. Hash
schema is particulaly useful when there are many sensors and relatively few nodes.

The special keys ``MIN`` and ``MAX`` can also be used. This is how a typical hash provider configuration
would look:


.. code-block:: ini

    [sensorcontainer]
    ...
    sensor_node_name = sensornode.example.net_f7aeb3ed
    partition_provider = name:hash, hash_ranges:0..1024|2048..4096

Notice the format of hash_ranges. A single sensor node can support multiple sub-ranges. Each sub-range
is of the form  ``{{RANGE_START}}..{{RANGE_END}}``. Multiple sub-range are combined using ``|``.

Some useful examples

* Full range - ``MIN..MAX`` or ``0..4294967296``
* First half of range - ``MIN..2147483648``
* Second half of range - ``2147483648..MAX``
* Multiple non-contiguous ranges - ``0..1024|2048..3072|2147483648..MAX``
