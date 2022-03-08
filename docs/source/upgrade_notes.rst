.. _upgrade_notes:

Upgrade Notes
=============

.. _ref-upgrade-notes-v3-7:

|st2| v3.7
----------

* As part of introducing the override pack metadata functionality, the name ``_global`` is
  reserved, and cannot be used for pack names or pack references, to avoid conflict between
  the global override file and individual pack override files.

.. _ref-upgrade-notes-v3-6:

|st2| v3.6
----------

* Prior to v3.5 the installation instructions for all OSes except for CentOS/RHEL 8
  said to use the version of RabbitMQ available in the OS distribution. This version is
  very old, and for 3.6 the installation instructions and simple install have been modified
  to install the latest version of RabbitMQ. It is not a requirement to upgrade RabbitMQ
  for installation of 3.6, but to keep compatibility with a clean installation, the RabbitMQ
  cluster should be upgraded for non CentOS/RHEL 8 systems.

* Retaining backwards compatibility, action delete API has been modified.
  The existing action delete command ``st2 action delete <pack>.<action>`` will delete
  only database entry.
  The action delete CLI command will now take ``-r`` or ``--remove-files`` argument
  to delete action from database along with related files from disk.
  API action DELETE method with ``{"remove_files": true}`` argument in json body will
  remove database entry of action along with files from disk.
  API action DELETE method with ``{"remove_files": false}`` or no additional argument
  in json body will remove only action database entry.

* systemd generators for ``st2api``, ``st2auth`` and ``st2stream`` socket files have replaced
  the static ``.socket`` files.  ``st2.conf`` has become the authoritative source for controlling
  the IP address and port the service will listen on.  This gives a more consistent and intuitive
  means of configuring these services.  If you previously configured these services by directly
  modifying the ``.socket`` file or using the ``DAEMON_ARGS`` environment variable, they are no
  longer referenced and ``st2.conf`` will need to be updated with the desired ip/port.

.. _ref-upgrade-notes-v3-5:

|st2| v3.5
----------

* Node was upgraded from v10 to v14. Node 14 repository will be required to be
  setup, prior to upgrade of st2chatops.
* Support for Ubuntu 16.04 (Xenial) was removed.
* Redis server is installed and configured as backend for the coordination service
  by default to support workflows with multiple branches and tasks with items.
  Upgrade requires coordination service to be setup manually.
  For workflows to be executed properly, setup the coordination service
  accordingly.
* Validation of action definitions are stricter. If an action definition has duplicate keys, |st2|
  will complain when ``st2ctl reload`` is performed at upgrade. Action/workflow definitions should be checked
  for duplicate keys before upgrade.
* ``%`` interpolation in st2 configuration parameters is no longer supported. Update your configuration
  parameters to fix strings if you use ``%`` interpolation to lookup keys as part of your parameter.
  
  Now ``%`` is a valid character in parameter values.
  
  This increases security because passwords with a ``%`` in it do no longer result into an error. 

* The underlying database field type for storing large values such as action execution result has
  changed for various database models (ActionExecutionDB, LiveActionDB, WorkflowExecutionDB,
  TaskExecutionDB, TriggerInstanceDB).

  For most users this change will result in 8-20x speed up when working with (reading and writing)
  large values from / to the database.

  The change is fully transparent to the end user and new objects created after upgrade to |st2|
  v3.5 will automatically utilize this new field type.

  Existing objects in the database will continue to utilize old field type.

  If you want to migrate them to the new field type, you can use
  ``st2-migrate-db-dict-field-values`` migration script which ships with |st2| v3.5. The script
  only operates on "finalized" objects (i.e. finished executions) and it's idempotent which means
  you can re-run it on failures or similar.

  It's worth noting that running this script is optional - in most cases users primarily care about
  performance for recent / new objects (e.g. viewing recent executions) so if you don't migrate
  existing database field values this means retrieving those objects will still be slow, but it
  doesn't affect newly created objects post v3.5 upgrade which will utilize new field type and
  as such, exhibit much better performance.

  By default the script will run in an interactive mode and display a prompt with a warning which needs
  to be acknowledged before continuing. If you want to run script in an non-interactive mode, pass
  ``--yes`` command line argument to it.

  The script also defaults to migrating data for the past 30 days. You can migrate objects from
  a different time period using ``--start-dt`` and ``--end-dt`` arguments as shown below.

  The script currently doesn't support batching so in case you have many objects in the database
  (especially trigger instances) you may need to migrate things in smaller chunks and call this
  script multiple time (e.g. using a day long intervals or shorter).

  Before running this script, you may also want to purge some old operational data. For information
  on that, please refer to :doc:`Purging Old Operational Data </troubleshooting/purging_old_data>`
  documentation page.

  .. code-block:: bash

    # Migrate objects with creation date between April 20th, 2021 and April 25th, 2021
    /opt/stackstorm/st2/bin/st2-migrate-db-dict-field-values --start-dt "2021-04-20T19:16:55Z" --end-dt "2021-04-25T19:26:55Z"

    # Migrate object between April 20th and "now"
    /opt/stackstorm/st2/bin/st2-migrate-db-dict-field-values --start-dt "2021-04-20T19:16:55Z" --end-dt "now"

  .. note::

    You are strongly recommended to create a full database backup before running this script.

    If you run this migration script and a need arises, you won't be able to rollback back to a
    previous version (v3.4) because code in previous version doesn't include support for this new
    field type (in such case you would need to restore the database backup).

.. _ref-upgrade-notes-v3-4:

|st2| v3.4
----------

* Python 2 support was removed.
  Any packs that only support python 2 will need to be migrated to python 3.
  Ubuntu Bionic 16.04 LTS and RHEL/CentOS 7.x ST2 distributions now use python version 3.

.. _ref-upgrade-notes-v3-3:

|st2| v3.3
----------

* The ``st2.action.file_writen`` trigger was renamed to ``st2.action.file_written``. As part of the
  upgrade to v3.3, please make sure to update all previous references to the
  ``st2.action.file_writen`` trigger to ``st2.action.file_written``:

  .. code-block:: yaml

    trigger:
      type: "core.st2.action.file_written"

* Support for Mistral workflows was removed. Before upgrading to v3.3, ensure all Mistral workflows
  have been converted to Orquesta workflows. Please review the :doc:`Orquesta </orquesta/index>` documentation for
  details on how these differ from Mistral workflows, some re-design may be required.
  A tool is available for assisting in this conversion, more information can be found
  in the ``orquestaconvert`` `README.md <https://github.com/StackStorm/orquestaconvert/blob/master/README.md>`_.

* The installation script now installs MongoDB 4.0 by default (previously, 3.4 was installed on
  RHEL/CentOS 7.x and Ubuntu 16.04).
  For information on how to upgrade MongoDB on existing installations, please refer to the official
  MongoDB documentation - https://docs.mongodb.com/v4.0/release-notes/4.0-upgrade-standalone/,
  https://docs.mongodb.com/manual/release-notes/4.0-upgrade-replica-set/.


* After upgrading to v3.3, st2mistral and postgresql services are no-longer required. These services can be stopped, disabled and the corresponding packages uninstalled.

.. _ref-upgrade-notes-v3-2:

|st2| v3.2
----------

* We have switched from unbuffered to fully buffered output for Python runner actions. This should
  result in better performance and smaller CPU utilization for actions which produce a lot of
  output.

  If you experience issues with some Python runner actions hanging out the real time action output
  is slower / less real-time than before, you can set ``actionrunner.stream_output_buffer_size``
  config option to ``-1`` and restart st2actionrunner processes (``sudo st2ctl restart-component
  st2actionrunner``).

  This will switch back to the unbuffered output.

  This config directly controls ``bufsize`` argument which is passed to
  ``st2common.util.green.shell.run_command()`` function so you can also
  experiment with other values which are supported by Python
  ``subprocess.Popen`` (https://docs.python.org/2/library/subprocess.html#popen-constructor)
  function.
* The workflow engine orquesta v1.1.0 made changes to the internal state of ``with items`` task.
  Before upgrading st2 to v3.2, please make sure all workflow executions are completed in the
  database. For example, if there is a workflow execution that has a ``with items`` task and is
  paused before st2 is upgraded to v3.2, the workflow execution will fail to run the with items
  task properly after the upgrade.
* The key word ``continue`` is now a reserved word in orquesta v1.1.0. Orquesta will complain if the
  workflow definition contains a task that is named ``continue``.
* When installing packs from Exchange index ``st2 pack install <pack_name>`` will now download latest
  release from the remote repository, instead of using latest available git commit from master as before.
* When upgrading an installation with the `Community LDAP auth backend <https://github.com/StackStorm/st2-auth-backend-ldap>`_
  configured, you will need to re-install the ``pyasn1`` python module into
  the ``/opt/stackstorm/st2`` virtualenv. This is caused by the fact that the core ``st2``
  package no longer bundles in the ``pyasn1`` module, so it will be absent post-upgrade.
  Running following command will be necessary for ``st2auth`` to function again:
  
  .. code-block:: bash

   /opt/stackstorm/st2/bin/pip install pyasn1
  

.. _ref-upgrade-notes-v3-0:

|st2| v3.0
----------

* CloudSlang (``cloudslang``) and Windows runners (``windows-cmd``, ``windows-script``) have been
  deprecated and removed from the base distribution of |st2|.

  CloudSlang runner has been fully deprecated and winexe based Windows runners have been replaced
  with new more stable and robust WinRM based Windows runners (see
  :doc:`Windows runners </install/config/winrm_runners>` page for more details on the new WinRM
  based Windows runners).

  Support and bug fixes for those runners won't be provided by the |st2| team anymore, but they can
  still be used and installed from a git repository:

  .. code-block:: bash

   # CloudSlang runner
   /opt/stackstorm/st2/bin/pip install "git+https://github.com/StackStorm/stackstorm-runner-cloudslang.git#egg=stackstorm-runner-cloudslang"

   # winexe based Windows runner
   /opt/stackstorm/st2/bin/pip install "git+https://github.com/StackStorm/stackstorm-runner-windows.git#egg=stackstorm-runner-windows"

   sudo st2ctl reload --register-runners
* The :doc:`Inquiries </inquiries>` API has been promoted from the ``/api/exp`` path to ``/api/v1``.
  If you have any external systems that use this API they will need to be updated to use the new
  path. st2client has been updated to use the new path.
* If you are using |ewc| with RBAC you need to update your ``/etc/st2/st2.conf`` config file for RBAC
  to work after the upgrade.

  Before:

    .. code-block:: bash

      [rbac]
      enable = True

  After:

    .. code-block:: bash

      [rbac]
      enable = True
      backend = enterprise

  After you do that, you need to restart st2api service for changes to take affect- ``sudo st2ctl
  restart-component st2api``.

  If you get error similar to the one below after updating the config and restarting the services
  it means you don't have ``bwc-enterprise`` and / or ``st2-rbac-backend`` debian / rpm package
  installed.

  ::

    ValueError: "enterprise" RBAC backend is not available. Make sure "bwc-enterprise" and
    "st2-rbac-backend" system packages are installed.
* In this release remote command and shell script runner has been fixed so new line characters
  produced by the commands and scripts which use sudo are not automatically converted from ``\n``
  to ``\r\n``.

  In the past, if you had an action which output ``hello\nworld`` to stdout, ``stdout`` attribute
  in execution result field would contain ``hello\r\nworld``, but now it will correctly contain
  ``hello\nworld``.
* RBAC is now configured and enabled by default when installing ``bwc-enterprise``
  (``st2-rbac-backend``) system package. If you don't want to use RBAC, you need to disable it in
  ``/etc/st2/st2.conf`` by setting ``rbac.enable`` config option to ``False``.

    .. code-block:: bash

      [rbac]
      enable = False

.. _ref-upgrade-notes-v2-10:

|st2| v2.10
-----------

* The GPG keys for StackStorm's apt and yum reposities metadata signing are updated. Any systems with
  StackStorm installed will complain about GPG key error on signature verification when running apt or yum
  update. Please see the :doc:`upgrades documentation <install/upgrades>` for how to update the GPG key.
* Python |st2| client methods have been renamed from ``st2client.liveactions.*`` to
  ``st2client.executions.*``. Previously those methods already represented operations on
  execution objects, but were incorrectly named.

  For backward compatibility reasons, old names will still work until v3.2.0 release when it will
  be fully removed.
* Old runner names which have been deprecated in |st2| v0.9.0 have been removed. If you still have
  any actions which refer to runners using old names you need to update them to keep them working.

  * ``run-local`` -> ``local-shell-cmd``
  * ``run-local-script`` -> ``local-shell-script``
  * ``run-remote`` -> ``remote-shell-cmd``
  * ``run-remote-script`` -> ``remote-shell-script``
  * ``run-python`` -> ``python-script``
  * ``run-http`` -> ``http-request``
* In |st2| v2.7 action runner modules have been refactored so they are now fully standalone and
  re-distributable Python packages.

  In this release we updated our runner loading mechanism which makes ``/opt/stackstorm/runners``
  directory obsolete.

  All the runners are now installed as Python packages into |st2| virtual environment
  (``/opt/stackstorm/st2``) during package build process and dynamically loaded when requested.

  This provides for more flexible installation and loading of runner modules. To install a custom
  runner, user now just needs to install Python package which contains runner module into |st2|
  virtual environment and restart |st2| services (``sudo st2ctl restart``) or run
  ``sudo st2ctl reload --register-runners`` command.

  Keep in mind that all the runners which are installed inside |st2| virtual environment are now
  automatically loaded and registered on each |st2| service start up. You only need to run 
  ``sudo st2ctl reload --register-runners`` if you are using runner outside the service context or
  if you didn't restart the services.

  For examples:

  .. code-block:: bash

   /opt/stackstorm/st2/bin/pip install "git+https://github.com/stackstorm/st2.git#egg=stackstorm-runner-cloudslang&subdirectory=contrib/runners/cloudslang_runner"

   sudo st2ctl reload --register-runners

  This change also makes ``content.runners_base_paths`` and ``content.system_runners_base_paths``
  config option obsolete and unused.

  If you previously had any custom runners installed in ``/opt/stackstorm/runners/`` directory, you
  need to make sure they follow Python package specification and install them in StackStorm virtual
  environment.

* This version introduces a new ``st2scheduler`` service. This can be configured in a similar
  way to existing services, for example with this entry in the ``/etc/st2/st2.conf`` config file:

  .. code-block:: ini

    [scheduler]
    logging = /etc/st2/logging.scheduler.conf

  Note the above setting is the default, and will be used if you do not have any site-specific ``[scheduler]]``
  settings in ``/etc/st2/st2.conf``.

  You can verify that the new ``st2scheduler`` service is running by checking the output of
  ``sudo st2ctl status`` and by inspecting the service log file at
  ``/var/log/st2/st2scheduler.log``.

.. _ref-upgrade-notes-v2-9:

|st2| v2.9
----------

* Trigger parameters and payload schema validation is now enabled by default
  (``system.validate_trigger_parameters`` and ``system.validate_trigger_payload`` config options
  now default to ``True``).

  This means that trigger parameters are now validated against the ``parameters_schema`` defined on
  the trigger type when creating a rule and trigger payload is validated against ``payload_schema``
  when dispatching a trigger via the sensor or via the webhooks API endpoint.

  This provides a much safer and user-friendly default value.

  Previously we didn't validate trigger payload for custom (non-system) triggers when dispatching
  a trigger via webhook which meant that webhooks API endpoint would silently accept an invalid
  trigger (e.g. referenced trigger doesn't exist in the database or the payload doesn't validate
  against the ``payload_schema``), but ``TriggerInstanceDB`` object would never be created
  because creation failed inside the ``st2rulesengine`` service. This would make such issues very
  hard to troubleshoot because only way to find out about this failure would be to inspect the
  ``st2rulesengine`` service logs.

  If you want to revert to the old behavior (validation is only performed for system triggers),
  you can do that by setting ``system.validate_trigger_parameters`` and
  ``system.validate_trigger_payload`` config option to ``False`` and restart the services
  (``sudo st2ctl restart``).

  Keep in mind that having this functionality enabled is strongly advised since it allows users
  to catch various issues related to typos, invalid payload, etc. much easier and faster.

  Before (webhook references an invalid trigger which doesn't exist in the database):

  .. code-block:: bash

    $ curl -X POST "http://127.0.0.1:9101/v1/webhooks/st2" -H "Content-Type: application/json" -data '{"trigger": "doesnt.exist", "payload": {"attribute1": "value1"}}' -H "St2-Trace-Tag: woo"
    {
        "trigger": "doesnt.exist",
        "payload": {
            "attribute1": "value1"
        }
    }

  After:

  .. code-block:: bash

    $ curl -X POST "http://127.0.0.1:9101/v1/webhooks/st2" -H "Content-Type: application/json" -data '{"trigger": "doesnt.exist", "payload": {"attribute1": "value1"}}' -H "St2-Trace-Tag: woo"
    {
        "faultstring": "Trigger payload validation failed and validation is enabled, not dispatching a trigger \"doesnt.exist\" ({u'attribute1': u'value1'}): Trigger type with reference \"doesnt.exist\" doesn't exist in the database"
    }

  Before (trigger payload doesn't validate against the payload schema):

  .. code-block:: bash

    $ curl -X POST "http://127.0.0.1:9101/v1/webhooks/st2" -H "Content-Type: application/json" -data '{"trigger": "core.st2.webhook", "payload": {"headers": "invalid", "body": {}}}' -H "St2-Trace-Tag: woo"
    {
        "trigger": "core.st2.webhook",
        "payload": {
            "body": {},
            "headers": "invalid"
        }
    }

  After:

  .. code-block:: bash

    $ curl -X POST "http://127.0.0.1:9101/v1/webhooks/st2" -H "Content-Type: application/json" -data '{"trigger": "core.st2.webhook", "payload": {"headers": "invalid", "body": {}}}' -H "St2-Trace-Tag: woo"
    {
        "faultstring": "Trigger payload validation failed and validation is enabled, not dispatching a trigger \"core.st2.webhook\" ({u'body': {}, u'headers': u'invalid'}): u'invalid' is not of type 'object', 'null'\n\nFailed validating 'type' in schema['properties']['headers']:\n    {'type': ['object', 'null']}\n\nOn instance['headers']:\n    u'invalid'"
    }

* ``GET /v1/executions/<execution id>/output[?output_type=stdout/stderr/other]`` API endpoint has
  been made non-blocking and it now only returns data produced by the execution so far (or all data
  if the execution has already finished).

  If you are interested in the real-time execution output as it's produced, you should utilize the
  general purpose stream API endpoint or a new execution output stream API endpoint which has been
  added in |st2| v2.9. For more information, please refer to the
  :doc:`/reference/action_output_streaming` documentation page.
* |st2| timers moved from ``st2rulesengine`` to ``st2timersengine`` service in ``v2.9``. Moving timers
  out of rules engine allows scaling rules and timers independently. ``st2timersengine`` is the new
  process that schedules all the user timers. Please note that when upgrading from older versions, you
  will need to carefully accept changes to ``st2.conf`` file. Otherwise, you risk losing access to
  ``st2`` database in MongoDB.

  .. Warning

    Please back up ``/etc/st2/st2.conf`` before upgrade.

  Please ensure that the following configuration section is enabled in ``/etc/st2/st2.conf``:

  .. code-block:: ini

    [timersengine]
    logging = /etc/st2/logging.timersengine.conf

  If you are already using a ``timer`` section in ``/etc/st2/st2.conf``, you can append the logging
  configuration parameter to the timer section too.

  .. code-block:: ini

    [timer]
    local_timezone = America/Los_Angeles
    logging = conf/logging.timersengine.conf

  We recommend renaming the ``timer`` config section to ``timersengine``. Though deprecated,
  using the ``timer`` section is still supported for backwards compatibility. In a future release,
  support for the ``timer`` section will be removed and ``timersengine`` will be the only way to
  configure timers.
* Support for new **output_schema** attribute has been added to the action metadata file. Keep in
  mind that action metadata files which contain this attribute will only work with |st2| v2.9.0
  and above.

.. _ref-upgrade-notes-v2-8:

|st2| v2.8
----------

* This version introduces new Orquesta runner and Orquesta workflows. For this functionality
  to work, new ``st2workflowengine`` service needs to be installed and running.

  If you are installing StackStorm on a new server using the official installation script this
  service is automatically installed and started.

  If you are  upgrading from a previous release using instructions from the :doc:`/install/upgrades`
  documentation page, you need to ensure ``/etc/st2/st2.conf`` file contains a new
  ``workflow_engine`` section with the corresponding ``logging`` config option, otherwise the
  service won't start.

  After you have completed all the steps from the "General Upgrade Procedure" page, you need to add
  the following entry to ``/etc/st2/st2.conf`` config file:

  .. code-block:: ini

    [workflow_engine]
    logging = /etc/st2/logging.workflowengine.conf

  After you have saved the configuration file you need to start the ``st2workflowengine`` service
  (all other services should already be running).

  .. code-block:: ini

    sudo st2ctl start

  You can verify that the new ``st2workflowengine`` service has indeed been started by running
  ``sudo st2ctl status`` and by inspecting the service log file at
  ``/var/log/st2/st2workflowengine.log``.

|st2| v2.7
----------

* Update output (result) object returned by the Windows runner so it's consistent with and matches
  the format returned by the local and remote runners.

  ``result`` attribute has been removed (same information is available in the ``stdout``
  attribute), ``exit_code`` renamed to ``return_code`` and two new attributes added -
  ``succeeded`` and ``failed``.

  Before:

  .. code-block:: python

    status: succeeded (1s elapsed)
    parameters:
      host: 10.0.0.1
      password: '********'
    result:
      stdout: "Uptime: 0 days, 18 hours, 15 minutes"
      stderr: ''
      result: "Uptime: 0 days, 18 hours, 15 minutes"
      exit_code: 0

  After:

  .. code-block:: python

    status: succeeded (1s elapsed)
    parameters:
      host: 10.0.0.1
      password: '********'
    result:
      stdout: "Uptime: 0 days, 18 hours, 15 minutes"
      stderr: ''
      return_code: 0
      succeeded: true
      failed: false

  Keep in mind that information contained in the ``result`` attribute which has been removed is
  also contained in ``stdout`` attribute so you only need to update your code if it relied on
  ``result`` and / or ``exit_code`` attribute being present.

|st2| v2.6
----------

* ``st2actions.runners.pythonrunner.Action`` class path for base Python runner actions has been
  deprecated since StackStorm v1.6.0 and will be fully removed in StackStorm v2.7.0. If you have
  any actions still using this path you are encouraged to update them to use
  ``st2common.runners.base_action.Action`` path.

  Old code:

  .. code-block:: python

    from st2actions.runners.pythonrunner import Action

  New code

  .. code-block:: python

    from st2common.runners.base_action import Action

|st2| v2.5
----------

* ``POST /v1/actionalias/match`` API endpoint now correctly returns a dictionary. Previously the
  code incorrectly returned an array with a single item (dictionary) on success. There is no need
  for this API endpoint to return an array since on success there will always only be a single
  item.

  If you have code which utilizes this API endpoint you need to update it to handle success
  response as a dictionary instead of an array with a single item (dictionary).

  Old response on a successful match:

  .. code-block:: json

    [
        {
            "actionalias": {
                "description": "Execute a command on a remote host via SSH.",
                "extra": {},
                "ack": {
                    "format": "Hold tight while I run command: *{{execution.parameters.cmd}}* on hosts *{{execution.parameters.hosts}}*"
                },
                "enabled": true,
                "name": "remote_shell_cmd",
                "result": {
                    "format": "Ran command *{{execution.parameters.cmd}}* on *{{ execution.result | length }}* hosts.\n\nDetails are as follows:\n{% for host in execution.result -%}\n    Host: *{{host}}*\n    ---> stdout: {{execution.result[host].stdout}}\n    ---> stderr: {{execution.result[host].stderr}}\n{%+ endfor %}\n"
                },
                "formats": [
                    "run {{cmd}} on {{hosts}}"
                ],
                "action_ref": "core.remote",
                "pack": "examples",
                "ref": "examples.remote_shell_cmd",
                "id": "59d2522a0640fd7e919fee7d",
                "uid": "action:examples:remote_shell_cmd"
            },
            "display": "run {{cmd}} on {{hosts}}",
            "representation": "run {{cmd}} on {{hosts}}"
        }
    ]

  New response on a successful match:

  .. code-block:: json

    {
        "actionalias": {
            "description": "Execute a command on a remote host via SSH.",
            "extra": {},
            "ack": {
                "format": "Hold tight while I run command: *{{execution.parameters.cmd}}* on hosts *{{execution.parameters.hosts}}*"
            },
            "enabled": true,
            "name": "remote_shell_cmd",
            "result": {
                "format": "Ran command *{{execution.parameters.cmd}}* on *{{ execution.result | length }}* hosts.\n\nDetails are as follows:\n{% for host in execution.result -%}\n    Host: *{{host}}*\n    ---> stdout: {{execution.result[host].stdout}}\n    ---> stderr: {{execution.result[host].stderr}}\n{%+ endfor %}\n"
            },
            "formats": [
                "run {{cmd}} on {{hosts}}"
            ],
            "action_ref": "core.remote",
            "pack": "examples",
            "ref": "examples.remote_shell_cmd",
            "id": "59d2522a0640fd7e919fee7d",
            "uid": "action:examples:remote_shell_cmd"
        },
        "display": "run {{cmd}} on {{hosts}}",
        "representation": "run {{cmd}} on {{hosts}}"
    }


|st2| v2.4
----------

* The ``st2kv`` function has been changed so that it no longer attempts to decrypt stored values by
  default. To return decrypted values, this must be explicitly enabled via parameter, e.g.:
  ``st2kv('st2_key_id', decrypt=true)``.

* The installation script now installs MongoDB 3.4 by default (previously, 3.2 was installed).
  For information on how to upgrade MongoDB on existing installations, please refer to the official
  MongoDB documentation - https://docs.mongodb.com/v3.4/release-notes/3.4-upgrade-standalone/,
  https://docs.mongodb.com/manual/release-notes/3.4-upgrade-replica-set/.

* Node.js v6 is now used by ChatOps. Previously v4 was used). See the :doc:`upgrades documentation
  <install/upgrades>` for how to switch to the Node.js v6 repositories.

|st2| v2.3
----------

* The ``dest_server`` parameter has been removed from the ``linux.scp`` action and replaced with
  the ``destination`` parameter.

  This offers more flexibility. ``source`` and ``destination`` parameters can now contain a
  local path or a full source/destination which includes the server part (e.g.
  ``server.fqdn:/etc/hosts``).

* The API endpoint for searching or showing packs has been updated to return an empty list
  instead of ``None`` when the pack was not found in the index. This is technically a breaking
  change, but a necessary one because returning ``None`` caused the client to throw an exception.

* Notifier now consumes the ``ActionExecution`` RabbitMQ exchange with queue name
  ``st2.notifiers.execution.work``. Notifier used to scan the ``LiveAction`` exchange with
  ``st2.notifiers.work`` queue name. When you upgrade from |st2| versions older than v2.3,
  make sure the ``st2.notifiers.work`` queue size is 0 before upgrading. If you upgrade when
  it's non-empty, you might miss notifications. Post-upgrade, please delete the ``st2.notifiers.work``
  queue manually using ``rabbitmqadmin delete queue name=st2.notifiers.work``. If this is not done, the
  queue will grow indefinitely and RabbitMQ will consume large amounts of disk space.
  See `issue 3622 <https://github.com/StackStorm/st2/issues/3622>`__ for details.

* Introduced a backward incompatible change (`PR #3514 <https://github.com/StackStorm/st2/pull/3514>`__)
  in the st2client API ``query()`` method. It returns a tuple of ``(result, total_number_of_items)``
  instead of ``result``. This is fixed in v2.3.2. Upgrade to v2.3.2 if you are seeing errors
  similar to those in issue `#3606 <https://github.com/StackStorm/st2/issues/3606>`_ or if you are
  using the st2client API's ``query()`` method.

|st2| v2.2
----------

* Additional validation has been introduced for triggers.

  1. Trigger payload is now validated against the trigger ``payload_schema`` schema when
     dispatching a trigger inside the sensor.

     Validation is only performed if the ``system.validate_trigger_payload`` config option is
     enabled and if the trigger object defines a ``payload_schema`` attribute.

  2. Trigger parameters are now validated for non-system (user-defined) triggers when creating
     a rule.

     Validation is only performed if the ``system.validate_trigger_parameters`` config option is
     enabled and if the trigger object defines ``parameters_schema`` attribute.

  Both of these configuration options are disabled by default with v2.2. In future they will be
  enabled by default.

* The database schema for Mistral has changed. The ``executions_v2`` table is no longer used. The
  table has been broken down into ``workflow_executions_v2``, ``task_executions_v2``, and
  ``action_executions_v2``. After upgrade, using the Mistral CLI commands such as
  ``mistral execution-list`` will return an empty table. The records in ``executions_v2`` have not
  been deleted. The commands are reading from the new tables. There is currently no migration
  script to move existing records from ``executions_v2`` into the new tables. To read from
  ``executions_v2``, either use ``psql`` or install an older version of the python-mistralclient in a
  separate Python virtual environment.

* If you’re seeing an error ``event_triggers_v2 already exists`` when running
  ``mistral-db-manage upgrade head``, this means the mistral services started before the
  ``mistral-db-manage`` commands were run. Refer to this :ref:`procedure <mistral_db_recover>` to
  recover the system.

* Jinja notations ``{{user.key}}`` and ``{{system.key}}`` to access datastore items under
  ``user`` and ``system`` scopes are now unsupported. Please use ``{{st2kv.user.key}}`` and
  ``{{st2kv.system.key}}`` notations instead. Also, please update your |st2| content
  (actions, rules and workflows) to use the new notation.

* When installing StackStorm using the installer script a random password is generated for MongoDB
  and PostgreSQL. This means you now need to explicitly pass the ``--config-file /etc/st2/st2.conf``
  argument to all ``st2`` CLI scripts (e.g. ``st2-apply-rbac-definitions``) which need access
  to the database (MongoDB). If you don't do that, "access denied" error will be returned, because
  it will try to use a default password when connecting to the database.

  .. code-block:: bash

    st2-apply-rbac-definitions --config-file /etc/st2/st2.conf

  If you need access to the plain-text version of the password used by StackStorm
  services to talk to MongoDB and PostgreSQL, you can find it in ``/etc/st2/st2.conf``
  (``[database]`` section) ``/etc/mistral/mistral.conf`` (``[database]`` section) files.

|st2| v2.1
----------

* **WARNING:** The following changes may require you to update your custom packs during the upgrade.

  * The ``version`` attribute in ``pack.yaml`` metadata must now contain a valid ``semver`` version
    string (``<major>.<minor>.<patch>``, e.g. ``1.0.1``). In addition, the ``email`` attribute must
    be a valid email address.

  * Pack ``ref`` and action parameter names can now only contain valid word characters (``a-z``,
    ``0-9`` and ``_``). No dashes! ``hpe_icsp`` is ok, but ``hpe-icsp`` is not.

  The ``st2ctl`` and ``st2-register-content`` scripts are now doing additional validation. If you
  happen to have a pack which doesn't satisfy these new validation criteria, it will fail to load.
  Therefore, to upgrade |st2| from v2.0.* to 2.1.*, follow these steps:

  1. Use ``yum`` or ``apt-get`` to upgrade to the newest version.

  2. Update community packs to the latest version from
     `StackStorm Exchange <https://exchange.stackstorm.org/>`__ with ``st2 pack install <pack>``.

  3. Reload the content with ``st2ctl reload --register-all``.

  4. If you have packs that don't satisfy the rules above, validation fails and the pack load will
     throw errors. Fix the packs to conform to the rules above, and reload the content again.

  In 2.1.0, |st2| attempts to auto-correct some validation failures and display a warning.
  In a future release this auto-correction will be removed. Please update your packs ASAP.

* `st2contrib <https://github.com/stackstorm/st2contrib>`__ is now deprecated and replaced by
  `StackStorm Exchange <https://exchange.stackstorm.org/>`__ . All the packs from
  `st2contrib <https://github.com/stackstorm/st2contrib>`__ have been migrated to StackStorm Exchange.
  For more information see :doc:`/reference/pack_management_transition`.

* Pack "subtree" repositories (repositories containing multiple packs inside the ``packs/`` subdir)
  are no longer supported. The subtree parameter in ``packs.install`` is removed. The new convention is
  one pack per git/GitHub repo. If you happen to use subtrees with your private packs, they will
  have to be split into multiple single-pack repositories in order for ``st2 pack install`` to be able
  to install the packs.

* The ``packs`` pack is deprecated starting from 2.1; in future versions it will be completely
  replaced with the ``st2 pack <...>`` commands and API endpoints.

* Pack metadata file (``pack.yaml``) can now contain a new ``ref`` attribute, in addition to ``name``.
  ``ref`` acts as a unique identifier; it offers for a more readable ``name``. For example, if a
  pack name is ``Travis CI``, a repo containing it is stackstorm-travis_ci, and ``ref`` is ``travis_ci``.
  Previously the pack files would live in ``travis_ci/`` directory and pack directory name served
  as a unique identifier for a pack.

* Support for ``.gitinfo`` file has been removed and as such the ``packs.info`` action has also been
  removed. All the pack directories at ``/opt/stackstorm/packs`` are now direct git checkouts of the
  corresponding pack repositories from Exchange or your own origin, so this file is not needed anymore.

* Datastore scopes are now ``st2kv.system`` and ``st2kv.user`` as opposed to ``system`` and ``user``.
  If you are accessing datastore items in your content, you should now use the Jinja expressions
  ``{{st2kv.system.foo}}`` and ``{{st2kv.user.foo}}``. The older Jinja expressions ``{{system.foo}}``
  and ``{{user.foo}}`` are still supported for backward compatibility but will be removed in future
  releases.

* Runners are now `pluggable`. With this version, we are piloting an ability to register
  runners just like other |st2| content. You can register runners by simply running
  ``st2ctl reload --register-runners``. This feature is in beta. No backward compatibility is
  guaranteed. Please wait for a release note indicating general availability of this feature.

* Config schemas now also support nested objects. Previously config schema and configuration files
  needed to be fully flat to be able to utilize default values from the config schema and dynamic
  configuration values.

  The config schema file can now contain arbitrary levels of nesting of the attributes and it will
  still work as expected.

  Old approach (flat schema):

  .. code-block:: yaml

    ---
      api_server_host:
        description: "API server host."
        type: "string"
        required: true
        secret: false
      api_server_port:
        description: "API server port."
        type: "integer"
        required: true
      api_server_token:
        description: "API server token."
        type: "string"
        required: true
        secret: true
      auth_server_host:
        description: "Auth server host."
        type: "string"
        required: true
        secret: false
      auth_server_port:
        description: "Auth server port."
        type: "integer"
        required: true

  New approach (nested schemas are supported):

  .. code-block:: yaml

    ---
      api_settings:
        description: "API related configuration options."
        type: "object"
        required: false
        additionalProperties: false
        properties:
          host:
            description: "API server host."
            type: "string"
            required: true
            secret: false
          port:
            description: "API server port."
            type: "integer"
            required: true
          token:
            description: "API server token."
            type: "string"
            required: true
            secret: true
      auth_settings:
        description: "Auth API related configuration options."
        type: "object"
        required: false
        additionalProperties: false
        properties:
          host:
            description: "Auth server host."
            type: "string"
            required: true
            secret: false
          port:
            description: "Auth server port."
            type: "integer"
            required: true

|st2| v2.0
----------

* ``st2ctl reload`` now also registers rules by default. Prior to this release actions, aliases,
  sensors, triggers and configs were registered. Now rules are also registered by default.
