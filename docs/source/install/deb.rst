Ubuntu / Debian
===============

This guide provides step-by step instructions on installing StackStorm on a single box per
:doc:`Reference deployment </install/overview>` on a Ubuntu/Debian. A script `st2bootstrap-deb.sh
<https://github.com/StackStorm/st2-packages/blob/master/scripts/st2bootstrap-deb.sh>`_, codifies the
instructions below.

.. warning :: Currently BETA! Please try, use and report bugs on
   `github.com/StackStorm/st2-packages <https://github.com/StackStorm/st2-packages/issues/new>`_.
   Soon, package-based installation will be
   the preferred path to installing StackStorm.

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

The following script will detect your platform and architecture and setup the repo accordingly. It'll also install the GPG key for repo signing.
Currently we support ``Ubuntu Trusty``, ``Debian Wheezy`` and ``Debian Jessie``.

  .. code-block:: bash

    curl -s https://packagecloud.io/install/repositories/StackStorm/staging-stable/script.deb.sh | sudo bash


Install StackStorm components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

      sudo apt-get install -y st2 st2mistral


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
    sudo useradd stanley
    sudo mkdir -p /home/stanley/.ssh
    sudo chmod 0700 /home/stanley/.ssh

    # On StackStorm host, generate ssh keys
    sudo ssh-keygen -f /home/stanley/.ssh/stanley_rsa -P ""

    # Authorize key-base acces
    sudo sh -c 'cat /home/stanley/.ssh/stanley_rsa.pub >> /home/stanley/.ssh/authorized_keys'
    sudo chmod 0600 /home/stanley/.ssh/authorized_keys
    sudo chown -R stanley:stanley /home/stanley

    # Enable passwordless sudo
    sudo sh -c 'echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2'
    sudo chmod 0440 /etc/sudoers.d/st2

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

Reference deployment uses File Based auth provider for simplicity. Refer to :doc:`/authentication` to configure and use PAM or LDAP autentication backends. To set up authentication with File Based provider:

* Create a user with a password:

  .. code-block:: bash

    # Install htpasswd utility if you don't have it
    sudo apt-get install -y apache2-utils
    # Create a user record in a password file.
    echo "Ch@ngeMe" | sudo htpasswd -i /etc/st2/htpasswd test

* Enable and configure auth in ``/etc/st2/st2.conf``:

  .. sourcecode:: ini

    [auth]
    # ...
    enabled = True
    backend = flat_file
    backend_kwargs = {"file_path": "/etc/st2/htpasswd"}
    # ...

* Restart the st2api service: ::

    sudo st2ctl restart-component st2api

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
    sudo apt-get install -y st2web nginx

    # Generate self-signed certificate or place your existing certificate under /etc/ssl/st2
    sudo mkdir -p /etc/ssl/st2
    sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/st2/st2.key -out /etc/ssl/st2/st2.crt \
    -days XXX -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information \
    Technology/CN=$(hostname)"

    # Remove default site, if present
    sudo rm /etc/nginx/sites-enabled/default
    # Copy and enable StackStorm's supplied config file
    sudo cp /usr/share/doc/st2/conf/nginx/st2.conf /etc/nginx/sites-available/
    sudo ln -s /etc/nginx/sites-available/st2.conf /etc/nginx/sites-enabled/st2.conf

    sudo service nginx restart

If you modify ports, or url paths in nginx configuration, make correspondent chagnes in st2web
configuration at ``/opt/stackstorm/static/webui/config.js``.

Use your browser to connect to ``https://${ST2_HOSTNAME}`` and login to the WebUI.

Setup ChatOps
-------------

If you already run Hubot instance, you only have to install the ``hubot-stackstorm`` plugin and configure StackStorm env variables, as described below. Otherwise, the easiest way to enable
:doc:`StackStorm ChatOps </chatops/index>` is to use `st2chatops <https://github.com/stackstorm/st2chatops/>`_ package.

* Validate that ``chatops`` pack is installed, and a notification rule is enabled: ::

      st2 rule list --pack=chatops

* Install NodeJS v4: follow instructions on `NodeJS install <https://nodejs.org/en/download/package-manager/>`_.
  In general case, it would only require you to add NodeSource v4 repo and install ``nodejs`` package: ::

      curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
      sudo apt-get install -y nodejs

* Install st2chatops package: ::

      sudo apt-get install -y st2chatops

* Edit ``/opt/stackstorm/chatops/st2chatops.env`` configuration file to point it to your st2
  installation and chat service you are using.
  By default it expects ``st2api`` and ``st2auth`` to be installed on the same host. If it's not the case, please update ``ST2_API`` and ``ST2_AUTH_URL`` variables or just point to correct host with ``ST2_HOSTNAME`` variable.
  The example configuration uses Slack; go to Slack web admin interface, create a Bot, and copy the authentication token into ``HUBOT_SLACK_TOKEN``.
  Or set environment variables under `Chat service adapter settings`, for other Chat services:
  `Slack <https://github.com/slackhq/hubot-slack>`_,
  `HipChat <https://github.com/hipchat/hubot-hipchat>`_,
  `Yammer <https://github.com/athieriot/hubot-yammer>`_,
  `Flowdock <https://github.com/flowdock/hubot-flowdock>`_,
  `IRC <https://github.com/nandub/hubot-irc>`_ ,
  `XMPP <https://github.com/markstory/hubot-xmpp>`_.

* Start the service: ::

      sudo service st2chatops start

* Go to your Chat room and begin ChatOps-ing. Read on :doc:`/chatops/index` section.

Upgrade to Enterprise Edition
-----------------------------
Enterprise Edition is deployed as an addition on top of StackStorm. Detailed instructions coming up soon.
If you are an Enterprise customer, reach out to support@stackstorm.com and we walk you through.