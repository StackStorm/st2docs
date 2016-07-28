:orphan:

High availability deployment
============================

|st2| has been systematically built with High availability(HA) as a goal. The exact deployment
steps to achieve HA depend on the specifics of the infrastructure in which |st2| is deployed. This
guide covers a brief explanation on various |st2| services, how they interact and the external
services necessary for |st2| to function. As the the description that follows outlines, |st2|
components also scale horizontally thus increasing the system throughput while achieving higher
availability.

In the section :doc:`/install/overview` a detailed picture and explanation on how single-box deployments
work is provided. Repeating the picture here to keep context and use as a reference to layer on some
HA deployment specific details.

.. figure :: /_static/images/st2-deployment-big-picture.png
    :align: center

.. source https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/edit

Components
----------

st2api
^^^^^^
This process host the REST API endpoints that serve requests from WebUI, CLI and ChatOps. It maintains
connections to MongoDB to store and retrieve information. It also connects to RabbitMQ to push various
kind of messages onto the message bus. It is a Python WSGI app running under gunicorn managed process
which by default listens on port ``9101`` and is front-ended by Nginx acting as a reverse proxy.

Multiple st2api processes can be behind a loadbalancer in an active-active configuration. Each of these
processes can be deployed on separate compute instances.

st2auth
^^^^^^^
All authentication is managed by this process. This process needs connection to MongoDB and an authentication
backend. See :ref:`authentication backends <ref-auth-backends>` for more information. It is a Python WSGI app running
under gunicorn managed process which by default listens on port ``9100`` and is front-ended by Nginx acting
as a reverse proxy.

Multiple st2auth processes can be behind a loadbalancer in an active-active configuration. Each of these processes
can be deployed on separate compute instances. If using the PAM authentication backend special care has to be
taken to guarantee that all boxes on which an instance of st2auth runs should have the same users. Generally,
all st2auth process should see the same identities, via some provider if applicable, for the system to work
predictably.

st2stream
^^^^^^^^^
This process exposes a server-sent event stream. Requires access to both MongoDB and RabbitMQ. It is also a
gunicorn managed process, listens on port ``9102`` by default and is front-ended by Nginx acting as a reverse
proxy. Clients like WebUI and ChatOps maintain a persistent connection with an st2stream process and receive
update from the st2stream server.

Multiple st2stream process can be behind a loadbalances in an active-active configuration. Since clients maintain
a persistent connection with a specific instance the client will loose event momentarily if an st2stream
process goes down. It would be the responsibility of the client to reconnect to an alternate stream connection
via the loadbalancer. Note that this is in contrast with ``st2api`` where each connection from a client is
short-lived. Take the long-lived nature of connection made to this process when configuring appropriate timeouts
for loadbalancer, wsgi app server like gunicorn etc.

st2sensorcontainer
^^^^^^^^^^^^^^^^^^
st2sensorcontainer manages the sensors to be run on a node. It will start, stop and restart based on policy
sensor running on a node. In this case node is same as a compute instance i.e. Virtual Machine and somewhere
down the line could be a container.

It is possible to run a st2sensorcontainer in HA mode by running one on each compute instance thus leading
to various sensor nodes. Each sensor node needs to be provided with proper partition information to share work
with other sensor nodes so that the same sensor does not run on different nodes. See :doc:`/reference/sensor_partitioning`
for information on how to partition sensors. At this point st2sensorcontainer's do not form a cluster and
distribute work or take over new work if some nodes in the cluster disappear. It would however be possible to a
sensor itself to be implemented with HA in mind so that the same sensor can be deployed on multiple nodes with
the sensor managing active-active or active-passive. Providing some platform level HA support for sensors is
likely to be an enhancement to StackStorm in future releases.


st2rulesengine
^^^^^^^^^^^^^^
This is a dual purpose process - its main function is to evaluate rules when it sees TriggerInstances and
decide if an ActionExecution is to be requested. It needs access to MongoDB to locate rules and RabbitMQ
to listen for TriggerInstances and request ActionExecutions. The auxiliary purpose of this process is to
run all the defined timers. See :ref:`timers <ref-rule-timers>` for specifics on setting up timers via rules.

Multiple st2rulesengine can run in active-active with only connections to MongoDB and RabbitMQ. All these will
share the TriggerInstance load and naturally pick up more work if one or more of the process becomes unavailable.
The timer function in each of the RulesEngine is not HA compatible. In the interim it is possible to disable the
timer in all but one of the st2rulesengine to avoid duplicate timer events, expect this to be fixed in a future
|st2| release.

st2actionrunner
^^^^^^^^^^^^^^^
All ActionExecutions are handled for execution by st2actionrunner. It manages the full life-cycle of an execution from
scheduling to one of the terminal states.

Multiple st2actionrunner can run in active-active with only connections to MongoDB and RabbitMQ. Work gets naturally
distributed across runners via RabbitMQ. Adding more st2actionrunner increases the ability of |st2| to execute actions.

In a proper distributed setup it is recommended to setup Zookeeper or Redis to provide a distributed co-ordination
layer. See :doc:`Policies </policies>`. Using a default file based co-ordination backend will not work as it would
in a single box deployment.

st2resultstracker
^^^^^^^^^^^^^^^^^
Tracks results of execution handed over to mistral. It requires access to MongoDB and RabbitMQ to perform its function.

Multiple st2resultstracker will co-operate with each other to perform work. At startup though there is a possibility
of extra work however there will no negative consequences of this duplication. Specifically the jobs to track results
also get stored in the DB in case there are no workers to take over the work, this pattern makes all result trackers
pick up the same work set on startup. Once this work set is exhausted all subsequent tasks are round-robined. If needed
st2resulttracker processes could be started in a staggered manner to avoid extra work.

st2notifier
^^^^^^^^^^^
This is a dual purpose process - its main function is to generate ``st2.core.actiontrigger`` and ``st2.core.notifytrigger``
based on the completion of ActionExecution. The auxiliary purpose is to act as a backup scheduler for actions that may
not have been scheduled.

Multiple st2notifiers can run in active-active requiring connections to RabbitMQ and MongoDB. For the auxiliary purpose to
function in an HA deployment when more than 1 st2notifiers are running either Zookeeper or Redis is required to provide co-ordination much like for policies. It is also possible to designate a single st2notifier as provider of auxiliary functions
by disabling the scheduler in all but 1 st2notifiers.

st2garbagecollector
^^^^^^^^^^^^^^^^^^^
Optional service that cleans up old executions and other operations data based on setup configurations. By default
this process does nothing and needs to be setup to perform any work.

By design it is a singleton process. Running multiple in active-active will not yield much benefit and also will not
do any harm. Ideal configuration is active-passive but |st2| does not itself provide ability to run this in active-passive.

mistral-api
^^^^^^^^^^^
Mistral api is served by this aptly named process. It needs access to PostgreSQL and RabbitMQ.

Multiple mistral-api can run and just like st2api in active-active configuration by using a loadbalancer to distribute at its
front end. In typical single box deployment mistral-api is local to the box and |st2| communicates via a direct HTTP
connection however for HA setup we recommend putting mistral-api behind a loadbalancer and setting up |st2| to communicate
via the loadbalancer.

mistral-server
^^^^^^^^^^^^^^
mistral-server is the worker engine for mistral i.e. the process which actually manages executions. |st2| plugin to
mistral i.e. ``st2mistral`` communicates back to |st2| api. This process needs access to PostgreSQL and RabbitMQ.

Multiple mistral-server can run and co-ordinate work in an active-active configuration. In an HA deployment all communication
with the |st2| API must be via the configured loadbalancer.

Required dependencies
---------------------
Some HA recommendations for the dependencies required by |st2| components. Depending on the exact infrastructure these
may not be suitable and would only serve as a suggestion.

MongoDB
^^^^^^^
|st2| uses this to cache Actions, Rules and Sensor metadata which already live in the filesystem. All the content should
ideally be source-control managed in preferably a git repository. |st2| also stores operation data like ActionExecution,
TriggerInstance etc. MongoDB supports `replica set high-availability <https://docs.mongodb.org/v2.4/core/replica-set-high-availability/>`__
which we recommend to provide a safe failover.

Loss of connectivity to a MongoDB cluster will cause downtime for |st2|. However, once a replica MongoDB is brought back it
should be quite possible to bring |st2| back to operational state by simply loading the content. Easy access to old
ActionExecutions will be lost but all the data of old ActionExecution will still be available in audit logs.

PostgreSQL
^^^^^^^^^^
Used primarily by ``mistral-api`` and ``mistral-server``. To deploy PostgreSQL in HA please see
`documentation <http://www.postgresql.org/docs/9.4/static/high-availability.html>`__ provided by the PostgreSQL project.

The data stored in PostgreSQL is operational for mistral therefore starting from a brand new PostgreSQL in case of loss
of a cluster will bring automation services back instantly. Certainly there will be downtime while a new DB cluster is provisioned.

RabbitMQ
^^^^^^^^
RabbitMQ is the communication hub for |st2| to co-ordinate and distribute work. See
`RabbitMQ documentation <https://www.rabbitmq.com/ha.html>`__ to understand HA deployment strategies.

Our recommendation is to mirror all the Queues and Exchanges so that loss of 1 server still retains functionality.

Zookeeper/Redis
^^^^^^^^^^^^^^^
Various |st2| features rely on a proper co-ordination backend in a distributed deployment to work correctly.

`This <http://zookeeper.apache.org/doc/trunk/zookeeperStarted.html#sc_RunningReplicatedZooKeeper>`__ shows
how to run a replicated zookeeper setup. See `this <http://redis.io/topics/sentinel>`__ to understand Redis
deployments using sentinel.


Nginx and loadbalancer
^^^^^^^^^^^^^^^^^^^^^^^
An Nginx server is required to reverse proxy each instance of ``st2api``, ``st2auth``, ``st2stream`` and ``mistral-api``.
This server will terminate SSL connections, shield clients from internal port numbers of various services and only require
ports 80 and 443 to be open on containers. Often it is best to deploy 1 set of all these services on a compute instance
and share an Nginx server.

There is also a need for a loadbalancer to frontend all the REST services. This results in an HA deployment for REST
services as well as single endpoint for clients. Most deployment infrastructures will already have a loadbalancer
solution which they would prefer to use so we do not provide any recommendations.

Sharing Content
---------------
In an HA setup with ``st2apu``, ``st2actionrunner`` and ``st2sensorcontainer`` each running on multiple boxes
the question of managing distributed content is crucial. |st2| does not provide a built-in solution to distributing
content on various boxes. Instead it relieas on management of |st2| content from outside and here are a few strategies.

Read-Write NFS mounts
^^^^^^^^^^^^^^^^^^^^^
If content folders i.e. ``/opt/stackstorm/packs`` and ``/opt/stackstorm/virtualenvs`` are placed on read-write NFS
mounts then writing from any |st2| node will be visible to other nodes. Special care needs to be take in case
of ``/opt/stackstorm/virtualenvs`` since that has symlinks to system libraries. If care is not taken to provision
all host boxes in an identical manner it could leads to unpredicatble behavior. Although possible to implement in
this manner it is certainly not ideal and perhaps managing the ``virtualenvs`` on every host box individually would
be a more robust approach.


Content management
^^^^^^^^^^^^^^^^^^
Managing pack installation using a content management tool of your choice. Assuming that the list of packs to be deployed
will be static in deployments then deploying content to |st2| nodes via CM tools could be a sub-step of an overall
|st2| deployment. This is perhaps the better of the two approaches to end up with a predicatble HA deployment of |st2|.

Reference HA setup
------------------

In this section we provide a highly opinionated and therefore prescriptive approach to deploying |st2| in HA. This deployment
has 3 independent boxes which we categorize as controller box and blueprint box. Let call these boxes ``st2-multi-node-cntl``,
``st2-multi-node-1`` and ``st2-multi-node-2``. For the sake of reference we will be using Ubuntu 14.04 as the base operating
system.

.. figure :: /_static/images/st2-deployment-multi-node.png
    :align: center

    StackStorm HA reference deployment.

.. source https://docs.google.com/drawings/d/1_BJa9ZtBjFa1Dxx6cPiFlmpTS9AsNzkkvp_vuyVV3bw/edit

Controller box
^^^^^^^^^^^^^^
This box runs all the shared required dependencies and some |st2| components.

* Nginx as loadbalancer
* MongoDB
* PostgreSQL
* RabbitMQ
* st2chatops
* st2web

In practice ``MongoDB``, ``PostgreSQL`` and ``RabbitMQ`` are often in standalone clusters managed outside of |st2|.
The 2 shared components i.e. ``st2chatops`` and ``st2web`` are placed here for sake of convenience and could be placed anywhere
with the right configuration.

Nginx acting as the loadbalancer can easily be switched out for Amazon ELB, HAProxy or any other of your choosing. In that case
``st2web`` which is being served off this Nginx will also need a new home.

``st2chatops`` which use ``hubot`` is not easily deployed in HA. Using something like `keepalived <http://www.keepalived.org/>`__
to maintain st2chatops in active-passive configuration would be an option.

Following are the steps to provision a controller box on Ubuntu 14.04.

Install required dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install ``MongoDB``, ``PostgreSQL`` and ``RabbitMQ``.

  .. code-block:: bash

        sudo apt-get install -y mongodb-server rabbitmq-server postgresql


2. Fix listen address in ``/etc/postgresql/9.3/main/postgresql.conf`` and have PostgreSQL listen an interface that has an
   IP address reachable from ``st2-multi-node-1`` and ``st2-multi-node-2``.

3. Fix ``bind_ip`` in ``/etc/mongodb.conf`` to bind MongoDB to an interface that has an IP address reachable
   from ``st2-multi-node-1`` and ``st2-multi-node-2``.

4. Restart MongoDB.

   .. code-block:: bash

        service mongodb restart

5. To ``/etc/postgresql/9.3/main/pg_hba.conf`` add an ACL rule. Here the subnet to allow access is ``10.0.3.1/24``

  .. code-block:: bash

        host       all  all  10.0.3.1/24  trust

6. restart PostgreSQL

  .. code-block:: bash

         service postgresql restart

7. Create Mistral DB in PostgreSQL.

  .. code-block:: bash

        cat << EHD | sudo -u postgres psql
        CREATE ROLE mistral WITH CREATEDB LOGIN ENCRYPTED PASSWORD 'StackStorm';
        CREATE DATABASE mistral OWNER mistral;
        EHD

8. Add stable |st2| repos.

  .. code-block:: bash

        curl -s https://packagecloud.io/install/repositories/StackStorm/staging-stable/script.deb.sh | sudo bash

9. Setup st2web and SSL termination. Follow :ref:`install webui and setup ssl<ref-install-webui-ssl-deb>`.  You will need to stop after removing the default nginx config file.

10. Sample configuration for Nginx as loadbalancer for controller box is provided below. With this configuration Nginx will loadbalance all requests between the two blueprint boxes ``st2-multi-node-1`` and ``st2-multi-node-2``. This includes requests to ``st2api``, ``st2auth`` and ``mistral-api``. Nginx also serves as the webserver for st2web.

.. literalinclude:: /../../st2/conf/HA/nginx/st2.conf.controller.sample

11. Create the st2 logs directory and the st2 user.

  .. code-block:: bash

        mkdir -p /var/log/st2
        useradd st2

12. Install st2chatops following from :ref:`setup chatops<ref-setup-chatops-deb>`.

Blueprint box
^^^^^^^^^^^^^
This box is a repeatable |st2| image that is essentially the single-box reference deployment with a few changes. The aim is
to Deploy as many of these boxes for desired HA objectives and also get some horizontal scaling. |st2| processes outlined
above support the capbility of being turned on-off individually therefore each box can also be made to offer different services.

1.  Add stable |st2| repos.

  .. code-block:: bash

        curl -s https://packagecloud.io/install/repositories/StackStorm/staging-stable/script.deb.sh | sudo bash

2. Install all |st2| components and mistral.

  .. code-block:: bash

        sudo apt-get install -y st2 st2mistral

3. Install Nginx.

  .. code-block:: bash

        sudo apt-get install -y nginx

4. Update Mistral connection to PostgreSQL in ``/etc/mistral/mistral.conf`` by changing ``atabase.connection`` property.

5. Update Mistral connection to RabbitMQ in ``/etc/mistral/mistral.conf`` by changing ``default.transport_url`` property.

6. Setup Mistral DB tables, etc.

  .. code-block:: bash

        /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head

7. Register mistral actions

  .. code-block:: bash

        /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate

8. Replace ``/etc/st2/st2.conf`` with the sample st2.conf provided below. This config points to the controller node or configuration values of ``database``, ``messaging`` and ``mistral``.

.. literalinclude:: /../../st2/conf/HA/st2.conf.sample

9. Generate a certificate.

  .. code-block:: bash

        sudo mkdir -p /etc/ssl/st2
        sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/st2/st2.key -out /etc/ssl/st2/st2.crt \
        -days XXX -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information \
        Technology/CN=$(hostname)"

9. If you are using self signed certificates you will need to add ``insecure = true`` to the ``mistral`` section of ``/etc/st2/st2.conf``.

10. Configure users & authentication as per :ref:`this documentation<ref-config-auth-deb>`. Make sure that user configuration on all boxes running ``st2auth`` is identical. This ensures consistent authentication from the entire |st2| install since the request to authenticate a user
   can be forwarded by the loadbalancer to any of the ``st2auth`` processes.

11. Use the sample Nginx config that is provided below for the blueprint boxes. In this config Nginx will act as the SSL termination endpoint for all the REST endpoints exposed by ``st2api``, ``st2auth`` and ``mistral-api``.

.. literalinclude:: /../../st2/conf/HA/nginx/st2.conf.blueprint.sample

12. To use Timer triggers with mistral please do the following to only enable them on one server by doing the following in `/etc/st2/st2.conf` 

    .. code-block:: yaml
        
        [timer]
        enable = False
        

13. See :doc:`/reference/sensor_partitioning` to decide on how to partition sensors that suit your requirements.

14. All content should be synced by choosing a suitable strategy as outlined above. This is cruicial to obtain predicatable outcomes.
