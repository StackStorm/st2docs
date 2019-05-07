Installation
============

Ready to install |st2|? Here's an overview of how to get your system up and running.

|st2| is distributed as RPMs and Debs for RedHat/CentOS and Ubuntu Linux systems, and as Docker
images. You can either use a script to automatically install and configure all components on a
single system, or you can follow the manual instructions for your OS.

Here's an overview of the options:

* **One-line Install:** Run our installation script for an opinionated install of all components
  on a single system. This is a our recommended way to get started. See the :ref:`Quick Install
  <ref-one-line-install>` section below for details.
* **Manual Installation:** Have custom needs? Maybe no Internet access from your servers? Or just
  don't like using scripted installs? Read the manual installation instructions for your OS
  (:doc:`Ubuntu 16 </install/u16>`, :doc:`Ubuntu 18 </install/u18>`, :doc:`RHEL/CentOS 6 </install/rhel6>`,
   :doc:`RHEL/CentOS 7 </install/rhel7>`), and adapt them to your needs. Here's some `additional guidance
  <https://stackstorm.com/2017/02/10/installing-stackstorm-offline-systems/>`_ for setting up an
  internal mirror for the |st2| repos. 
* **Ansible Playbooks:** If you are an Ansible user, check these :doc:`/install/ansible` for
  installing |st2|. Ideal for repeatable, consistent, idempotent installation of |st2|.
* **High Availability** Entrusting business critical automation tasks to a system like StackStorm
  leads to higher demands on that system. StackStorm can run in a HA mode to ensure these needs.
  :doc:`/install/k8s_ha` automates entire complex infrastructure as a reproducible blueprint.

.. only:: community

  .. include:: /_includes/community_only_installs_overview.rst


Choose the option that best suits your needs.

Upgrading to |ewc|? This is installed as a set of additional packages on top of StackStorm. You
can either install StackStorm + |ewc| in one go, or add the |ewc| packages to an existing
StackStorm system. If you are using |ewc|, you can also add Network Automation Suites.
Read the :doc:`/install/ewc` documentation for more.

.. _ref-one-line-install:

.. rubric:: Quick Install

Grab a **clean** 64-bit Linux system that fits the :doc:`system requirements
<system_requirements>`. Make sure that ``curl`` is up to date using ``sudo apt-get install curl``
on Ubuntu, or ``sudo yum install curl nss`` on RHEL/CentOS. Then run this command:

.. code-block:: bash

   curl -sSL https://stackstorm.com/packages/install.sh | bash -s -- --user=st2admin --password='Ch@ngeMe'

This is an opinionated installation of |st2|. It will download and install all components, as per
the :doc:`single host reference deployment <./overview>`. It assumes that you have a clean, basic
installation of Ubuntu or RHEL/CentOS. 

If you are trying to install |st2| on a server with other applications, or local customisations,
you may run into problems. In that case, you should use one of the manual installation methods.

The script itself is not idempotent. If you try to re-run the script on top of a failed
installation, it will fail. Start again with a clean system, or switch to a manual install.

If you're installing behind a proxy, just export the proxy ENV variables
``http_proxy``, ``https_proxy``, ``no_proxy`` before running the script.

.. code-block:: bash

  export http_proxy=http://proxy.server.io:port
  export https_proxy=http://proxy.server.io:port
  export no_proxy=localhost,127.0.0.1

In case of MITM proxy, you may need to export additional ``proxy_ca_bundle_path``, see :ref:`packs-behind-proxy`.


If you have problems accessing the Web UI on a RHEL 7/CentOS 7 system, check the
:ref:`system firewall settings <ref-rhel7-firewall>`.

.. include:: __installer_passwords.rst

.. rubric:: Other Installation Options

For more details on reference deployments, or OS-specific installation instructions, see below:

.. toctree::
    :maxdepth: 1

    Reference Deployment Overview <overview>
    system_requirements
    Ubuntu 16.04 <u16>
    Ubuntu 18.04 <u18>
    RHEL 7 / CentOS 7 <rhel7>
    RHEL 6 / CentOS 6 <rhel6>
    Kubernetes / HA <k8s_ha>
    Ansible Playbooks <ansible>

.. include:: /_includes/community_only_installs_toctree.rst

.. toctree::
    :maxdepth: 1

    Extreme Workflow Composer <ewc>
    config/index
    upgrades
    uninstall
