The following commands will test your |st2| installation. They should all complete successfully:

.. code-block:: bash

  st2 --version

  st2 -h

  # List the actions from a 'core' pack
  st2 action list --pack=core

  # Run a local shell command
  st2 run core.local -- date -R

  # See the execution results
  st2 execution list

  # Fire a remote comand via SSH (Requires passwordless SSH)
  st2 run core.remote hosts='localhost' -- uname -a

  # Install a pack
  st2 pack install st2

Use the supervisor script to manage |st2| services:

.. code-block:: bash

  sudo st2ctl start|stop|status|restart|restart-component|reload|clean

At this point you have a minimal working installation, and can happily play with |st2|: follow the
:doc:`/start` tutorial, :ref:`deploy the examples <start-deploy-examples>`, explore and install
packs from `StackStorm Exchange <https://exchange.stackstorm.org>`__.

But there is no joy without a Web UI, no security without SSL or authentication, no fun without
ChatOps, and no money without |bwc|. Read on!
