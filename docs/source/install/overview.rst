Overview: Single-box Reference Deployment
==========================================

First, let's review what the main |st2| components are, their role, and how they are wired
together when |st2| is deployed on a single box. As you follow the installation instructions
in this section, this is your target "reference deployment".

.. figure :: /_static/images/st2-deployment-big-picture.png
    :align: center
.. figure  https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/pub?w=960&amp;h=720
..    :align: center

    |st2| single-box reference deployment.

.. source https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/edit


1. st2 services
----------------
st2 services provide the main |st2| functionality. They are located at ``/opt/stackstorm/st2``,
share a dedicated Python virtualenv, and are configured by /etc/st2/st2.conf.

    * **st2sensorcontainer** runs sensors from ``/opt/stackstorm/packs``. It manages the sensors to
      be run on a node. It will start, stop and restart based on policy the sensors running on a node.
    * **st2rulesengine** evaluates rules when it sees TriggerInstances and decides if an ActionExecution
      is to be requested. It needs access to MongoDB to locate rules and RabbitMQ to listen for
      TriggerInstances and request ActionExecutions. The auxiliary purpose of this process is to
      run all the defined timers.
    * **st2actionrunners** run actions from packs under ``/opt/stackstorm/packs`` via a variety of
      :doc:`/reference/runners`. Runners may require some runner-specific configurations, e.g. SSH needs to be
      configured for running remote actions based on `remote-shell-runner` and `remote-command-runner`.
      Windows prerequisites must be in place to run Windows runners. See :doc:`Runners </reference/runners>`
      for details.
    * **st2resultstracker** keeps track of long-running workflow executions, calling the Mistral
      API endpoint.
    * **st2notifier** generates ``st2.core.actiontrigger`` and ``st2.core.notifytrigger`` based
      on the completion of ActionExecution. The auxiliary purpose is to act as a backup scheduler
      for actions that may not have been scheduled.
    * **st2garbagecollector** is an optional service to periodically delete old execution history
      data from the database, per settings in ``/etc/st2/st2.conf``.
    * **st2auth** is an authentication service with the REST endpoint. A variety of auth backends
      is available; see :doc:`/authentication`. Reference deployment uses
      `flat file auth backend <https://github.com/StackStorm/st2-auth-backend-flat-file>`_.
    * **st2api** is REST API web service endpoint, used by CLI and WebUI. It also serves webhooks
      for webhook triggers.
    * **st2stream** is an event stream consumption HTTP endpoint where various useful events are posted.
      These events are consumed by WebUI and hubot i.e. ChatOps to update with results etc.


2. st2client
-------------

``st2client`` is the CLI and Python bindings for the |st2| API. To configure CLI to point to the right
API, authentication options, suppressing insecure warnings for self-signed certificates and other
conveniences see :doc:`/reference/cli`. ``st2client`` is packaged with ``st2``, or can be installed
independently.

3. st2mistral
--------------

:doc:`/mistral` is a workflow service component that |st2| uses for long-running workflows. It
is packaged as ``st2mistral`` ``deb`` or ``rpm``, installed under ``/opt/stackstorm/mistral``,
runs in a dedicated Python virtualenv, and is configured by ``/etc/mistral/mistral.conf``. ``mistral-
server`` runs workflow logic and calling actions, reaching out to st2api for action execution
requests. ``st2mistral`` is a mistral plugin with stackstorm extensions. ``mistral-api`` is an
internal end-point accessed by ``st2actionrunner`` and ``st2notifier``. In a single-box deployment
it is restricted to localhost.


4. NGINX for WebUI and SSL termination
--------------------------------------
* **nginx** provides SSL termination, redirects HTTP to HTTPS, serves WebUI as static HTML,
  and reverse-proxies REST API endpoints to st2* web services.

* **StackStorm WebUI** (st2web, and Workflow Designer, for Brocade Workflow Composer) are installed at ``/opt/statckstorm/static/webui``
  and configured via ``webui/config.js``. `st2web` comes in its own ``deb`` and ``rpm``. `Flow` is
  deployed with ``bwc-enterprise`` package. They are HTML5 applications, served as static HTML,
  and calling |st2| st2auth and st2api REST API endpoints. NGINX proxies st2auth and st2api
  requests through 443 HTTPS port to ``/api`` and ``/auth``.

5. st2chatops - ChatOps components
----------------------------------
|st2| Chatops components are `Hubot <https://hubot.github.com/>`_, `|st2|'s Hubot adapter
<https://github.com/StackStorm/hubot-stackstorm>`_, and plugins for connecting to `different
Chat services <https://hubot.github.com/docs/adapters/>`_. They are packaged in ``st2chatops``
``deb`` and ``rpm``, installed at ``/opt/stackstorm/chatops/`` and configured in
``/opt/stackstorm/chatops/st2chatops.env``.

ChatOps can be also enabled as a Docker image `StackStorm/st2chatops <https://github.com/StackStorm/st2chatops>`_,
or by installing `hubot-stackstorm plugin <https://github.com/StackStorm/hubot-stackstorm>`_ on your existing Hubot instance.

Dependencies
---------------
The required dependencies are RabbitMQ, MongoDB, and PostgreSQL. The optional dependencies are:

  - nginx for SSL termination, reverse-proxying API endpoints and serving static HTML.
  - Redis or Zookeeper for concurrency policies (see :doc:`/reference/policies`).
  - LDAP for Brocade Workflow Composer LDAP authentication.


Multi-box/HA deployment
-----------------------
For specific information on multi-box deployments to achieve HA or horizontal scale see :doc:`/reference/ha`.
