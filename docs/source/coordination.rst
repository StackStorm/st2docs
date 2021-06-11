Coordination
============

Coordination backend is required to support workflows with multiple branches or tasks with items and
actions with concurrency policies defined.

StackStorm utilizes the ``OpenStack Tooz`` library for communicating with the coordination backend.
The coordination backend must support the ``Locking`` functionality as defined by the ``Tooz`` 
interface. Please refrence the `OpenStack Tooz compatability page <https://docs.openstack.org/tooz/latest/user/compatibility.html>`_
for more information what interfaces are implemented by various backends.

The following is a list of backends that can be configured for the coordination service. For the
full list of the supported backends and how to configure them, please visit
`OpenStack Tooz documentation <https://docs.openstack.org/tooz/latest/>`_.
 
 * Redis
 * Zookeeper
 * consul
 * etcd
 * file (for testing when all the services are running on a single host)

The configuration of the coordination service is done in the ``coordination`` section
of ``/etc/st2/st2.conf``. The following are configuration examples for Redis and Zookeeper.

Redis:

.. code-block:: ini

    [coordination]
    url = redis://:password@host:port

ZooKeeper:

.. code-block:: ini

    [coordination]
    url = kazoo://username:password@host:port

Some of these coordination backends also require corresponding client libraries to be installed
in |st2| virtualenv. We do not ship these libraries by default. As an example, to install the client
library in |st2| virtualenv, run:

.. sourcecode:: bash

    sudo su

    # Example when using redis backend
    /opt/stackstorm/st2/bin/pip install redis

    # Example when using consul backend
    /opt/stackstorm/st2/bin/pip install consul
