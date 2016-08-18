Roadmap
=======

|st2| is still under active development. We welcome community feedback, and encourage contributions. Here's what we see as our top priorities:

* **StackStorm Pack Exchange:** Make integration and automation packs discoverable, continuously tested, and community rated. Solve the problem of packs spread all over GitHub.
* **Multi-node deployments:** Provide platform support for content deployment to multiple worker nodes, with better integration with git/GitHub. Simplify development and deployment of "automation as code" at scale.
* **Multi target configurations for integration packs:** For a given integration pack, define and manage multiple targets. This should allow the user to choose which one of a set of configurations to use for a given action.
* **Docker based installer:** Complete the vision of OS independent, layered Docker-based installer, to increase reliability, modularity, and speed of deployment.
* **History and Audit service:** History view with advanced search over years worth of execution records, over multiple versions of continuously upgraded StackStorm.
* **At-scale refinements:** Ensure event handling reliability, and event storm resilience. Complete support for multi-node deployment of sensor containers and rules engines for resilience and throughput.
* **Security hardening:** Complete security audit and address issues discovered so far.
* **First class Windows support:** switch to pywinrm for better license. Remote PowerShell via Powershell.REST.API. Windows-native ActionRunners. 
* **Projects and Uber-flow:** Introduce projects to group and manage rules and workflows. Handle versions and dependencies. "Productize" flow-rule-flow-rule chain pattern, aka "uber-flow". Manage large number of automations across users and teams, on a single StackStorm deployment at enterprise scale.
* **Action Output Structure Definition**: Enable optional definition of action payload, so that it can be inspected and used when passing data between actions in workflows.
* **RBACv2:**

  * **Filters**: Tag and property based filters, more refined and convenient access control.
  * **Permissions**: Permissions on key value objects, arbitrary triggers, support for a default role to be assigned to new users.
  * **WebUI**: UI for RBAC configuration.
  * **ChatOps**: Allow users to authenticate with StackStorm via bot on chat. Check permissions of the user who triggered an action / ran a command. Introduce a special set of permission types for ChatOps.
* **API Docs:** Generate REST API docs.
* **Monitoring Docs:** Create |st2| monitoring guidelines.	
* **More integration packs:** push more content to the community to help work with most common and widely used tools. Tell us if there is a tool you love and think we should integrate with, or better yet write a pack!

Is there some other feature you're desperately missing? Submit an `issue <https://github.com/StackStorm/st2docs/issues>`_!

See :doc:`/changelog` for the full gory history of everything we've delivered so far.

.. include:: __engage.rst
