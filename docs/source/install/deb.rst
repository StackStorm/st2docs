Ubuntu / Debian
=================

This guide provides step-by step instructions on installing StackStorm on a single box on a Ubuntu/Debian.
A script `st2bootstrap-deb.sh <https://github.com/StackStorm/st2-packages/blob/master/scripts/st2bootstrap-deb.sh>`_,
codifies the instructions below.

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

If you already run Hubot instance, you only have to install the ``hubot-stackstorm`` plugin and configure StackStorm env variables, as described below. Otherwise, the easiest way to enable StackStorm Chatops
:doc:`StackStorm ChatOps </chatops/index>` is to use Docker and run `stackstorm/hubot <https://hub.docker.com/r/stackstorm/hubot/>`_ docker image.

* Validate that ``chatops`` pack is installed, and a notification rule is enabled: ::

      ls /opt/stackstorm/packs/chatops && (st2 rule get chatops.notify || st2 rule create /opt/stackstorm/packs/chatops/rules/notify_hubot.yaml)

* Install docker: follow instructions on `Docker install <https://docs.docker.com/engine/installation/linux/ubuntulinux/>`_.

* Pull the StackStorm/hubot image: ::

      docker pull stackstorm/hubot

* Set a hostname or IP address that will be accessable form a docker container,
  as $ST2_HOSTNAME environment variable: ::

      export ST2_HOSTNAME={MY_STACKSTORM_HOST_NAME}

* Create ``st2hubot.env`` configuration file to keep all Chatops related settings in one place.
  Copy the example below; **edit to use your password**. The example uses Slack; go to Slack
  web admin interface, create a Bot, and copy the authentication token into ``HUBOT_SLACK_TOKEN``.
  Or set environment variables under `Chat service adapter settings`, for other Chat services:
  `Slack <https://github.com/slackhq/hubot-slack>`_,
  `HipChat <https://github.com/hipchat/hubot-hipchat>`_,
  `Yammer <https://github.com/athieriot/hubot-yammer>`_,
  `Flowdock <https://github.com/flowdock/hubot-flowdock>`_,
  `IRC <https://github.com/nandub/hubot-irc>`_ ,
  `XMPP <https://github.com/markstory/hubot-xmpp>`_.

  .. code-block :: bash

    if [ -z "$ST2_HOSTNAME" ]; then
       echo "Please set ST2_HOSTNAME to an externally accessable FQDN or IP.";
       return 1;
    fi

    #####################################################################
    # Hubot settings

    # set if you don’t have a valid SSL certificate.
    NODE_TLS_REJECT_UNAUTHORIZED=0
    # Hubot port - must be accessable from StackStorm
    EXPRESS_PORT=8081
    # Log level
    HUBOT_LOG_LEVEL=debug
    # Bot name
    HUBOT_NAME=yourbot
    #
    HUBOT_ALIAS=?

    ######################################################################
    # StackStorm settings

    # StackStorm api endpoint. (Don’t use `localhost` as it would point to the Docker container).
    ST2_API_URL=https://${ST2_HOSTNAME}/api
    # StackStorm auth endpoint. (Don’t use `localhost` as it would point to the Docker container).
    ST2_AUTH_URL=https://${ST2_HOSTNAME}/auth
    # ST2 credentials
    ST2_AUTH_USERNAME=test
    ST2_AUTH_PASSWORD=Ch@ngeMe
    # Public URL of StackStorm instance: used it to offer links to execution details in a chat.
    ST2_WEBUI_URL=https://${ST2_HOSTNAME}

    ######################################################################
    # Chat service adapter settings

    # For Slack, see https://github.com/slackhq/hubot-slack
    # For other adapters, see correspondent settings https://hubot.github.com/docs/adapters/

    # Hubot adapter plugin: slack, hipchat, irc, yammer, xmpp, flowdock
    HUBOT_ADAPTER=slack
    # Slack authentication token
    HUBOT_SLACK_TOKEN=xoxb-CHANGE-ME-PLEASE

* Use the script below to start the docker image. It is set up for Slack; for other Chats,
  edit it to pass the environment variables as required for your Chat service adapter.

  .. code-block :: bash

    #!/bin/bash
    # st2hubot-docker-run.sh - Conviniense script for running stackstorm-hubot docker container

    ST2_CONTAINER=stackstorm-hubot

    if [[ ! -z $(docker ps -a | grep $ST2_CONTAINER) ]];
    then
      echo "Terminating a previously running $ST2_CONTAINER instance..."
      /usr/bin/docker rm --force $ST2_CONTAINER
    fi

    # Export hubot-stackstorm settings
    . st2hubot.env || exit 1;

    # Launch with env variables
    echo "Running $ST2_CONTAINER ..."
    /usr/bin/docker run                                              \
      --name $ST2_CONTAINER --net bridge --detach=true               \
      -m 0b -p 8081:8080 --add-host $ST2_HOSTNAME:10.0.1.100         \
      -e ST2_WEBUI_URL=$ST2_WEBUI_URL                                \
      -e ST2_AUTH_URL=$ST2_AUTH_URL                                  \
      -e ST2_API=$ST2_API_URL                                        \
      -e ST2_AUTH_USERNAME=$ST2_AUTH_USERNAME                        \
      -e ST2_AUTH_PASSWORD=$ST2_AUTH_PASSWORD                        \
      -e EXPRESS_PORT=$EXPRESS_PORT                                  \
      -e NODE_TLS_REJECT_UNAUTHORIZED=$NODE_TLS_REJECT_UNAUTHORIZED  \
      -e HUBOT_ALIAS=$HUBOT_ALIAS                                    \
      -e HUBOT_LOG_LEVEL=$HUBOT_LOG_LEVEL                            \
      -e HUBOT_NAME=$HUBOT_NAME                                      \
      -e HUBOT_ADAPTER=$HUBOT_ADAPTER                                \
      -e HUBOT_SLACK_TOKEN=$HUBOT_SLACK_TOKEN                        \
      stackstorm/hubot


  Run the script, and ensure that hubot-stackstorm is running and there are no errors ::

      ./st2hubot-docker-run.sh
      docker inspect -f {{.State.Status}} stackstorm-hubot
      docker logs stackstorm-hubot

  To automatically start ``stackstorm-hubot``, use `restart policies
  <https://docs.docker.com/engine/reference/run/#restart-policies-restart>`_,
  or `integrate with a process manager <https://docs.docker.com/engine/admin/host_integration/>`_.
  An `init script <https://gist.github.com/emedvedev/3236a3bf104b2f0184f1>`_ is  available; replace the environment variables with your values and save it as ``/etc/init.d/docker-hubot``
  to start it at boot and control it with ``service docker-hubot``.

* Go to your Chat room and begin Chatopsing. Read on :doc:`/chatops/index` section.

Upgrade to Enterprise Edition
-----------------------------
Enterprise Edition is deployed as an addition on top of StackStorm. Detailed instructions coming up soon.
If you are an Enterprise customer, reach out to support@stackstorm.com and we provide the instructions.
