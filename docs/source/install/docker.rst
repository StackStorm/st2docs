Docker Image
============

Overview
--------

Likely the easiest and quickest method of setting up StackStorm is via:

  https://github.com/stackstorm/st2-docker

This page provides detailed instructions to ensure a successful installation.

For further details with examples, please refer to https://github.com/StackStorm/st2-docker/blob/master/README.md.

Host Requirements
-----------------

* Install the latest versions of Docker engine, and optionally ``docker-compose``. The
  installation instructions are located at https://www.docker.com/community-edition and
  https://docs.docker.com/compose/install respectively.

.. note::
  We require at least version 1.13.0 of Docker engine. If you choose to use ``docker-compose``,
  it must also be at least version 1.13.0.

* If you use Kubernetes, refer to
  https://github.com/StackStorm/st2-docker/blob/master/runtime/kubernetes-1ppc/README.md
  for more information.

Docker Images
-------------

The ``stackstorm/stackstorm`` image comes pre-installed with the ``st2``, ``st2web``,
``st2mistral`` and ``st2chatops`` packages.

If you install the image ``stackstorm/stackstorm:2.3.2``, then it comes pre-installed with the
StackStorm 2.3.2 release packages. Similarly, if you install the image
``stackstorm/stackstorm:2.2.1``, then it comes pre-installed with the StackStorm 2.2.1 release
packages. The ``stackstorm/stackstorm:latest`` image simply references the image with the highest
version number.

The mongo, rabbitmq, postgres and redis containers store their data on persistent storage.
Additionally, the stackstorm container persists the contents of ``/var/log``. If you do not wish to
persist this data, then remove the appropriate entries from ``docker-compose.yml``.

Usage
-----

Assuming Docker engine and ``docker-compose`` are properly installed, it is easy to run StackStorm.

First, clone the ``st2-docker`` repository and change directory to ``st2-docker``. Unless specified
otherwise, all subsequent commands assume they are run within ``st2-docker`` directory:

.. sourcecode:: bash

    git clone https://github.com/stackstorm/st2-docker
    cd st2-docker

Second, execute:

.. sourcecode:: bash

    make env

to create the environment files under ``conf/`` used by ``docker-compose``. You may want to change
the values of the variables as necessary, but the defaults should be okay if you are not using any
off-cluster services (e.g. mongo, redis, postgres, rabbitmq).

Below is the complete list of available options that can be used to customize your container.

+---------------------------+-------------------------------------------------------------------------------------------------------------+
|         Parameter         |       Description                                                                                           |
+===========================+=============================================================================================================+
| ``ST2_USER``              | StackStorm account username                                                                                 |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``ST2_PASSWORD``          | StackStorm account password                                                                                 |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``MONGO_HOST``            | MongoDB server hostname                                                                                     |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``MONGO_PORT``            | MongoDB server port (typically `27017`)                                                                     |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``MONGO_DB``              | *(Optional)* MongoDB dbname (will use `st2` if not specified)                                               |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``MONGO_USER``            | *(Optional)* MongoDB username (will connect without credentials if this and `MONGO_PASS` are not specified) |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``MONGO_PASS``            | *(Optional)* MongoDB password                                                                               |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``RABBITMQ_HOST``         | RabbitMQ server hostname                                                                                    |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``RABBITMQ_PORT``         | RabbitMQ server port (typically `5672`)                                                                     |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``RABBITMQ_DEFAULT_USER`` | RabbitMQ username                                                                                           |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``RABBITMQ_DEFAULT_PASS`` | RabbitMQ password                                                                                           |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``POSTGRES_HOST``         | PostgreSQL server hostname                                                                                  |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``POSTGRES_PORT``         | PostgreSQL server port (typically `5432`)                                                                   |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``POSTGRES_DB``           | PostgreSQL database                                                                                         |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``POSTGRES_USER``         | PostgreSQL username                                                                                         |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``POSTGRES_PASSWORD``     | PostgreSQL password                                                                                         |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``REDIS_HOST``            | Redis server hostname                                                                                       |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``REDIS_PORT``            | Redis server port                                                                                           |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``REDIS_PASSWORD``        | *(Optional)* Redis password                                                                                 |
+---------------------------+-------------------------------------------------------------------------------------------------------------+

Third, start the containers:

.. sourcecode:: bash

  docker-compose up -d

This will pull the required images from docker hub, and then start them.

When the time comes for you to stop the docker environment, run:

.. sourcecode:: bash

  docker-compose down

