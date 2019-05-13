High Availability Deployment
============================

|st2| has been systematically built with High availability(HA) as a goal. The exact deployment
steps to achieve HA depend on the specifics of the infrastructure in which |st2| is deployed. This
guide covers a brief explanation on various |st2| services, how they interact and the external
services necessary for |st2| to function. Note that |st2| components also scale horizontally thus
increasing the system throughput while achieving higher availability.

In the section :doc:`/install/overview` a detailed picture and explanation of how single-box
deployments work is provided. Let's reproduce the picture here, to keep some context, and use it as
a reference to layer on some HA deployment-specific details.

.. figure :: /_static/images/st2-deployment-big-picture.png
    :align: center

.. source https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/edit

.. note::

    A reproducible blueprint of StackStorm HA cluster is available as a code based on Docker and Kubernetes, see :doc:`/install/k8s_ha`.


Components
----------

First, a review of |st2| components:

st2api
^^^^^^
This process hosts the REST API endpoints that serve requests from WebUI, CLI and ChatOps. It
maintains connections to MongoDB to store and retrieve information. It also connects to RabbitMQ
to push messages onto the message bus. It is a Python WSGI app running under a gunicorn-managed
process which by default listens on port ``9101``. It is front-ended by Nginx, acting as a reverse
proxy.

Multiple ``st2api`` processes can be behind a load balancer in an active-active configuration.
Each of these processes can be deployed on separate compute instances.

st2auth
^^^^^^^
All authentication is managed by this process. This process needs a connection to MongoDB and an
authentication backend. See :ref:`authentication backends <ref-auth-backends>` for more
information. It is a Python WSGI app running under a gunicorn-managed process which by default
listens on port ``9100``. It is front-ended by Nginx acting as a reverse proxy.

Multiple ``st2auth`` processes can be behind a load balancer in an active-active configuration.
Each of these processes can be deployed on separate compute instances. If using the PAM
authentication backend, special care has to be taken to guarantee that all boxes on which an
instance of ``st2auth`` runs should have the same users. Generally, all ``st2auth`` process should
see the same identities, via some provider if applicable, for the system to work predictably.

st2stream
^^^^^^^^^
This process exposes a server-sent event stream. It requires access to both MongoDB and RabbitMQ.
It is also a gunicorn-managed process, listening on port ``9102`` by default. It is front-ended by
Nginx acting as a reverse proxy. Clients like WebUI and ChatOps maintain a persistent connection
with an ``st2stream`` process and receive update from the ``st2stream`` server.

Multiple ``st2stream`` process can be behind a load balancer in an active-active configuration.
Since clients maintain a persistent connection with a specific instance the client will briefly
lose events if an ``st2stream`` process goes down. It is the responsibility of the client to
reconnect to an alternate stream connection via the load balancer. Note that this is in contrast
with ``st2api`` where each connection from a client is short-lived. Take the long-lived nature of
connections made to this process when configuring appropriate timeouts for load balancers, wsgi
app servers like gunicorn etc.

st2sensorcontainer
^^^^^^^^^^^^^^^^^^
``st2sensorcontainer`` manages the sensors to be run on a node. It will start, stop and restart
sensors running on a node. In this case a node is the same as a compute instance i.e. a Virtual
Machine. In future this could be a container.

It is possible to run ``st2sensorcontainer`` in HA mode by running one process on each compute
instance. Each sensor node needs to be provided with proper partition information to share work
with other sensor nodes so that the same sensor does not run on different nodes.
See :doc:`/reference/sensor_partitioning` for information on how to partition sensors. Currently
``st2sensorcontainer`` processes do not form a cluster and distribute work or take over
new work if some nodes in the cluster disappear. It is possible for a sensor itself to be
implemented with HA in mind so that the same sensor can be deployed on multiple nodes with the
sensor managing active-active or active-passive. Providing some platform level HA support for
sensors is likely to be an enhancement to |st2| in future releases.

.. _st2sensorcontainer-single-sensor-mode:

By default sensor container service runs in managed mode. This means that the sensor container
process manages child processes for all the running sensors and restarts them if they crash or
similar.

In some scenarios this is not desired and service / process life-cycle (restarting, scaling out,
etc.) is handled by a third party service such as Kubernetes.

To account for such deployments, sensor container can be started in single sensor mode using
``--single-sensor-mode`` and ``--sensor-ref`` command line options. When those options are
provided, sensor container service will run a single sensor and exit immediately if a sensor
crashes or similar.

For example:

.. code-block:: bash

  st2sensorcontainer --single-sensor-mode --sensor-ref linux.FileWatchSensor

st2rulesengine
^^^^^^^^^^^^^^
``st2rulesengine`` evaluates rules when it sees
TriggerInstances and decide if an ActionExecution is to be requested. It needs access to MongoDB to
locate rules and RabbitMQ to listen for TriggerInstances and request ActionExecutions.

Multiple ``st2rulesengine`` processes can run in active-active with only connections to MongoDB and
RabbitMQ. All these will share the TriggerInstance load and naturally pick up more work if one or
more of the processes becomes unavailable.

st2timersengine
^^^^^^^^^^^^^^^

``st2timersengine`` is responsible for scheduling all user specified timers. See
:ref:`timers <ref-rule-timers>` for the specifics on setting up timers via rules.
``st2timersengine`` process needs access to both Mongo database and RabbitMQ message bus.

You have to have exactly one active ``st2timersengine`` process running to schedule all timers.
Having more than one active ``st2timersengine`` will result in duplicate timer events and therefore
duplicate rule evaluations leading to duplicate workflows or actions.

In HA deployments, external monitoring needs to setup and a new ``st2timersengine`` process needs
to be spun up to address failover. Losing the ``st2timersengine`` will mean no timer events will be
injected into |st2| and therefore no timer rules would be evaluated.

st2workflowengine
^^^^^^^^^^^^^^^^^

``st2workflowengine`` drives the execution of orquesta workflows. Once the orquesta action runner
passes the workflow execution request to the ``st2workflowengine``, the workflow engine evaluates
the execution graph generated by the workflow definition and identifies the next set of tasks to
run. If the workflow execution is still in a running state and there are tasks identified, the
workflow engine will launch new action executions according to the task spec in the workflow
definition.

When an action execution completed under the context of an orquesta workflow, the
``st2workflowengine`` processes the completion logic and determines if the task is completed. If
the task is completed, the workflow engine then evaluates the criteria for task transition and
identifies the next set of tasks and launch new action executions accordingly. This continues to
happen until there are no more tasks to execute or the workflow execution is in a completed
state.

Multiple ``st2workflowengine`` processes can run in active-active with only connections to MongoDB
and RabbitMQ. All the workflow engine processes will share the load and pick up more work if one or
more of the processes become available. However, please note that if one of the workflow engines
goes offline unexpectedly while processing a request, it is possible that the request or the
particular instance of the workflow execution will be in an unexpected state.

st2actionrunner
^^^^^^^^^^^^^^^
All ActionExecutions are handled by ``st2actionrunner``. Once an execution is scheduled
``st2actionrunner`` handles the life-cycle of an execution to one of the terminal states.

Multiple ``st2actionrunner`` processes can run in active-active with only connections to MongoDB
and RabbitMQ. Work gets naturally distributed across runners via RabbitMQ. Adding more
``st2actionrunner`` processes increases the ability of |st2| to execute actions.

In a proper distributed setup it is recommended to setup Zookeeper or Redis to provide a
distributed co-ordination layer. See :doc:`Policies </reference/policies>`. Using the default
file-based co-ordination backend will not work as it would in a single box deployment.

st2scheduler
^^^^^^^^^^^^
``st2scheduler`` is responsible for handling ingress action execution requests.
It takes incoming requests off the bus and queues them for eventual scheduling
with an instance of ``st2actionrunner``.

Multiple instances of ``st2scheduler`` can be run at a time. Database
versioning prevents multiple execution requests from being picked up by
different schedulers. Scheduler garbage collection handles executions that might
have failed to be scheduled by a failed ``st2scheduler`` instance.


st2resultstracker
^^^^^^^^^^^^^^^^^
Tracks results of execution handed over to Mistral. It requires access to MongoDB and RabbitMQ to
perform its function.

Multiple ``st2resultstracker`` processes will co-operate with each other to perform work. At
startup there is a possibility of extra work however there are no negative consequences of this
duplication. Specifically the jobs to track results also get stored in the DB in case there are no
workers to take over the work. This pattern makes all result trackers pick up the same work set on
startup. Once this work set is exhausted all subsequent tasks are round-robined. If needed
``st2resultstracker`` processes could be started in a staggered manner to avoid extra work.

st2notifier
^^^^^^^^^^^
This is a dual purpose process - its main function is to generate ``st2.core.actiontrigger`` and
``st2.core.notifytrigger`` based on the completion of ActionExecution. The auxiliary purpose is to
act as a backup scheduler for actions that may not have been scheduled.

Multiple ``st2notifier`` processes can run in active-active mode, using connections to RabbitMQ
and MongoDB. For the auxiliary purpose to function in an HA deployment when more than one
``st2notifier`` is running, either Zookeeper or Redis is required to provide co-ordination. It is
also possible to designate a single ``st2notifier`` as provider of auxiliary functions by disabling
the scheduler in all but one ``st2notifiers``.

st2garbagecollector
^^^^^^^^^^^^^^^^^^^
Optional service that cleans up old executions and other operations data based on setup
configurations. By default this process does nothing and needs to be setup to perform any work.

By design it is a singleton process. Running multiple instances in active-active will not yield
much benefit, but will not do any harm. The ideal configuration is active-passive but |st2| itself
does not provide the ability to run this in active-passive.


mistral-api
^^^^^^^^^^^
Mistral API is served by this aptly named process. It needs access to PostgreSQL and RabbitMQ.

Multiple ``mistral-api`` processes can run in an active-active configuration by using a load
balancer to distribute at its front end. This is similar to ``st2api``. In a typical single box
deployment ``mistral-api`` is local to the box and |st2| communicates via a direct HTTP connection.
For HA setup we recommend putting ``mistral-api`` behind a load balancer and setting up |st2| to
communicate via the load balancer.

mistral-server
^^^^^^^^^^^^^^
``mistral-server`` is the worker engine for mistral i.e. the process which actually manages
executions. The |st2| plugin to mistral (``st2mistral``) communicates back to the |st2| API. This
process needs access to PostgreSQL and RabbitMQ.

Multiple ``mistral-server`` processes can run and co-ordinate work in an active-active
configuration. In an HA deployment all communication with the |st2| API must be via the configured
load balancer.

Required Dependencies
---------------------
This section has some HA recommendations for the dependencies required by |st2| components. This
should serve as a guide only. The exact configuration will depend upon the site infrastructure.

MongoDB
^^^^^^^
|st2| uses this to cache Actions, Rules and Sensor metadata which already live in the filesystem.
All the content should ideally be source-control managed, preferably in a git repository. |st2|
also stores operational data like ActionExecution, TriggerInstance etc. The Key-Value datastore
contents are also maintained in MongoDB.

MongoDB supports `replica set high-availability
<https://docs.mongodb.org/v3.4/core/replica-set-high-availability/>`__, which we recommend to
provide safe failover. See :ref:`here<ref-mongo-ha-config>` for how to configure |st2| to connect
to MongoDB replica sets.

Loss of connectivity to a MongoDB cluster will cause downtime for |st2|. However, once a replica
MongoDB is brought back it should be possible to bring |st2| back to operational state by
simply loading the content (through ``st2ctl reload --register-all`` and ``st2 key load``. Easy
access to old ActionExecutions will be lost but all the data of old ActionExecutions will still
be available in audit logs.

PostgreSQL
^^^^^^^^^^
Used primarily by ``mistral-api`` and ``mistral-server``. To deploy PostgreSQL in HA please see
`the PostgreSQL documentation <http://www.postgresql.org/docs/9.4/static/high-availability.html>`__.

The data stored in PostgreSQL is operational for Mistral, therefore starting from a brand new
PostgreSQL in case of loss of a cluster will bring automation services back instantly. There will
be downtime while a new DB cluster is provisioned.

RabbitMQ
^^^^^^^^
RabbitMQ is the communication hub for |st2| to co-ordinate and distribute work. See
`RabbitMQ documentation <https://www.rabbitmq.com/ha.html>`__ to understand HA deployment
strategies.

Our recommendation is to mirror all the Queues and Exchanges so that the loss of one server does
not affect functionality.

See :ref:`here<ref-rabbitmq-cluster-config>` for how to configure |st2| to connect to a RabbitMQ
cluster.

Zookeeper/Redis
^^^^^^^^^^^^^^^
Various |st2| features rely on a proper co-ordination backend in a distributed deployment to work
correctly.

`This <http://zookeeper.apache.org/doc/trunk/zookeeperStarted.html#sc_RunningReplicatedZooKeeper>`__
shows how to run a replicated Zookeeper setup. See `this <http://redis.io/topics/sentinel>`__ to
understand Redis deployments using sentinel.

Nginx and Load Balancing
^^^^^^^^^^^^^^^^^^^^^^^^
An load balancer is required to reverse proxy each instance of ``st2api``, ``st2auth``,
``st2stream`` and ``mistral-api``. In the reference setup, Nginx is used for this. This server
terminates SSL connections, shields clients from internal port numbers of various services
and only require ports 80 and 443 to be open on containers.

Often it is best to deploy one set of all these services on a compute instance and share an Nginx
server.

There is also a need for a load balancer to frontend all the REST services. This results in an HA
deployment for REST services as well as single endpoint for clients. Most deployment
infrastructures will already have a load balancer solution which they would prefer to use so we do
not provide any specific recommendations.

Sharing Content
---------------
In an HA setup with ``st2api``, ``st2actionrunner`` and ``st2sensorcontainer`` each running on
multiple boxes the question of managing distributed content is crucial. |st2| does not provide a
built-in solution to distributing content on various boxes. Instead it relies on external
management of |st2| content. Here are a few strategies:

Read-Write NFS mounts
^^^^^^^^^^^^^^^^^^^^^
If the content folders i.e. ``/opt/stackstorm/packs`` and ``/opt/stackstorm/virtualenvs`` are
placed on read-write NFS mounts then writes from any |st2| node will be visible to other nodes.
Special care needs to be taken with ``/opt/stackstorm/virtualenvs`` since that has symlinks to
system libraries. If care is not taken to provision all host boxes in an identical manner it could
lead to unpredictable behavior. Managing the ``virtualenvs`` on every host box individually would
be a more robust approach.

Content management
^^^^^^^^^^^^^^^^^^
Manage pack installation using a configuration management tool of your choice, such as Ansible,
Puppet, Chef, or Salt. Assuming that the list of packs to be deployed will be static, then
deploying content to |st2| nodes via CM tools could be a sub-step of an overall |st2| deployment.
This is perhaps the better of the two approaches to end up with a predictable HA deployment.

Reference HA setup
------------------

In this section we provide a highly opinionated and therefore prescriptive approach to deploying
|st2| in HA. This deployment has 3 independent boxes which we categorize as "controller box" and
"blueprint box." We'll call these boxes ``st2-multi-node-cntl``, ``st2-multi-node-1`` and
``st2-multi-node-2``. For the sake of reference we will be using Ubuntu 14.04 as the base OS.
Obviously you can also use RedHat/CentOS.

.. figure :: /_static/images/st2-deployment-multi-node.png
    :align: center

    |st2| HA reference deployment.

.. source https://docs.google.com/drawings/d/1_BJa9ZtBjFa1Dxx6cPiFlmpTS9AsNzkkvp_vuyVV3bw/edit

Controller Box
^^^^^^^^^^^^^^
This box runs all the shared required dependencies and some |st2| components:

* Nginx as load balancer
* MongoDB
* PostgreSQL
* RabbitMQ
* st2chatops
* st2web

In practice ``MongoDB``, ``PostgreSQL`` and ``RabbitMQ`` will usually be on standalone clusters
managed outside of |st2|. The two shared components (``st2chatops`` and ``st2web``) are placed here
for the sake of convenience. They could be placed anywhere with the right configuration.

The Nginx load balancer can easily be switched out for Amazon ELB, HAProxy or any other of your
choosing. In that case ``st2web`` which is being served off this Nginx instance will also need a
new home.

``st2chatops`` which uses ``hubot`` is not easily deployed in HA. Using something like
`keepalived <http://www.keepalived.org/>`__ to maintain ``st2chatops`` in active-passive
configuration is an option.

Follow these steps to provision a controller box on Ubuntu 14.04:

Install Required Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install ``MongoDB``, ``PostgreSQL`` and ``RabbitMQ``:

  .. code-block:: bash

      $ sudo apt-get install -y mongodb-server rabbitmq-server postgresql


2. Fix the listen address in ``/etc/postgresql/9.3/main/postgresql.conf`` and have PostgreSQL
   listen on an interface that has an IP address reachable from ``st2-multi-node-1`` and
   ``st2-multi-node-2``.

3. Fix ``bind_ip`` in ``/etc/mongodb.conf`` to bind MongoDB to an interface that has an IP address
   reachable from ``st2-multi-node-1`` and ``st2-multi-node-2``.

4. Restart MongoDB:

   .. code-block:: bash

      $ sudo service mongodb restart

5. Add an ACL rule to ``/etc/postgresql/9.3/main/pg_hba.conf``. In this example we're allowing
   access from the subnet ``10.0.3.0/24``

  .. code-block:: bash

        host       all  all  10.0.3.0/24  trust

6. Restart PostgreSQL:

  .. code-block:: bash

      $ sudo service postgresql restart

7. Create Mistral DB in PostgreSQL:

  .. code-block:: bash

      $ cat << EHD | sudo -u postgres psql
      CREATE ROLE mistral WITH CREATEDB LOGIN ENCRYPTED PASSWORD 'StackStorm';
      CREATE DATABASE mistral OWNER mistral;
      EHD

8. Add stable |st2| repos:

  .. code-block:: bash

      $ curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.deb.sh | sudo bash

9. Setup ``st2web`` and SSL termination. Follow :ref:`install webui and setup
   ssl<ref-install-webui-ssl-deb>`. You will need to stop after removing the default Nginx config
   file.

10. A sample configuration for Nginx as load balancer for the controller box is provided below.
    With this configuration Nginx will load balance all requests between the two blueprint boxes
    ``st2-multi-node-1`` and ``st2-multi-node-2``. This includes requests to ``st2api``,
    ``st2auth`` and ``mistral-api``. Nginx also serves as the webserver for ``st2web``.

  .. literalinclude:: /../../st2/conf/HA/nginx/st2.conf.controller.sample
     :language: none

11. Create the st2 logs directory and the st2 user:

  .. code-block:: bash

        mkdir -p /var/log/st2
        useradd st2

12. Install ``st2chatops`` following :ref:`setup chatops<ref-setup-chatops-deb>`.

Blueprint box
^^^^^^^^^^^^^
This box is a repeatable |st2| image that is essentially the single-box reference deployment with a
few changes. The aim is to deploy as many of these boxes for desired HA objectives and horizontal
scaling. |st2| processes outlined above can be turned on/off individually, therefore each box can
also be made to offer different services.

1.  Add stable |st2| repos:

  .. code-block:: bash

      $ curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.deb.sh | sudo bash

2. Install all |st2| components and mistral:

  .. code-block:: bash

      $ sudo apt-get install -y st2 st2mistral

3. Install Nginx:

  .. code-block:: bash

      $ sudo apt-get install -y nginx

4. Update Mistral connection to PostgreSQL in ``/etc/mistral/mistral.conf`` by changing the
   ``database.connection`` property.

5. Update Mistral connection to RabbitMQ in ``/etc/mistral/mistral.conf`` by changing  the
   ``default.transport_url`` property.

6. Setup Mistral database:

  .. code-block:: bash

      $ /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head

7. Register mistral actions:

  .. code-block:: bash

      $ /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate | grep -v -e openstack -e keystone

8. Replace ``/etc/st2/st2.conf`` with the sample ``st2.conf`` provided below. This config points to
   the controller node or configuration values of ``database``, ``messaging`` and ``mistral``.

  .. literalinclude:: /../../st2/conf/HA/st2.conf.sample
     :language: ini

9. Generate a certificate:

  .. code-block:: bash

      $ sudo mkdir -p /etc/ssl/st2
      $ sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/st2/st2.key -out /etc/ssl/st2/st2.crt \
        -days XXX -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information \
        Technology/CN=$(hostname)"

10. If you are using self-signed certificates you will need to add ``insecure = true`` to the
    ``mistral`` section of ``/etc/st2/st2.conf``.

11. Configure users & authentication as per :ref:`this documentation<ref-config-auth-deb>`. Make
    sure that user configuration on all boxes running ``st2auth`` is identical. This ensures
    consistent authentication from the entire |st2| install since the request to authenticate a
    user can be forwarded by the load balancer to any of the ``st2auth`` processes.

12. Use the sample Nginx config that is provided below for the blueprint boxes. In this config
    Nginx will act as the SSL termination endpoint for all the REST endpoints exposed by
    ``st2api``, ``st2auth`` and ``mistral-api``:

  .. literalinclude:: /../../st2/conf/HA/nginx/st2.conf.blueprint.sample
     :language: nginx

13. To use Timer triggers with Mistral, enable them on only one server. Make this change in
    ``/etc/st2/st2.conf``:

    .. code-block:: yaml

        [timer]
        enable = False


14. See :doc:`/reference/sensor_partitioning` to decide how to partition sensors to suit your
    requirements.

15. All content should be synced by choosing a suitable strategy as outlined above. This is crucial
    to obtain predictable outcomes.
