Roadmap
=======

|st2| is still under active development. We welcome community feedback, and encourage
contributions. Here's our plans for the next two releases - remember these are subject to change!

3.1 - ETA February 2019
-----------------------

* **WebUI:** Datastore viewer/editor.
* **Orquesta:** Updates & Bug fixes, workflow runtime graph.
* **ChatOps:** RBAC.
* **SAML:** Support SAML authentication.
* **Ubuntu 18.04:** Support Ubuntu 18.04 LTS, with Python 3.6.

3.2 - ETA May 2019
-----------------------

* **Orquesta:** Dry-Run (simulated) workflows.
* **RHEL 8.x:** Support RHEL 8.x (assuming it has been released!)
* **Ubuntu 14.04:** Drop support for EoL Ubuntu 14.04.
* **WebUI:** RBAC configuration via UI.
* **Job Scheduling:** Job scheduling for ad-hoc jobs.

Monitor the `master branch <https://github.com/StackStorm/st2/>`_ to see how we're progressing.

See something you really like? Make sure to get involved with testing and PR feedback. 

Backlog
-------

Here's some more things on our list that we haven't scheduled yet:

* **History and Audit service:** History view with advanced search over years worth of execution
  records, over multiple versions of continuously upgraded |st2|.
* **At-scale refinements:** Ensure event handling reliability, and event storm resilience. Complete
  support for multi-node deployment of sensor containers and rules engines for resilience and
  throughput.
* **DB/Filesystem Consistency:** Provide better tooling for managing consistency between database and
  filesystem consistency for rules, actions, sensors, etc.
* **Configurable Sensors:** Run multiple instances of the same sensor, with different configurations.
* **Pack Dependency:** Better automatic handling of pack dependencies.
* **Pluggable Configuration:** Support multiple configuration backends for better security.
* **RBACv2:**

  * **Filters**: Tag and property based filters, more refined and convenient access control.
  * **Permissions**: Permissions on key value objects, arbitrary triggers, support for a default role.

Something else you'd like to see on the backlog? Submit an
`issue <https://github.com/StackStorm/st2/issues>`_. Or want to see something implemented sooner?
Submit a PR!

Release History
---------------

.. rubric:: Done in v3.0

* **Orquesta GA:** GA release of "Orquesta" workflow engine. Includes ``with-items``,
  delay, scheduling, notifications, Unicode support. Begin Mistral deprecation.
* **Workflow Designer v2:** Complete overhaul of Workflow Designer for easier creation
  and editing of workflows via a Web UI.
* **ChatOps:** Update ChatOps components, and add support for Microsoft Teams.
* **HA:** Simplify & streamline running |st2| in HA mode.
* **k8s:** Reference configurations for running |st2| Community and Enterprise in HA mode on k8s.

.. rubric:: Done in v2.9

* **Orquesta Second Beta:** Second beta of new "Orquesta" workflow engine.
* **WebUI:** Real-time streaming output, and Inquiries support
* **Action Output Structure Definition:** Enable optional definition of action payload, so that it
  can be inspected and used when passing data between actions in workflows.
* **k8s:** Beta reference configuration for running |st2| Enterprise in HA mode on k8s.
* **Windows Runners:** Add pywinrm-based Windows runner.

.. rubric:: Done in v2.8

* **Orquesta Beta:** Public beta of new "Orquesta" workflow engine (nb this was originally named "Orchestra").
* **WebUI:** Update look & feel of Web UI, and add "Triggers" tab for troubleshooting rules.
* **Python3 Actions:** Support Python 3 actions on a per-pack basis.
* **Metrics Framework:** New framework for metrics collection for action results, time, etc.

.. rubric:: Done in v2.7

* **Action Versioning:** Allow running specific action version - better management of rolling upgrades.
* **Mistral Callbacks:** Refactor Mistral to support callbacks instead of polling.
* **UTF-8/Unicode:** Allow UTF-8/Unicode characters in pack config files.
* **Virtual Appliance:** Vagrantbox/Virtual Appliance with ST2 already installed, for quicker testing.

.. rubric:: Done in v2.6

* **React Web UI:** Rewrote st2web Web UI to use React framework.
* **Streaming Output:** Streaming output enabled by default.
* **Pack Development:** Shared ``lib`` directory for actions and sensors.
* **st2client:** Python 3 support for ``st2client``.

.. rubric:: Done in v2.5

* **st2.ask:** Support ability to request/provide permission to proceed with workflow.
* **Streaming Output:** Provide streaming output from long-running actions as it is received.

.. rubric:: Done in v2.4

* **Pack UI:** Web interface for pack management.
* **Pause and Resume:** Pause and Resume Workflows and ActionChains.

.. rubric:: Done in v2.3

* **API Docs:** Auto-generated REST API docs - see `api.stackstorm.com
  <https://api.stackstorm.com>`_.
* **Monitoring Docs:** Create |st2| monitoring guidelines.
* **Docker based installer:** Complete the vision of OS independent, layered Docker-based
  installer, to increase reliability, modularity, and speed of deployment.

.. rubric:: Done in v2.2

* **Mistral Jinja support:** Mistral workflows now support Jinja notation.
* **Security improvements:** Better default security posture for MongoDB, RabbitMQ, PostgreSQL.

.. rubric:: Done in v2.1

* **StackStorm Pack Exchange:** Make integration and automation packs discoverable, continuously
  tested, and community rated. Solve the problem of packs spread all over GitHub.
* **Ubuntu Xenial (16.04) support**

.. rubric:: Done in v1.6

* **MongoDB:** MongoDB 3.x support.
* **Datastore:** Access K/V datastore from the Mistral workflows.

.. rubric:: Done in v1.5

* **Pack configuration:** Configuration separated from the pack code.
* **Datastore:** Key/value datastore secrets.

.. rubric:: Done in v1.4

* **Packaging:** Deprecation of All-in-One Installer.
* **Packaging:** Native deb/rpm packages with bundled python dependencies.
* **ChatOps:** ChatOps API support for Slack/HipChat providers.

.. rubric:: Done in v1.3

* **Workflows:** ``st2 re-run`` - resume failed workflows.
* **Scale:** Garbage collection service.

.. rubric:: Done in v1.2

* **Packs:** Pack Testing support.
* **ChatOps:** Fully reworked ChatOps with Jinja templating.
* **Policies:** Timeout and retry policies.

.. rubric:: Done in v1.1

* **FLOW:** Visual workflow representation and drag-and-drop workflow designer.
* **RBAC:** Role based access control for packs, actions, triggers and rules.
* **Pluggable authentication backends** including PAM, Keystone, Enterprise LDAP.
* **All-in-one installer**: production ready single-box reference deployment with graphical setup
  wizard.
* **RHEL 6 and 7 support**
* **Trace-tags**: ability to track a complete chain of triggers, rules, executions, related to a
  given triggering event.
* **Native SSH:** replace Fabric; Fabric based SSH still available and can be enabled via config.
* **WebUI major face-lift**


.. rubric:: Done in v0.11

* **ChatOps:** two-way chat integration beyond imagination.
* **More integration packs**: Major integrations - Salt, Ansible, some significant others.
  `Check the full list <https://exchange.stackstorm.org/>`_.

.. rubric:: Done in v0.9

* **Experimental windows support:** windows runner, and windows commands.
* **Web UI complete basics:** rule create/edit/delete in UI.

.. rubric:: Done in v0.8

* **Web UI:** refactor history view, create and edit rules and workflows, add graphical
  representations for workflow definitions and executions.
* **Improved** `Mistral <https://wiki.openstack.org/wiki/Mistral>`_  **integration:** simplified
  Mistral DSL for |st2| actions, visibility of workflow executions, and reliable of |st2|-Mistral
  communication. Includes Mistral improvements, features, and fixes.
* **Operational supportability:** Better output formats, better visibility to ongoing actions,
  better logs, better debugging tools.
* **Scale and reliability improvements:** deployed and run at scale, shown some good numbers, and
  more work identified.

.. rubric:: Done in v0.6.0

* **YAML:** complete moving to YAML for defining rules, action and trigger metadata,
  configurations, etc.
* **Plugin isolation and management:** Improved managements of sensors, action runners and provide
  isolated environments.
* **Reliability:** improvements on sensor and action isolation and reliability.

See :doc:`/changelog` for the full gory history of everything we've delivered so far.

.. include:: __engage_community.rst
