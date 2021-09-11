Overview: Single-box Reference Deployment
==========================================

This page describes a "reference deployment" of all |st2| components installed on a single system.
It explains what the main components are, their role, and how they are wired together.

If you use the :doc:`one line quick install script </install/index/>`, it will set up your system
as shown below:

.. figure :: /_static/images/st2-deployment-big-picture.png
    :align: center
.. figure  https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/pub?w=960&amp;h=720
..    :align: center

    |st2| single-box reference deployment.

.. source https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/edit


1. StackStorm services
----------------------
"st2" services provide the main |st2| functionality. They are located at ``/opt/stackstorm/st2``,
share a dedicated Python virtualenv, and are configured via ``/etc/st2/st2.conf``.

* **st2sensorcontainer** runs sensors from ``/opt/stackstorm/packs``. It manages the sensors to be
  run on a node. It will start, stop and restart based on policy the sensors running on a node.
* **st2rulesengine** evaluates rules when it sees TriggerInstances and decides if an
  ActionExecution is to be requested. It needs access to MongoDB to locate rules and RabbitMQ to
  listen for TriggerInstances and request ActionExecutions. The auxiliary purpose of this process
  is to run all the defined timers.
* **st2timersengine** is used for scheduling all user specified timers aka |st2| cron.
* **st2scheduler** is responsible for scheduling action executions which are then run by
  ``st2actionrunner`` service. It takes care of things such as delaying executions and
  applying user-defined pre-run policies.
* **st2actionrunners** run actions from packs under ``/opt/stackstorm/packs`` via a variety of
  :doc:`/reference/runners`. Runners may require some runner-specific configurations, e.g. SSH
  needs to be configured for running remote actions based on ``remote-shell-runner`` and
  ``remote-command-runner``.
* **st2notifier** generates ``st2.core.actiontrigger`` and ``st2.core.notifytrigger``
  TriggerInstances on the completion of an ActionExecution. The auxiliary purpose is to act as a backup scheduler for actions that may not have been scheduled.
* **st2garbagecollector** is an optional service to periodically delete old execution history data
  from the database, per settings in ``/etc/st2/st2.conf``.
* **st2auth** is an authentication service with a REST endpoint. A variety of authentication
  backends are available; see :doc:`/authentication` for more details. The reference deployment
  uses `flat file auth backend <https://github.com/StackStorm/st2-auth-backend-flat-file>`_.
* **st2api** is REST API web service endpoint, used by CLI and WebUI. It also serves webhooks for
  webhook triggers.
* **st2stream** is an event stream consumption HTTP endpoint where various useful events are
  posted. These events are consumed by WebUI and hubot i.e. ChatOps to update with results etc.
* **st2workflowengine** is responsible for running Orquesta workflows.

Some services follow active/active model and can scale horizontally (``st2actionrunner``,
``st2rulesengine``, ``st2auth``, ``st2api``, ``st2stream``, ``st2scheduler``, ``st2notifier``,
``st2workflowengine``). Multiple instances of those services can run to increase the overall system
throughput.

Other services (``st2timersengine``, ``st2garbagecollector``, ``st2sensorcontainer``) require only
a single instance to be running for the system to function correctly.

For more information on those limitations and how to configure services for HA, please refer to
:doc:`/reference/ha` and :doc:`/install/k8s_ha`.

2. st2client
-------------

``st2client`` is the CLI and Python bindings for the |st2| API. To configure the CLI to point to
the right API, authentication options, suppress insecure warnings for self-signed certificates and
other conveniences see the :doc:`/reference/cli`. ``st2client`` is packaged with ``st2``, or can be
installed independently.

3. NGINX for WebUI and SSL termination
--------------------------------------
* **nginx** provides SSL termination, redirects HTTP to HTTPS, serves WebUI static components, and
  reverse-proxies REST API endpoints to st2* web services.
* **StackStorm WebUI** (st2web, including Workflow Designer) are installed at
  ``/opt/stackstorm/static/webui`` and configured via ``webui/config.js``. ``st2web``
  comes in its own ``deb`` and ``rpm`` package. In StackStorm versions earlier than 3.3 Workflow
  Designer was deployed as part of the ``bwc-enterprise`` package. They are HTML5 applications,
  served as static HTML, and call |st2| st2auth and st2api REST API endpoints. NGINX proxies
  inbound requests to ``/api`` and ``/auth`` to the st2api and st2auth services respectively.
  With StackStorm version 3.4 and later, the workflow designer is entirely integrated into st2web,
  and the ``bwc-enterprise`` package is no longer distributed.

4. st2chatops - ChatOps components
----------------------------------
|st2| Chatops components are `Hubot <https://hubot.github.com/>`_, `|st2|'s Hubot adapter
<https://github.com/StackStorm/hubot-stackstorm>`_, and plugins for connecting to `different Chat
services <https://hubot.github.com/docs/adapters/>`_. They are packaged as ``st2chatops``,
installed at ``/opt/stackstorm/chatops/`` and configured in
``/opt/stackstorm/chatops/st2chatops.env``.

ChatOps can be also enabled by installing `hubot-stackstorm plugin
<https://github.com/StackStorm/hubot-stackstorm>`_ on your existing Hubot instance.

Dependencies
------------
The required dependencies are RabbitMQ, MongoDB, and Redis (or Zookeeper).

The coordination service is required for workflows that has multiple branches and tasks with items. Previously, the coordination service is optional to support concurrency policies. The backend for the coordination service can be configured to use Redis, Zookeeper, or other. Since v3.5, redis server is installed as part of the single node installation script. The python redis client is also installed into the |st2| virtualenv. If using Zookeeper, the kazoo module needs to be manually installed into the |st2| virtualenv.

The optional dependencies are:

  - nginx for SSL termination, reverse-proxying API endpoints and serving static HTML.
  - LDAP authentication.


Multi-box/HA deployment
-----------------------
For specific information on multi-box deployments to achieve HA or horizontal scale see
:doc:`/reference/ha` and :doc:`/install/k8s_ha`.
