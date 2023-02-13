Uninstall
=========

We strongly believe in Automation, and advise that servers should be treated as `Cattle not Pets
<http://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/>`_. Therefore, our
recommendation is to destroy the VM or container, rather than uninstalling |st2|.

Unfortunately some users operate in environments where it is difficult to get a new VM on demand,
or they need to re-run a failed |st2| installation. For them, we offer this guidance on how to
remove |st2| and related applications.

.. warning::

  * The instructions given here will delete data. 
  * If you are trying to recover from a failed installation, some of these steps may fail. Proceed
    with all instructions, and ignore any errors.
  * Proceed with caution if you have other applications running on this system, especially if you
    are re-using components such as RabbitMQ, MongoDB, Nginx or PostgreSQL. You will need to
    manually delete the relevant databases & configurations.
  * Removing the |st2| packages will not automatically remove all dependencies that may have been
    installed. Because we don't know exactly which applications were installed originally, we
    can't know for sure which dependencies are safe to remove. These can be left on your system.

Overview
--------

The uninstallation procedure follows this outline:

1. Stop services.
2. Remove packages.
3. Remove |st2| system user.
4. Remove databases and other dependencies.
5. Remove repositories.
6. Clean up any remaining logs, configurations and directories.


The exact steps vary slightly between Linux distributions. This is highlighted in the instructions
below. Only execute the instructions for your distribution.

1. Stop Services
----------------

* Ubuntu 18.04/20.04:

  .. sourcecode:: bash

    sudo st2ctl stop
    sudo service nginx stop
    sudo service mongod stop
    sudo service rabbitmq-server stop
    sudo service redis-server stop

* RHEL/CentOS/RockyLinux:

  .. sourcecode:: bash

    sudo st2ctl stop
    sudo systemctl stop nginx
    sudo systemctl stop mongod
    sudo systemctl stop rabbitmq-server
    sudo systemctl stop redis

.. note::

  If uninstalling a version earlier than StackStorm 3.3, add postgresql to list of services to stop if is running on your system.



2. Remove Packages
------------------

* Ubuntu 18.04/20.04:

  If you are using StackStorm only:

  .. sourcecode:: bash

    sudo apt-get purge st2 st2chatops st2web

  If you have |ewc| installed, instead use:

  .. sourcecode:: bash

    sudo apt-get purge st2 st2chatops st2web bwc-ui st2flow


* RHEL/CentOS/RockyLinux:

  If you are using StackStorm only:

  .. sourcecode:: bash

    sudo yum erase st2 st2chatops st2web

  If you have |ewc| installed, instead use: 

  .. sourcecode:: bash

    sudo yum erase st2 st2chatops st2web bwc-ui st2flow

.. note::

  If uninstalling a version earlier than StackStorm 3.3, add st2mistral to list of packages to remove if it is installed on your system.


3. Remove |st2| System User
---------------------------

* Ubuntu/RHEL/CentOS/RockyLinux:

  .. sourcecode:: bash

    sudo userdel -r stanley
    sudo rm -f /etc/sudoers.d/st2


4. Remove Databases and Other Dependencies
------------------------------------------

* Ubuntu:

  .. sourcecode:: bash

    sudo apt-get purge mongodb-org* rabbitmq-server erlang* nginx nodejs redis-server

* RHEL/CentOS/RockyLinux:

  .. sourcecode:: bash

    sudo yum erase mongodb-org* rabbitmq-server erlang* nginx nodejs redis

.. note::

  If uninstalling a version earlier than StackStorm 3.3, add postgresql* to list of databases to remove if it is installed on your system.


5. Remove Repositories
----------------------

* Ubuntu:

  .. sourcecode:: bash

    sudo rm -f /etc/apt/sources.list.d/mongo* /etc/apt/sources.list.d/nginx.list
    sudo rm -f /etc/apt/sources.list.d/StackStorm* /etc/apt/sources.list.d/nodesource* 
    sudo rm -f /etc/apt/sources.list.d/rabbitmq*

* RHEL/CentOS/RockyLinux:

  .. sourcecode:: bash

    sudo rm -f /etc/yum.repos.d/mongodb-org* /etc/yum.repos.d/StackStorm*
    sudo rm -f /etc/yum.repos.d/pgdg-94* /etc/yum.repos.d/nginx* /etc/yum.repos.d/nodesource*
    sudo rm -f /etc/yum.repos.d/rabbitmq_erlang* /etc/yum.repos.d/*rabbitmq-server*


5. Clean Up Remaining Content
-----------------------------

Some files and directories will still remain after removing packages. This step will remove those
last pieces.

* Ubuntu:

  .. sourcecode:: bash

    sudo rm -rf /etc/st2 /opt/stackstorm
    sudo rm -rf /var/log/st2 /var/log/mongodb
    sudo rm -rf /var/lib/mongodb /var/run/mongodb.pid 
    sudo rm -rf /etc/redis/redis.conf /var/lib/redis
    sudo userdel -r redis

* RHEL/CentOS/RockyLinux:

  .. sourcecode:: bash

    sudo rm -rf /etc/st2 /etc/mongod* /etc/rabbitmq /etc/nginx /opt/stackstorm
    sudo rm -rf /var/log/st2 /var/log/mongodb /var/log/rabbitmq /var/log/nginx
    sudo rm -rf /var/lib/rabbitmq /var/lib/mongo
    sudo rm -rf /etc/redis/redis.conf /var/lib/redis
    sudo userdel -r redis

At this point, your system is no longer running any |st2|-related services, and all the main
dependencies have been removed. You can either re-install |st2|, or use this system for other
applications.

.. note::

  If uninstalling a version earlier than StackStorm 3.3, add /var/log/mistral and /var/lib/pgsql to the list of directories to remove if present.

