Roadmap
=======

|st2| is still under active development. We welcome community feedback, and encourage
contributions. Here's our plans for the next releases.


.. note::

    This is a roadmap. It represents our current product direction. All product releases
    will be on a when-and-if available basis. Actual feature development and timing of releases
    will be at the sole discretion of the development team. This roadmap does not create a
    commitment to deliver a specific feature. Contents are subject to change without notice.
    
    If there's something you really need, remember: this is Open Source. Write and contribute
    the feature. Pull Requests are open to anyone.


3.7
---

* The roadmap for ``3.7`` is in the works, stay tuned!

Monitor the `master branch <https://github.com/StackStorm/st2/>`_ to see how we're progressing.

Backlog
-------

Here's some more nice things on our list that we haven't scheduled yet:

* **Python ChatOps:** Convert ChatOps backend to Python
* **ChatOps:** Support RBAC.
* **K8s/HA:** Graduate `K8s Helm chart <https://github.com/stackstorm/stackstorm-ha>`_ from beta to stable.
* **Workflow runtime graph:** Runtime view of workflow execution in st2flow for |ewc|.
* **Workflow dry run:** Ability to run unit tests on orquesta workflows for |ewc|.
* **SSO:** Support SSO with SAML2 for |ewc| web UI (beta).
* **Job Scheduling:** Job scheduling for ad-hoc jobs.
* **Datastore viewer/editor:** Datastore viewer/editor at web UI.
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

.. rubric:: Done in v3.6
* RabbitMQ:** Updated all OS to use latest RabbitMQ
* Security improvements:** Use Jinja sandbox to mitigate against CVE-2021-44657
* API changes:** Additional option to remove files when deleting packs
* Service configuration:** Changes made to simplify the service configuration to make it simpler to change ports used by services
* Profiling:** New flags to support debugging and profiling --enable-profiler and --enable-eventlet-blocking-detection

.. rubric:: Done in v3.5

* **Ubuntu Focal:** Add support for Ubuntu 20.04, with Python 3.8 and Mongo 4.4
* **Ubuntu Xenial:** Remove support for Ubuntu 16.04
* **Performance improvements:** Performance improvements on JSON serialization/deserialization
* **Redis:** Add Redis as a coordination backend

.. rubric:: Done in v3.4

* **Python 2 deprecation:** Updated RHEL/CentOS 7.x and Ubuntu 16.04 to use Python 3.6, and update packs in StackStorm-Exchange 
* **RBAC:** Integrate ``st2rbac`` (previously EWC/BWC) features into core.
* **LDAP:** Integrate ``st2ldap`` (previously EWC/BWC) features into core.
* **st2flow:** Integrate ``st2flow`` (previously EWC/BWC) features into ``st2web``.

.. rubric:: Done in v3.3

* **RHEL/CentOS:** Drop support for RHEL/CentOS 6.x.
* **Mistral deprecation:** Orquesta replaces Mistral as the workflow engine.
* **HipChat Removal:** The HipChat adapter has been removed from st2chatops.
* **Chef:** Deprecated `chef-stackstorm <https://github.com/stackstorm/chef-stackstorm>`_ deployment.
* **Docker:** Overhaul for `st2-docker <https://github.com/stackstorm/st2-docker>`_ deployment.
* **MongoDB:** Require MongoDB 4.0 across all OSes.

.. rubric:: Done in v3.2

* **RHEL/CentOS:** Support CentOS 8/RHEL 8 with Python 3.6 and MongoDB 4.0.
* **Ubuntu:** Stop producing Ubuntu 14.04 packages.
* **Core:** Pack install with dependencies.
* **Orquesta:** Support task retry in workflow definition.
* **Orquesta:** Support rerun of workflow execution from task(s).

.. rubric:: Done in v3.1

* **Ubuntu:** GA Support Ubuntu 18.04, with Python 3.6
* **Ubuntu:** Drop Ubuntu 14.04 support. Packages are still available for a limited time.
* **MongoDB:** Support MongoDB 4.0 (required for Ubuntu 18.04).
* **ChatOps:** Microsoft Teams GA.
* **Core:** Support latest ``pip`` and ``requests()``.

.. rubric:: Done in v3.0

* **Orquesta GA:** GA release of "Orquesta" workflow engine.
* **Workflow Designer v2:** Complete overhaul of Workflow Designer for easier creation
  and editing of workflows via a Web UI. Includes Orquesta workflow editing and creation.
* **ChatOps:** Microsoft Teams Beta.
* **Python3:** All Exchange packs updated for Python3 CI/CD.
* **Legacy Runners:** Remove legacy CloudSlang and Winexe runners.

.. rubric:: Done in v2.10

* **Orquesta RC:** Release Candidate of "Orquesta" workflow engine. Includes ``with-items``,
  delay, scheduling, notifications, Unicode support. Begin Mistral deprecation.
* **ChatOps:** Update ChatOps components.
* **HA:** Simplify & streamline running |st2| in HA mode.
* **k8s:** Reference configurations for running |st2| Community and Enterprise in HA mode on k8s.
* **Ubuntu 18.04:** Beta support of Ubuntu 18.04, MongoDB 4.0, Python 3.6.

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
