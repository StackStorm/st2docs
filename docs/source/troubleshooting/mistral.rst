Mistral Issues
==============

This section contains information on how to troubleshoot Mistral related issues.

Troubleshooting Mistral database upgrade
----------------------------------------

The mistral and mistral-api services must be stopped at time of upgrading the st2mistral package
and the mistral database schema. If the st2mistral package has been upgraded and the services are
started before the ``mistral-db-manage upgrade head`` command is run, then the
``mistral-db-manage upgrade head`` command may fail. When the mistral and mistral-api services run,
SQLAlchemy automatically creates tables, relationships, and indices that do not exist. In the case
where there are new database objects in the upgraded database schema, the 
``mistral-db-manage upgrade head`` command will fail because the actual schema in the database is
now different than its spec and it no longer can create the new database objects. When that happens,
the new database tables, relationships, and indices must be deleted before the
``mistral-db-manage upgrade head`` command can be re-run. For more details, review the specific
section for the version being upgraded in :doc:`/install/upgrades`.
