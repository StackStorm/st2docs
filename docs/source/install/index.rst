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
  (:doc:`Ubuntu 14/16 </install/deb>`, :doc:`RHEL/CentOS 6 </install/rhel6>`, :doc:`RHEL/CentOS 7
  </install/rhel7>`), and adapt them to your needs. Here's some `additional guidance
  <https://stackstorm.com/2017/02/10/installing-stackstorm-offline-systems/>`_ for setting up an
  internal mirror for the |st2| repos. 
* **Ansible Playbooks:** If you are an Ansible user, check these :doc:`/install/ansible` for
  installing |st2|. Ideal for repeatable, consistent, idempotent installation of |st2|.
* **Docker:** |st2| is now supported on Docker - check out our :doc:`docker` instructions.
* **Vagrant:** Vagrant is a quick way to spin up a test system - see  `st2vagrant
  <https://github.com/StackStorm/st2vagrant>`_. This will bring up a new VM, and install |st2|.

Choose the option that best suits your needs.

Upgrading to |bwc|? This is installed as a set of additional packages on top of StackStorm. You
can either install StackStorm + |bwc| in one go, or add the |bwc| packages to an existing
StackStorm system. If you are using |bwc|, you can also add Brocade Network Automation Suites.
Read the :doc:`/install/bwc` documentation for more.

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
installation, it fail. Start again with a clean system, or switch to a manual install.

If you have problems accessing the Web UI on a RHEL 7/CentOS 7 system, check the
:ref:`system firewall settings <ref-rhel7-firewall>`.

.. include:: __installer_passwords.rst

.. rubric:: Other Installation Options

For more details on reference deployments, or OS-specific installation instructions, see below:

.. toctree::
    :maxdepth: 1

    Reference Deployment Overview <overview>
    system_requirements
    Ubuntu 14.04 / 16.04 <deb>
    RHEL 7 / CentOS 7 <rhel7>
    RHEL 6 / CentOS 6 <rhel6>
    Docker <docker>
    Ansible Playbooks <ansible>
    Brocade Workflow Composer <bwc>
    config/index
    upgrades
