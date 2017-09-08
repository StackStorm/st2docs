Docker Image
============

Overview
--------

Likely the easiest and quickest method of setting up StackStorm is via:

  https://github.com/stackstorm/st2-docker

This page provides detailed instructions to ensure a successful installation.

Host Requirements
-----------------

* Install the latest versions of Docker engine and ``docker-compose``. The installation instructions
  are located at https://www.docker.com/community-edition and
  https://docs.docker.com/compose/install respectively.

.. note::
  We require at least version 1.13.0 of Docker engine and ``docker-compose``.

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

Getting a shell prompt in the stackstorm container
--------------------------------------------------

After the containers are running, you can acccess a shell within the stackstorm container using the
following command:

.. sourcecode:: bash

  docker exec -it stackstorm /bin/bash

Running custom shell scripts on boot
------------------------------------

This container supports running arbitrary shell scripts on container boot. Any ``*.sh`` file
located under ``/entrypoint.d`` directory will be executed inside the container just before starting
stackstorm services.

For example, if you want to modify ``/etc/st2/st2.conf`` to set ``system_packs_base_path``
parameter, create ``modify-st2-config.sh`` with the follwing content:

.. sourcecode:: bash

  #!/bin/bash
  crudini --set /etc/st2/st2.conf content system_packs_base_path /opt/stackstorm/custom_packs

Then bind mount it to ``/entrypoint.d/modify-st2-config.sh``:

* via ``docker run``

.. sourcecode:: bash

  docker run -it -d --privileged \
    -v /path/to/modify-st2-config.sh:/entrypoint.d/modify-st2-config.sh \
      stackstorm/stackstorm:latest

* via changes to ``docker-compose.yml`` and subsequent execution of ``docker-compose up -d``

.. sourcecode:: yaml

  services:
    stackstorm:
      image: stackstorm/stackstorm:${TAG:-latest}
        : (snip)
      volumes:
        - /path/to/modify-st2-config.sh:/entrypoint.d/modify-st2-config.sh

The above example shows just modifying st2 config but basically there is no limitation so you can do
almost anything.

You can also bind mount a specific directory to /entrypoint.d then place scripts as much as you
want. All of them will be executed as long as the file name ends with ``*.sh``.

Note: scripts will be executed in alphabetical order of the file name.

To enable/disable chatops
-------------------------

Chatops is installed in the ``stackstorm`` image, but not started by default.

To enable chatops, delete the file ``/etc/init/st2chatops.override`` using a script in
``/entrypoint.d/``.

.. sourcecode:: bash

  #!/bin/bash

  sudo rm /etc/init/st2chatops.override

If you need to disable chatops, run the following using a script in ``/entrypoint.d``:

.. sourcecode:: bash

  #!/bin/bash

  echo manual | sudo tee /etc/init/st2chatops.override

Sample Usage
============

For sample usage, please see https://github.com/stackstorm/st2-docker.
