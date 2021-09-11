:orphan:

Run From Sources
=================

Environment Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~

Requirements:

-  git
-  python3.6 (or python3.8 for Ubuntu 20.04), pip, virtualenv, tox
-  MongoDB (http://docs.mongodb.org/manual/installation)
-  RabbitMQ (http://www.rabbitmq.com/download.html)
-  screen

Ubuntu
------

.. note::
  For Ubuntu 20.04 replace with python3.8 equivalents


.. code-block:: bash

    apt-get install python-pip python-virtualenv gcc git make realpath screen libffi-dev libssl-dev python3.6-dev libldap2-dev libsasl2-dev
    apt-get install mongodb mongodb-server
    apt-get install rabbitmq-server

CentOS/RHEL
-----------

.. note::
  For RHEL 7.x you may need to enable the optional server rpms repository to be able to install the python3-devel RPM


.. code-block:: bash

    OSRELEASE_VERSION=`lsb_release -s -r | cut -d'.' -f 1`

    yum install python-pip python-virtualenv python-tox gcc-c++ git-all screen icu libicu libicu-devel openssl-devel openldap-devel python3-devel

    yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-${OSRELEASE_VERSION}.noarch.rpm

    # Add key and repo for the latest stable MongoDB (4.0)
    rpm --import https://www.mongodb.org/static/pgp/server-4.0.asc
    sh -c "cat <<EOT > /etc/yum.repos.d/mongodb-org-4.repo
    [mongodb-org-4]
    name=MongoDB Repository
    baseurl=https://repo.mongodb.org/yum/redhat/${OSRELEASE_VERSION}/mongodb-org/4.0/x86_64/
    gpgcheck=1
    enabled=1
    gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
    EOT"

    yum install crudini
    yum install mongodb-org
    yum install rabbitmq-server
    systemctl start mongod rabbitmq-server
    systemctl enable mongod rabbitmq-server

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
    python3 setup.py develop

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


Install |st2| Web UI
~~~~~~~~~~~~~~~~~~~~~~

Installing the st2 Web UI.

.. code-block:: bash

    sudo apt install npm
    sudo npm install -g n
    sudo n v10.15.3
    sudo npm install -g gulp-cli lerna yarn

.. code-block:: bash

    git clone https://github.com/StackStorm/st2web.git
    cd st2web
    # bootstrap the micromodules
    lerna bootstrap
    # bring the stackstorm ui
    gulp


Default Credentials to Login
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    username: testu
    password: testp

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
