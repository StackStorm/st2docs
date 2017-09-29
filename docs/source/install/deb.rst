Ubuntu Trusty/Xenial
====================

.. include:: common/intro.rst

.. contents::

System Requirements
-------------------

Please check the :doc:`supported versions and system requirements <system_requirements>`.

Minimal Installation
--------------------

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. include:: __mongodb_note.rst

Install MongoDB, RabbitMQ, and PostgreSQL:

.. code-block:: bash

  sudo apt-get update
  sudo apt-get install -y gnupg-curl
  sudo apt-get install -y curl

  # Add key and repo for the latest stable MongoDB (3.4)
  wget -qO - https://www.mongodb.org/static/pgp/server-3.4.asc | sudo apt-key add -
  sudo sh -c "cat <<EOT > /etc/apt/sources.list.d/mongodb-org-3.4.list
  deb http://repo.mongodb.org/apt/ubuntu $(lsb_release -c | awk '{print $2}')/mongodb-org/3.4 multiverse
  EOT"
  sudo apt-get update

  sudo apt-get install -y mongodb-org
  sudo apt-get install -y rabbitmq-server
  sudo apt-get install -y postgresql

For Ubuntu ``Xenial`` you may need to enable and start MongoDB.

.. code-block:: bash

  sudo systemctl enable mongod
  sudo systemctl start mongod

Setup Repositories
~~~~~~~~~~~~~~~~~~

The following script will detect your platform and architecture and setup the appropriate |st2|
repository. It will also add the the GPG key used for package signing.

.. code-block:: bash

  curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.deb.sh | sudo bash

Install |st2| Components
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

  sudo apt-get install -y st2 st2mistral

.. include:: common/configure_components.rst

Setup Datastore Encryption
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/datastore_crypto_key.rst

Setup Mistral Database
~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/setup_mistral_database.rst

.. _ref-config-ssh-sudo-deb:

Configure SSH and SUDO
~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/configure_ssh_and_sudo.rst

Start Services
~~~~~~~~~~~~~~

.. include:: common/start_services.rst

Verify
~~~~~~

.. include:: common/verify.rst

.. _ref-config-auth-deb:

Configure Authentication
------------------------

The reference deployment uses a file-based authentication provider for simplicity. Refer to
:doc:`/authentication` to configure and use PAM or LDAP authentication backends.

To set up authentication with file-based provider:

* Create a user with a password:

  .. code-block:: bash

    # Install htpasswd utility if you don't have it
    sudo apt-get install -y apache2-utils
    # Create a user record in a password file.
    echo 'Ch@ngeMe' | sudo htpasswd -i /etc/st2/htpasswd st2admin

.. include:: common/configure_authentication.rst

.. _ref-install-webui-ssl-deb:

Install WebUI and Setup SSL Termination
---------------------------------------

`NGINX <http://nginx.org/>`_ is used to serve WebUI static files, redirect HTTP to HTTPS, provide
SSL termination, and reverse-proxy st2auth and st2api API endpoints. To set it up: install the
``st2web`` and ``nginx`` packages, generate certificates or place your existing certificates under
``/etc/ssl/st2``, and configure nginx with |st2|'s supplied :github_st2:`site config file st2.conf
<conf/nginx/st2.conf>`.

|st2| depends on Nginx version >=1.7.5. Ubuntu has an older version in the package repositories, so
you will need to add the official Nginx repository:


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

If you modify ports, or url paths in the nginx configuration, make the corresponding changes in
the st2web configuration at ``/opt/stackstorm/static/webui/config.js``.

Use your browser to connect to ``https://${ST2_HOSTNAME}`` and login to the WebUI.

.. include:: common/api_access.rst

.. _ref-setup-chatops-deb:

Setup ChatOps
-------------

If you already run a Hubot instance, you can install the `hubot-stackstorm plugin
<https://github.com/StackStorm/hubot-stackstorm>`_ and configure |st2| environment variables, as
described below. Otherwise, the easiest way to enable :doc:`StackStorm ChatOps </chatops/index>`
is to use the `st2chatops <https://github.com/stackstorm/st2chatops/>`_ package.

* Validate that the ``chatops`` pack is installed, and a notification rule is enabled:

  .. code-block:: bash

    # Ensure chatops pack is in place
    ls /opt/stackstorm/packs/chatops
    # Create notification rule if not yet enabled
    st2 rule get chatops.notify || st2 rule create /opt/stackstorm/packs/chatops/rules/notify_hubot.yaml

* Add `NodeJS v6 repository <https://nodejs.org/en/download/package-manager/>`_:

  .. code-block:: bash

    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -

* Install the ``st2chatops`` package:

  .. code-block:: bash

    sudo apt-get install -y st2chatops

.. include:: common/configure_chatops.rst

* Start the service:

  .. code-block:: bash

    sudo service st2chatops start

* Reload st2 packs to make sure ``chatops.notify`` rule is registered:

  .. code-block:: bash

    sudo st2ctl reload --register-all

* That's it! Go to your Chat room and begin ChatOps-ing. Read more in the :doc:`/chatops/index` section.

A Note on Security
------------------

.. include:: common/security_notes.rst

Upgrade to |bwc|
----------------

.. include:: common/bwc_intro.rst

.. code-block:: bash

  # Set up Brocade Workflow Composer repository access
  curl -s https://${BWC_LICENSE_KEY}:@packagecloud.io/install/repositories/StackStorm/enterprise/script.deb.sh | sudo bash
  # Install Brocade Workflow Composer
  sudo apt-get install -y bwc-enterprise