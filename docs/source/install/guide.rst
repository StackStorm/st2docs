Installation Guide
===================
This guide provides step-by step instructions on installing StackStorm on a single box per :doc:`Reference deployment </install/overview>` on a Ubuntu/Debian or Redhat/CentOS.

.. contents::


Minimal installation
--------------------

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

Install MongoDB, RabbitMQ, and PostgreSQL.

  .. rst-class:: ubuntu

    Ubuntu/Debian

  .. code-block:: bash

    sudo apt-get install -y mongodb-server rabbitmq-server postgresql

  .. rst-class:: centos

    CentOS/RHEL

  .. code-block:: bash

    TBD


Setup repositories
~~~~~~~~~~~~~~~~~~~

  .. rst-class:: ubuntu

    Ubuntu/Debian

  .. code-block:: bash

    wget -qO - https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
    echo "deb https://dl.bintray.com/stackstorm/`lsb_release -cs`_staging stable main" | sudo tee /etc/apt/sources.list.d/st2-stable.list
    sudo apt-get update

  .. rst-class:: centos

    CentOS/RHEL

  .. code-block:: bash

    TBD

Install StackStorm components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  .. rst-class:: ubuntu

    Ubuntu/Debian

  .. code-block:: bash

      sudo apt-get update
      sudo apt-get install st2 st2-mistral

  .. rst-class:: centos

    CentOS/RHEL

  .. code-block:: bash

    TBD

If you are not running RabbitMQ, MongoDB or PostgreSQL on the same box, or changed defauls,
please adjust the settings:

    * RabbitMQ connection at ``/etc/st2/st2.conf`` and ``/etc/mistral/mistral.conf``
    * MongoDB at ``/etc/st2/st2.conf``
    * PostgreSQL at ``/etc/mistral/mistral.conf``

Setup Mistral Database
~~~~~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

    # Create Mistral DB in postgres
    cat << EHD | sudo -u postgres psql
    CREATE ROLE mistral WITH CREATEDB LOGIN ENCRYPTED PASSWORD 'StackStorm';
    CREATE DATABASE mistral OWNER mistral;
    EHD

    #DZ: Do we REALLY need this, unless we upgrade Mistral?
    /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head
    #DZ: Do we REALLY need this? we don't use any default mistral actions and workflows...
    /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate

Configure SSH and SUDO
~~~~~~~~~~~~~~~~~~~~~~
To run local and remote shell actions, StackStorm uses a special system user (default ``stanley``).
For remote linux actions, SSH is used. It is advised to configure identity file based SSH access on all remote hosts. We also recommend configuring SSH access to localhost for running examples and testing.

* Take these steps on all boxes where you run stackstorm remote actions, **including** ``localhost``.

  .. code-block:: bash

    # Create an SSH system user
    useradd stanley
    mkdir -p /home/stanley/.ssh
    chmod 0700 /home/stanley/.ssh

    # Generate ssh keys on StackStorm box and copy over public key into remote box.
    ssh-keygen -f /home/stanley/.ssh/stanley_rsa -P ""
    cp ${KEY_LOCATION}/stanley_rsa.pub /home/stanley/.ssh/stanley_rsa.pub

    # Authorize key-base acces
    cat /home/stanley/.ssh/stanley_rsa.pub >> /home/stanley/.ssh/authorized_keys
    chmod 0600 /home/stanley/.ssh/authorized_keys
    chown -R stanley:stanley /home/stanley

    # Enable passwordless sudo
    echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2

* Enable passwordless sudo on for system user on StackStorm host
  (required for local script actions, using ``local-shell-cmd`` and ``local-shell-script`` runners).

  .. code-block:: bash

    echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2

* Adjust configuration in ``/etc/st2/st2.conf``:

  .. sourcecode:: ini

    [system_user]
    user = stanley
    ssh_key_file = /home/stanley/.ssh/stanley_rsa

Check it all works
~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

    st2 --version

    st2 -h

    st2 action list --pack=core

    # List the actions from a 'core' pack
    st2 action list --pack=core

    # Run a local shell command
    st2 run core.local -- date -R

    # See the execution results
    st2 execution list

    # Fire a remote comand via SSH (Requires passwordless SSH)
    st2 run core.remote hosts='localhost' -- uname -a


-----------------

At this point you have a minimal working installation, and can happily play with StackStorm, do quickstart, deploy examples (see ...) and so on.

But there is no joy without WebUI, no security without SSL termination, no fun without ChatOps, and no money without Enterprise edition. Read on, move on!

-----------------

Configure Authentication
------------------------

Reference deployment uses File Based auth provider for simplicity. Refer to :doc:`/authentication` to configure and use PAM or LDAP autentication backends. To set it up:

* Enable and configure auth in ``/etc/st2/st2.conf``:

  .. sourcecode:: ini

    [auth]
    ...
    enabled = True
    backend = flat_file
    backend_kwargs = {"file_path": "/etc/st2/htpasswd"}
    ...

* Create a user with a password:

  .. code-block:: bash

      sudo htpasswd -cb /etc/st2/htpasswd test Ch@ngeMe

* Authenticate, export the token for st2 CLI, and check that it works:

  .. code-block:: bash

      # Shortcut to authenticate and export the token
      export ST2_AUTH_TOKEN=$(st2 auth test -p Ch@ngeMe -t)

      # Check that it works
      st2 action list


Install WebUI and setup SSL termination
---------------------------------------

* install nginx
* generate certificate (instructions, pointer to a script)
* configure nginx - copy files to site-enabled loosly explain what we are doing which is
    * http-https redirect
    * SSL termination and HTTPS
    * serve the client as static content
    * serve API and AUTH off  HTTPS and reverse-proxy them so that less ports and no CORS issues


Set up ChatOps
--------------

* just run docker? The secret there is in upstart script(s)
* Or manual installation, see instructions under :ref:`Chatops Configuration <chatops-configuration>`.


Upgrade to Enterprise Edition
-----------------------------
Enterprise Edition is deployed as an addition on top of StackStorm. Detailed instructions coming up;
meantime if you are an enterprise customer call support and we walk you through.