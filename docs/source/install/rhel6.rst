RHEL 6/CentOS 6
===============

If you're just looking for a quick "one-liner" installation, check the :doc:`top-level install
guide </install/index>`. If you need a customised installation, use this guide for step-by step instructions for installing |st2| on a single RHEL 6/CentOS 6 64-bit system as per the
:doc:`Reference deployment </install/overview>`.

.. note:: 

  `Use the Source, Luke! <http://c2.com/cgi/wiki?UseTheSourceLuke>`_ We strive to keep the
  documentation current, but the best way to find out what really happens is to look at the code
  of the `installer script
  <https://github.com/StackStorm/st2-packages/blob/master/scripts/st2bootstrap-el6.sh>`_.

.. contents::

System Requirements
-------------------

Please check the :doc:`supported versions and system requirements <system_requirements>`.

Minimal Installation
--------------------

Install libffi-devel Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RHEL 6 may not ship with ``libffi-devel`` package, which is a dependency for |st2|. If that is the
case, set up the ``server-optional`` repository, following the instructions at
https://access.redhat.com/solutions/265523.
Or, find a version of ``libffi-devel`` compatible with the ``libffi`` version installed. For
example:

.. code :: bash

  [ec2-user@ip-172-30-0-79 ~]$ rpm -qa libffi
  libffi-3.0.5-3.4.el6.x86_64

  sudo yum localinstall -y ftp://fr2.rpmfind.net/linux/centos/6/os/x86_64/Packages/libffi-devel-3.0.5-3.4.el6.x86_64.rpm

Use a service such as http://rpmfind.net to find the required RPM.

Adjust SELinux Policies
~~~~~~~~~~~~~~~~~~~~~~~

If your system has SELinux in Enforcing mode, please follow these instructions to adjust SELinux
policies. This is needed for successful installation. If you are not happy with these policies,
you may want to tweak them according to your security practices.

* First check if SELinux is in Enforcing mode:

  .. code-block:: bash

    getenforce

* If previous command returns 'Enforcing', then run the following commands:

  .. code-block:: bash

    # SELINUX management tools, not available for some minimal installations
    sudo yum install -y policycoreutils-python

    # Allow network access for nginx
    sudo setsebool -P httpd_can_network_connect 1

.. note ::

  If you see messages like "SELinux: Could not downgrade policy file", it means you are trying to
  adjust policy configurations when SELinux is disabled. You can ignore this error.

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. include:: __mongodb_note.rst

Install MongoDB, RabbitMQ, and PostgreSQL.

.. code-block:: bash

  sudo yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

  # Add key and repo for the latest stable MongoDB (3.4)
  sudo rpm --import https://www.mongodb.org/static/pgp/server-3.4.asc
  sudo sh -c "cat <<EOT > /etc/yum.repos.d/mongodb-org-3.4.repo
  [mongodb-org-3.4]
  name=MongoDB Repository
  baseurl=https://repo.mongodb.org/yum/redhat/6Server/mongodb-org/3.4/x86_64/
  gpgcheck=1
  enabled=1
  gpgkey=https://www.mongodb.org/static/pgp/server-3.4.asc
  EOT"

  sudo yum -y install mongodb-org
  sudo yum -y install rabbitmq-server
  sudo service mongod start
  sudo service rabbitmq-server start
  sudo chkconfig mongod on
  sudo chkconfig rabbitmq-server on

  # Install and configure postgres 9.4. Based on the OS type, install the ``redhat`` one or ``centos`` one.
  # RHEL:
  if grep -q "Red Hat" /etc/redhat-release; then sudo yum -y localinstall http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-redhat94-9.4-2.noarch.rpm; fi

  # CentOS:
  if grep -q "CentOS" /etc/redhat-release; then sudo yum -y localinstall http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-centos94-9.4-2.noarch.rpm; fi

  sudo yum -y install postgresql94-server postgresql94-contrib postgresql94-devel

  # Initialize PostgreSQL
  sudo service postgresql-9.4 initdb

  # Make localhost connections to use an MD5-encrypted password for authentication
  sudo sed -i "s/\(host.*all.*all.*127.0.0.1\/32.*\)ident/\1md5/" /var/lib/pgsql/9.4/data/pg_hba.conf
  sudo sed -i "s/\(host.*all.*all.*::1\/128.*\)ident/\1md5/" /var/lib/pgsql/9.4/data/pg_hba.conf

  # Start PostgreSQL service
  sudo service postgresql-9.4 start
  sudo chkconfig postgresql-9.4 on


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

If you are not running RabbitMQ, MongoDB or PostgreSQL on the same system, or have changed the
defaults, please adjust these settings:

* RabbitMQ connection at ``/etc/st2/st2.conf`` and ``/etc/mistral/mistral.conf``
* MongoDB at ``/etc/st2/st2.conf``
* PostgreSQL at ``/etc/mistral/mistral.conf``

See the :doc:`Configuration documentation </install/config/config>` for more information.

Setup Datastore Encryption
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/datastore_crypto_key.rst

Setup Mistral Database
~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/setup_mistral_database.rst

Configure SSH and SUDO
~~~~~~~~~~~~~~~~~~~~~~

To run local and remote shell actions, |st2| uses a special system user (by default ``stanley``).
For remote Linux actions, SSH is used. We recommend configuring public key-based SSH access on all
remote hosts. We also recommend configuring SSH access to localhost for running examples and
testing.

* Create |st2| system user, enable passwordless sudo, and set up ssh access to "localhost" so
  that SSH-based actions can be tested locally. You will need elevated privileges to do this:

  .. include:: common/configure_ssh_and_sudo.rst

* Configure SSH access and enable passwordless sudo on the remote hosts which |st2| will be running
  remote actions on via SSH. Using the public key generated in the previous step, follow the
  instructions at :ref:`config-configure-ssh`. To control Windows boxes, configure access for
  :doc:`Windows runners </install/config/windows_runners>`.

* If you are using a different user, or path to their SSH key, you will need to change this
  section in ``/etc/st2/st2.conf``: 

  .. include:: common/configure_system_user.rst

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
    sudo htpasswd -bs /etc/st2/htpasswd st2admin 'Ch@ngeMe'

* Enable and configure authentication in ``/etc/st2/st2.conf``:

  .. sourcecode:: ini

    [auth]
    # ...
    enabled = True
    backend = flat_file
    backend_kwargs = {"file_path": "/etc/st2/htpasswd"}
    # ...

* Restart the st2api service:

  .. code-block:: bash

    sudo st2ctl restart-component st2api

* Authenticate, set the token environment variable, and check that it works:

  .. code-block:: bash

    # Get an auth token to use in CLI or API
    st2 auth st2admin

    # A shortcut to authenticate and export the token
    export ST2_AUTH_TOKEN=$(st2 auth st2admin -p 'Ch@ngeMe' -t)

    # Check that it works
    st2 action list

Check out the :doc:`/reference/cli` to learn other convenient ways to authenticate via CLI.

Install WebUI and Setup SSL Termination
---------------------------------------

`NGINX <http://nginx.org/>`_ is used to serve WebUI static files, redirect HTTP to HTTPS, provide
SSL termination, and reverse-proxy st2auth and st2api API endpoints. To set it up: install the
``st2web`` and ``nginx`` packages, generate certificates or place your existing certificates under
``/etc/ssl/st2``, and configure nginx with |st2|'s supplied :github_st2:`site config file st2.conf
<conf/nginx/st2.conf>`.

|st2| depends on Nginx version >=1.7.5. RHEL6 has an older version in the package repositories, so
you will need to add the official Nginx repository:

.. code-block:: bash

  # Add key and repo for the latest stable nginx
  sudo rpm --import http://nginx.org/keys/nginx_signing.key
  sudo sh -c "cat <<EOT > /etc/yum.repos.d/nginx.repo
  [nginx]
  name=nginx repo
  baseurl=http://nginx.org/packages/rhel/6/x86_64/
  gpgcheck=1
  enabled=1
  EOT"

  # Install st2web and nginx
  sudo yum -y install st2web nginx

  # Generate a self-signed certificate or place your existing certificate under /etc/ssl/st2
  sudo mkdir -p /etc/ssl/st2

  sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/st2/st2.key -out /etc/ssl/st2/st2.crt \
  -days 365 -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information \
  Technology/CN=$(hostname)"

  # Copy and enable the supplied nginx config file
  sudo cp /usr/share/doc/st2/conf/nginx/st2.conf /etc/nginx/conf.d/

  # Disable default_server configuration in existing /etc/nginx/nginx.conf
  sudo sed -i 's/default_server//g' /etc/nginx/conf.d/default.conf

  sudo service nginx restart
  sudo chkconfig nginx on

If you modify ports, or url paths in the nginx configuration, make the corresponding changes in
the st2web configuration at ``/opt/stackstorm/static/webui/config.js``.

Use your browser to connect to ``https://${ST2_HOSTNAME}`` and login to the WebUI.

If you are trying to access the API from outside the box and you have configured nginx according to
these instructions, use ``https://${EXTERNAL_IP}/api/v1/${REST_ENDPOINT}``.

For example:

.. code-block:: bash

  curl -X GET -H  'Connection: keep-alive' -H  'User-Agent: manual/curl' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'X-Auth-Token: <YOUR_TOKEN>' https://1.2.3.4/api/v1/actions

Similarly, you can connect to auth REST endpoints with ``https://${EXTERNAL_IP}/auth/v1/${AUTH_ENDPOINT}``.

You can see the actual REST endpoint for a resource in |st2|
by adding a ``--debug`` option to the CLI command for the appropriate resource.

For example, to see the endpoint for getting actions, invoke

.. code-block:: bash

  st2 --debug action list

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

* Review and edit the ``/opt/stackstorm/chatops/st2chatops.env`` configuration file to point it to
  your |st2| installation and the Chat Service you are using. At a minimum, you should generate an
  :ref:`API key <authentication-apikeys>` and set the ``ST2_API_KEY`` variable. By default
  ``st2api`` and ``st2auth`` are expected to be on the same host. If that is not the case, please
  update the ``ST2_API`` and ``ST2_AUTH_URL`` variables or just point to the correct host with
  ``ST2_HOSTNAME``.

  The example configuration uses Slack. To set this up, go to the Slack web admin interface, create
  a Bot, and copy the authentication token into ``HUBOT_SLACK_TOKEN``.

  If you are using a different Chat Service, set the corresponding environment variables under the
  ``Chat service adapter settings`` section in ``st2chatops.env``:
  `Slack <https://github.com/slackhq/hubot-slack>`_,
  `HipChat <https://github.com/hipchat/hubot-hipchat>`_,
  `Yammer <https://github.com/athieriot/hubot-yammer>`_,
  `Flowdock <https://github.com/flowdock/hubot-flowdock>`_,
  `IRC <https://github.com/nandub/hubot-irc>`_ ,
  `XMPP <https://github.com/markstory/hubot-xmpp>`_.

* Start the service:

  .. code-block:: bash

    sudo service st2chatops start

    # Ensure it will start on boot
    sudo chkconfig st2chatops on

* Reload st2 packs to make sure the ``chatops.notify`` rule is registered:

  .. code-block:: bash

    sudo st2ctl reload --register-all

* That's it! Go to your Chat room and begin ChatOps-ing. Read more in the :doc:`/chatops/index`
  section.

A Note on Security
------------------

.. include:: common/security_notes.rst

Upgrade to |bwc|
----------------

|bwc| is deployed as a set of additional packages on top of |st2|. You will need an active |bwc|
subscription, and a license key to access |bwc| repositories. To add your license key, replace
``${BWC_LICENSE_KEY}`` in the command below with the key you received when registering or
purchasing.

.. code-block:: bash

  # Set up Brocade Workflow Composer repository access
  curl -s https://${BWC_LICENSE_KEY}:@packagecloud.io/install/repositories/StackStorm/enterprise/script.rpm.sh | sudo bash
  # Install Brocade Workflow Composer
  sudo yum install -y bwc-enterprise

To learn more about |bwc|, request a quote, or get an evaluation license go to
`stackstorm.com/product <https://stackstorm.com/product/#enterprise/>`_.