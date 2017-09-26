Sensor Troubleshooting
======================

If a particular sensor is not running or appears to not be working (e.g.
triggers are not emitted) follow these steps to debug it:

1. Verify Sensor is Registered
------------------------------

The first step is verifying that sensor is registered in the database. You can
do that by inspecting the output of the command below and making sure your
sensor is present:

.. sourcecode:: bash

    st2 sensor list

If your sensor is not listed, this means it's not registered. You can
register it by running the ``st2ctl`` script:

.. sourcecode:: bash

    sudo st2ctl reload --register-sensors --register-fail-on-failure --verbose

This will register sensors for all the packs which are available on the file
system. As you can see, we also use ``--register-fail-on-failure`` and ``--verbose``
flags.

This will cause the register script to exit with a non-zero exit code, and print a failure
in case registration of a particular sensor fails (e.g. typo in sensor metadata
file, invalid YAML, etc).

2. Verify Virtual Environment Exists
------------------------------------

After confirming that the sensor has been registered, you should check that a
virtual environment has been created for that sensor's pack.

You can check this by confirming the existence of the
``/opt/stackstorm/virtualenvs/<pack name>`` directory. If the directory and
virtual environment doesn't exist, you can create it using this command:

.. sourcecode:: bash

    st2 run packs.setup_virtualenv packs=<pack name>

3. Checking st2sensorcontainer Logs
-----------------------------------

If the sensor still doesn't appear to be running or working, you should run the sensor
container service in the foreground in debug and single sensor mode. In this mode the sensor
container will only run the sensor you specified and all log messages with level DEBUG and
higher will be printed directly to the console.

.. sourcecode:: bash

    /opt/stackstorm/st2/bin/st2sensorcontainer --config-file=/etc/st2/st2.conf --debug --sensor-ref=pack.SensorClassName

The log output will usually give you a clue as to what is going on. Common issues include typos and
syntax errors in the sensor class code, uncaught exceptions being thrown that causes the sensor to
exit, etc.