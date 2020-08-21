Nginx and WSGI
--------------

Production |st2| installations use `nginx <http://nginx.org/en/>`_ for SSL termination, serving
Web UI static content, and running st2auth and st2api as WSGI apps via gunicorn/uwsgi. |st2| nginx
configurations can be found at ``/etc/nginx/sites-enabled/st2*.conf``.

``st2auth`` and ``st2api`` can also run using a built-in simple Python server. This is used for
development and strongly discouraged for any production. Be aware that some settings in
``/etc/st2.conf`` are only effective when running in development mode, and don't apply when
running under WSGI servers. Refer to the comments in
:github_st2:`st2.conf.sample <conf/st2.conf.sample>`.

Configure MongoDB
-----------------

|st2| requires a connection to MongoDB to operate.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section:

.. code-block:: ini

    [database]
    host = <MongoDB host>
    port = <MongoDB server port>
    db_name = <User define database name, usually st2>
    username = <username for db login>
    password = <password for db login>

The ``username`` and ``password`` properties are optional.

.. _ref-mongo-ha-config:

|st2| also supports `MongoDB replica sets
<https://docs.mongodb.com/v3.4/core/replication-introduction/>`_ using `MongoDB URI string
<https://docs.mongodb.com/v3.4/reference/connection-string/>`_.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section:

.. code-block:: ini

    [database]
    host = mongodb://<#MDB_NODE_1>,<#MDB_NODE_2>,<#MDB_NODE_3>/?replicaSet=<#MDB_REPLICA_SET_NAME>

* You can also add ports, usernames and passwords, etc to your connection string. See
  https://docs.mongodb.com/v3.4/reference/connection-string/

* To understand more about setting up a MongoDB replica set, see
  https://docs.mongodb.com/v3.4/tutorial/deploy-replica-set/

|st2| also supports SSL/TLS to encrypt MongoDB connections. A few extra properties need be added to
the configuration apart from the ones outlined above.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section:

.. code-block:: ini

    [database]
    ...
    ssl = <True or False>
    ssl_keyfile = <Path to key file>
    ssl_certfile = <Path to certificate>
    ssl_cert_reqs = <One of none, optional or required>
    ssl_ca_certs = <Path to certificate form mongod>
    ssl_match_hostname = <True or False>

* ``ssl`` - Enable or disable connection over TLS/SSL or not. Default is False.
* ``ssl_keyfile`` - Private keyfile used to identify the local connection against MongoDB. If
  specified ssl is assumed to be True.
* ``ssl_certfile`` - Certificate file used to identify the local connection. If specified ssl is
  assumed to be True.
* ``ssl_cert_reqs`` - Specifies whether a certificate is required from the other side of the
  connection, and whether it will be validated if provided.
* ``ssl_ca_certs`` - Certificates file containing a set of concatenated CA certificates, which are
  used to validate certificates passed from MongoDB.
* ``ssl_match_hostname`` - Enable or disable hostname matching. Not recommended to disable and
  defaults to True.

.. note::

  Only certain distributions of MongoDB support SSL/TLS:

  * MongoDB enterprise versions have SSL/TLS support.
  * Build MongoDB from source to enable SSL/TLS support. See
    https://github.com/mongodb/mongo/wiki/Build-Mongodb-From-Source for more information.

Configure RabbitMQ
------------------

|st2| uses RabbitMQ for messaging between its services.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section:

.. code-block:: ini

    [messaging]
    url = amqp://#RMQ_USER:#RMQ_PASSWD@#RMQ_HOST:#RMQ_PORT/#RMQ_VHOST

The ``#RMQ_VHOST`` property is optional and can be left blank.

|st2| also supports SSL/TLS to encrypt RabbitMQ connections. To enable SSL, you need to set
``messaging.ssl`` config option to ``True`` or pass ``?ssl=true`` query parameter at the end of
the connection URL string.

For example:

.. code-block:: ini

   [messaging]
   url = amqp://guest:guest@127.0.0.1:5671/
   ssl = True

or


.. code-block:: ini

   [messaging]
   url = amqp://guest:guest@127.0.0.1:5671/?ssl=true

In addition to encrypted connection to RabbitMQ, some other SSL related options which are
documented below are also supported:

.. code-block:: ini

    [messaging]
    ...
    ssl = <True or False>
    ssl_keyfile = <Path to key file>
    ssl_certfile = <Path to certificate>
    ssl_cert_reqs = <One of none, optional or required>
    ssl_ca_certs = <Path to CA certificate>
    login_method = <One of PLAIN, AMQPLAIN or EXTERNAL>

* ``ssl`` - Enable or disable connection over TLS/SSL or not. Default is False.
* ``ssl_keyfile`` - Private keyfile used to identify the local connection against RabbitMQ. If
  specified ssl is assumed to be True.
* ``ssl_certfile`` - Certificate file used to identify the local connection. If specified ssl is
  assumed to be True.
* ``ssl_cert_reqs`` - Specifies whether a certificate is required from the other side of the
  connection, and whether it will be validated if provided.
* ``ssl_ca_certs`` - Certificates file containing a set of concatenated CA certificates, which are
  used to validate certificates passed from RabbitMQ.
* ``login_method`` - Login method to use. Default is ``PLAIN``. Other possible
  options are ``AMQPLAIN`` and ``EXTERNAL``.

.. note::

   RabbitMQ doesn't expose an SSL / TLS listener by default and needs to be configured to enable
   TLS support. For more information, refer to the official documentation -
   `Enabling TLS Support in RabbitMQ <https://www.rabbitmq.com/ssl.html#enabling-tls>`_.

.. _ref-rabbitmq-cluster-config:

|st2| also supports `RabbitMQ cluster <https://www.rabbitmq.com/clustering.html>`_.

In :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>` include the following section:

.. code-block:: ini

    [messaging]
    cluster_urls = amqp://#RMQ_USER:#RMQ_PASSWD@#RMQ_NODE_1:#RMQ_PORT/#RMQ_VHOST,
                   amqp://#RMQ_USER:#RMQ_PASSWD@#RMQ_NODE_2:#RMQ_PORT/#RMQ_VHOST,
                   amqp://#RMQ_USER:#RMQ_PASSWD@#RMQ_NODE_3:#RMQ_PORT/#RMQ_VHOST

* To understand more about setting up a RabbitMQ cluster, see
  https://www.rabbitmq.com/clustering.html
* RabbitMQ HA guide - https://www.rabbitmq.com/ha.html


.. _config-configure-ssh:

Configure SSH
-------------

To run actions on remote hosts, |st2| uses SSH. We recommend using public key-based based SSH
access on all remote hosts.

The |st2| ssh user and path to SSH key are set in ``/etc/st2/st2.conf``. During installation,, the
one-line install script configures ssh on the local box for the user ``stanley``.

Follow these steps to configure a ``stanley`` user on remote sytems:

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

To verify, run this from your |st2| system:

.. code-block:: bash

    # ssh should not require a password since the key is already provided
    ssh -i /home/stanley/.ssh/stanley_rsa stanley@host.example.com

    # make sure that no password is required
    sudo su

SSH Troubleshooting
~~~~~~~~~~~~~~~~~~~

* Validate that passwordless SSH configuration works for the destination. Assuming the default
  user ``stanley``:

  .. code-block:: bash

    sudo ssh -i /home/stanley/.ssh/stanley_rsa -t stanley@host.example.com uname -a

Using SSH config
~~~~~~~~~~~~~~~~

|st2| allows loading an SSH config file local to the system user. This is a configurable option. To
enable, add the following to ``/etc/st2/st2.conf``

.. code-block:: ini

    [ssh_runner]
    use_ssh_config = True
    ...

SUDO Access
-----------

|st2|'s ``shell`` actions -  ``local-shell-cmd``, ``local-shell-script``, ``remote-shell-cmd``,
``remote-shell-script``- are performed by a special user. By default, this user is named
``stanley``. This is configurable via :github_st2:`st2.conf <conf/st2.prod.conf>`.

.. note:: the ``stanley`` user requires the following access:

  * Sudo access to all boxes on which the script action will run.
  * SETENV option needs to be set for all the commands. This way environment variables which are
    available to the local runner actions will also be available when the user executes local
    runner actions under a different user or with root privileges.
  * As some actions require sudo privileges, password-less sudo access to all boxes.

One way of setting up passwordless sudo is perform the below operation on each remote box:

.. code-block:: bash

    echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2

.. _config-logging:

Configure Logging
-----------------

By default, the logs can be found in ``/var/log/st2``.

* With the standard logging setup you will see files like ``st2*.log`` and ``st2*.audit.log`` in
  the log folder.

* Per-component logging configuration can be found in ``/etc/st2/logging.<component>.conf``.
  Those files use `Python logging configuration format
  <https://docs.python.org/2/library/logging.config.html#configuration-file-format>`_.
  Log file location and other settings can be modified in these configuration files, e.g. to
  change the output to use syslog instead.

* |st2| ships with example configuration files to show how to use syslog - these are at
  ``/etc/st2/syslog.<component>.conf``. To use them, edit ``/etc/st2/st2.conf``, and change the
  ``logging =`` lines to point to the syslog configuration file. You can also see more
  instructions and example configurations at :github_exchange:`exchange-misc/syslog
  <exchange-misc/tree/master/syslog>`.

* By default, log rotation is handled via logrotate. Default log rotation config
  (:github_st2:`logrotate.conf <conf/logrotate.conf>`) is included with all package-based
  installations. Note that ``handlers.RotatingFileHandler`` is used by default in
  ``/etc/st2/logging.*.conf``, but the ``maxBytes`` and ``backupCount`` args are not specified so
  no rotation is performed by default which then lets logrotate handle the rotation. If you want
  Python services instead of logrotate to handle the log rotation, update the logging configs as
  shown below:

  .. code-block:: ini

      [handler_fileHandler]
      class=handlers.RotatingFileHandler
      level=DEBUG
      formatter=verboseConsoleFormatter
      args=("logs/st2api.log", "a", 100000000, 5)

  In this case the log file will be rotated when it reaches 100000000 bytes (100MB) and a maximum
  of 5 old log files will be kept. For more information, see `RotatingFileHandler
  <https://docs.python.org/2/library/logging.handlers.html#rotatingfilehandler>`_ docs.

  Keep in mind that log level names need to be uppercase (e.g. ``DEBUG``, ``INFO``, etc.).

* Sensors run in their own process so it is recommended to not allow sensors to share the same
  ``RotatingFileHandler``. To configure a separate handler per sensor
  ``/etc/st2/logging.sensorcontainer.conf`` can be updated as follows, where ``MySensor`` is
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


* Check out LogStash configuration and Kibana dashboard for pretty logging and audit at
  :github_exchange:`exchange-misc/logstash <exchange-misc/tree/master/logstash>`

.. _config-configure-actionrunner-workers:

Configure The Number of Action Runner Workers
---------------------------------------------

In CentOS/RHEL the number of action workers defaults to 10. In Ubuntu the number of workers
defaults to the number of CPU cores the machine has. You may wish to increase the number of workers
in an HA setup or on system with plenty of resources.

The number of workers can be increased by modifying the environment variable ``WORKERS``. To persist
the number of ``st2actionrunner`` workers, create or edit the environment variable file for your
distribution and add the number of workers, eg. 25: ``WORKERS=25``. On RHEL/CentOS we use the
``/etc/sysconfig/st2actionrunner`` file and on Ubuntu use the ``/etc/default/st2actionrunner``
file to pass custom environment variables to the ``st2actionrunner`` service/unit:

.. code-block:: bash

    WORKERS=25

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

In order to manage secrets masking on a system-wide basis you can also modify ``/etc/st2/st2.conf``
and control secrets masking at 2 levels i.e. API and logs. Note that this feature only controls
external visibility of secrets and does not control how secrets are stored as well as managed by
|st2|.

* To mask secrets in API response. This is enabled on a per API basis and only available to admin
  users.

  .. sourcecode:: ini

    [api]
    ...
    mask_secrets = True


* To mask secrets in logs:

  .. sourcecode:: ini

    [log]
    ...
    mask_secrets = True

For more information and limitations on secrets masking please refer to
:doc:`../../reference/secrets_masking`.
