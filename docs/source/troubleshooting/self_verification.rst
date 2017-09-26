Running Self-Verification
=========================

|st2| includes a script to verify the installation, using |st2| itself.

The script covers the following aspects of |st2|:

* Basic ``st2`` commands
* Examples pack installation
* Commands described in :doc:`/start`
* :doc:`/packs` actions
* :doc:`/actionchain` and :doc:`/mistral` Workflows

To run the self-verification:

1. If you don't have :ref:`encryption keys setup already<admin-setup-for-encrypted-datastore>`, do so.
   This requires both |st2| and system admin privileges.

2. Run the self-check script. This also copies the examples from ``/usr/share/doc/st2/examples``
   to ``/opt/stackstorm/packs/`` and registers the content. This step pollutes your |st2| environment by
   downloading fixtures from `st2tests <https://github.com/StackStorm/st2tests/tree/master/packs/>`__.

.. code-block:: bash

    sudo ST2_AUTH_TOKEN=$(st2 auth st2admin -p '<PASSWORD>' -t) /opt/stackstorm/st2/bin/st2-self-check
