Installing |ewc|
================

StackStorm is an event-driven DevOps automation platform with all the essential features suitable
for small businesses and teams. It’s free and open source under the Apache 2.0 license.

|ewc| (EWC) is the commercial version of the StackStorm automation platform. EWC adds priority
support, advanced features such as fine-tuned access control (RBAC), LDAP, and Workflow Designer. To
learn more about |ewc|, get an evaluation license, or request a quote, visit `Workflow Composer Product Page
<https://www.extremenetworks.com/product/workflow-composer/>`_ and `Contact Sales <https://www.extremenetworks.com/contact-sales/>`_.

.. image:: /_static/images/flow/pkg_promote_workflow.png
    :align: center

You can also add Network Automation Suites on top of an |ewc| system. See
`ewc-docs.extremenetworks.com/solutions/overview.html <https://ewc-docs.extremenetworks.com/solutions/overview.html>`_
to learn more.

Quick Evaluation
----------------

To install |ewc| for a quick evaluation, run the commands below on a clean 64-bit Linux box that
meets the :doc:`/install/system_requirements`. Replace ``${EWC_LICENSE_KEY}`` with the key you
received when registering for evaluation or purchasing EWC.

.. code-block:: bash

  curl -sSL -O https://stackstorm.com/ewc/install.sh && chmod +x install.sh
  ./install.sh --user=st2admin --password='Ch@ngeMe' --license=${EWC_LICENSE_KEY}

Upgrading from Community
------------------------

Already have a working StackStorm system, and want to add |ewc|? No problem! No need to install a
new system. You can install |ewc| on top of your existing system. Just run install commands, again
replacing ``${EWC_LICENSE_KEY}`` with the license key you received when registering:

.. code-block:: bash

  curl -sSL -O https://stackstorm.com/ewc/install.sh && chmod +x install.sh
  ./install.sh --user=st2admin --password='Ch@ngeMe' --license=${EWC_LICENSE_KEY}

To understand the full details of the installation procedure, or to install |ewc| manually, follow
the installation guide for your Linux version: :doc:`/install/u16`, :doc:`/install/u18`, :doc:`/install/rhel7`, :doc:`/install/rhel8`,
or :doc:`/install/rhel8`. It will walk you through installing and configuring StackStorm and |ewc|.
The last step of the instructions is "Upgrade to |ewc|".

High Availability deployment
----------------------------
Using |ewc| in production and need better safety for all important operations you delegate to automation engine?
StackStorm was built with High Availability in mind - check out :ref:`StackStorm Enterprise HA in Kubernetes <ref-ewc-ha>` for  deployment blueprint.

.. include:: /__engage_enterprise.rst
