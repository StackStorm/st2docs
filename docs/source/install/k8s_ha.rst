|st2| HA Cluster in Kubernetes - BETA
=====================================

This document provides an installation blueprint for a Highly Available StackStorm cluster
based on `Kubernetes <https://kubernetes.io/>`__, a container orchestration platform at planet scale.

The cluster deploys a minimum of 2 replicas for each component of StackStorm microservices for redundancy and reliability. It
also configures backends like MongoDB HA Replicaset, RabbitMQ HA and etcd cluster that st2 relies on for database,
communication bus, and distributed coordination respectively. That raises a fleet of more than ``30`` pods total.

The source code for K8s resource templates is available as a GitHub repo:
`StackStorm/stackstorm-ha <https://github.com/StackStorm/stackstorm-ha>`_.

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

However, here are some minimal instructions to get started.

Deployment
__________
The StackStorm HA cluster is available as a Helm chart, a bundled K8s package which
makes installing the complex StackStorm infrastructure as easy as:

.. code-block:: bash

  # Add Helm StackStorm repository
  helm repo add stackstorm https://helm.stackstorm.com/

  helm install stackstorm/stackstorm-ha

Once the deployment is finished, it will show you the first steps to get started working with the new cluster via WebUI
or ``st2`` CLI client:

.. figure :: /_static/images/helm-chart-notes.png
    :align: center


The installation uses some unsafe defaults which we recommend you change for production use via Helm ``values.yaml``.

Helm Values
___________
Helm package ``stackstorm-ha`` comes with default settings (see `values.yaml <https://github.com/StackStorm/stackstorm-ha/blob/master/values.yaml>`_).
Fine-tune them to achieve desired configuration for the StackStorm HA K8s cluster.

.. note::
    Keep custom values you want to override in a separated yaml file so they won't get lost.
    Example: ``helm install -f custom_values.yaml`` or ``helm upgrade -f custom_values.yaml``

You can configure:

- number of replicas for each component
- st2 auth secrets
- st2.conf settings
- RBAC roles, assignments and mappings (enterprise only)
- custom st2 packs and its configs
- st2web SSL certificate
- SSH private key
- K8s resources and settings to control pod/deployment placement
- Mongo, RabbitMQ clusters
- in-cluster Docker registry

.. warning::
    It's highly recommended to set your own secrets as the file contains unsafe defaults like self-signed SSL certificates, SSH keys, StackStorm access credentials and MongoDB/RabbitMQ passwords!

Upgrading
_________
After making changes to Helm values, upgrade the cluster:

.. code-block:: bash

  helm repo update
  helm upgrade <release-name> stackstorm/stackstorm-ha

It will redeploy components which were affected by the change, taking care to keep
the desired number of replicas to sustain every service alive during the rolling upgrade.


.. _ref-ewc-ha:

Enterprise (EWC)
________________

Installation
~~~~~~~~~~~~
By default, StackStorm Community free and open-source version is deployed via Helm chart.
If you want to install :doc:`StackStorm Enterprise (Extreme Workflow Composer) </install/ewc>`, run:

.. code-block:: bash

  # Replace `<EWC_LICENSE_KEY>` with a real license key, obtained in Email
  helm install \
    --set enterprise.enabled=true \
    --set enterprise.license=<EWC_LICENSE_KEY> \
    stackstorm/stackstorm-ha

It will pull enterprise images from our private Docker registry. This adds advanced functionality and enterprise support.

.. note::
    Don't have StackStorm Enterprise License?

    Request a 90-day free trial at https://stackstorm.com/features/#ewc

RBAC & LDAP Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~
Enterprise edition allows configuring features like :doc:`/rbac` and :doc:`LDAP Authentication </authentication>`.
Include ``enterprise`` section in Helm values with preferred RBAC and LDAP settings:

.. code-block:: yaml

  ##
  ## StackStorm Enterprise settings (Optional)
  ##
  enterprise:
    # Enable/Disable StackStorm Enterprise. Enabling will download StackStorm Enterprise Docker images.
    enabled: true
    # Required StackStorm Enterprise license key.
    license: ""

    # StackStorm Role Based Access Control settings (https://docs.stackstorm.com/rbac.html)
    rbac:
      # Custom StackStorm RBAC roles, shipped in '/opt/stackstorm/rbac/roles/'
      # See https://docs.stackstorm.com/rbac.html#defining-roles-and-permission-grants
      roles:
        sample.yaml: |
          # sample RBAC role file, see https://docs.stackstorm.com/rbac.html#defining-roles-and-permission-grants
          ---
          name: "sample"
          description: "Example Role which contains no permission grants and serves for demonstration purposes"

      # Custom StackStorm RBAC role assignments, shipped in '/opt/stackstorm/rbac/assignments/'
      # See: https://docs.stackstorm.com/rbac.html#defining-user-role-assignments
      assignments:
        st2admin.yaml: |
          ---
          username: st2admin
          roles:
            - system_admin
        stanley.yaml: |
          ---
          username: stanley
          roles:
            - admin

      # StackStorm RBAC LDAP groups-to-roles mapping rules, shipped in '/opt/stackstorm/rbac/mappings/'
      # See RBAC Roles Based on LDAP Groups: https://docs.stackstorm.com/rbac.html#automatically-granting-roles-based-on-ldap-group-membership
      mappings:
        stormers.yaml: |
          ---
          group: "CN=stormers,OU=groups,DC=stackstorm,DC=net"
          description: "Automatically grant admin role to all stormers group members."
          roles:
            - "admin"

Upgrading from Community
~~~~~~~~~~~~~~~~~~~~~~~~
Additionally, you can benefit by upgrading from Community to Enterprise edition at any time, with no loss of data:

.. code-block:: bash

  # Replace `<EWC_LICENSE_KEY>` with a real license key, obtained in Email
  helm upgrade \
    --set enterprise.enabled=true \
    --set enterprise.license=<EWC_LICENSE_KEY> \
    <release-name> \
    stackstorm/stackstorm-ha


Tips & Tricks
_____________
Save custom Helm values you want to override in a separate file, upgrade the cluster:

.. code-block:: bash

  helm upgrade -f custom_values.yaml <release-name> stackstorm/stackstorm-ha

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
required packs into a Docker image that you can codify, version, package and distribute in a repeatable way.
The responsibility of this Docker image is to hold pack content and their virtualenvs.
So the custom st2 pack docker image you have to build is essentially a couple of read-only directories that
are shared with the corresponding st2 services in the cluster.

For your convenience, we created a new ``st2-pack-install <pack1> <pack2> <pack3>`` command
that will help to install custom packs during the Docker build process without relying on DB and MQ connection.

Helm chart brings helpers to simplify this experience like `stackstorm/st2pack:builder <https://hub.docker.com/r/stackstorm/st2packs/>`_
Docker image and private Docker registry you can optionally enable in Helm values.yaml to easily push/pull
your custom packs within the cluster.

For more detailed instructions see `StackStorm/stackstorm-ha#Installing packs in the cluster <https://github.com/StackStorm/stackstorm-ha#Installing-packs-in-the-cluster>`_.

.. note::
  There is an alternative approach, - sharing pack content via read-write-many NFS (Network File System) as :doc:`/reference/ha` recommends.
  As beta is in progress and both methods have their pros and cons, we'd like to hear your feedback and which way would work better for you.

Components
----------
For HA reasons, by default and at a minimum StackStorm K8s cluster deploys more than ``30`` pods in total.
This section describes their role and deployment specifics.

st2client
_________
A helper container to switch into and run st2 CLI commands against the deployed StackStorm cluster.
All resources like credentials, configs, RBAC, packs, keys and secrets are shared with this container.

.. code-block:: bash

  # obtain st2client pod name
  ST2CLIENT=$(kubectl get pod -l app=st2client -o jsonpath="{.items[0].metadata.name}")

  # run a single st2 client command
  kubectl exec -it ${ST2CLIENT} -- st2 --version

  # switch into a container shell and use st2 CLI
  kubectl exec -it ${ST2CLIENT} /bin/bash


st2web
______
st2web is a StackStorm Web UI admin dashboard. By default, st2web K8s config includes a Pod Deployment and a Service.
``2`` replicas (configurable) of st2web serve the web app and proxy requests to st2auth, st2api, st2stream.

.. note::
  By default, st2web is a NodePort Service and is not exposed to the public net.
  If your Kubernetes cluster setup supports the LoadBalancer service type, you can edit the
  corresponding helm values to configure st2web as a LoadBalancer service in order to expose it
  and the services it proxies to the public net.

st2auth
_______
All authentication is managed by the ``st2auth`` service.
K8s configuration includes a Pod Deployment backed by ``2`` replicas by default and Service of type ClusterIP listening on port ``9100``.
Multiple st2auth processes can be behind a load balancer in an active-active configuration. You can increase the number
of replicas if required.

st2api
______
This service hosts the REST API endpoints that serve requests from WebUI, CLI, ChatOps and other st2 components.
K8s configuration consists of Pod Deployment with ``2`` default replicas for HA and ClusterIP Service accepting HTTP requests on port ``9101``.
This is one of the most important |st2| services. We recommend increasing the number of replicas to distribute load
if you are planning a high-volume environment. 

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
Only a single replica is created via K8s Deployment as timersengine can't work in active-active mode at the moment
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
In an HA deployment there must be a minimum of ``2`` replicas of st2notifier running, requiring a coordination backend,
which in our case is etcd.

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

st2scheduler
____________

``st2scheduler`` is responsible for handling ingress action execution requests.

``2`` replicas for K8s Deployment are configured by default to increase StackStorm scheduling throughput.
Relies on database versioning for coordination.

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
StackStorm employs etcd as a distributed coordination backend, required for st2 cluster components to work properly in HA scenario.
`3` node Raft cluster is deployed via external official Helm chart dependency `etcd <https://github.com/helm/charts/tree/master/incubator/etcd>`_.
As any other Helm dependency, it's possible to further configure it for specific scaling needs via ``values.yaml``.

Docker registry
_______________
If you do not already have an appropriate docker registry for storing custom st2 packs images, we made it
very easy to deploy one in your k8s cluster. You can optionally enable in-cluster Docker registry via
``values.yaml`` by setting ``docker-registry.enabled: true`` and additional 3rd party charts `docker-registry <https://github.com/helm/charts/tree/master/stable/docker-registry>`_
and `kube-registry-proxy <https://github.com/helm/charts/tree/master/incubator/kube-registry-proxy>`_ will be configured.


Feedback Needed!
----------------
As this deployment method new and beta is in progress, we ask you to try it and provide your feedback via
bug reports, ideas, feature or pull requests in `StackStorm/stackstorm-ha <https://github.com/StackStorm/stackstorm-ha>`_,
and ecourage discussions in `Slack <https://stackstorm.com/community-signup>`_ ``#docker`` channel or write us an email.


.. only:: community

    .. include:: /__engage_community.rst

.. only:: enterprise

    .. include:: /__engage_enterprise.rst
