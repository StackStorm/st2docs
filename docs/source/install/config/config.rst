Nginx and WSGI
--------------

Production |st2| installations use `nginx <http://nginx.org/en/>`_ for SSL termination,
serving static content of WebUI,
and running st2auth and st2api as WSGI apps via gunicorn/uwsgi. |st2| nginx configurations
can be found at ``/etc/nginx/sites-enabled/st2*.conf``.

``st2auth`` and ``st2api`` can also run using a built-in simple Python server. This is used for development and strongly discouraged for any production. Be aware that some settings in /etc/st2.conf are only effective when running in development mode, and don't apply when running under WSGI servers. Refer to the comments in
:github_st2:`st2.conf.sample <conf/st2.conf.sample>`.

Configure MongoDB
-----------------

|st2| requires a connection to MongoDB to operate.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section :

.. code-block:: bash

    [database]
    host = <MongoDB host>
    port = <MongoDB server port>
    db_name = <User define database name, usually st2>
    username = <username for db login>
    password = <password for db login>

The ``username`` and ``password`` properties are optional.

|st2| also supports `MongoDB replica sets <https://docs.mongodb.com/v2.4/core/replication-introduction/>`_
using `MongoDB URI string <https://docs.mongodb.com/v2.4/reference/connection-string/>`_.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section :

.. code-block:: bash

    [database]
    host = mongodb://<#MDB_NODE_1>,<#MDB_NODE_2>,<#MDB_NODE_3>/?replicaSet=<#MDB_REPLICA_SET_NAME>

* You can also add ports, usernames and passwords, etc to your connection string - https://docs.mongodb.com/v2.4/reference/connection-string/

* To understand more about setting up a MongoDB replica set - https://docs.mongodb.com/v2.4/tutorial/deploy-replica-set/

|st2| also supports SSL/TLS to encrypt connections. A few extra properties need be added to
the configuration apart from the ones outlined above.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section :

.. code-block:: bash

    [database]
    ...
    ssl = <True or False>
    ssl_keyfile = <Path to key file>
    ssl_certfile = <Path to certificate>
    ssl_cert_reqs = <One of none, optional or required>
    ssl_ca_certs = <Path to certificate form mongod>
    ssl_match_hostname = <True or False>

* ``ssl`` - Enable or disable connection over TLS/SSL or not. Default is False.
* ``ssl_keyfile`` - Private keyfile used to identify the local connection against MongoDB. If specified ssl is assumed to be True.
* ``ssl_certfile`` - Certificate file used to identify the local connection. If specified ssl is assumed to be True.
* ``ssl_cert_reqs`` - Specifies whether a certificate is required from the other side of the connection, and whether it will be validated if provided.
* ``ssl_ca_certs`` - Certificates file containing a set of concatenated CA certificates, which are used to validate certificates passed from MongoDB.
* ``ssl_match_hostname`` - Enable or disable hostname matching. Not recommended to disable and defaults to True.

.. note:: Only certain distributions of MongoDB support SSL/TLS.

    * MonogoDB enterprise vesions have SSL/TLS support.
    * Build MongoDB from source to enable SSL/TLS support. See https://github.com/mongodb/mongo/wiki/Build-Mongodb-From-Source for more information.

Configure RabbitMQ
------------------

|st2| uses RabbitMQ for messaging between its services.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section:

.. code-block:: bash

    [messaging]
    url = <amqp://#RMQ_USER:#RMQ_PASSWD@#RMQ_HOST:#RMQ_PORT/#RMQ_VHOST>

The ``#RMQ_VHOST`` property is optional and can be left blank.

|st2| also supports `RabbitMQ cluster <https://www.rabbitmq.com/clustering.html>`_.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section :

.. code-block:: bash

    [messaging]
    cluster_urls = <amqp://#RMQ_USER:#RMQ_PASSWD@#RMQ_NODE_1:#RMQ_PORT/#RMQ_VHOST>,
                   <amqp://#RMQ_USER:#RMQ_PASSWD@#RMQ_NODE_2:#RMQ_PORT/#RMQ_VHOST>,
                   <amqp://#RMQ_USER:#RMQ_PASSWD@#RMQ_NODE_3:#RMQ_PORT/#RMQ_VHOST>


* To understand more about setting up a RabbitMQ cluster - https://www.rabbitmq.com/clustering.html
* RabbitMQ HA guide - https://www.rabbitmq.com/ha.html


.. _config-configure-ssh:

Configure SSH
-------------

To run actions on remote hosts, |st2| uses SSH. It is advised to configure identity file based SSH access on all remote hosts.

The |st2| ssh user and path to SSH key are set in ``/etc/st2/st2.conf``. During installation, ``st2_deploy.sh`` script configures ssh on the local box for a user `stanley`.

Follow these steps on a remote box to setup `stanley` user on remote boxes.

.. code-block:: bash

    useradd stanley
    mkdir -p /home/stanley/.ssh
    chmod 0700 /home/stanley/.ssh

    # generate ssh keys and copy over public key to remote box.
    ssh-keygen -f /home/stanley/.ssh/stanley_rsa -P ""
    cp ${KEY_LOCATION}/stanley_rsa.pub /home/stanley/.ssh/stanley_rsa.pub

    # authorize key-based access.
    cat /home/stanley/.ssh/stanley_rsa.pub >> /home/stanley/.ssh/authorized_keys
    chmod 0600 /home/stanley/.ssh/authorized_keys
    chown -R stanley:stanley /home/stanley
    echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2

    # ensure requiretty is not set to default in the /etc/sudoers file.
    sudo sed -i -r "s/^Defaults\s+\+requiretty/# Defaults +requiretty/g" /etc/sudoers

To verify do the following from the |st2| box

.. code-block:: bash

    # ssh should not require a password since the key is already provided
    ssh -i /home/stanley/.ssh/stanley_rsa stanely@host.example.com

    # make sure that no password is required
    sudo su

SSH Troubleshooting
~~~~~~~~~~~~~~~~~~~

* Validate that passwordless SSH configuration works fine for the destination. Assuming default user `stanley`:

    .. code-block:: bash

        sudo ssh -i /home/stanley/.ssh/stanley_rsa -t stanley@host.example.com uname -a

Using SSH config
~~~~~~~~~~~~~~~~

|st2| allows loading of the SSH config file local to the system user. This is a configurable option. To
enable, add the following to ``/etc/st2/st2.conf``

.. code-block:: bash

    [ssh_runner]
    use_ssh_config = True
    ...

SUDO Access
-----------

|st2|'s ``shell`` actions -  ``local-shell-cmd``, ``local-shell-script``, ``remote-shell-cmd``, ``remote-shell-script``- are performed by a special user. By default, this user is named ``stanley``. This is configurable via :github_st2:`st2.conf <conf/st2.prod.conf>`.

.. note:: `stanley` user requires the following access:

    * Sudo access to all boxes on which script action will run.
    * SETENV option needs to be set for all the commands. This way environment variables which are
      available to the local runner actions will also be available when user executes local runner
      action under a different user or with root privileges.
    * As some actions require sudo privileges password-less sudo access to all boxes.

One way of setting up passwordless sudo is perform the below operation on each remote box:

.. code-block:: bash

    echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2

.. _config-logging:

Configure Logging
-----------------

By default, the logs can be found in ``/var/log/st2``.

* With the standard logging setup you will see files like ``st2*.log`` and
  ``st2*.audit.log`` in the log folder.

* Per component logging configuration can be found in ``/etc/st2/logging.<component>.conf``.
  Those files use `Python logging configuration format <https://docs.python.org/2/library/logging.config.html#configuration-file-format>`_.
  Log file location and other settings can be modified in these configuration files, e.g. to
  change the output to use syslog instead.

* |st2| ships with example configuration files to show how to use syslog - these are at
  ``/etc/st2/syslog.<component>.conf``. To use them, edit ``/etc/st2/st2.conf``, and change
  the ``logging =`` lines to point to the syslog configuration file. You can also see more
  instructions and example configurations at :github_exchange:`exchange-misc/syslog <exchange-misc/tree/master/syslog>`.

* By default, log rotation is handled via logrotate. Default log rotation config
  (:github_st2:`logrotate.conf <conf/logrotate.conf>`) is included with all the
  package based installations. Note that ``handlers.RotatingFileHandler`` is used by
  default in ``/etc/st2*/logging.conf``, but the ``maxBytes`` and ``backupCount`` args are not
  specified so no rotation is performed by default which then lets logrotate handle the rotation.
  If you want Python services instead of logrotate to handle the log rotation, update the
  logging configs as shown below:

  .. code-block:: ini

      [handler_fileHandler]
      class=handlers.RotatingFileHandler
      level=DEBUG
      formatter=verboseConsoleFormatter
      args=("logs/st2api.log", "a", 100000000, 5)

  In this case the log file will be rotated when it reaches 100000000 bytes (100
  MB) and a maximum of 5 old log files will be kept. For more information, see
  `RotatingFileHandler <https://docs.python.org/2/library/logging.handlers.html#rotatingfilehandler>`_
  docs.

* Sensors run in their own process so it is recommended to not allow sensors to share the same
  ``RotatingFileHandler``. To configure a separate handler per sensor
  ``/etc/st2reactor/logging.sensorcontainer.conf`` can be updated as follows, where ``MySensor`` is
  the sensor in the ``mypack`` pack that will have its own log file:

  .. code-block:: ini

      [loggers]
      keys=root,MySensor

      [handlers]
      keys=consoleHandler, fileHandler, auditHandler, MySensorFileHandler, MySensorAuditHandler

      [logger_MySensor]
      level=INFO
      handlers=consoleHandler, MySensorFileHandler, MySensorAuditHandler
      propagate=0
      qualname=st2.SensorWrapper.mypack.MySensor

      [handler_MySensorFileHandler]
      class=handlers.RotatingFileHandler
      level=INFO
      formatter=verboseConsoleFormatter
      args=("logs/mysensor.log",)

      [handler_vSphereEventSensorAuditHandler]
      class=handlers.RotatingFileHandler
      level=AUDIT
      formatter=gelfFormatter
      args=("logs/mysensor.audit.log",)

* Check out LogStash configuration and Kibana dashboard for pretty logging and
  audit at :github_exchange:`exchange-misc/logstash <exchange-misc/tree/master/logstash>`.


Configure Mistral
-----------------
There are a number of configurable options available under the mistral section in ``/etc/st2/st2.conf``. If the mistral section is not provided, default values will be used. By default, all Keystone related options are unset and |st2| will not pass any credentials for authentication to Mistral. Please refer to OpenStack and Mistral documentation for Keystone setup.

+-----------------------+--------------------------------------------------------+
| options               | description                                            |
+=======================+========================================================+
| v2_base_url           | Mistral API v2 root endpoint                           |
+-----------------------+--------------------------------------------------------+
| retry_exp_msec        | Multiplier for the exponential backoff.                |
+-----------------------+--------------------------------------------------------+
| retry_exp_max_msec    | Max time for each set of backoff.                      |
+-----------------------+--------------------------------------------------------+
| retry_stop_max_msec   | Max time to stop retrying.                             |
+-----------------------+--------------------------------------------------------+
| keystone_username     | Username for authentication with OpenStack Keystone.   |
+-----------------------+--------------------------------------------------------+
| keystone_password     | Password for authentication with OpenStack Keystone.   |
+-----------------------+--------------------------------------------------------+
| keystone_project_name | OpenStack project scope.                               |
+-----------------------+--------------------------------------------------------+
| keystone_auth_url     | v3 Auth URL for OpenStack Keystone.                    |
+-----------------------+--------------------------------------------------------+

::

    # Example with basic options. The v2_base_url is set to http://workflow.example.com:8989/v2.
    # On connection error, the following configuration sets up the action runner to retry
    # connecting to Mistral for up to 10 minutes. The retries is setup to be exponential for
    # 5 minutes. So in this case, there will be two sets of exponential retries during
    # the 10 minutes.

    [mistral]
    v2_base_url = http://workflow.example.com:8989/v2
    retry_exp_msec = 1000
    retry_exp_max_msec = 300000
    retry_stop_max_msec = 600000

::

    # Example with auth options.

    [mistral]
    v2_base_url = http://workflow.example.com:8989/v2
    retry_exp_msec = 1000
    retry_exp_max_msec = 300000
    retry_stop_max_msec = 600000
    keystone_username = mistral
    keystone_password = pass123
    keystone_project_name = default
    keystone_auht_url = http://identity.example.com:5000/v3


Authentication
--------------

Please refer to :doc:`/authentication` to learn details of authentication, integrations with
various identity providers, and managing API tokens.

Configure ChatOps
-----------------

|st2| brings native two-way ChatOps support. To learn more about ChatOps, and how to configure it manually, please refer to :ref:`Configuration section under ChatOps <chatops-configuration>`.

.. _mask-secrets:

Configure secrets masking
-------------------------
In order to manage secrets masking on a system-wide basis you can also modify ``/etc/st2/st2.conf`` and
control secrets masking at 2 levels i.e. API and logs. Note that this feature only controls external
visibility of secrets and does not control how secrets are stored as well as managed by |st2|.

* To mask secrets in API response. This is enabled on a per API basis and only available to admin users.

.. sourcecode:: bash

    [api]
    ...
    mask_secrets=True


* To mask secrets in logs

.. sourcecode:: bash

    [logging]
    ...
    mask_secrets=True
