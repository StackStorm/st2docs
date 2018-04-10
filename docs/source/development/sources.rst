:orphan:

Run From Sources
=================

Environment Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~

Requirements:

-  git
-  python, pip, virtualenv, tox
-  MongoDB (http://docs.mongodb.org/manual/installation)
-  RabbitMQ (http://www.rabbitmq.com/download.html)
-  screen

Ubuntu
------

.. code-block:: bash

    apt-get install python-pip python-virtualenv python-dev gcc git make realpath screen libffi-dev libssl-dev
    apt-get install mongodb mongodb-server
    apt-get install rabbitmq-server

Fedora
------

.. code-block:: bash

    yum install python-pip python-virtualenv python-tox gcc-c++ git-all screen icu libicu libicu-devel openssl-devel

    yum install mongodb mongodb-server
    systemctl enable mongod
    systemctl restart mongod

    yum install rabbitmq-server
    systemctl enable rabbitmq-server
    systemctl restart rabbitmq-server

Optional Requirements
~~~~~~~~~~~~~~~~~~~~~

Mistral
-------
Mistral workflow engine also has its own requirements. For more information, please refer to the
:github_mistral:`Mistral README <README.rst>`.

Project Requirements
~~~~~~~~~~~~~~~~~~~~

Once the environment is setup, clone the git repo, and make the project. This will create the
Python virtual environment under StackStorm, download and install required dependencies, and run
tests:

.. code-block:: bash

    git clone https://github.com/StackStorm/st2.git
    cd st2
    # Note: Some of the tests rely on the submodules so you need to check them
    # out to make sure all the tests will pass locally
    git submodule update --init --recursive
    make requirements

Configure System User
~~~~~~~~~~~~~~~~~~~~~

Create a system user for executing SSH actions:

.. code-block:: bash

    useradd -d /home/stanley stanley
    su stanley
    ssh-keygen -f /home/stanley/.ssh/stanley_rsa -t rsa -b 4096 -C "stanley@stackstorm.com" -N ''
    exit

Specify a user for running local and remote SSH actions. See :ref:`config-configure-ssh`. In 
``st2/conf/st2.dev.conf``, change ``ssh_key_file`` to point to the user's key file:

.. code-block:: ini

    [system_user]
    user = stanley
    ssh_key_file = /home/[current user]/.ssh/stanley_rsa

Running
~~~~~~~

Activate the virtualenv before starting the services:

.. code-block:: bash

    source virtualenv/bin/activate

Run the following to start |st2|:

.. code-block:: bash

    ./tools/launchdev.sh start

It will start |st2| components in ``screen`` sessions.

Additional commands:

.. code-block:: bash

    source virtualenv/bin/activate  # Activates the Python virtual environment
    tools/launchdev.sh startclean    # Reset and launches all StackStorm services in screen sessions
    tools/launchdev.sh start         # Launches all StackStorm services in screen sessions
    tools/launchdev.sh stop          # Stops all StackStorm screen sessions and services

If the services are started successfully, you will see the following
output:

.. code-block:: bash

    Starting all st2 servers...
    Changing working directory to /home/vagrant/st2/./tools/.....
    Using st2 config file: /home/vagrant/st2/./tools/../conf/st2.dev.conf
    Using content packs base dir: /opt/stackstorm/packs
    No Sockets found in /var/run/screen/S-vagrant.

    Starting screen session st2-api...
    Starting screen session st2-actionrunner...
        starting runner  1 ...
    No screen session found.
    Starting screen session st2-sensorcontainer
    Starting screen session st2-rulesengine...
    Starting screen session st2-resultstracker...
    Starting screen session st2-notifier...

    Registering sensors, actions, rules and aliases...
    ...

|st2| can now be operated using the REST API, |st2| CLI, and the st2client Python client library.

.. _setup-st2-cli:

Install |st2| CLI
~~~~~~~~~~~~~~~~~~~~~~

The |st2| CLI client needs to be installed. It is not necessary to install this into the
virtualenv. However, the client may need to be installed with sudo if not in the virtualenv:

.. code-block:: bash

    cd ./st2client
    python setup.py develop

Verify Installation
~~~~~~~~~~~~~~~~~~~

To make sure all the components are installed correctly:

.. code-block:: bash

    st2 --version
    st2 --help
    st2 action list
    st2 run core.local uname

Additional Makefile targets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

 - ``make all`` creates virtualenv, installs dependencies, and runs tests
 - ``make tests`` runs all the tests
 - ``make lint`` runs lint tasks (``flake8``, ``pylint``)
 - ``make docs`` compiles this documentation
 - ``make clean`` clears .pyc's and docs
 - ``make distclean`` runs ``make clean`` target and also drops virtualenv
 - ``make requirements`` installs Python requirements
 - ``make virtualenv`` creates an empty virtual environment

Manual Testing
~~~~~~~~~~~~~~

If you only need to test a specific module, it might be reasonable to call ``nosetests`` directly.
Make sure your virtualenv is active then run:

.. code-block:: bash

    nosetests -v {project_name}/tests

or if you only want to run a test for specific file or even class or method, run:

.. code-block:: bash

    nosetests -v {project_name}/tests/{path_to_test_file}/{test_file}.py:{Classname}.{method_name}

.. rubric:: What's Next?

* Get going with :doc:`/start`.
* Check out `tutorials on stackstorm.com <https://stackstorm.com/category/tutorials/>`__ - a growing set of practical examples of automating with StackStorm.

.. include:: /__engage_community.rst
