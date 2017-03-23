Ubuntu Trusty / Xenial
======================

If you're just looking for a "one-liner" installation, check the :doc:`top-level install guide </install/index>`. Otherwise, you
can use this guide for step-by step instructions for installing |st2| on a single Ubuntu/Debian 64 bit system as per
the :doc:`Reference deployment </install/overview>`.

.. note:: `Use the Source, Luke! <http://c2.com/cgi/wiki?UseTheSourceLuke>`_ We strive to keep the documentation current, but the best way to find out what really happens is to look at the code of the `installer script
  <https://github.com/StackStorm/st2-packages/blob/master/scripts/st2bootstrap-deb.sh>`_.

.. contents::

System Requirements
-------------------

Please check :doc:`supported versions and system requirements <system_requirements>`.

Minimal installation
--------------------

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. include:: __mongodb_note.rst

Install MongoDB, RabbitMQ, and PostgreSQL.

  .. code-block:: bash

    sudo apt-get update
    sudo apt-get install -y gnupg-curl
    sudo apt-get install -y curl

    # Add key and repo for the latest stable MongoDB (3.2)
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
    sudo sh -c "cat <<EOT > /etc/apt/sources.list.d/mongodb-org-3.2.list
    deb http://repo.mongodb.org/apt/ubuntu $(lsb_release -c | awk '{print $2}')/mongodb-org/3.2 multiverse
    EOT"
    sudo apt-get update

    sudo apt-get install -y mongodb-org
    sudo apt-get install -y rabbitmq-server
    sudo apt-get install -y postgresql

For Ubuntu ``Xenial`` you may need to enable and start MongoDB.

  .. code-block:: bash

    sudo systemctl enable mongod
    sudo systemctl start mongod

Setup repositories
~~~~~~~~~~~~~~~~~~~

The following script will detect your platform and architecture and setup the repo accordingly. It will also install the GPG key for repo signing.

  .. code-block:: bash

    curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.deb.sh | sudo bash

Install |st2| components
~~~~~~~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

      sudo apt-get install -y st2 st2mistral

If you are not running RabbitMQ, MongoDB or PostgreSQL on the same box, or have changed defaults,
please adjust the settings:

  * RabbitMQ connection at ``/etc/st2/st2.conf`` and ``/etc/mistral/mistral.conf``
  * MongoDB at ``/etc/st2/st2.conf``
  * PostgreSQL at ``/etc/mistral/mistral.conf``

Setup Datastore Encryption
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/datastore_crypto_key.rst

Setup Mistral Database
~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/setup_mistral_database.rst

.. _ref-config-ssh-sudo-deb:

Configure SSH and SUDO
~~~~~~~~~~~~~~~~~~~~~~

To run local and remote shell actions, |st2| uses a special system user (default ``stanley``).
For remote Linux actions, SSH is used. It is advised to configure identity file based SSH access on all remote hosts. We also recommend configuring SSH access to localhost for running examples and testing.

* Create |st2| system user, enable passwordless sudo, and set up ssh access to "localhost" so that SSH-based action can be tried and tested locally. You will need elevated privileges to do this.

.. include:: common/configure_ssh_and_sudo.rst

* Configure SSH access and enable passwordless sudo on the remote hosts which |st2| would control
  over SSH. Use the public key generated in the previous step; follow instructions at :ref:`config-configure-ssh`.
  To control Windows boxes, configure access for :doc:`Windows runners </install/config/windows_runners>`.

* Adjust configuration in ``/etc/st2/st2.conf`` if you are using a different user or path to the key:

.. include:: common/configure_system_user.rst

Start Services
~~~~~~~~~~~~~~

.. include:: common/start_services.rst


Verify
~~~~~~

.. include:: common/verify.rst

-----------------

At this point you have a minimal working installation, and can happily play with |st2|:
follow :doc:`/start` tutorial, :ref:`deploy examples <start-deploy-examples>`, explore and install packs from `StackStorm Exchange <https://exchange.stackstorm.org>`__.

But there is no joy without WebUI, no security without SSL termination, no fun without ChatOps, and no money without Brocade Workflow Composer. Read on, move on!

-----------------

.. _ref-config-auth-deb:

Configure Authentication
------------------------

The reference deployment uses File Based auth provider for simplicity. Refer to :doc:`/authentication`
to configure and use PAM or LDAP authentication backends.

.. include:: __pam_auth_backend_requirements.rst

To set up authentication with File Based provider:

* Create a user with a password:

  .. code-block:: bash

    # Install htpasswd utility if you don't have it
    sudo apt-get install -y apache2-utils
    # Create a user record in a password file.
    echo 'Ch@ngeMe' | sudo htpasswd -i /etc/st2/htpasswd st2admin

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
    export ST2_AUTH_TOKEN=$(st2 auth st2admin -p 'Ch@ngeMe' -t)

    # Check that it works
    st2 action list

Check out :doc:`/reference/cli` to learn convenient ways to authenticate via CLI.

.. _ref-install-webui-ssl-deb:

Install WebUI and setup SSL termination
---------------------------------------

`NGINX <http://nginx.org/>`_ is used to serve WebUI static files, redirect HTTP to HTTPS,
provide SSL termination for HTTPS, and reverse-proxy st2auth and st2api API endpoints.
To set it up, install `st2web` and `nginx`, generate certificates or place your existing
certificates under ``/etc/ssl/st2``, and configure nginx with |st2|'s supplied
:github_st2:`site config file st2.conf<conf/nginx/st2.conf>`.

|st2| depends on Nginx version >=1.7.5; since Ubuntu 14 has an older version
in the package repositories at the time of writing, you will have to include
the official Nginx repository into the source list:

  .. code-block:: bash

    # Add key and repo for the latest stable nginx
    sudo apt-key adv --fetch-keys http://nginx.org/keys/nginx_signing.key
    sudo sh -c "cat <<EOT > /etc/apt/sources.list.d/nginx.list
    deb http://nginx.org/packages/ubuntu/ $(lsb_release -c | awk '{print $2}') nginx
    EOT"
    sudo apt-get update

    # Install st2web and nginx
    # note nginx should be > 1.4.6
    sudo apt-get install -y st2web nginx

    # Generate self-signed certificate or place your existing certificate under /etc/ssl/st2
    sudo mkdir -p /etc/ssl/st2
    sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/st2/st2.key -out /etc/ssl/st2/st2.crt \
    -days XXX -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information \
    Technology/CN=$(hostname)"

    # Remove default site, if present
    sudo rm /etc/nginx/conf.d/default.conf
    # Copy and enable the supplied nginx config file
    sudo cp /usr/share/doc/st2/conf/nginx/st2.conf /etc/nginx/conf.d/

    sudo service nginx restart

If you modify ports, or url paths in the nginx configuration, make the corresponding changes in st2web
configuration at ``/opt/stackstorm/static/webui/config.js``.

Use your browser to connect to ``https://${ST2_HOSTNAME}`` and login to the WebUI.

If you are trying to access the API from outside the box and you've nginx setup according to
these instructions you can do so by hitting ``https://${EXTERNAL_IP}/api/v1/${REST_ENDPOINT}``.
For example:

  .. code-block:: bash

    curl -X GET -H  'Connection: keep-alive' -H  'User-Agent: manual/curl' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'X-Auth-Token: <YOUR_TOKEN>' https://1.2.3.4/api/v1/actions

You should be able to hit auth REST endpoints, if need be, by hitting ``https://${EXTERNAL_IP}/auth/v1/${AUTH_ENDPOINT}``.

You can see the actual REST endpoint for a resource in |st2|
by adding a ``--debug`` option to the CLI command for the appropriate resource.

For example, to see the endpoint for getting actions, invoke

  .. code-block:: bash

    st2 --debug action list

.. _ref-setup-chatops-deb:

Setup ChatOps
-------------

If you already run a Hubot instance, you only have to install the `hubot-stackstorm plugin <https://github.com/StackStorm/hubot-stackstorm>`_ and configure |st2| env variables, as described below. Otherwise, the easiest way to enable
:doc:`StackStorm ChatOps </chatops/index>` is to use the `st2chatops <https://github.com/stackstorm/st2chatops/>`_ package.

* Validate that ``chatops`` pack is installed, and a notification rule is enabled: ::

    # Ensure chatops pack is in place
    ls /opt/stackstorm/packs/chatops
    # Create notification rule if not yet enabled
    st2 rule get chatops.notify || st2 rule create /opt/stackstorm/packs/chatops/rules/notify_hubot.yaml

* `Add NodeJS v4 repository <https://nodejs.org/en/download/package-manager/>`_: ::

      curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -

* Install st2chatops package: ::

      sudo apt-get install -y st2chatops

* Review and edit ``/opt/stackstorm/chatops/st2chatops.env`` configuration file to point it to your
  |st2| installation and Chat Service you are using. By default ``st2api`` and ``st2auth``
  are expected to be on the same host. If that is not the case, please update ``ST2_API`` and
  ``ST2_AUTH_URL`` variables or just point to correct host with ``ST2_HOSTNAME`` variable.

  The example configuration uses Slack; go to Slack web admin interface, create a Bot, and copy the authentication token into ``HUBOT_SLACK_TOKEN``.
  If you are using a different Chat Service, set corresponding environment variables under
  `Chat service adapter settings`:
  `Slack <https://github.com/slackhq/hubot-slack>`_,
  `HipChat <https://github.com/hipchat/hubot-hipchat>`_,
  `Yammer <https://github.com/athieriot/hubot-yammer>`_,
  `Flowdock <https://github.com/flowdock/hubot-flowdock>`_,
  `IRC <https://github.com/nandub/hubot-irc>`_ ,
  `XMPP <https://github.com/markstory/hubot-xmpp>`_.

* Start the service: ::

      sudo service st2chatops start

* Reload st2 packs to make sure ``chatops.notify`` rule is registered: ::

      sudo st2ctl reload --register-all

* That's it! Go to your Chat room and begin ChatOpsing. Read more in the :doc:`/chatops/index` section.

A Note on Security
------------------

.. include:: common/security_notes.rst

Upgrade to Brocade Workflow Composer
------------------------------------

Brocade Workflow Composer is deployed as an addition on top of StackStorm. You will need an active
Brocade Workflow Composer subscription, and a license key to access Brocade Workflow Composer repositories.
To add your license key, replace ``${BWC_LICENSE_KEY}`` in the command below with the key you received when
registering or purchasing.

.. code-block:: bash

    # Set up Brocade Workflow Composer repository access
    curl -s https://${BWC_LICENSE_KEY}:@packagecloud.io/install/repositories/StackStorm/enterprise/script.deb.sh | sudo bash
    # Install Brocade Workflow Composer
    sudo apt-get install -y bwc-enterprise

To learn more about Brocade Workflow Composer, request a quote, or get an evaluation license go
to `stackstorm.com/product <https://stackstorm.com/product/#enterprise/>`_.
