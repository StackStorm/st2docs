:orphan:

Run From Sources
========================================================================

Environment Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Requirements:

-  git
-  tig(optional interactive tui for git commits)
-  python3.8 for Ubuntu 20.04 and RockyLinux/RHEL 8
-  python3.9 for RockyLinux/RHEL 9
-  python3.10 for Ubuntu 22.04
-  pip, virtualenv, tox
-  MongoDB
   - Ubuntu (https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)
   - RHEL (https://www.mongodb.com/docs/v4.4/tutorial/install-mongodb-on-red-hat/)
-  RabbitMQ / Erlang 26.x
   - Ubuntu (https://www.rabbitmq.com/docs/install-debian)
   - RHEL (https://www.rabbitmq.com/docs/install-rpm)
-  Redis Stack (https://redis.io/docs/install/install-stack/linux/)
-  tmux

Ubuntu
------------------------------------------------------------------------

Install required packages for python development.

.. code-block:: bash

    apt-get install python3-pip python3-venv gcc git make tmux libffi-dev libssl-dev python3-dev libldap2-dev libsasl2-dev


Install a supported version of MongoDB, RabbitMQ / Erlang and Redis.

`Ubuntu 20.04 Focal </install/u20#install-dependencies>`
`Ubuntu 22.04 Jammy </install/u22#install-dependencies>`


Rocky Linux / RedHat Enterprise Linux
------------------------------------------------------------------------

.. code-block:: bash

    dnf install python-pip gcc-c++ git-all tmux icu libicu libicu-devel openssl-devel openldap-devel python3-devel

    OSRELEASE_VERSION=$(source /etc/os-release; echo ${VERSION_ID%.*})
    dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-${OSRELEASE_VERSION}.noarch.rpm

.. note::

  virtualenv is not available on Rocky9 and by extension the python-tox package can't be installed.  Use venv module instead.
  screen has been removed from Rocky9 so developer tooling uses tmux instead.


Install a supported version of MongoDB, RabbitMQ / Erlang and Redis.

`Red Hat Enterprise Linux 8 and compatible distributions </install/rhel8#install-dependencies>`
`Red Hat Enterprise Linux 9 and compatible distributions </install/rhel9#install-dependencies>`


Project Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Activate the virtualenv before starting the services:

.. code-block:: bash

    source virtualenv/bin/activate

Run the following to start |st2|:

.. code-block:: bash

    ./tools/launchdev.sh start

It will start |st2| components in ``tmux`` sessions.

Additional commands:

.. code-block:: bash

    source virtualenv/bin/activate   # Activates the Python virtual environment
    tools/launchdev.sh startclean    # Reset and launches all StackStorm services in screen sessions
    tools/launchdev.sh start         # Launches all StackStorm services in screen sessions
    tools/launchdev.sh stop          # Stops all StackStorm screen sessions and services

If the services are started successfully, you will see the following output:

.. code-block:: bash

  ./tools/launchdev.sh start
  Initialising system variables ...
  Current user:group = root:root
  Using virtualenv: /root/workspace/st2/virtualenv
  Using python: /root/workspace/st2/virtualenv/bin/python (Python 3.10.12)
  Log file location: /root/workspace/st2/./tools/../logs
  Using st2 config file: /root/workspace/st2/conf/st2.dev.conf
  Starting all st2 servers ...
  Changing working directory to /root/workspace/st2/./tools/..
  Using config base dir: /opt/stackstorm/configs
  Using content packs base dir: /opt/stackstorm/packs
  Starting st2-api using gunicorn ...
  Starting st2-stream using gunicorn ...
  Starting st2-workflow engine(s):
     st2-workflow-1 ...
  Starting st2-actionrunner(s):
     st2-actionrunner-1 ...
  Starting st2-garbagecollector ...
  Starting st2-scheduler(s):
     st2-scheduler-1 ...
  Starting st2-sensorcontainer ...
  Starting st2-rulesengine ...
  Starting st2-timersengine ...
  Starting st2-notifier ...
  Starting st2-auth using gunicorn ...
  ...

|st2| can now be operated using the REST API, |st2| CLI, and the st2client Python client library.

.. _setup-st2-cli:

Install |st2| CLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The |st2| CLI client needs to be installed. It is not necessary to install this into the
virtualenv. However, the client may need to be installed with sudo if not in the virtualenv:

.. code-block:: bash

    cd ./st2client
    python3 setup.py develop

Verify Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To make sure all the components are installed correctly:

.. code-block:: bash

    st2 --version
    st2 --help
    st2 action list
    st2 run core.local uname

Additional Makefile targets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 - ``make all`` creates virtualenv, installs dependencies, and runs tests
 - ``make tests`` runs all the tests
 - ``make lint`` runs lint tasks (``flake8``, ``pylint``)
 - ``make docs`` compiles this documentation
 - ``make clean`` clears .pyc's and docs
 - ``make distclean`` runs ``make clean`` target and also drops virtualenv
 - ``make requirements`` installs Python requirements
 - ``make virtualenv`` creates an empty virtual environment


Install |st2| Web UI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    username: testu
    password: testp

Manual Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
