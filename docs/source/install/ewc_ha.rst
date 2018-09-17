|bwc| HA Cluster - BETA
=======================

|bwc| (EWC) is the commercial version of the StackStorm automation platform. EWC adds priority
support, advanced features such as fine-tuned access control, LDAP, and Workflow Designer. To
learn more about |bwc|, get an evaluation license, or request a quote, visit `extremenetworks.com/product/workflow-composer
<https://www.extremenetworks.com/product/workflow-composer/>`_.

This document provides an installation blueprint for a Highly Availabile StackStorm Enterprise (|bwc|) cluster
based on `Kubernetes <https://kubernetes.io/>`__, a container orchestration platform with a planet scale.

The cluster deploys minimum 2 replicas for each component of StackStorm microservices for redundancy and reliability,
as well as configures backends like MongoDB HA Replicaset, RabbitMQ HA and etcd cluster that st2 relies on for database,
communication bus, and distributed coordination respectively. That raises a fleet of more than a ``30`` pods in summ.

The source code for K8s resource templates is available as a GitHub repo (TODO):
`StackStorm/stackstorm-enterprise-ha <https://github.com/StackStorm/stackstorm-enterprise-ha>`_.

.. warning::
    **Beta quality!**
    As this deployment method available in beta version, documentation and code may be substantially modified and refactored.

.. contents:: Contents
   :local:

---------------------------

Requirements
------------
* `Kubernetes <https://kubernetes.io/docs/setup/pick-right-solution/>`__ cluster
* `Helm <https://docs.helm.sh/using_helm/#install-helm>`__, the K8s package manager and `Tiller <https://docs.helm.sh/using_helm/#initialize-helm-and-install-tiller>`_
* Enough computing resources for production use, respecting :doc:`/install/system_requirements`

Usage
-----
This document assumes some basic knowledge of Kubernetes and Helm.
Please refer to `K8s <https://kubernetes.io/docs/home/>`__ and `Helm <https://docs.helm.sh/>`__
documentation if you find any difficulties using these tools.

However here are some minimal instructions to get started.

Deployment
__________
StackStorm Enterprise HA cluster available as a Helm chart, a bundled K8s package which
makes installing complex StackStorm infrastructure easy as:

.. code-block:: bash

  # Add Helm StackStorm repository
  helm repo add stackstorm https://helm.stackstorm.com/

  # Replace `<EWC_LICENSE_KEY>` with a real license key, obtained in Email
  helm install --set secrets.st2.license=<EWC_LICENSE_KEY> stackstorm/stackstorm-enterprise-ha

.. note::
    Don't have StackStorm Enterprise License?

    Request a 90-day free trial at https://stackstorm.com/#product

Once the deployment is finished, it'll show you first steps how to start working with the new cluster via WebUI or st2 client:

.. figure :: /_static/images/helm-chart-notes.png
    :align: center


The installation uses some unsafe defaults which are recommended to change thoughtfully for production use via Helm ``values.yaml``.

Helm values.yaml
________________
Helm package ``stackstorm-enterprise-ha`` comes with the default settings in ``values.yaml``.
Fine-tune them to achieve desired configuration for the StackStorm Enterprise HA K8s cluster.

You can configure:

- number of replicas for each component
- st2 auth secrets
- st2.conf settings
- RBAC roles, assignments and mappings
- custom st2 pack configs
- st2web SSL certificate
- SSH private key
- K8s resources and settings to control pod/deployment placement
- configuration for Mongo, RabbitMQ clusters

.. warning::
    It's highly recommended to set your own secrets as file contains unsafe defaults like self-signed SSL certificates, SSH keys, StackStorm access credentials and MongoDB/RabbitMQ passwords!

Upgrading
_________
Once you make any changes to Helm values, upgrade the cluster:

.. code-block:: bash

  helm repo update
  helm upgrade <release-name> stackstorm/stackstorm-enterprise-ha

It will redeploy components which were affected by the change, taking care about keeping
desired number of replicas to sustain every service alive during the rolling upgrade.


Tips & Tricks
_____________
Save custom Helm values you want to override in a separated file, upgrade the cluster:

.. code-block:: bash

  helm upgrade -f custom_values.yaml <release-name> stackstorm/stackstorm-enterprise-ha

Get all logs for entire StackStorm cluster with dependent services for Helm release:

.. code-block:: bash

  kubectl logs -l release=<release-name>

Grab all logs only for stackstorm backend services, excluding st2web and DB/MQ/etcd:

.. code-block:: bash

  kubectl logs -l release=<release-name>,tier=backend


Custom st2 packs
----------------
To follow the stateless model, shipping custom st2 packs is now part of the deployment process.
It means that ``st2 pack install`` won't work in a distributed environment and you have to bundle all the
required packs into a Docker image that you could codify, version, package and distribute in a repeatable way.
The responsibility of such Docker image is to hold pack content and their virtualenvs.
So custom st2 pack Docker image you have to build is just read-only dirs that are shared with the corresponding
st2 services in a cluster.

For the convenience we created new ``st2-pack-install <pack1> <pack2> <pack3>`` command
that'll help to install custom packs during the Docker build process without relying on DB and MQ connection.

Helm chart brings helpers to simplify this experience like `stackstorm/st2pack:builder <https://hub.docker.com/r/stackstorm/st2packs/>`_
Docker image and private Docker registry you can optionally enable in Helm values.yaml to push/pull
your custom packs within a cluster easily.

For more detailed instructions see `StackStorm/stackstorm-enterprise-ha#Installing packs in the cluster <https://github.com/StackStorm/stackstorm-enterprise-ha#Installing-packs-in-the-cluster>`_.

.. note::
  There is an alternative approach, - sharing pack content via read-write-many NFS (Network File System) as :doc:`/reference/ha` recommends.
  As beta is in progress and both methods have their pros and cons, we'd like to hear your feedback and which way would work better for you.

Components
----------
For HA reasons, by default and at a minimum StackStorm K8s cluster deploys more than a ``30`` pods in total.
This section describes their role and deployment specifics.

st2client
_________
A helper container to switch into and run st2 CLI commands against the deployed StackStorm Enterprise cluster.
All resources like credentials, configs, RBAC, packs, keys and secrets are shared with this container.

.. code-block:: bash

  # obtain st2client pod name
  ST2CLIENT=$(kubectl get pod -l app=st2client,support=enterprise -o jsonpath="{.items[0].metadata.name}")

  # run a single st2 client command
  kubectl exec -it ${ST2CLIENT} -- st2 --version

  # switch into a container shell and use st2 CLI
  kubectl exec -it ${ST2CLIENT} /bin/bash


st2web
______
st2web is a StackStorm Web UI admin dashboard. By default, st2web K8s config includes a Pod Deployment and a Service.
``2`` replicas (configurable) of st2web serve the web app and proxify requests to st2auth, st2api, st2stream.

.. note::
  K8s Service uses only NodePort at the moment, so installing this chart will not provision a K8s resource of type LoadBalancer or Ingress (TODO!).
  Depending on your Kubernetes cluster setup you may need to add additional configuration to access the Web UI service or expose it to public net.

st2auth
_______
All authentication is managed by ``st2auth`` service.
K8s configuration includes a Pod Deployment backed by ``2`` replicas by default and Service of type ClusterIP listening on port ``9100``.
Multiple st2auth processes can be behind a load balancer in an active-active configuration and you can increase number of replicas per your discretion.

st2api
______
Service hosts the REST API endpoints that serve requests from WebUI, CLI, ChatOps and other st2 components.
K8s configuration consists of Pod Deployment with ``2`` default replicas for HA and ClusterIP Service accepting HTTP requests on port ``9101``.
Being one of the most important StackStorm services with a lot of logic involved,
it's recommended to increase number of replicas to distribute the load if you'd plan increased processing environment.

st2stream
_________
StackStorm st2stream - exposes a server-sent event stream, used by the clients like WebUI and ChatOps to receive updates from the st2stream server.
Similar to st2auth and st2api, st2stream K8s configuration includes Pod Deployment with ``2`` replicas for HA (can be increased in ``values.yaml``)
and ClusterIP Service listening on port ``9102``.

st2rulesengine
______________
st2rulesengine evaluates rules when it sees new triggers and decides if new action execution should be requested.
K8s config includes Pod Deployment with ``2`` (configurable) replicas by default for HA.

st2timersengine
_______________
st2timersengine is responsible for scheduling all user specified `timers <https://docs.stackstorm.com/rules.html#timers>`_ aka st2 cron.
Only single replica is created via K8s Deployment as timersengine can't work in active-active mode at the moment
(multiple timers will produce duplicated events) and it relies on K8s failover/reschedule capabilities to address cases of process failure.

st2workflowengine
_________________
st2workflowengine drives the execution of orquesta workflows and actually schedules actions to run by another component ``st2actionrunner``.
Multiple st2workflowengine processes can run in active-active mode and so minimum ``2`` K8s Deployment replicas are created by default.
All the workflow engine processes will share the load and pick up more work if one or more of the processes become available.

.. note::
  As Mistral is going to be deprecated and removed from StackStorm platform soon, Helm chart relies only on
  :doc:`Orquesta st2workflowengine </orquesta/index>` as a new native workflow engine.

st2notifier
___________
Multiple st2notifier processes can run in active-active mode, using connections to RabbitMQ and MongoDB and generating triggers based on
action execution completion as well as doing action rescheduling.
In an HA deployment minimum ``2`` replicas of st2notifier is running, requiring coordination backend, which is ``etcd`` in our case.

st2sensorcontainer
__________________
st2sensorcontainer manages StackStorm sensors: starts, stops and restarts them as a subprocesses.
At the moment K8s configuration consists of Deployment with hardcoded ``1`` replica.
Future plans are to re-work this setup and benefit from Docker-friendly `single-sensor-per-container mode #4179 <https://github.com/StackStorm/st2/pull/4179>`_
(since st2 ``v2.9``) as a way of :doc:`/reference/sensor_partitioning`, distributing the computing load
between many pods and relying on K8s failover/reschedule mechanisms, instead of running everything on ``1`` single instance of st2sensorcontainer.

st2actionrunner
_______________
Stackstorm workers that actually execute actions.
``5`` replicas for K8s Deployment are configured by default to increase StackStorm ability to execute actions without excessive queuing.
Relies on ``etcd`` for coordination. This is likely the first thing to lift if you have a lot of actions
to execute per time period in your StackStorm cluster.

st2garbagecollector
___________________
Service that cleans up old executions and other operations data based on setup configurations.
Having ``1`` st2garbagecollector replica for K8s Deployment is enough, considering its periodic execution nature.
By default this process does nothing and needs to be configured in st2.conf settings (via ``values.yaml``).
Purging stale data can significantly improve cluster abilities to perform faster and so it's recommended to configure st2garbagecollector in production.

`MongoDB HA ReplicaSet <https://github.com/helm/charts/tree/master/stable/mongodb-replicaset>`_
________________________________________________________________________________________________
StackStorm works with MongoDB as a database engine. External Helm Chart is used to configure MongoDB HA `ReplicaSet <https://docs.mongodb.com/manual/tutorial/deploy-replica-set/>`_.
By default ``3`` nodes (1 primary and 2 secondaries) of MongoDB are deployed via K8s StatefulSet.
For more advanced MongoDB configuration, refer to official `mongodb-replicaset <https://github.com/helm/charts/tree/master/stable/mongodb-replicaset>`_
Helm chart settings, which might be fine-tuned via ``values.yaml``.

`RabbitMQ HA Cluster <https://docs.stackstorm.com/latest/reference/ha.html#rabbitmq>`_
______________________________________________________________________________________
RabbitMQ is a message bus StackStorm relies on for inter-process communication and load distribution.
External Helm Chart is used to deploy `RabbitMQ cluster <https://www.rabbitmq.com/clustering.html>`_ in Highly Available mode.
By default ``3`` nodes of RabbitMQ are deployed via K8s StatefulSet.
For more advanced RabbitMQ configuration, please refer to official `rabbitmq-ha <https://github.com/helm/charts/tree/master/stable/rabbitmq-ha>`_
Helm chart repository, - all settings could be overridden via ``values.yaml``.

etcd
____
StackStorm employs etcd as a distributed coordination backend, required for StackStorm cluster components to work properly in HA scenario.
Currently, due to low demands, only ``1`` instance of etcd is created via K8s Deployment.
Future plans to switch to official Helm chart and configure etcd/Raft cluster properly with ``3`` nodes by default.

Feedback Needed!
----------------
As this deployment method new and beta is in progress, we ask you to try it and provide your feedback via
bug reports, ideas, feature or pull requests in `StackStorm/stackstorm-enterprise-ha <https://github.com/StackStorm/stackstorm-enterprise-ha>`_,
and ecourage discussions in `Slack <https://stackstorm.com/community-signup>`_ ``#docker`` channel or write us an email.


.. only:: community

    .. include:: /__engage_community.rst

.. only:: enterprise

    .. include:: /__engage_enterprise.rst
