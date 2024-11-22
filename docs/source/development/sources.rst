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


Install a supported version of MongoDB.

.. note::
  Mongo provides packages for Ubuntu 22.04 LTS ("Jammy") starting from MongoDB 6.0.4.  Adapt installation instructions according.

.. code-block:: bash

	apt-get install gnupg curl
	curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/mongodb-server-4.4.gpg
	sudo chmod 644 /etc/apt/trusted.gpg.d/mongodb-server-4.4.gpg

	export VERSION_CODENAME=$(source /etc/os-release; echo $VERSION_CODENAME)
	export DISTRO_ID=$(source /etc/os-release; echo $ID)
	sudo cat <<EOF >/etc/apt/sources.list.d/mongodb-org-4.4.list
	deb [ arch=amd64 ] https://repo.mongodb.org/apt/${DISTRO_ID} ${VERSION_CODENAME}/mongodb-org/4.4 multiverse
	EOF
	cat /etc/apt/sources.list.d/mongodb-org-4.4.list

	sudo apt update
	sudo apt-get install -y mongodb-org-server mongodb-org-shell mongodb-org-tools

Install a supported version of RabbitMQ / Erlang

.. code-block:: bash

	# configure repository
	# install package

Install a supported version of Redis

.. code-block:: bash

	apt-get install gnupg curl
	curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/redis-archive-keyring.gpg
	sudo chmod 644 /etc/apt/trusted.gpg.d/redis-archive-keyring.gpg
	export VERSION_CODENAME=$(source /etc/os-release; echo $VERSION_CODENAME)
	sudo cat <<EOF >/etc/apt/sources.list.d/redis.list
	deb [ arch=amd64 ] https://packages.redis.io/deb $VERSION_CODENAME main
	EOF
	cat /etc/apt/sources.list.d/redis.list
	sudo apt-get update
	sudo apt-get install redis-stack-server

	systemctl enable redis-stack-server
	systemctl start redis-stack-server


RockyLinux/RHEL
------------------------------------------------------------------------

.. code-block:: bash

    dnf install python-pip gcc-c++ git-all tmux icu libicu libicu-devel openssl-devel openldap-devel python3-devel

    OSRELEASE_VERSION=$(source /etc/os-release; echo ${VERSION_ID%.*})
    dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-${OSRELEASE_VERSION}.noarch.rpm

.. note::

  virtualenv is not available on Rocky9 and by extension the python-tox package can't be installed.  Use venv module instead.
  screen has been removed from Rocky9 and tmux is the recommended replacement.


Install a supported version of MongoDB.

.. code-block:: bash

OSRELEASE_VERSION=$(source /etc/os-release; echo ${VERSION_ID%.*})
cat <<EOF >/etc/yum.repos.d/mongodb-org-4.4.repo
[mongodb-org-4.4]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/${OSRELEASE_VERSION}/mongodb-org/4.4/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://pgp.mongodb.com/server-4.4.asc
EOF

    yum install crudini
    systemctl start mongod
    systemctl enable mongod

Install a supported version of RabbitMQ / Erlang

.. code-block:: bash

	rpm --import 'https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc'
	rpm --import 'https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key'
	rpm --import 'https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key'

	cat <<EOF >/etc/yum.repos.d/rabbitmq.repo
	##
	## Zero dependency Erlang RPM
	##

	[modern-erlang]
	name=modern-erlang-el9
	# uses a Cloudsmith mirror @ yum.novemberain.com.
	# Unlike Cloudsmith, it does not have any traffic quotas
	baseurl=https://yum1.novemberain.com/erlang/el/9/\$basearch
			https://yum2.novemberain.com/erlang/el/9/\$basearch
			https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/rpm/el/9/\$basearch
	repo_gpgcheck=1
	enabled=1
	gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key
	gpgcheck=1
	sslverify=1
	sslcacert=/etc/pki/tls/certs/ca-bundle.crt
	metadata_expire=300
	pkg_gpgcheck=1
	autorefresh=1
	type=rpm-md

	[modern-erlang-noarch]
	name=modern-erlang-el9-noarch
	# uses a Cloudsmith mirror @ yum.novemberain.com.
	# Unlike Cloudsmith, it does not have any traffic quotas
	baseurl=https://yum1.novemberain.com/erlang/el/9/noarch
			https://yum2.novemberain.com/erlang/el/9/noarch
			https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/rpm/el/9/noarch
	repo_gpgcheck=1
	enabled=1
	gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key
		   https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc
	gpgcheck=1
	sslverify=1
	sslcacert=/etc/pki/tls/certs/ca-bundle.crt
	metadata_expire=300
	pkg_gpgcheck=1
	autorefresh=1
	type=rpm-md

	[modern-erlang-source]
	name=modern-erlang-el9-source
	# uses a Cloudsmith mirror @ yum.novemberain.com.
	# Unlike Cloudsmith, it does not have any traffic quotas
	baseurl=https://yum1.novemberain.com/erlang/el/9/SRPMS
			https://yum2.novemberain.com/erlang/el/9/SRPMS
			https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/rpm/el/9/SRPMS
	repo_gpgcheck=1
	enabled=1
	gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key
		   https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc
	gpgcheck=1
	sslverify=1
	sslcacert=/etc/pki/tls/certs/ca-bundle.crt
	metadata_expire=300
	pkg_gpgcheck=1
	autorefresh=1


	##
	## RabbitMQ Server
	##

	[rabbitmq-el9]
	name=rabbitmq-el9
	baseurl=https://yum2.novemberain.com/rabbitmq/el/9/\$basearch
			https://yum1.novemberain.com/rabbitmq/el/9/\$basearch
			https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-server/rpm/el/9/\$basearch
	repo_gpgcheck=1
	enabled=1
	# Cloudsmith's repository key and RabbitMQ package signing key
	gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key
		   https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc
	gpgcheck=1
	sslverify=1
	sslcacert=/etc/pki/tls/certs/ca-bundle.crt
	metadata_expire=300
	pkg_gpgcheck=1
	autorefresh=1
	type=rpm-md

	[rabbitmq-el9-noarch]
	name=rabbitmq-el9-noarch
	baseurl=https://yum2.novemberain.com/rabbitmq/el/9/noarch
			https://yum1.novemberain.com/rabbitmq/el/9/noarch
			https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-server/rpm/el/9/noarch
	repo_gpgcheck=1
	enabled=1
	# Cloudsmith's repository key and RabbitMQ package signing key
	gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key
		   https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc
	gpgcheck=1
	sslverify=1
	sslcacert=/etc/pki/tls/certs/ca-bundle.crt
	metadata_expire=300
	pkg_gpgcheck=1
	autorefresh=1
	type=rpm-md

	[rabbitmq-el9-source]
	name=rabbitmq-el9-source
	baseurl=https://yum2.novemberain.com/rabbitmq/el/9/SRPMS
			https://yum1.novemberain.com/rabbitmq/el/9/SRPMS
			https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-server/rpm/el/9/SRPMS
	repo_gpgcheck=1
	enabled=1
	gpgkey=https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key
	gpgcheck=0
	sslverify=1
	sslcacert=/etc/pki/tls/certs/ca-bundle.crt
	metadata_expire=300
	pkg_gpgcheck=1
	autorefresh=1
	type=rpm-md
	EOF
	cat /etc/yum.repos.d/rabbitmq.repo

	dnf update -y

	dnf install socat logrotate -y
	dnf install -y erlang rabbitmq-server

    systemctl start rabbitmq-server
    systemctl enable rabbitmq-server


Install a supported version of Redis

.. code-block:: bash

	cat <<EOF >/etc/yum.repos.d/redis.repo
	[Redis]
	name=Redis
	baseurl=http://packages.redis.io/rpm/rhel7
	enabled=1
	gpgcheck=1
	EOF

	curl -fsSL https://packages.redis.io/gpg > /tmp/redis.key
	sudo rpm --import /tmp/redis.key
	sudo yum install epel-release
	sudo yum install redis-stack-server

	systemctl enable redis-stack-server
	systemctl start redis-stack-server


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
