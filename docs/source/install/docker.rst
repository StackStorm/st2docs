Docker
======

Like Docker? So do we!

One of the quickest ways to get StackStorm running is using Docker. This page will show you the basics
of how to use StackStorm with Docker. 

For more detailed information and examples, check out the `README
<https://github.com/StackStorm/st2-docker/blob/master/README.md>`_ at our `st2-docker GitHub repo
<https://github.com/StackStorm/st2-docker>`_.

  .. note::
    If you use Kubernetes, check the :doc:`/install/k8s_ha` for more information.

Host Requirements
-----------------
* Install the latest versions of ``Docker`` engine and ``docker-compose``. Installation
  instructions are at https://www.docker.com/community-edition and
  https://docs.docker.com/compose/install.

Docker Images
-------------
Docker-compose deployment relies on pre-built, tested and deployed to Docker Hub StackStorm images.
Check out `stackstorm/st2-dockerfiles <https://github.com/stackstorm/st2-dockerfiles>`_ GitHub repository
if you need more details about the StackStorm Dockerfiles internals.

Usage
-----
Assuming ``Docker engine`` and ``docker-compose`` are properly installed, getting started is easy.

First, clone the ``st2-docker`` repository. Unless specified otherwise, all subsequent
commands assume they are run within ``st2-docker`` directory:

.. code-block:: bash

    git clone https://github.com/stackstorm/st2-docker
    cd st2-docker

You may want to change some variables as necessary. The defaults should be okay.
Below is the complete list of available options that can be used to customize your containers:

+---------------------------+-------------------------------------------------------------------------------------------------------------+
|         Parameter         |       Description                                                                                           |
+===========================+=============================================================================================================+
| ``ST2_VERSION``           | Tag at the end of the docker image (ie: ``stackstorm/st2api:v3.3dev``).                                     |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``ST2_IMAGE_REPO``        | The image or path to the images. Default is ``stackstorm/``.                                                |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``ST2_EXPOSE_HTTP``       | Port to expose st2web port 80 on.  Default is ``127.0.0.1:80``, and you may want to do ``0.0.0.0:80``.      |
+---------------------------+-------------------------------------------------------------------------------------------------------------+
| ``ST2_PACKS_DEV``         | Directory to development packs. This allows you to develop packs locally. Default is ``./packs.dev``.       |
+---------------------------+-------------------------------------------------------------------------------------------------------------+

Then, start the containers:

.. code-block:: bash

  docker-compose up -d

This will pull the required images from Docker Hub, and then start them.

To switch to shell inside the container where you can use ``st2`` CLI:

.. sourcecode:: bash

  docker-compose exec st2client bash

Navigate the UI configured by default at http://localhost/.
Username/Password pair is ``st2admin:Ch@ngeMe`` and could be configured via ``files/htpasswd``.

To stop the containers, run:

.. sourcecode:: bash

  docker-compose down

More information can be found in the ``st2-docker`` `README.md <https://github.com/StackStorm/st2-docker/blob/master/README.md>`_.
