RHEL 6 / CentOS 6
=================

This guide provides step-by step instructions for installing StackStorm on a single RHEL 6/CentOS 6 system per
the :doc:`Reference deployment </install/overview>`.

.. rubric:: TL;DR

That's OK! You're busy, we get it. How do you just get started? Get yourself a clean box, and run this command:

::

   curl -sSL https://stackstorm.com/packages/install.sh | bash -s -- --user=st2admin --password=<CHANGEME>

.. contents::

Supported platforms
-------------------

We support RedHat 6 / CentOS 6 and test on `Red Hat Enterprise Linux (RHEL) 6 (HVM) Amazon AWS AMI <https://aws.amazon.com/marketplace/pp/B00CFQWLS6/ref=srh_res_product_title?ie=UTF8&sr=0-8&qid=1457037733401>`_
and `puppetlabs/centos-6.6-64-nocm Vagrant box <https://atlas.hashicorp.com/puppetlabs/boxes/centos-6.6-64-nocm>`_. Other RPM based distributions and versions will likely work with some tweaks, you are welcome to try and report successes to the `community <https://stackstorm.com/community-signup>`_.


Sizing the server
-----------------
While the system can operate with lower specs, these are the recommendations
for the best experience while testing or deploying |st2|:

+--------------------------------------+-----------------------------------+
|            Testing                   |         Production                |
+======================================+===================================+
|  * Dual CPU system                   | * Quad core CPU system            |
|  * 1GB of RAM                        | * >16GB RAM                       |
|  * Recommended EC2: **t2.medium**    | * Recommended EC2: **m4.xlarge**  |
+--------------------------------------+-----------------------------------+

.. contents::


Minimal installation
--------------------

Install libffi-devel package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RHEL 6 may not ship with ``libffi-devel`` which is a dependency for |st2|.
If that is the case, set up `server-optional` repository, following instructions at https://access.redhat.com/solutions/265523.
Or, find a version of libffi-devel compatible with libffi on the box, and install this version of ``libffi-devel```. For example:

.. code :: bash

  [ec2-user@ip-172-30-0-79 ~]$ rpm -qa libffi
  libffi-3.0.5-3.2.el6.x86_64

  sudo yum localinstall -y ftp://fr2.rpmfind.net/linux/centos/6.7/os/x86_64/Packages/libffi-devel-3.0.5-3.2.el6.x86_64.rpm

Adjust SELinux policies
~~~~~~~~~~~~~~~~~~~~~~~

If your RHEL/CentOS box has SELinux in Enforcing mode, please follow these instructions to adjust SELinux
policies. This is needed for successful installation. If you are not happy with these policies,
you may want to tweak them according to your security practices.

* Check if SELinux is enforcing:

    .. code-block:: bash

        getenforce

* If previous command returns 'Enforcing', then run the following commands to adjust SELinux policies:

    .. code-block:: bash

        # SELINUX management tools, not available for some minimal installations
        sudo yum install -y policycoreutils-python

        # Allow network access for nginx
        sudo setsebool -P httpd_can_network_connect 1

    .. note ::

      If you see messages like "SELinux: Could not downgrade policy file", it means
      you are trying to adjust policy configurations when SELinux is disabled. You can
      ignore this error.

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. include:: __mongodb_32_note.rst

Install MongoDB, RabbitMQ, and PostgreSQL.

  .. code-block:: bash

    sudo yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

    # Add key and repo for the latest stable MongoDB (3.2)
    sudo rpm --import https://www.mongodb.org/static/pgp/server-3.2.asc
    sudo sh -c "cat <<EOT > /etc/yum.repos.d/mongodb-org-3.2.repo
    [mongodb-org-3.2]
    name=MongoDB Repository
    baseurl=https://repo.mongodb.org/yum/redhat/6Server/mongodb-org/3.2/x86_64/
    gpgcheck=1
    enabled=1
    gpgkey=https://www.mongodb.org/static/pgp/server-3.2.asc
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

    # Setup postgresql at a first time
    sudo service postgresql-9.4 initdb

    # Make localhost connections to use an MD5-encrypted password for authentication
    sudo sed -i "s/\(host.*all.*all.*127.0.0.1\/32.*\)ident/\1md5/" /var/lib/pgsql/9.4/data/pg_hba.conf
    sudo sed -i "s/\(host.*all.*all.*::1\/128.*\)ident/\1md5/" /var/lib/pgsql/9.4/data/pg_hba.conf

    # Start PostgreSQL service
    sudo service postgresql-9.4 start
    sudo chkconfig postgresql-9.4 on


Setup repositories
~~~~~~~~~~~~~~~~~~~

The following script will detect your platform and architecture and setup the repo accordingly. It'll also install the GPG key for repo signing.

  .. code-block:: bash

    curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.rpm.sh | sudo bash

Install StackStorm components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  .. code-block:: bash

      sudo yum install -y st2 st2mistral

If you are not running RabbitMQ, MongoDB or PostgreSQL on the same box, or changed defaults,
please adjust the settings:

  * RabbitMQ connection at ``/etc/st2/st2.conf`` and ``/etc/mistral/mistral.conf``
  * MongoDB at ``/etc/st2/st2.conf``
  * PostgreSQL at ``/etc/mistral/mistral.conf``

Setup Mistral Database
~~~~~~~~~~~~~~~~~~~~~~

.. include:: common/setup_mistral_database.rst

Configure SSH and SUDO
~~~~~~~~~~~~~~~~~~~~~~

To run local and remote shell actions, StackStorm uses a special system user (default ``stanley``).
For remote Linux actions, SSH is used. It is advised to configure identity file based SSH access on
all remote hosts. We also recommend configuring SSH access to localhost for running examples and
testing.

* Create StackStorm system user, enable passwordless sudo, and set up ssh access to "localhost" so
  that SSH-based action can be tried and tested locally. You will need elevated privileges to do this.

.. include:: common/configure_ssh_and_sudo.rst

* Configure SSH access and enable passwordless sudo on the remote hosts which StackStorm would control
  over SSH. Use the public key generated in the previous step; follow instructions at :ref:`config-configure-ssh`.
  To control Windows boxes, configure access for :doc:`Windows runners </config/windows_runners>`.

* Adjust configuration in ``/etc/st2/st2.conf`` if you are using a different user or path to the key:

.. include:: common/configure_system_user.rst

Start Services
~~~~~~~~~~~~~~

.. include:: common/start_services.rst

Verify
~~~~~~

.. include:: common/verify.rst

-----------------

At this point you have a minimal working installation, and can happily play with StackStorm: follow
:doc:`/start` tutorial, :ref:`deploy examples <start-deploy-examples>`, explore and install packs
from `st2contrib`_.

But there is no joy without WebUI, no security without SSL termination, no fun without ChatOps,
and no money without Enterprise edition. Read on, move on!

-----------------

Configure Authentication
------------------------

The reference deployment uses File Based auth provider for simplicity. Refer to :doc:`/authentication`
to configure and use PAM or LDAP authentication backends.

.. include:: __pam_auth_backend_requirements.rst

To set up authentication with File Based provider:

* Create a user with a password:

  .. code-block:: bash

    # Install htpasswd utility if you don't have it
    sudo yum -y install httpd-tools
    # Create a user record in a password file.
    sudo htpasswd -bs /etc/st2/htpasswd st2admin Ch@ngeMe

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
    st2 auth st2admin

    # A shortcut to authenticate and export the token
    export ST2_AUTH_TOKEN=$(st2 auth st2admin -p Ch@ngeMe -t)

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

StackStorm depends on Nginx version >=1.7.5; since RHEL6 has an older version
in the package repositories at the time of writing, you will have to include
the official Nginx repository into the list:

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

    # Generate self-signed certificate or place your existing certificate under /etc/ssl/st2
    sudo mkdir -p /etc/ssl/st2

    sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/st2/st2.key -out /etc/ssl/st2/st2.crt \
    -days 365 -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information \
    Technology/CN=$(hostname)"

    # Copy and enable StackStorm's supplied config file
    sudo cp /usr/share/doc/st2/conf/nginx/st2.conf /etc/nginx/conf.d/

    # Disable default_server configuration in existing /etc/nginx/nginx.conf
    sudo sed -i 's/default_server//g' /etc/nginx/conf.d/default.conf

    sudo service nginx restart
    sudo chkconfig nginx on

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


Setup ChatOps
-------------

If you already run Hubot instance, you only have to install the `hubot-stackstorm plugin <https://github.com/StackStorm/hubot-stackstorm>`_ and configure StackStorm env variables, as described below. Otherwise, the easiest way to enable
:doc:`StackStorm ChatOps </chatops/index>` is to use `st2chatops <https://github.com/stackstorm/st2chatops/>`_ package.

* Validate that ``chatops`` pack is installed, and a notification rule is enabled: ::

    # Ensure chatops pack is in place
    ls /opt/stackstorm/packs/chatops
    # Create notification rule if not yet enabled
    st2 rule get chatops.notify || st2 rule create /opt/stackstorm/packs/chatops/rules/notify_hubot.yaml

* `Install NodeJS v4 <https://nodejs.org/en/download/package-manager/>`_: ::

      curl -sL https://rpm.nodesource.com/setup_4.x | sudo -E bash -
      sudo yum install -y nodejs

* Install st2chatops package: ::

      sudo yum install -y st2chatops


* Review and edit ``/opt/stackstorm/chatops/st2chatops.env`` configuration file to point it to your
  |st2| installation and Chat Service you are using. By default ``st2api`` and ``st2auth``
  are expected to be on the same host. If that is not the case, please update ``ST2_API`` and
  ``ST2_AUTH_URL`` variables or just point to correct host with ``ST2_HOSTNAME`` variable. Use
  `ST2_WEBUI_URL` if an external address of your StackStorm host is different.

  The example configuration uses Slack. In case of Slack, go to Slack web admin interface,
  `create and configure a Bot <https://api.slack.com/bot-users>`_, invite a Bot to the rooms,
  and copy the authentication token into ``HUBOT_SLACK_TOKEN`` variable.

  If you are using a different Chat Service, make the appropriate bot configurations,
  and set corresponding environment variables under
  `Chat service adapter settings`:
  `Slack <https://github.com/slackhq/hubot-slack>`_,
  `HipChat <https://github.com/hipchat/hubot-hipchat>`_,
  `Yammer <https://github.com/athieriot/hubot-yammer>`_,
  `Flowdock <https://github.com/flowdock/hubot-flowdock>`_,
  `IRC <https://github.com/nandub/hubot-irc>`_ ,
  `XMPP <https://github.com/markstory/hubot-xmpp>`_.

* Start the service: ::

      sudo service st2chatops start

      # Starting st2chatops on boot
      sudo chkconfig st2chatops on

* Reload st2 packs to make sure ``chatops.notify`` rule is registered: ::

      sudo st2ctl reload --register-all

* That's it! Go to your Chat room and begin ChatOps-ing. Read more in the :doc:`/chatops/index` section.

Upgrade to Enterprise Edition
-----------------------------
Enterprise Edition is deployed as an addition on top of StackStorm Community. You will need an active
Enterprise subscription, and a license key to access StackStorm enterprise repositories.

.. code-block:: bash

    # Set up Enterprise repository access
    curl -s https://${ENTERPRISE_LICENSE_KEY}:@packagecloud.io/install/repositories/StackStorm/enterprise/script.rpm.sh | sudo bash
    # Install Enterprise editions
    sudo yum install -y st2enterprise

To learn more about StackStorm Enterprise, request a quote, or get an evaluation license go
to `stackstorm.com/product <https://stackstorm.com/product/#enterprise/>`_.
