Upgrades
========

When new versions of |st2| are released, they are published to our APT and Yum repositories. You
can use standard Linux package management tools to install these upgraded packages.

As part of the general upgrade procedure, you will need to run scripts to upgrade the Mistral Database prior
to restarting |st2| services. See below for more details. Depending on the versions you are upgrading to and
from, you may need to run additional :ref:`migration scripts<migration-scripts-to-run>`.

If you skipped a version and are upgrading to a newer version, please make sure you also run the
migration scripts for skipped versions.

Update GPG Key
--------------

.. warning::

    The GPG keys used for signing our apt and yum repository metadata have been updated. If you are upgrading
    an existing system that has the old keys installed, it will need updating. See the instructions below for
    how to do this.
    
    Failure to update the keys will result in signature verification errors during package update.

For |st2| community version on Ubuntu, run the following command to update your keys. If you
are running a non production version of StackStorm, then replace ``stable`` in the URL with the
appropriate repository name.

.. sourcecode:: bash

    curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.deb.sh | sudo bash

For |st2| enterprise version on Ubuntu, both the gpg keys for community and enterprise need to be
imported separately. Run the following commands to update both keys. If you are running
a non production version of StackStorm, then replace ``stable`` in the curl with the appropriate
repository name. Replace ``<license_key>`` with your enterprise license key.

.. sourcecode:: bash

    curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.deb.sh | sudo bash
    curl -s https://<license_key>:@packagecloud.io/install/repositories/StackStorm/enterprise/script.deb.sh | sudo bash

For reference, the following is the error shown if the new gpg key(s) is not added on Ubuntu. Please
note the URLs that failed on retrieval should be ``https://packagecloud.io/StackStorm/stable`` for the
|st2| community and ``https://packagecloud.io/StackStorm/enterprise`` for the |st2| enterprise repo::

    $ sudo apt-get update
    Get:7 https://packagecloud.io/StackStorm/stable/ubuntu xenial InRelease [23.2 kB]
    Err:7 https://packagecloud.io/StackStorm/stable/ubuntu xenial InRelease
    The following signatures couldn't be verified because the public key is not available: NO_PUBKEY C2E73424D59097AB
    Hit:8 http://archive.ubuntu.com/ubuntu xenial InRelease         
    Hit:9 http://archive.ubuntu.com/ubuntu xenial-updates InRelease
    Hit:10 http://archive.ubuntu.com/ubuntu xenial-backports InRelease
    Fetched 23.2 kB in 1s (12.3 kB/s)
    Reading package lists... Done
    W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: https://packagecloud.io/StackStorm/stable/ubuntu xenial InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY C2E73424D59097AB
    W: Failed to fetch https://packagecloud.io/StackStorm/stable/ubuntu/dists/xenial/InRelease  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY C2E73424D59097AB
    W: Some index files failed to download. They have been ignored, or old ones used instead.

For |st2| community version on RHEL/CentOS, run the following command to update the keys. If you
are running a non production version of StackStorm, then replace ``stable`` in the URL with the
appropriate repository name.

.. sourcecode:: bash

    curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.rpm.sh | sudo bash

For |st2| enterprise version on RHEL/CentOS, both the gpg keys for community and enterprise need to be
import separately. Run the following commands to update the keys. If you are running a
non production version of StackStorm, then replace ``stable`` in the URLs with the appropriate
repository name. Replace ``<license_key>`` with your enterprise license key.

.. sourcecode:: bash

    curl -s https://packagecloud.io/install/repositories/StackStorm/stable/script.rpm.sh | sudo bash
    curl -s https://<license_key>:@packagecloud.io/install/repositories/StackStorm/enterprise/script.rpm.sh | sudo bash

If the new gpg keys are not setup in advanced on RHEL/CentOS, running ``yum update`` will auto-retrieve
the new gpg key for appropriate respository. ``yum update`` will ask if you want to import the new gpg keys.
Verify that the key is retrieved from ``https://packagecloud.io/StackStorm/stable/gpgkey`` for the |st2|
community and enter ``y`` to confirm. For |st2| enterprise repo, an additional key needs to be retrieved from
``https://packagecloud.io/StackStorm/enterprise/gpgkey``.

For reference, the following is a sample output from ``yum update``. Please note the URLs where the key
is retrieved from should be ``https://packagecloud.io/StackStorm/stable`` for the
|st2| community and ``https://packagecloud.io/StackStorm/enterprise`` for the |st2| enterprise repo::

    $ sudo yum update
    Loaded plugins: fastestmirror
    Loading mirror speeds from cached hostfile
    StackStorm_stable/x86_64/signature                                                             |  836 B  00:00:00     
    Retrieving key from https://packagecloud.io/StackStorm/stable/gpgkey
    Importing GPG key 0xF6C28448:
    Userid     : "https://packagecloud.io/StackStorm/stable (https://packagecloud.io/docs#gpg_signing) <support@packagecloud.io>"
    Fingerprint: 2664 b321 ca26 c6be fe81 aa46 723c b7a7 f6c2 8448
    From       : https://packagecloud.io/StackStorm/stable/gpgkey
    Is this ok [y/N]: y
    StackStorm_stable/x86_64/signature                                                             | 1.0 kB  00:00:15 !!! 
    StackStorm_stable-source/signature                                                             |  836 B  00:00:00     
    Retrieving key from https://packagecloud.io/StackStorm/stable/gpgkey
    Importing GPG key 0xF6C28448:
    Userid     : "https://packagecloud.io/StackStorm/stable (https://packagecloud.io/docs#gpg_signing) <support@packagecloud.io>"
    Fingerprint: 2664 b321 ca26 c6be fe81 aa46 723c b7a7 f6c2 8448
    From       : https://packagecloud.io/StackStorm/stable/gpgkey
    Is this ok [y/N]: y
    StackStorm_stable-source/signature                                                             |  951 B  00:00:10 !!! 
    (1/2): StackStorm_stable-source/primary                                                        |  175 B  00:00:00     
    (2/2): StackStorm_stable/x86_64/primary                                                        |  27 kB  00:00:00     
    StackStorm_stable                                                                                             124/124

General Upgrade Procedure
-------------------------

This is the standard upgrade procedure:

1. Stop ``st2*`` services, and check all processes have terminated:

   .. sourcecode:: bash

      sudo st2ctl stop
      ps auxww | grep st2
      
   If any `st2`-related processes are still running, kill them with `kill -9`.

2. Upgrade |st2| packages using distro-specific tools:

   Ubuntu:

   .. sourcecode:: bash

      sudo apt-get install --only-upgrade st2 st2web st2chatops st2mistral

   RHEL/CentOS:

   .. sourcecode:: bash

      sudo yum update st2 st2web st2chatops st2mistral

   Omit st2mistral if it is not installed on your distribution.

3. Upgrade Mistral database:

   This step can be skipped if st2mistral is not installed on your distribution.

   .. sourcecode:: bash

     /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head
     /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate | grep -v -e openstack -e keystone -e ironicclient

   .. warning::

      The mistral and mistral-api services must be stopped at time of upgrade. If the services are
      restarted before the mistral-db-manage commands are run, then the
      ``mistral-db-manage upgrade head`` command may fail.

4. Run the migration scripts (if any). See below for version-specific migration scripts.

5. Ensure all content is registered:

   .. sourcecode:: bash

      sudo st2ctl reload --register-all

6. Start |st2| services:

   .. sourcecode:: bash

      sudo st2ctl start

.. _migration-scripts-to-run:

Version-specific Migration Scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We document :ref:`upgrade notes<upgrade_notes>` for the various versions. The upgrade notes section gives
an idea of what major changes happened with each release. You may also want to take a look at the detailed
:doc:`/changelog` for each version.

The following sections call out the migration scripts that need to be run when upgrading to the
respective version. If you are upgrading across multiple versions, make sure you run the scripts for
any skipped versions:

v2.10
'''''

* Node.js v10 is now used by ChatOps (previously v6 was used). The following procedure should be
  used to upgrade:

  Ubuntu:

  .. sourcecode:: bash

     curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
     sudo apt-get install --only-upgrade st2chatops

  RHEL/CentOS:

  .. sourcecode:: bash

     sudo sed -i.bak 's|^baseurl=\(https://rpm.nodesource.com\)/[^/]\{1,\}/\(.*\)$|baseurl=\1/pub_10.x/\2|g' /etc/yum.repos.d/nodesource-*.repo
     sudo yum clean all
     sudo rpm -e --nodeps npm
     sudo yum upgrade st2chatops
* Yammer support has been removed.

v2.9
''''

* This version introduced new ``st2timersengine`` service which needs to be configured in
  ``/etc/st2/st2.conf`` config file for it to work. For more information, please refer to Upgrade
  Notes - :ref:`ref-upgrade-notes-v2-9`.

v2.8
''''

* This version introduced new ``st2workflowengine`` service which needs to be configured in
  ``/etc/st2/st2.conf`` config file for it to work. For more information, please refer to Upgrade
  Notes - :ref:`ref-upgrade-notes-v2-8`.

v2.5
''''

* If you have the `DC Fabric Automation Suite <https://ewc-docs.extremenetworks.com/solutions/dcfabric/overview.html>`_
  version 1.1 installed, you must upgrade this to >= v1.1.1. Follow `these instructions <https://ewc-docs.extremenetworks.com/solutions/dcfabric/install.html#upgrade-from-previous-version>`_.

v2.4
''''

* Node.js v6 is now used by ChatOps (previously v4 was used). The following procedure should be
  used to upgrade:

  Ubuntu:

  .. sourcecode:: bash

     curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
     sudo apt-get install --only-upgrade st2chatops

  RHEL/CentOS:

  .. sourcecode:: bash

     curl -sL https://rpm.nodesource.com/setup_6.x | sudo -E bash -
     sudo yum clean all
     sudo rpm -e --nodeps npm
     sudo yum upgrade st2chatops

* |ewc| users on RHEL or CentOS must run this command after upgrading packages:

  .. sourcecode:: bash

     sudo /opt/stackstorm/st2/bin/pip install --find-links /opt/stackstorm/share/wheels --no-index --quiet --upgrade st2-enterprise-auth-backend-ldap

This is a known issue, and will be resolved in a future release. This only applies to |ewc| users.
It is not required for those using Open Source StackStorm.

v2.2
''''

* The database schema for Mistral has changed. The executions_v2 table is no longer used. The
  table is being broken down into workflow_executions_v2, task_executions_v2, and
  action_executions_v2. After upgrade, using the Mistral commands from the command line such as
  ``mistral execution-list`` will return an empty table. The records in executions_v2 have not
  been deleted. The commands are reading from the new tables. There is currently no migration
  script to move existing records from executions_v2 into the new tables. To read from
  executions_v2, either use psql or install an older version of the python-mistralclient in a
  separate python virtual environment.

  .. warning::

     Please be sure to follow the general steps listed above to do the database upgrade.

  .. _mistral_db_recover:

*  If you're seeing an error ``event_triggers_v2 already exists`` when running
   ``mistral-db-manage upgrade head``, this means the mistral services started before the
   mistral-db-manage commands were run. SQLAlchemy automatically creates new tables in
   the updated database schema and it conflicts with the mistral-db-manage commands.
   To recover, open the psql shell and delete the new tables manually and rerun the
   mistral-db-manage commands. The following is a sample script to recover from the errors.

  .. sourcecode:: bash

     sudo service mistral-api stop
     sudo service mistral stop
     sudo -u postgres psql
     \connect mistral
     DROP TABLE event_triggers_v2;
     DROP TABLE workflow_executions_v2 CASCADE;
     DROP TABLE task_executions_v2;
     DROP TABLE action_executions_v2;
     DROP TABLE named_locks;
     \q
     /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head
     /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate
     sudo service mistral start
     sudo service mistral-api start

v2.1
''''

* Datastore model migration - Scope names are now ``st2kv.system`` and ``st2kv.user`` as
  opposed to ``system`` and ``user``.

  .. code-block:: bash

     /opt/stackstorm/st2/bin/st2-migrate-datastore-scopes.py

* We are piloting pluggable runners (See :ref:`upgrade notes<upgrade_notes>`). Runners now
  have to be explicitly registered just like other content.

  .. code-block:: bash

     /opt/stackstorm/st2/bin/st2-migrate-runners.sh

* Service restart ``st2ctl restart`` and reload ``st2ctl reload`` are required after upgrade
  for the new pack management features to work properly. Some of the pack management actions
  and workflows have changed.


Content Roll-Over
-----------------

In some cases, you may need to roll over the automation from one instance of |st2| to another box
or deployment. To do this, provision a new |st2| instance, and roll over the content. Thanks to
the "Infrastructure as Code" approach, all |st2| content and artifacts are simple files, and
should be kept under source control.


1. Install |st2| ``VERSION_NEW`` on a brand new instance using packages based installer.
2. Package all your packs from the old ``VERSION_OLD`` instance and place them under some SCM
   like git (you should have done it long ago). Each pack must be in its own repo.
3. Save your key-value pairs from the st2 datastore: ``st2 key list -j > kv_file.json``
4. Grab packs from the SCM. If the SCM is git then you can directly install them with
   ``st2 pack install <repo-url>=<pack-list>>``
5. Reconfigure all external services to point to the new |st2| instance.
6. Load your keys to the datastore: ``st2 key load kv_file.json``. You might have to adjust the
   JSON files to include ``scope`` and ``secret`` if you are upgrading from a version < 1.5.
   See migration script in ``/opt/stackstorm/st2/bin/st2-migrate-datastore-to-include-scope-secret.py``.
7. Back up audit log from ``VERSION_OLD`` server found under ``/var/log/st2/*.audit.log`` and move
   to a safe location. Note that history of old executions will be lost during such a transition,
   but a full audit record is still available in the log files that were transferred over.
