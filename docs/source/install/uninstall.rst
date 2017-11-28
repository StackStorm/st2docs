Uninstall
=========

We strongly believe in Automation, and believe that servers should be treated as `Pets not Cattle <http://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/>`_. So our usual response to the question "How do I uninstall |st2|?" is: "Don't uninstall. Destroy the VM or container, and spin up a new base system." This is faster and more reliable than any other method.

However, some users are not able to get a new VM on demand, or perhaps they are trying to re-run a failed installation.

For those users, we offer this guidance on how to remove |st2| and related applications.

Caveats
-------

* The instructions given here will delete data. Do not execute them unless you are sure about what you are doing.
* If you are trying to recover from a failed installation, some of these steps may fail, depending on what stage your install failed at. Proceed with all instructions, and ignore any errors.
* If you have a distributed system, you will need to modify these instructions to suit your environment.
* Proceed with caution if you have other applications running on this system, especially if you are re-using components such as RabbitMQ, MongoDB, Nginx or PostgreSQL. In that case you will need to manually delete the relevant databases & configurations, rather than completely removing them.
* Removing the |st2| packages will not automatically remove all dependencies installed. Because we don't know exactly which applications were installed originally, we can't know for sure which dependencies are safe to remove. It should not cause any issues if any of these are left on your system. They will use some disk space, but no other resources.

Overview
--------

The uninstallation procedure follows this outline:

1. Stop services.
2. Remove packages.
3. Remove |st2| system user.
4. Remove databases and other dependencies.
5. Remove repositories.
6. Clean up any remaining logs and configuration files.


The exact steps vary slightly between Linux distributions. This is highlighted in the instructions below.

1. Stop Services
----------------

Ubuntu systems:

   .. sourcecode:: bash

      sudo st2ctl stop
      sudo service nginx stop
      sudo service postgresql stop
      sudo service mongod stop
      sudo service rabbitmq-server stop

RHEL/CentOS:

  .. sourcecode:: bash

    <some command>


2. Remove Packages
------------------

|st2| on Ubuntu systems:

   .. sourcecode:: bash

      sudo apt-get purge st2 st2mistral st2chatops st2web

If you are running |bwc|, you should instead use:

   .. sourcecode:: bash

      sudo apt-get purge st2 st2mistral st2chatops st2web bwc-ui st2flow

|st2| on RHEL/CentOS systems:

   .. sourcecode:: bash

      sudo yum remove st2 st2mistral st2chatops st2web

If you are running |bwc|, you should instead use:

   .. sourcecode:: bash

      sudo yum remove st2 st2mistral st2chatops st2web bwc-ui st2flow


3. Remove |st2| System User
---------------------------

Ubuntu/RHEL/CentOS:

  .. sourcecode:: bash

  sudo userdel -r stanley
  sudo rm -f /etc/sudoers.d/st2


4. Remove Databases and Other Dependencies
------------------------------------------

Ubuntu:

  .. sourcecode:: bash

    sudo apt-get purge postgresql 

RHEL/CentOS: