:orphan:

High availability deployment
============================

|st2| has been systematically built with High availability(HA) as a goal. The exact deployment
steps to achieve HA depend on the specifics of the infrastructure in which |st2| is deployed. This
guide covers a brief explanation on various |st2| services, how they interact and the external
services necessary for |st2| to function.

In the section :doc:`/install/overview` a detailed picture and explanation on how single-box deployments
work is provided. Repeating the picture here to keep context and use as a reference to layer on some
HA deployment specific details.

.. figure :: /_static/images/st2-deployment-big-picture.png
    :align: center

Components
----------

st2api
~~~~~~
This process host the REST API endpoints that serve requests from  WebUI, CLI and ChatOps. It maintains
connections to MongoDB to store and retrieve information. It also connects to RabbitMQ to push various
kind of messages onto the message bus. It is a gunicorn managed process which by default listens on
port ``9101`` and is front-ended by Nginx acting as a reverse proxy.

n st2api processes can be behind a loadbalancer in an active-active configuration. Each of these
processes can be deployed on separate compute instances.

st2auth
~~~~~~~
All authentication is managed by this process. This process needs connection to MongoDB and an authentication
backend. See `Authentication backends<ref-sensors-authoring-a-sensor>` for more information. It is a gunicorn
managed process which by default listens on port ``9102`` and is front-ended by Nginx acting as a reverse proxy.

n st2auth processes can be behind a loadbalancer in an active-active configuration. Each of these processes
can be deployed on separate compute instances. If using the PAM authentication backend special care has to be
taken to guarantee that all boxes on which an instance of st2auth runs should have the same users. Generally,
all st2auth process should see the same identities, via some provider if applicable, for the system to work
predictably.

st2stream
~~~~~~~~~
This process exposes a server-sent event stream. Requires access to both MongoDB and RabbitMQ. It is also a
gunicorn managed process, listens on port ``9102`` by default and is front-ended by Nginx acting as a reverse
proxy. Clients like WebUI and ChatOps maintain a persistent connection with an st2stream process and receive
update from the st2stream server.

n st2stream process can be behind a loadbalance in an active-active configuration. Since clients maintain
a persistent connection with a specific instance the client will loose event momentarily if an st2stream
process goes down. It would be the responsibility of the client to reconnect to an alternate stream connection
via the loadbalancer.

st2sensorcontainer
~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~
This is a dual purpose process - its main function is to evaluate rules when it sees TriggerInstances and
decide if an ActionExecution is to be requested. It needs access to MongoDB to locate rules and RabbitMQ
to listen for TriggerInstances and request ActionExecutions. The auxiliary purpose of this process is to
run all the defined timers. See `Timers <ref-rule-timers>` for specifics on setting up timers via rules.

n st2rulesengine can run in active-active with only connections to MongoDB and RabbitMQ. All these will share the
TriggerInstance load and naturally pick up more work if one or more of the process becomes unavailable. The timer
function in each of the RulesEngine is not HA compatible. In the interim it is possible to disable the timer
in all but one of the st2rulesengine to avoid duplicate timer events, expect this to be fixed in a future |st2| release.

st2actionrunner
~~~~~~~~~~~~~~~
All ActionExecutions are handled for execution by st2actionrunner. It manages the full life-cycle of an execution from
scheduling to one of the terminal states.

n st2actionrunner can run in active-active with only connections to MongoDB and RabbitMQ. Work gets naturally
distributed across runners via RabbitMQ. Adding more st2actionrunner increases the ability of |st2| to execute actions.

In a proper distributed setup it is recommended to setup Zookeeper or Redis to provide a distributed co-ordination
layer. See :doc:`Policies </policies>`. Using a default file based co-ordination backend will not work as it would
in a single box deployment.

st2resultstracker
~~~~~~~~~~~~~~~~~
Tracks results of execution handed over to mistral. It requires access to MongoDB and RabbitMQ to perform its function.

n st2resultstracker will co-operate with each other to perform work. At startup though there is a possibility
of work however there will not be any negative consequences to this duplicate work. Specifically the jobs to track results
also get stored in the DB in case there is no worker to take over the work and this pattern makes all result trackers
pick up the same initial work set. Once this work set is exhausted all subsequents tasks are round-robined.

st2notifier
~~~~~~~~~~~
This is a dual purpose process - its main function is to generate ``st2.core.actiontrigger`` and ``st2.core.notifytrigger``
based on the completion of ActionExecution. The auxiliary purpose is to act as a backup scheduler for actions that may
not have been scheduled.

n st2notifiers can run in active-active requiring connections to RabbitMQ and MongoDB. For the auxiliary purpose to function
in an HA deployment when more than 1 st2notifiers are running either Zookeeper or Redis is required to provide co-ordination
much like for policies. It is also possible to designate a single st2notifier as provider of auxiliary functions by
disabling the scheduler in all but 1 st2notifiers.

st2garbagecollector
~~~~~~~~~~~~~~~~~~~
Cleans up old executions and other operations data based on setup configurations. By default this process does nothing
and needs to be setup to perform any work.

By design it is a singleton process. Running multiple in active-active will not yield much benefit and also will not
do any harm. Ideal configuration is active-passive but |st2| does not itself provide ability to run this in active-passive.

mistral-api
~~~~~~~~~~~
Mistral api is served by this aptly named process. It needs access to PostgreSQL and RabbitMQ.

n mistral-api can run and just like st2api in active-active configuration by using a loadbalancer to distribute at its
front end. In typical single box deployment mistral-api is local to the box and |st2| communicates via a direct HTTP
connection however for HA setup we recommend putting mistral-api behind a loadbalancer and setting up |st2| to communicate
via the loadbalancer.

mistral-server
~~~~~~~~~~~~~~
mistral-server is the worker engine for mistral i.e. the process which actually manages executions. |st2| plugin to
mistral i.e. ``st2mistral`` communicates back to |st2| api. This process needs access to PostgreSQL and RabbitMQ.

n mistral-server can run and co-ordinate work in an active-active configuration. In an HA deployment all communication
with the |st2| API must be via the configured loadbalancer.

Required dependencies
---------------------
Some HA recommendations for the dependencies required by |st2| components. Depending on the exact infrastructure these
may not be suitable and would only serve as a suggestion.

MongoDB
~~~~~~~
|st2| uses this to cache Actions, Rules and Sensor metadata which already live in the filesystem. All the content should
ideally be source-control managed in preferably a git repository. |st2| also stores operation data like ActionExecution,
TriggerInstance etc. MongoDB supports `replica set high-availability <https://docs.mongodb.org/v2.4/core/replica-set-high-availability/>` which we recommend to provide a safe failover.

Loss of connectivity to a MongoDB cluster will cause downtime for |st2|. However, once a replica MongoDB is brought back it
should be quite possible to bring |st2| back to operational state by simply loading the content. Easy access to old ActionExecutions will be lost but all the data of old ActionExecution will still be available in audit logs.

PostgreSQL
~~~~~~~~~~
Used primarily by ``mistral-api`` and ``mistral-server``. To deploy PostgreSQL in HA please see `documentation <http://www.postgresql.org/docs/9.4/static/high-availability.html>` provided by the PostgreSQL project.

The data stored in PostgreSQL is operational for mistral therefore starting from a brand new PostgreSQL in case of loss
of a cluster will bring automation services back instantly. Certainly there will be downtime while a new DB cluster is provisioned.

RabbitMQ
~~~~~~~~
RabbitMQ is the communication hub for |st2| to co-ordinate and distribute work. See `RabbitMQ documentation <https://www.rabbitmq.com/ha.html>` to understand HA deployment strategies.

Our recommendation is to mirror all the Queues and Exchanges so that loss of 1 server still retains functionality.

Zookeeper/Redis
~~~~~~~~~~~~~~~
Various |st2| features rely on a proper co-ordination backend in a distributed deployment to work correctly.

`This <http://zookeeper.apache.org/doc/trunk/zookeeperStarted.html#sc_RunningReplicatedZooKeeper>` shows how to run a replicated zookeeper setup. See `this <http://redis.io/topics/sentinel>` to understand Redis deployments using sentinel.


Nginx and loadbalancer
~~~~~~~~~~~~~~~~~~~~~~~
An Nginx server is required to reverse proxy each instance of ``st2api``, ``st2auth``, ``st2stream`` and ``mistral-api``. This server will terminate SSL connections, shield clients from internal port numbers of various services and only require ports 80 and 443 to be open on containers. Often it is best to deploy 1 set of all these services on a compute instance and share an Nginx server.

There is also a need for a loadbalancer to frontend all the REST services. This results in an HA deployment for REST services as well as single endpoint for clients. Most deployment infrastructures will already have a loadbalancer solution which they would
prefer to use so we do not provide any recommendations.


Reference HA setup
------------------

In this section we provide a highly opinionated and therefore prescriptive approach to deploying |st2| in HA.

.. insert an awesome diagram here

Shared/Controller box
~~~~~~~~~~~~~~~~~~~~~
This box contains shared services.

Blueprint box
~~~~~~~~~~~~~
This box is a repeatable |st2| image which is mostly equivalent to the single-box reference deployment with a few changes. Deploy
as many of these boxes for HA and also achieve horizontal scale. Note that with service level granularity different instances
of a blueprint box can have different services enabled.



