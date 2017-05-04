.. note::

  When using packages to install |st2| a special Python virtual environment is
  created in ``/opt/stackstorm/st2/`` for |st2| dependencies and components.

  This means that if you want to work and manipulate StackStorm installation
  (e.g. use ``python`` binary from that virtualenv or install new auth backend)
  you need to work with the |st2| virtual environment.

  You can do so by activating the virtual environment or running ``python`` /
  ``pip`` binary directly from the virtual environment as shown below.

  .. code-block: bash

    # by activating the virtual environment

    source /opt/stackstorm/st2/bin/activate

    pip install foo

    # or by directly invoking binaries from the virtual environment
    /opt/stackstorm/st2/bin/python

    /opt/stackstorm/st2/bin/pip install foo

