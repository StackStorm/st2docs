.. _migration-scripts-to-run:

Migration scripts to run on upgrades
====================================

Migration scripts most often need to be run when upgrading to |st2| versions that
include data model changes. The runbook is usually

1. Stop |st2| services on the box.

.. sourcecode:: bash

   sudo st2ctl stop

2. Run the migration script (if any). See section below for StackStorm
   version-specific migration scripts.

3. Upgrade |st2| packages (``st2``, ``st2web``, `st2chatops``, ``st2mistral``
   and ``bwc-enterprise`` using distro specific tools.

Ubuntu:


.. sourcecode:: bash

   sudo apt-get install --only-upgrade $PKG_NAME

RHEL / CentOS:

.. sourcecode:: bash

   sudo yum update $PKG_NAME

4. Upgrade Mistral database.

.. sourcecode:: bash

  # Stop related services
  service mistral-api stop
  service mistral stop

  # Upgrade database
  /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head
  /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate

  # Restart related services
  service mistral start
  service mistral-api start

5. Start |st2| services.

.. sourcecode:: bash

   sudo st2ctl start

We usually document :ref:`upgrade notes<upgrade_notes>` for the various versions. The upgrade
notes section gives an idea of what major changes happened with each release. You may also want
to take a look at detailed :doc:`/changelog` for each version.
Following sections call out the migration scripts that need to be run before upgrading to the
respective version

Version-specific migration scripts
----------------------------------

v1.5
~~~~

* Datastore model migration

::

    /opt/stackstorm/st2/bin/st2-migrate-datastore-to-include-scope-secret.py
