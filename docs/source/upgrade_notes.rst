.. _upgrade_notes:

Upgrade Notes
=============

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

|st2| v1.6
----------

* Python runner actions can now return execution status (success, failure) by returning a tuple
  from the Python action class ``run()`` method. The first item in this tuple is a boolean flag
  indicating success or failure and the second one is the result. For example:

  .. code-block:: python

    def run(self):
        #
        # Code to do something awesome
        #
        if something_awesome_working == True
            return (True, result)  #  Succeeded is True and the result from action on success
        return (False, result)  #  Succeeded is False and the result from action on failure

  This allows users to also return a result from a failing action. This result can then be used in
  workflows, etc. Previously this was not possible since the only way for action to be considered
  as failed was to throw an exception or exit with a non-zero exit code.

  **Note:**  This change is fully backward compatible unless you have an existing action which
  returns a tuple with two items.

  For existing actions which don't return a status flag, the same rules apply as before - an action
  is considered successful unless it throws an exception or exits with a non-zero exit code.

  If you have an existing action which returns a tuple with two items such as the one shown in the
  example below, you have two options:

  .. code-block:: python

    def run(self):
        result = ('item1', 'item2')
        return result

  1. Update action to return a list instead of a tuple.

     .. code-block:: python

        def run(self):
            result = ('item1', 'item2')
            return list(result)

     or

     .. code-block:: python

        def run(self):
            result = ['item1', 'item2']
            return result

  2. Update action to also return a status.

     .. code-block:: python

        def run(self):
            result = ('item1', 'item2')
            return (True, result)

|st2| v1.5
----------

* The previously deprecated Fabric-based remote runner has been removed. This means
  ``ssh_runner.use_paramiko_ssh_runner`` config option is now obsolete.

* Underscore (``_``) prefix has been removed from the ``sensor_service`` and ``config`` variable
  available on the ``Sensor`` and ``PollingSensor`` class. Those variables are now available via
  ``self.sensor_service`` and ``self.config`` respectively.

  For backward compatibility reasons and ease of migration, the old approach will still work, but
  you are encouraged to upgrade your sensors to use the new way of referencing those variables.

* Support for loading content (sensors, actions and rules) from ``.json`` files has been removed.
  Support for JSON was deprecated a long time ago and now the only supported format is YAML
  files with ``.yaml`` extension).

  If you want to directly save content which you retrieve from the API using CLI on disk, you can
  now use the ``--yaml`` flag with the ``list`` and ``get`` CLI commands (e.g.
  ``st2 rule get <rule ref> --yaml > packs/<my pack>/my_rule.yaml``).

* Pack config files located inside the pack directory (``config.yaml``) have been deprecated in
  favor of the new pack configuration v2. This new configuration approach offers more flexibility.
  In addition, those new config files are located outside the pack directory, in the
  ``/opt/stackstorm/configs/`` directory. This makes it easier to follow an infrastructure as code
  approach. Updating packs is also easier, as users don't need to directly manipulate
  pack content anymore.

  For more information about the new pack configuration, please see :doc:`/reference/pack_configs`.

* New ``log`` attribute has been added to the action execution object. This attribute is a list
  and contains all the state (status) transitions for executions (e.g. requested -> scheduled
  -> running -> complete, etc.).

  Keep in mind that this attribute will only be populated for new execution objects (those created
  after the upgrade to v1.5).

* The datastore data model has changed. We've introduced the notion of ``scope`` and
  ``secret``. See :ref:`Scoping items in datastore<datastore-scopes-in-key-value-store>` and
  :ref:`storing secrets in datastore<datastore-storing-secrets-in-key-value-store>` for details.

  A migration tool is provided (``/opt/stackstorm/st2/bin/st2-migrate-datastore-to-include-scope-secret.py``)
  if you are upgrading from older versions.

|st2| v1.4
----------

* ``matchregex`` rule criteria operator has been updated so now the dot character (``.``) also
  matches a new line. This makes the existing criteria patterns which use dot character more greedy.
  Previously, it didn't match new lines so some of the existing ``matchregex`` criteria patterns
  which operate on multi line strings might be affected.

  For example, let's say we have the following criteria pattern - ``.*stackstorm.*``. Previously,
  the following string - ``test\nstackstorm\ntest`` would not match, but now it does.

  If you are affected and you want to revert to the old behavior (less greedy matches), you can do
  so by modifying the criteria pattern regular expression so it's less greedy (e.g. by adding ``^``
  and/or ``$`` character or similar).

  ``matchregex`` is now deprecated in favor of ``regex`` and ``iregex`` operators.

* ``regex`` and ``iregex`` been added to the rule criteria operators list. These behave like
  ``re.search('pattern', trigger_value)`` and ``re.search('pattern',trigger_value, re.IGNORECASE)``
  in Python.  They do not have the DOTALL modifier. To match newline characters, they must be
  explicit in the search pattern.

* To make working with non-string positional parameters in the local and remote runner script
  actions easier, simple new rules for parameter value serialization have been established.
  Previously all the values were serialized as Python literals which made all the parameters
  with type other than ``string`` very hard to parse and use in the script actions.

  More information about new positional parameter serialization rules can be found in the
  :ref:`documentation<ref-positional-parameters-serialization>`.

* The list of required and optional configuration arguments for the LDAP authentication backend has
  changed. The LDAP authentication backend supports other login name such as sAMAccountName. This
  requires a separate service account for the LDAP backend to query for the DN related to the login
  name for bind to validate the user password. Also, users must be in one or more groups specified
  in ``group_dns`` to be granted access.

* Mistral has deprecated the use of task name (i.e. ``$.task1``) to reference task result. It is
  replaced with a ``task`` function that returns attributes of the task such as id, state, result,
  and additional information (i.e. ``task(task1).result``).

|st2| v1.3
----------


* New ``abandoned`` action execution status has been introduced. State is applied to action execution
  when an actionrunner currently running some executions quits or is killed via TERM. This is therefore
  effectively a failure state as |st2| can no longer validate the state of this execution. Being a
  failure state, any code that checks for an action failure should be updated to check for ``abandoned``
  state in addition to ``failed`` and ``timeout``.

|st2| v1.2
----------

* Refactor retries in the Mistral action runner to use exponential backoff. Configuration options
  for Mistral have changed. The options ``max_attempts`` and ``retry_wait`` are deprecated. Please
  refer to the configuration section of docs for more details.
* Change ``headers`` and ``params`` parameters in the ``core.http`` action from ``string`` to
  ``object``. If you have any code or rules that call this action, you need to update it to
  pass in a new and correct type.
* Local runner has been updated so all the commands which are executed as a different user and
  result in using ``sudo`` set ``$HOME`` variable to the home directory of the target user.
  Previously, the ``$HOME`` variable reflected the home directory of the user which executed
  ``sudo`` and under which action runner is running.

  Keep in mind that this condition is only met if action runner is running as root and/or if
  action runner is running a system user (stanley) and a different user is requested when running
  a command using ``user`` parameter.
* Support of default values is added to the API model. As a result, input parameters defined in
  the action metadata that is of type ``string`` no longer supports None or null.
* New ``timeout`` action execution status has been introduced. This status is a special type of
  a failure and implies an action timeout.

 All the existing runners (local, remote, python, http, action chain) have been updated to utilize
 this new status when applicable. Previously, if an action timed out, status was set to ``failed``
 and the timeout could only be inferred from the error message in the result object.

 If you have code which checks for an action failure you need to update it to also check for
 ``timeout`` in addition to ``failed`` status.

Upgrading from 1.1
~~~~~~~~~~~~~~~~~~

To upgrade a pre-1.2.0 StackStorm instance provisioned with the :doc:`install/all_in_one`, you will
need to perform the following steps:

1. Back up ``/opt/puppet/hieradata/answers.json``.

2. Update (or insert) the following lines in ``/opt/puppet/hieradata/answers.yaml``:

  .. code-block:: puppet

    st2::version: 1.2.0
    st2::revision: 8
    st2::mistral_git_branch: st2-1.2.0
    hubot::docker: true

  If ``answers.yaml`` does not exist, create it. If you changed any install parameters manually
  (e.g. password, ChatOps token, SSH user), put these values into ``answers.yaml`` as well,
  otherwise they'll be overwritten.

3. If you're running ChatOps, stop the Hubot service with ``service hubot stop``.

4. Remove ``/etc/facter/facts.d/st2web_bootstrapped.txt`` and execute ``update-system``:

  .. code-block:: bash

     sudo rm /etc/facter/facts.d/st2web_bootstrapped.txt
     sudo update-system

5. After the update is done, restart |st2| and hubot:

  .. code-block:: bash

    sudo st2ctl restart
    sudo service docker-hubot restart

To verify the upgrade, please follow the link to run the :doc:`self-verification script <troubleshooting/self_verification>`.

|st2| v1.1
----------

Migrating to v1
~~~~~~~~~~~~~~~
The ``st2_deploy scripted installer`` will upgrade v0.13 to v1.1. However we encourage you to switch
to :doc:`install/all_in_one`. To migrate to new All-in-one deployment from existing pre-v1.1
installations:

1. Install |st2| on a new clean box with :doc:`install/all_in_one`.
2. Copy the content from the previous installation to ``/opt/stackstorm/packs``
   and reload it with ``st2ctl reload --register-all``.
3. Adjust the content according to upgrade notes below. Test and ensure your automations work.
4. Save the audit log files from ``/var/log/st2/*.audit.log`` for future reference.
   We do not migrate execution history to the new installation, but all the execution data is
   kept in these structured logs for audit purpose.

.. warning:: Don't run the All-in-one installer over an existing |st2| deployment.

Changes
~~~~~~~
* Triggers now have a ``ref_count`` property which must be included in Trigger objects
  created in previous versions of |st2|. A migration script is provided at
  ``${dist_packages}/st2common/bin/migrate_triggers_to_include_ref_count.py``.
  The migration script is run as part of ``st2_deploy.sh`` when you upgrade from versions >= 0.13
  to v1.1.
* Messaging queues are now exclusive and in some cases renamed from previous versions. To
  remove old queues run the migration script
  ``${dist_packages}/st2common/bin/migrate_messaging_setup.py`` after installation. The migration
  script is run as part of ``st2_deploy.sh`` when you upgrade from versions >= 0.13 to v1.1.
* Mistral is updated to YAQL v1.0. Earlier versions of YAQL are deprecated. Expect some minor
  syntax changes to YAQL expressions.
* Mistral has implemented new YAQL function for referencing environment variables in the data
  context. The ``env()`` function replaces ``$.__env`` when referencing the environment variables.
  For example, ``$.__env.st2_execution_id`` becomes ``env().st2_execution_id``.

  **WARNING**: Referencing ``$.__env`` will lead to YAQL evaluation errors! Please update your workflows
  accordingly.
* Mistral has implemented new YAQL function for referencing task result. Given ``task1``,
  the function call ``task(task1).result``, replaces ``$.task1`` when referencing the result of
  ``task1``. The old reference style will be fully deprecated in the next major release of Mistral
  (the OpenStack Mitaka release cycle).

|st2| v 0.11
------------

* Rules now have to be part of a pack. If you don't specify a pack, the pack name is assumed to be
  ``default``. A migration script is installed at
  ``${dist_packages}/st2common/bin/migrate_rules_to_include_pack.py``. This migration script
  is run as part of ``st2_deploy.sh`` when you upgrade from versions < 0.9 to 0.11.

|st2| v0.9
----------

* Process names for all |st2| services now start with ``st2``. ``sensor_container`` now runs as
  ``st2sensorcontainer``, ``rules_engine`` runs as ``st2rulesengine``, ``actionrunner`` now runs as
  ``st2actionrunner``. ``st2ctl`` has been updated to handle the name change seamlessly. If you
  have tools that rely on the old process names, upgrade them to use the new names.

* All |st2| tools now use the ``st2`` prefix as well. ``rule_tester`` is now ``st2-rule-tester``,
  registercontent is now ``st2-register-content``.

* Authentication is now enabled by default for production (package based) deployments. For
  information on how to configure this, see :doc:`/authentication`.

* For consistency reasons, the runners have been renamed:

  * ``run-local`` -> ``local-shell-cmd``
  * ``run-local-script`` -> ``local-shell-script``
  * ``run-remote`` -> ``remote-shell-cmd``
  * ``run-remote-script`` -> ``remote-shell-script``
  * ``run-python`` -> ``python-script``
  * ``run-http`` -> ``http-request``

  Note: For backward compatibility reasons, those runners are still available and can be referenced
  through their old names, but you are encouraged to update your actions to use the new names.
