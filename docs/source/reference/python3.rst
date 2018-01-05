Python 3 Support
================

The StackStorm services require and are executed within a Python 2.7 environment.

Within a pack, the action code, sensors and other executable code can be executed in Python 3 where required.
To specify Python 3 as a requirement for a pack, set the ``python3`` attribute within ``system`` to true in ``pack.yaml``

.. code-block:: yaml

    ref: example
    name: Example
    system:
        python3: true

This attribute is global to that pack only and will execute any Python code within the pack under a Python 3 virtual environment.

The StackStorm configuration has a ``python3_binary`` setting to specify the default Python 3 binary path. This defaults to /usr/bin/python3 in both Ubuntu and Redhat. 
For newer versions of ubuntu, /usr/bin/python3 is a symlink to python3.5 or python3.6.

Python 3 has to be explicitly specified in the pack meta file, else Python 2.7 will be used.

If the user does not have a Python 3 binary installed it will fail on Pack Installation, virtualenv will raise an error.

