.. _migration-scripts-to-run:

Migration scripts to run on upgrades
====================================

Migration scripts most often need to be run *before* upgrading |st2| packages.
The runbook is usually

1. Run the migration script
2. Upgrade ``st2`` packages using distro specific tools
   (``apt-get install --only-upgrade $PKG_NAME`` for Ubuntu and ``yum update $PKG_NAME`` for RHEL/CentOS)

We usually document :ref:`upgrade notes<upgrade_notes>` for the various versions. The upgrade
notes section gives an idea of what major changes happened with each release. You may also want
to take a look at detailed :doc:`/changelog` for each version.
Following sections call out the migration scripts that need to be run before upgrading to the
respective version

v1.5
----

* Datastore model migration

::

    /opt/stackstorm/st2/bin/st2-migrate-datastore-to-include-scope-secret.py
