Overview: Single-box Reference Deployment
=========================================

.. todo:: short intro paragraph: this is reference deployment for single box, follow installation
    guide to get here.

.. figure:: https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/pub?w=960&amp;h=720
    :align: center

    StackStorm single-box reference deployment.

.. source https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/edit

.. todo:: keep image live `on google.drive <https://docs.google.com/drawings/d/1X6u8BB9bnWkW8C81ERBvjIKRfo9mDos4XEKeDv6YiF0/edit>`_ while WIP but copy a final .png under _static

1. st2* services
----------------
st2* services provide main stackstorm functionality. They are located at ``/opt/stackstorm/st2``, share a dedicated Python virtualenv, and configured by /etc/st2/st2.conf.

    * st2sensorcontainer runs sensor from ``/opt/stackstorm/packs``.
    * st2rulesengine is evaluating triggers against the rules, and send action execution requests.
    * st2actionrunners run actions from packs under ``/opt/stackstorm/packs`` via a variety of :doc:`/runners`. Runners may require some runner-specific configurations: SSH needs to be cofigured for running remote actions based on `remote-shell-runner` and `remote-command-runner`.
    * st2resultstracker** is keeping track of long-running workflow executions. Calls Mistral API endpoint.
    * st2notifier service supports :doc:`/chatops/notifications`. `TODO: specify or refer what needs configuration to enable it`.
    * st2garbagecollector** is an optional service to periodically delete old execution history data from the database, per settings in st2.conf.
    * st2auth is an authentication service with the REST endpoint. A variety of auth backends is available; see :doc:`/authentication`. Reference deployment uses <flat file backend `https://github.com/StackStorm/st2-auth-backend-flat-file`>_ backend.
    * st2api is REST API web service endpoint; it also serves webhooks for webhook triggers.


2. st2-mistral
--------------
Mistral is a workflow service component that StackStorm uses for long-running workflows. It is installed under ``/opt/stackstorm/mistral``, runs in a dedicated Python virtualenv, and configured by /etc/mistral/mistral.conf. ``mistral`` reaches out to st2api for action execution requests. ``mistral-api`` is an internal end-point accessed by st2actionrunner and st2notifier. In a single-box deployment it is restricted to localhost.

3. st2client
-------------
st2client is the `st2` CLI and python bindings for StackStorm API. To configure CLI to point to the right API, authenticate options, suppressing unsecure warnings for self-signed certificates and othe cool stuff see :doc:`/cli`.


4. ngnix for WebUI and SSL termination
--------------------------------------
* **nginx** provides SSL termination, redirects HTTP to HTTPS, serves WebUI as static HTML, and reverse-proxies REST API endpoints to st2* web services.

* **StackStorm WebUI** (st2web and flow) are installed at ``/opt/statckstorm/static/webui`` and configured by `webui/config.js`. They are are HTML5 applications, served as static HTML and calling StackStorm st2auth and st2api REST API endpoints. With ngnix proxying st2auth and st2api through 443 HTTPS port it's all good. Overwise proper CORS configuration is required both on st2 and `webui/config.js`. TODO:XXXX polish text here.

5. Chatops components
---------------------
StackStorm Chatops components are `Hubot <https://hubot.github.com/>`_, `StackStorm's Hubot adapter <https://github.com/StackStorm/hubot-stackstorm>`_, and plugins for connecting to `different Chat services <https://hubot.github.com/docs/adapters/>`_. They are installed at /opt/stackstorm/chatops/ and configured via `/opt/stackstorm/chatops/hubot/hubot.env`, see :ref:`Chatops Configuration <chatops-configuration>`.

.. todo:: Change the text if we go for docker way of deployment.

6. Dependencies
---------------
The required dependencies are RabbitMQ, MongoDB, and PostgreSQL. The optional dependencies are:

  - nginx for SSL termination, reverse-proxying API endpoints and serving static HTML.
  - Redis or Zookeeper for concurrency policies (see :doc:`/policies`).
  - LDAP for StackStorm Enterprise LDAP authentication.





