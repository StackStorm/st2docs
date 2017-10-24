RHEL 7/CentOS 7
===============

.. include:: common/intro.rst

.. contents:: Contents
   :local:

System Requirements
-------------------

Please check the :doc:`supported versions and system requirements <system_requirements>`.

Minimal Installation
--------------------

Adjust SELinux Policies
~~~~~~~~~~~~~~~~~~~~~~~

If your system has SELinux in Enforcing mode, please follow these instructions to adjust SELinux
policies. This is needed for successful installation. If you are not happy with these policies,
you may want to tweak them according to your security practices.

* First check if SELinux is in Enforcing mode:

  .. code-block:: bash

    getenforce

* If the previous command returns 'Enforcing', then run the following commands:

  .. code-block:: bash

    # SELINUX management tools, not available for some minimal installations
    sudo yum install -y policycoreutils-python

    # Allow network access for nginx
    sudo setsebool -P httpd_can_network_connect 1

    # Allow RabbitMQ to use port '25672', otherwise it will fail to start
    sudo semanage port --list | grep -q 25672 || sudo semanage port -a -t amqp_port_t -p tcp 25672

.. note::

  If you see messages like "SELinux: Could not downgrade policy file", it means you are trying to
  adjust policy configurations when SELinux is disabled. You can ignore this error.

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. include:: __mongodb_note.rst

Install MongoDB, RabbitMQ, and PostgreSQL:

.. code-block:: bash

  sudo yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

  # Add key and repo for the latest stable MongoDB (3.4)
  sudo rpm --import https://www.mongodb.org/static/pgp/server-3.4.asc
  sudo sh -c "cat <<EOT > /etc/yum.repos.d/mongodb-org-3.4.repo
  [mongodb-org-3.4]
  name=MongoDB Repository
  baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.4/x86_64/
  gpgcheck=1
  enabled=1
  gpgkey=https://www.mongodb.org/static/pgp/server-3.4.asc
  EOT"

  sudo yum -y install mongodb-org
  sudo yum -y install rabbitmq-server
  sudo systemctl start mongod rabbitmq-server
  sudo systemctl enable mongod rabbitmq-server

  # Install and configure postgres
  sudo yum -y install postgresql-server postgresql-contrib postgresql-devel

  # Initialize PostgreSQL
  sudo postgresql-setup initdb

  # Make localhost connections to use an MD5-encrypted password for authentication
  sudo sed -i "s/\(host.*all.*all.*127.0.0.1\/32.*\)ident/\1md5/" /var/lib/pgsql/data/pg_hba.conf
  sudo sed -i "s/\(host.*all.*all.*::1\/128.*\)ident/\1md5/" /var/lib/pgsql/data/pg_hba.conf

  # Start PostgreSQL service
  sudo systemctl start postgresql
  sudo systemctl enable postgresql

Setup Repositories
~~~~~~~~~~~~~~~~~~

The following script will detect your platform and architecture and setup the appropriate |st2|
repository. It will also add the the GPG key used for package signing.

.. code-block:: bash

  curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.rpm.sh | sudo bash

Install |st2| Components
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

  sudo yum install -y st2 st2mistral

.. include:: common/configure_components.rst

Setup Datastore Encryption
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/datastore_crypto_key.rst

Setup Mistral Database
~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/setup_mistral_database.rst

Configure SSH and SUDO
~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/configure_ssh_and_sudo.rst

Start Services
~~~~~~~~~~~~~~

.. include:: common/start_services.rst

Verify
~~~~~~

.. include:: common/verify.rst

Configure Authentication
------------------------

The reference deployment uses a file-based authentication provider for simplicity. Refer to
:doc:`/authentication` to configure and use PAM or LDAP authentication backends.

To set up authentication with file-based provider:

* Create a user with a password:

  .. code-block:: bash

    # Install htpasswd utility if you don't have it
    sudo yum -y install httpd-tools
    # Create a user record in a password file.
    echo 'Ch@ngeMe' | sudo htpasswd -i /etc/st2/htpasswd st2admin

.. include:: common/configure_authentication.rst

Install WebUI and Setup SSL Termination
---------------------------------------

`NGINX <http://nginx.org/>`_ is used to serve WebUI static files, redirect HTTP to HTTPS, provide
SSL termination, and reverse-proxy st2auth and st2api API endpoints. To set it up: install the
``st2web`` and ``nginx`` packages, generate certificates or place your existing certificates under
``/etc/ssl/st2``, and configure nginx with |st2|'s supplied :github_st2:`site config file st2.conf
<conf/nginx/st2.conf>`.

|st2| depends on Nginx version >=1.7.5. RHEL has an older version in the package repositories, so
you will need to add the official Nginx repository:

.. code-block:: bash

  # Add key and repo for the latest stable nginx
  sudo rpm --import http://nginx.org/keys/nginx_signing.key
  sudo sh -c "cat <<EOT > /etc/yum.repos.d/nginx.repo
  [nginx]
  name=nginx repo
  baseurl=http://nginx.org/packages/rhel/$releasever/x86_64/
  gpgcheck=1
  enabled=1
  EOT"

  # Install st2web and nginx
  sudo yum install -y st2web nginx

  # Generate a self-signed certificate or place your existing certificate under /etc/ssl/st2
  sudo mkdir -p /etc/ssl/st2
  sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/st2/st2.key -out /etc/ssl/st2/st2.crt \
  -days 365 -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information \
  Technology/CN=$(hostname)"

  # Copy and enable the supplied nginx config file
  sudo cp /usr/share/doc/st2/conf/nginx/st2.conf /etc/nginx/conf.d/

  # Disable default_server configuration in existing /etc/nginx/nginx.conf
  sudo sed -i 's/default_server//g' /etc/nginx/nginx.conf

  sudo systemctl restart nginx
  sudo systemctl enable nginx

If you modify ports, or url paths in the nginx configuration, make the corresponding changes in
the st2web configuration at ``/opt/stackstorm/static/webui/config.js``.

Use your browser to connect to ``https://${ST2_HOSTNAME}`` and login to the WebUI.

.. _ref-rhel7-firewall:

If you are unable to connect to the web browser, you may need to change the default firewall
settings. You can do this with these commands:

.. code-block:: bash

  firewall-cmd --zone=public --add-service=http --add-service=https
  firewall-cmd --zone=public --permanent --add-service=http --add-service=https

This will allow inbound HTTP (port 80) and HTTPS (port 443) traffic, and make those changes
survive reboot.

.. include:: common/api_access.rst

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

    curl -sL https://rpm.nodesource.com/setup_6.x | sudo -E bash -

* Install the ``st2chatops`` package:

  .. code-block:: bash

    sudo yum install -y st2chatops

.. include:: common/configure_chatops.rst

* Start the service:

  .. code-block:: bash

    sudo systemctl start st2chatops

    # Start st2chatops on boot
    sudo systemctl enable st2chatops

* Reload st2 packs to make sure the ``chatops.notify`` rule is registered:

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
  curl -s https://${BWC_LICENSE_KEY}:@packagecloud.io/install/repositories/StackStorm/enterprise/script.rpm.sh | sudo bash
  # Install Brocade Workflow Composer
  sudo yum install -y bwc-enterprise

.. rubric:: What's Next?

* Check out the :doc:`/start` Guide to build a simple automation.
* Get more actions, triggers, rules:


    * Install integration packs from `StackStorm Exchange <https://exchange.stackstorm.org>`__  - follow the :doc:`/packs` guide.
    * :ref:`Convert your scripts into StackStorm actions. <ref-actions-converting-scripts>`
    * Learn how to :ref:`write custom actions <ref-actions-writing-custom>`.

* Use workflows to stitch actions into higher level automations - :doc:`/workflows`.
* Check out `tutorials on stackstorm.com <https://stackstorm.com/category/tutorials/>`__
