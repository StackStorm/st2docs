Running Self-Verification
=========================

|st2| includes a script for verifying the system installation.

The script covers the following aspects of |st2|:

* Basic ``st2`` commands
* Examples pack installation
* Commands described in :doc:`/start`
* :doc:`/packs` actions
* :doc:`/actionchain` and :doc:`/mistral` Workflows

To run the |st2| self-verification script:

1. If you don't have :ref:`encryption keys setup already<admin-setup-for-encrypted-datastore>`, do so.
   This will require both |st2| and system admin privileges to configure.

2. Run the self-check script ``/opt/stackstorm/st2/bin/st2-self-check``. This also copies the examples from ``/usr/share/doc/st2/examples`` to ``/opt/stackstorm/packs/`` and registers the content. Running this step will pollute your |st2| environment because it will download fixtures from `st2tests <https://github.com/StackStorm/st2tests/tree/master/packs/>`__.

..code-block:: bash

    sudo ST2_AUTH_TOKEN=$(st2 auth st2admin -p '<PASSWORD>' -t) /opt/stackstorm/st2/bin/st2-self-check
