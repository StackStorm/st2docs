Ubuntu / Debian
=================

This guide provides step-by step instructions on installing StackStorm on a single box on a Ubuntu/Debian.
A script `st2bootstrap-deb.sh <https://github.com/StackStorm/st2-packages/blob/master/scripts/st2bootstrap-deb.sh>`_,
codifies the instructions below and is a master source of truth in case of inconsistencies: code wins over docs.

.. warning :: Currently BETA! Please try, use and report bugs on
   `github.com/StackStorm/st2-packages <https://github.com/StackStorm/st2-packages/issues/new>`_.
   Soon, package-based installation will be
   the preferred path to installing StackStorm. Support for CentOS/RHEL is coming.

.. contents::


Minimal installation
--------------------

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

Install MongoDB, RabbitMQ, and PostgreSQL.

  .. code-block:: bash

    sudo apt-get update
    sudo apt-get install -y mongodb-server rabbitmq-server postgresql


Setup repositories
~~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

    # Pick OS version from: trusty, jessie, wheezy
    export DISTRO=trusty
    wget -qO - https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
    echo "deb https://dl.bintray.com/stackstorm/${DISTRO}_staging stable main" | sudo tee /etc/apt/sources.list.d/st2-staging-stable.list
    unset DISTRO
    sudo apt-get update


Install StackStorm components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

      sudo apt-get update
      sudo apt-get install st2 st2mistral


If you are not running RabbitMQ, MongoDB or PostgreSQL on the same box, or changed defauls,
please adjust the settings:

    * RabbitMQ connection at ``/etc/st2/st2.conf`` and ``/etc/mistral/mistral.conf``
    * MongoDB at ``/etc/st2/st2.conf``
    * PostgreSQL at ``/etc/mistral/mistral.conf``

Setup Mistral Database
~~~~~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

    # Create Mistral DB in PostgreSQL
    cat << EHD | sudo -u postgres psql
    CREATE ROLE mistral WITH CREATEDB LOGIN ENCRYPTED PASSWORD 'StackStorm';
    CREATE DATABASE mistral OWNER mistral;
    EHD

    # Setup Mistral DB tables, etc.
    /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head
    # Register mistral actions
    /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate

Configure SSH and SUDO
~~~~~~~~~~~~~~~~~~~~~~
To run local and remote shell actions, StackStorm uses a special system user (default ``stanley``).
For remote linux actions, SSH is used. It is advised to configure identity file based SSH access on all remote hosts. We also recommend configuring SSH access to localhost for running examples and testing.

* Create StackStorm system user, enable passwordless sudo, and set up ssh access to "localhost" so that SSH-based action can be tried and tested locally. You will need elevated privileges to do this.

  .. code-block:: bash

    # Create an SSH system user (default `stanley` user may be already created)
    useradd stanley
    mkdir -p /home/stanley/.ssh
    chmod 0700 /home/stanley/.ssh

    # On StackStorm host, generate ssh keys
    ssh-keygen -f /home/stanley/.ssh/stanley_rsa -P ""

    # Authorize key-base acces
    cat /home/stanley/.ssh/stanley_rsa.pub >> /home/stanley/.ssh/authorized_keys
    chmod 0600 /home/stanley/.ssh/authorized_keys
    chown -R stanley:stanley /home/stanley

    # Enable passwordless sudo
    echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2

* Configure SSH access and enable passwordless sudo on the remote hosts which StackStorm would control
  over SSH. Use the public key generated in the previous step; follow instructions at :ref:`config-configure-ssh`.
  To control Windows boxes, configure access for :doc:`Windows runners </config/windows_runners>`.

* Adjust configuration in ``/etc/st2/st2.conf`` if you are using a different user or path to the key:

  .. sourcecode:: ini

    [system_user]
    user = stanley
    ssh_key_file = /home/stanley/.ssh/stanley_rsa

Start Services
~~~~~~~~~~~~~~
* Start services ::

    sudo st2ctl start

* Register sensors and actions ::

    st2ctl reload

Verify
~~~~~~

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

    # Install a pack
    st2 run packs.install packs=st2

Use the supervisor script to manage |st2| services: ::

    st2ctl start|stop|status|restart|restart-component|reload|clean


-----------------

At this point you have a minimal working installation, and can happily play with StackStorm:
follow :doc:`/start` tutorial, :ref:`deploy examples <start-deploy-examples>`, explore and install packs from `st2contrib`_.

But there is no joy without WebUI, no security without SSL termination, no fun without ChatOps, and no money without Enterprise edition. Read on, move on!

-----------------

Configure Authentication
------------------------

Reference deployment uses File Based auth provider for simplicity. Refer to :doc:`/authentication` to configure and use PAM or LDAP autentication backends. To set it up:

* Enable and configure auth in ``/etc/st2/st2.conf``:

  .. sourcecode:: ini

    [auth]
    # ...
    enabled = True
    backend = flat_file
    backend_kwargs = {"file_path": "/etc/st2/htpasswd"}
    # ...

* Create a user with a password:

  .. code-block:: bash

      # Install htpasswd utility if you don't have it
      sudo apt-get install apache2-utils
      # Create a user record in a password file.
      echo "Ch@ngeMe" | sudo htpasswd -i /etc/st2/htpasswd test

* Authenticate, export the token for st2 CLI, and check that it works:

  .. code-block:: bash

    # Get an auth token and use in CLI or API
    st2 auth test

    # A shortcut to authenticate and export the token
    export ST2_AUTH_TOKEN=$(st2 auth test -p Ch@ngeMe -t)

    # Check that it works
    st2 action list

Check out :doc:`/cli` to learn convinient ways to authenticate via CLI.

Install WebUI and setup SSL termination
---------------------------------------
`NGINX <http://nginx.org/>`_ is used to serve WebUI static files, redirect HTTP to HTTPS,
provide SSL termination for HTTPS, and reverse-proxy st2auth and st2api API endpoints.
To set it up: install `st2web` and `nginx`, generate certificates or place your existing
certificates under ``/etc/ssl/st2``, and configure nginx with StackStorm's supplied
:github_st2:`site config file st2.conf<conf/nginx/st2.conf>`.

  .. code-block:: bash

    # Install st2web and nginx
    apt-get install st2web nginx

    # Generate self-signed certificate or place your existing certificate under /etc/ssl/st2
    mkdir -p /etc/ssl/st2
    openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/st2/st2.key -out /etc/ssl/st2/st2.crt \
    -days XXX -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information \
    Technology/CN=$(hostname)"

    # Remove default site, if present
    rm /etc/nginx/sites-enabled/default
    # Copy and enable StackStorm's supplied config file
    cp /usr/share/doc/st2/conf/nginx/st2.conf /etc/nginx/sites-available/
    ln -s /etc/nginx/sites-available/st2.conf /etc/nginx/sites-enabled/st2.conf

    service nginx restart

If you modify ports, or url paths in nginx configuration, make correspondent chagnes in st2web
configuration at ``/opt/stackstorm/static/webui/config.js``.

Set up ChatOps
--------------

.. todo:: detail this section

If you already have Hubot installed and working, you only have to install the ``hubot-stackstorm`` plugin and configure StackStorm env variables (below) to get started.

Otherwise, the easiest way to install Hubot and configure StackStorm ChatOps is to use `stackstorm/hubot <https://hub.docker.com/r/stackstorm/hubot/>`_ docker image. Make sure all the prerequisites are in order:

  * You should have the ``chatops`` pack installed in StackStorm (it should be there by default), and the ``chatops.notify`` rule is enabled.
  * If Docker is not installed, follow the instructions at the `Docker website <https://docs.docker.com/engine/installation/linux/ubuntulinux/>`_.
  * Pull the ``stackstorm/hubot`` image: ``docker pull stackstorm/hubot``.

To pass StackStorm credentials and your chat adapter settings to Hubot, you'll have to launch the container with environment variables necessary for Hubot to run.

Hubot settings (change those to suit your environment):

  * ``HUBOT_ADAPTER=<adapter>``: your adapter (``slack``, ``hipchat``, ``irc``, ``yammer``, ``xmpp`` and ``flowdock`` are supported).
  * ``NODE_TLS_REJECT_UNAUTHORIZED=0``: set if you don't have a valid SSL certificate.
  * ``EXPRESS_PORT=8081``
  * ``HUBOT_LOG_LEVEL=debug``
  * ``HUBOT_NAME=hubot``
  * ``HUBOT_ALIAS=!``

StackStorm plugin for Hubot also requires you to set the following:

  * ``ST2_AUTH_USERNAME``: username Hubot should use to launch StackStorm actions.
  * ``ST2_AUTH_PASSWORD``: password for the user.
  * ``ST2_WEBUI_URL``: public URL of your StackStorm instance. Hubot needs it to give users links to execution details.
  * ``ST2_AUTH_URL``: StackStorm auth endpoint. Default is ``https://<hostname>:443/auth`` (don't use ``localhost`` because it will point to the Docker container).
  * ``ST2_API``: StackStorm API endpoint. Default is ``https://<hostname>:443/api`` (no ``localhost``, same as above).

Chat credentials are configured according to the adapter settings:

  * Slack: `hubot-slack <https://github.com/slackhq/hubot-slack>`_.
  * HipChat: `hubot-hipchat <https://github.com/hipchat/hubot-hipchat>`_.
  * Yammer: `hubot-yammer <https://github.com/athieriot/hubot-yammer>`_.
  * Flowdock: `hubot-flowdock <https://github.com/flowdock/hubot-flowdock>`_.
  * IRC: `hubot-irc <https://github.com/nandub/hubot-irc>`_.
  * XMPP: `hubot-xmpp <https://github.com/markstory/hubot-xmpp>`_.

An example of the final startup script for the container:

  .. code-block:: bash

    # Terminate and clear a running instance
    /usr/bin/docker rm stackstorm/hubot >/dev/null 2>&1

    # Launch with env variables
    /usr/bin/docker run                                          \
      --name hubot --net bridge --detach=true                    \
      -m 0b -p 8081:8080 --add-host aptwe:10.0.1.100             \
      -e ST2_WEBUI_URL=https://aptwe                             \
      -e ST2_AUTH_URL=https://aptwe:443/auth                     \
      -e ST2_API=https://aptwe:443/api                           \
      -e ST2_AUTH_USERNAME=chatops_bot                           \
      -e ST2_AUTH_PASSWORD=x6hgOCD4mWGe9LuOzsXZg0cu4OkCOPNr      \
      -e EXPRESS_PORT=8081                                       \
      -e NODE_TLS_REJECT_UNAUTHORIZED=0                          \
      -e HUBOT_ALIAS=!                                           \
      -e HUBOT_LOG_LEVEL=debug                                   \
      -e HUBOT_NAME=hubot                                        \
      -e HUBOT_ADAPTER=yammer                                    \
      -e HUBOT_YAMMER_ACCESS_TOKEN=2361395-RlgDFJSgVk3xsLFyOtjPA \
      -e HUBOT_YAMMER_GROUPS=Bots                                \
      stackstorm/hubot

Upgrade to Enterprise Edition
-----------------------------
Enterprise Edition is deployed as an addition on top of StackStorm. Detailed instructions coming up soon.
If you are an Enterprise usercustomer, call support@stackstorm.com and we provide the instructions.
