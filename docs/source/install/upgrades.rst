Upgrades
========

To upgrade |st2|, use the standard upgrade procedure for your Linux
distribution. You can simply upgrade the specific packages namely ``st2``, ``st2web``,
``st2chatops``, ``st2mistral`` and ``bwc-enterprise``.

Most of these upgrades should be seamless and do no require the user to do anything else.
For ``st2`` package, depending on the ``from`` version and the ``to`` version, you might need to run
migration scripts for picking up data model changes.

The list of migrations to run when upgrading to a version is listed in the
:ref:`section below<migration-scripts-to-run>`.

If you skipped a version and are upgrading to a newer version, please make sure you *run migration
scripts* for skipped versions as well.


Upgrade Procedure
-----------------

:ref:`Migration scripts<migration-scripts-to-run>` most often need to be run when upgrading to |st2|
:versions that include data model changes. The typical **upgrade** procedure is

1. Stop ``st2*`` services on the box.

.. sourcecode:: bash

   sudo st2ctl stop

2. Upgrade |st2| packages (``st2``, ``st2web``, ``st2chatops``, ``st2mistral``
   and ``bwc-enterprise`` using distro specific tools.

  Ubuntu:

  .. sourcecode:: bash

     sudo apt-get install --only-upgrade $PKG_NAME

  RHEL / CentOS:

  .. sourcecode:: bash

     sudo yum update $PKG_NAME

3. Upgrade Mistral database.

.. sourcecode:: bash

  /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head
  /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate

.. warning::

    The mistral and mistral-api services must be stopped at time of upgrade. If the services are
    restarted before the mistral-db-manage commands are run, then the
    ``mistral-db-manage upgrade head`` command may fail.

4. Run the migration script (if any). See section below for |st2|
   version-specific migration scripts.

5. Start |st2| services.

.. sourcecode:: bash

   sudo st2ctl start

.. _migration-scripts-to-run:

Version-specific Migration Scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We document :ref:`upgrade notes<upgrade_notes>` for the various versions. The upgrade
notes section gives an idea of what major changes happened with each release. You may also want
to take a look at detailed :doc:`/changelog` for each version.
Following sections call out the migration scripts that need to be run before upgrading to the
respective version

v2.2
'''''

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
'''''

* Datastore model migration - Scope names are now ``st2kv.system`` and ``st2kv.user`` as
  opposed to ``system`` and ``user``.

::

   /opt/stackstorm/st2/bin/st2-migrate-datastore-scopes.py

* We are piloting pluggable runners (See :ref:`upgrade notes<upgrade_notes>`). Runners now
  have to be explicitly registered just like other content.

::

  /opt/stackstorm/st2/bin/st2-migrate-runners.sh

* Service restart ``st2ctl restart`` and reload ``st2ctl reload`` are required after upgrade
  for the new pack management features to work properly. Some of the pack management actions
  and workflows have changed.

v1.5
'''''

* Datastore model migration

::

    /opt/stackstorm/st2/bin/st2-migrate-datastore-to-include-scope-secret.py

Content Roll-Over
-----------------

In some cases, you may need to roll over the automation from one instance of |bwc| to
another box or deployment. To do this, provision a new |st2| instance, and roll over the content.
Thanks to the "Infrastructure as code" approach, all |st2| content and artifacts are simple files,
and should be kept under source control.


1. Install |st2| ``VERSION_NEW`` on a brand new instance using packages based installer.
2. Package all your packs from the old ``VERSION_OLD`` instance and place them under some SCM
   like git (you should have done it long ago).
3. Save your key-value pairs from the st2 datastore: ``st2 key list -j > kv_file.json``
4. Grab packs from the SCM.
5. If the SCM is git then it is possible to use ``st2 run packs.install packs=<pack-list>
   repo_url=<repo-url>``
6. Reconfigure all external services to point to the new |st2| instance.
7. Load your keys to the datastore: ``st2 key load kv_file.json``. You might have to readjust
   the JSON files to include ``scope`` and ``secret`` if you are upgrading from version < 1.5 to 1.5 onwards. See migration script in ``/opt/stackstorm/st2/bin/st2-migrate-datastore-to-include-scope-secret.py`` for an idea.
8. Back up audit log from ``VERSION_OLD`` server found under ``/var/log/st2/*.audit.log`` and
   move to a safe location. Note that history of old executions will be lost during such a transition, but a full audit record is still available in the log files that were transferred over.

