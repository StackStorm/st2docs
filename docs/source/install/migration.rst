.. _migration-scripts-to-run:

Migration scripts to run on upgrades
====================================

Migration scripts most often need to be run when upgrading to |st2| versions that
include data model changes. The runbook is usually

1. Stop |st2| services on the box (``sudo st2ctl stop``).
2. Run the migration script.
3. Upgrade |st2| packages (``st2``, ``st2web``,
   ``st2chatops``, ``st2mistral`` and ``st2enterprise`` using distro specific tools
   ``apt-get install --only-upgrade $PKG_NAME`` for Ubuntu and ``yum update $PKG_NAME`` for RHEL/CentOS).
4. Start |st2| services. (``sudo st2ctl start``)

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
