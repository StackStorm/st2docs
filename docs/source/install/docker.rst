Docker
======

Like `Docker <https://www.docker.com>`_? And `Kubernetes <https://kubernetes.io>`_? So do we! 

One of the quickest ways to get StackStorm running is using Docker. This page will show you the basics
of how to use StackStorm with Docker. 

For more detailed information and examples, check out the `README
<https://github.com/StackStorm/st2-docker/blob/master/README.md>`_ at our `st2-docker GitHub repo
<https://github.com/StackStorm/st2-docker>`_.

Host Requirements
-----------------

* Install the latest versions of Docker engine, and optionally ``docker-compose``. Installation
  instructions are at https://www.docker.com/community-edition and
  https://docs.docker.com/compose/install.

  .. note::
    We require at least version 1.13.0 of Docker engine. If you choose to use ``docker-compose``
    it must also be at least version 1.13.0.

* If you use Kubernetes, check the :doc:`/install/k8s_ha`
  for more information.

Docker Images
-------------

The ``stackstorm/stackstorm`` image comes pre-installed with the ``st2``, ``st2web``,
``st2mistral`` and ``st2chatops`` packages.

.. note::

    This docker image only supports the open source version of StackStorm. Please contact
    `enterprise support <https://www.extremenetworks.com/support/contact/>`_ if you want more
    info on running Extreme Workflow Composer (EWC) in container.

We use version tags, so if you install the image ``stackstorm/stackstorm:2.3.2``, then it has the
StackStorm 2.3.2 release packages. Similarly, if you install image ``stackstorm/stackstorm:2.2.1``,
then it has the StackStorm 2.2.1 release packages. The ``stackstorm/stackstorm:latest`` image simply
references the image with the highest version number. Don't worry, this will still be a stable GA
release, not a nightly build.

The mongo, rabbitmq, postgres and redis containers store their data on persistent storage.
Additionally, the stackstorm container persists the contents of ``/var/log``. If you do not wish to
persist this data, then remove the appropriate entries from ``docker-compose.yml``.

Usage
-----

Assuming Docker engine and ``docker-compose`` are properly installed, getting started is easy.

First, clone the ``st2-docker`` repository and change directory to ``st2-docker``. Unless specified
otherwise, all subsequent commands assume they are run within ``st2-docker`` directory:

.. code-block:: bash

    git clone https://github.com/stackstorm/st2-docker
    cd st2-docker

Second, execute:

.. code-block:: bash

    make env

to create the environment files under ``conf/`` used by ``docker-compose``. Prior to doing so, you
may want to change some variables as necessary. The defaults should be okay if you are not using
any off-cluster services (e.g. mongo, redis, postgres, rabbitmq).

Below is the complete list of available options that can be used to customize your container:

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

.. code-block:: bash

  docker-compose up -d

This will pull the required images from Docker Hub, and then start them.

To stop the containers, run:

.. sourcecode:: bash

  docker-compose down

