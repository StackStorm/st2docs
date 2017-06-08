Roadmap
=======

|st2| is still under active development. We welcome community feedback, and encourage contributions. Here's what we see as our top priorities:

* **Multi-node deployments:** Provide platform support for content deployment to multiple worker nodes, with better integration with git/GitHub. Simplify development and deployment of "automation as code" at scale.
* **Multi target configurations for integration packs:** For a given integration pack, define and manage multiple targets. This should allow the user to choose which one of a set of configurations to use for a given action.
* **Docker based installer:** Complete the vision of OS independent, layered Docker-based installer, to increase reliability, modularity, and speed of deployment.
* **History and Audit service:** History view with advanced search over years worth of execution records, over multiple versions of continuously upgraded |st2|.
* **At-scale refinements:** Ensure event handling reliability, and event storm resilience. Complete support for multi-node deployment of sensor containers and rules engines for resilience and throughput.
* **Security hardening:** Complete security audit and address issues discovered so far.
* **First class Windows support:** switch to pywinrm for better license. Remote PowerShell via Powershell.REST.API. Windows-native ActionRunners. 
* **Projects and Uber-flow:** Introduce projects to group and manage rules and workflows. Handle versions and dependencies. "Productize" flow-rule-flow-rule chain pattern, aka "uber-flow". Manage large number of automations across users and teams, on a single |st2| deployment at enterprise scale.
* **Action Output Structure Definition**: Enable optional definition of action payload, so that it can be inspected and used when passing data between actions in workflows.
* **RBACv2:**

  * **Filters**: Tag and property based filters, more refined and convenient access control.
  * **Permissions**: Permissions on key value objects, arbitrary triggers, support for a default role to be assigned to new users.
  * **WebUI**: UI for RBAC configuration.
  * **ChatOps**: Allow users to authenticate with |st2| via bot on chat. Check permissions of the user who triggered an action / ran a command. Introduce a special set of permission types for ChatOps.

* **API Docs:** Generate REST API docs.
* **Monitoring Docs:** Create |st2| monitoring guidelines.
* **More integration packs:** push more content to the community to help work with most common and widely used tools. Tell us if there is a tool you love and think we should integrate with, or better yet write a pack!

Is there some other feature you're desperately missing? Submit an `issue <https://github.com/StackStorm/st2docs/issues>`_!

Release History
---------------

.. rubric:: Done in v2.2

* **Mistral Jinja support:** Mistral workflows now support Jinja notation
* **Security improvements:** Better default security posture for MongoDB, RabbitMQ, PostgreSQL

.. rubric:: Done in v2.1

* **StackStorm Pack Exchange:** Make integration and automation packs discoverable, continuously tested, and community rated. Solve the problem of packs spread all over GitHub.
* **Ubuntu Xenial (16.04) support**

.. rubric:: Done in v1.6

* **MongoDB:** MongoDB 3.x support
* **Datastore:** Access K/V datastore from the Mistral workflows

.. rubric:: Done in v1.5

* **Pack configuration:** Configuration separated from the pack code
* **Datastore:** Key/value datastore secrets

.. rubric:: Done in v1.4

* **Packaging:** Deprecation of All-in-One Installer
* **Packaging:** Native deb/rpm packages with bundled python dependencies
* **ChatOps:** ChatOps API support for Slack/Hipchat providers

.. rubric:: Done in v1.3

* **Workflows:** ``st2 re-run`` - resume failed workflows
* **Scale:** Garbage collection service

.. rubric:: Done in v1.2

* **Packs:** Pack Testing support
* **ChatOps:** Fully reworked ChatOps with Jinja templating
* **Policies:** Timeout and retry policies

.. rubric:: Done in v1.1

* **FLOW:** Visual workflow representation and drag-and-drop workflow designer.
* **RBAC:** Role based access control for packs, actions, triggers and rules.
* **Pluggable auth backends** including PAM, Keystone, Enterprise LDAP.
* **All-in-one installer**: production ready single-box reference deployment with graphical setup wizard.
* **RHEL 6 and 7 support**
* **Trace-tags**: ability to track a complete chain of triggers, rules, executions, related to a given triggering event.
* **Native SSH:** replace Fabric; Fabric based SSH still available and can be enabled via config.
* **WebUI major face-lift**


.. rubric:: Done in v0.11

* **ChatOps:** two-way chat integration beyond imagination.
* **More integration packs**: Major integrations - Salt, Ansible, some significant others. `Check the full list <https://exchange.stackstorm.org/>`_.

.. rubric:: Done in v0.9

* **Experimental windows support:** windows runner, and windows commands.
* **Web UI complete basics:** rule create/edit/delete in UI.

.. rubric:: Done in v0.8

* **Web UI:** refactor history view, create and edit rules and workflows, add graphical representations for workflow definitions and executions.
* **Improving** `Mistal <https://wiki.openstack.org/wiki/Mistral>`_  **integration:** simplified Mistral DSL for |st2| actions, visibility of workflow executions, and reliabile of |st2|-Mistral communication. Includes Mistral improvements, features, and fixes.
* **Operational supportability:** Better output formats, better visibility to ongoing actions, better logs, better debugging tools.
* **Scale and reliability improvements:** deployed and run at scale, shown some good numbers, and more work identified.

.. rubric:: Done in v0.6.0

* **YAML:** complete moving to YAML for defining rules, action and trigger metadata, configurations, etc.
* **Plugin isolation and management:** Improved managements of sensors, action runners and provide isolated environments.
* **Reliability:** improvements on sensor and action isolation and reliability

See :doc:`/changelog` for the full gory history of everything we've delivered so far.

.. include:: __engage_community.rst
