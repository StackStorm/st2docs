Ubuntu / Debian
===============

This guide provides step-by step instructions on installing StackStorm on a single box per
:doc:`Reference deployment </install/overview>` on a Ubuntu/Debian. A script `st2bootstrap-deb.sh
<https://github.com/StackStorm/st2-packages/blob/master/scripts/st2bootstrap-deb.sh>`_, codifies the
instructions below.

.. warning :: Currently in BETA! Upgrades are being tested, but will be supprted only once packages graduate
    from BETA, likely from 1.4 onwards. At that point, package-based installation will be
    the preferred path to installing StackStorm.

    Please try, use and report bugs on
    `github.com/StackStorm/st2-packages <https://github.com/StackStorm/st2-packages/issues/new>`_.


.. contents::


Supported versions
------------------

We support Ubuntu 14.04, and test on `Ubuntu Server 14.04 LTS (HVM) Amazon AWS AMI <https://aws.amazon.com/marketplace/pp/B00JV9TBA6/ref=srh_res_product_title?ie=UTF8&sr=0-3&qid=1457037882965>`_
and `puppetlabs/ubuntu-14.04-64-nocm Vagrant box <https://atlas.hashicorp.com/puppetlabs/boxes/ubuntu-14.04-64-nocm>`_. Other Debian based distributions and versions will likely work with some tweaks, you are welcome to try and report success to the `community <https://stackstorm.com/community-signup>`_.

Sizing the server
-----------------
While the system can operate with less equipped servers, these are recommended
for the best experience while testing or deploying |st2|.

+--------------------------------------+-----------------------------------+
|            Testing                   |         Production                |
+======================================+===================================+
|  * Dual CPU system                   | * Quad core CPU system            |
|  * 1GB of RAM                        | * >16GB RAM                       |
|  * Recommended EC2: **t2.medium**    | * Recommended EC2: **m4.xlarge**  |
+--------------------------------------+-----------------------------------+

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

  .. code-block:: bash

    curl -s https://packagecloud.io/install/repositories/StackStorm/staging-stable/script.deb.sh | sudo bash


Install StackStorm components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

      sudo apt-get install -y st2 st2mistral


If you are not running RabbitMQ, MongoDB or PostgreSQL on the same box, or changed defaults,
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

.. _ref-config-ssh-sudo-deb:

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

.. _ref-config-auth-deb:

Configure Authentication
------------------------

Reference deployment uses File Based auth provider for simplicity. Refer to :doc:`/authentication` to configure and use PAM or LDAP autentication backends. To set up authentication with File Based provider:

* Create a user with a password:

  .. code-block:: bash

    # Install htpasswd utility if you don't have it
    sudo apt-get install -y apache2-utils
    # Create a user record in a password file.
    echo "Ch@ngeMe" | sudo htpasswd -i /etc/st2/htpasswd st2admin

* Enable and configure auth in ``/etc/st2/st2.conf``:

  .. sourcecode:: ini

    [auth]
    # ...
    enable = True
    backend = flat_file
    backend_kwargs = {"file_path": "/etc/st2/htpasswd"}
    # ...

* Restart the st2api service: ::

    sudo st2ctl restart-component st2api

* Authenticate, export the token for st2 CLI, and check that it works:

  .. code-block:: bash

    # Get an auth token and use in CLI or API
    st2 auth st2admin

    # A shortcut to authenticate and export the token
    export ST2_AUTH_TOKEN=$(st2 auth st2admin -p Ch@ngeMe -t)

    # Check that it works
    st2 action list

Check out :doc:`/cli` to learn convenient ways to authenticate via CLI.

.. _ref-install-webui-ssl-deb:

Install WebUI and setup SSL termination
---------------------------------------
`NGINX <http://nginx.org/>`_ is used to serve WebUI static files, redirect HTTP to HTTPS,
provide SSL termination for HTTPS, and reverse-proxy st2auth and st2api API endpoints.
To set it up, install `st2web` and `nginx`, generate certificates or place your existing
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

If you modify ports, or url paths in nginx configuration, make correspondent changes in st2web
configuration at ``/opt/stackstorm/static/webui/config.js``.

Use your browser to connect to ``https://${ST2_HOSTNAME}`` and login to the WebUI.


.. _ref-setup-chatops-deb:

Setup ChatOps
-------------

If you already run a Hubot instance, you only have to install the `hubot-stackstorm plugin <https://github.com/StackStorm/hubot-stackstorm>`_ and configure StackStorm env variables, as described below. Otherwise, the easiest way to enable
:doc:`StackStorm ChatOps </chatops/index>` is to use the `st2chatops <https://github.com/stackstorm/st2chatops/>`_ package.

* Validate that ``chatops`` pack is installed, and a notification rule is enabled: ::

      st2 rule list --pack=chatops

* `Install NodeJS v4 <https://nodejs.org/en/download/package-manager/>`_: ::

      curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
      sudo apt-get install -y nodejs

* Install st2chatops package: ::

      sudo apt-get install -y st2chatops

* Review and edit ``/opt/stackstorm/chatops/st2chatops.env`` configuration file to point it to your
  StackStorm installation and Chat Service you are using. By default ``st2api`` and ``st2auth``
  are expected to be on the same host. If it's not the case, please update ``ST2_API`` and
  ``ST2_AUTH_URL`` variables or just point to correct host with ``ST2_HOSTNAME`` variable. Use
  `ST2_WEBUI_URL` if an external address of your StackStorm host is different.

  The example configuration uses Slack; go to Slack web admin interface, create a Bot, and copy the authentication token into ``HUBOT_SLACK_TOKEN``.
  If you are using other Chat Service, set correspondent environment variables under
  `Chat service adapter settings`:
  `Slack <https://github.com/slackhq/hubot-slack>`_,
  `HipChat <https://github.com/hipchat/hubot-hipchat>`_,
  `Yammer <https://github.com/athieriot/hubot-yammer>`_,
  `Flowdock <https://github.com/flowdock/hubot-flowdock>`_,
  `IRC <https://github.com/nandub/hubot-irc>`_ ,
  `XMPP <https://github.com/markstory/hubot-xmpp>`_.

* Start the service: ::

      sudo service st2chatops start

* That's it! Go to your Chat room and begin ChatOpsing. Read on :doc:`/chatops/index` section.

Upgrade to Enterprise Edition
-----------------------------
Enterprise Edition is deployed as an addition on top of StackStorm Community. You will need an active
Enterprise subscription, and a license key to access StackStorm enterprise repositories.

.. code-block:: bash

    curl -s https://${ENTERPRISE_LICENSE_KEY}:@packagecloud.io/install/repositories/StackStorm/enterprise/script.deb.sh | sudo bash
    sudo apt-get install -y st2enterprise

To learn more about StackStorm Enterprise, request a quote, or get an evaluation license go
to `stackstorm.com/product <https://stackstorm.com/product/#enterprise/>`_.
