.. note::

  |st2| uses a Python virtual environment in ``/opt/stackstorm/st2/`` for |st2|
  dependencies and components.

  This means that if you want to work with the |st2| installation (e.g. use the
  ``python`` binary from that virtualenv or to install a new auth backend), you
  need to use the |st2| virtual environment.

  You can do so by activating the virtual environment or running 
  ``python``/``pip`` directly from the virtual environment:

  .. code-block:: bash

    # by activating the virtual environment

    $ source /opt/stackstorm/st2/bin/activate

    $ sudo pip install foo

    # or by directly invoking binaries from the virtual environment
    $ /opt/stackstorm/st2/bin/python

    $ sudo /opt/stackstorm/st2/bin/pip install foo

