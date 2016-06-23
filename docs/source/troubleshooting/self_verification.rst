Running Self-Verification
=========================

|st2| package-based installations come with a script, that allows to verify |st2| installation, using |st2| itself.
Currently script covers the following aspects of |st2|:

* Basic ``st2`` commands (similar to the commands outlined in *Manual Verification* section)
* Examples pack installation
* Commands described in Quick Start
* Packs pack actions
* ActionChain and Mistral Workflows

To run the self-verification:

1. Install pre-requisite OS packages. The only dependency right now is ``bc``. To install the package, run

::
    sudo apt-get install bc  # Ubuntu

or

::
    sudo yum install bc  # CentOS/RHEL

2. If you don't have :ref:`encryption keys setup already<admin-setup-for-encrypted-datastore>`, do so. This requires admin privileges on the box and |st2|.

3. Run the self-check script. This also copies over the examples from `` /usr/share/doc/st2/examples`` to ``/opt/stackstorm/packs/`` and registers the content from examples.
This step pollutes your |st2| environment by downloading fixtures from `st2tests<https://github.com/StackStorm/st2tests/tree/master/packs>`_.

::

    sudo /opt/stackstorm/st2/bin/st2-self-check
