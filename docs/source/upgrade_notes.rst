.. _upgrade_notes:

Upgrade Notes
=============

|st2| in development
--------------------

* Python runner actions can now return execution status (success, failure) by returning a tuple 
  from the Python action class ``run()`` method. First item in this tuple is a boolean flag
  indicating a success and the second one is the result. For example:

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

  For existing actions which don't return a status flag, same rules apply as before - action is
  considered as succeeded unless it throws an exception or exits with a non-zero exit code.

  If you have an existing action which returns a tuple with two items such as the one shown in the
  example below, you have two options.

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

* Old and deprecated Fabric based remote runner has been removed. This means
  ``ssh_runner.use_paramiko_ssh_runner`` config option is now obsolete and has no affect.
* Underscore (``_``) prefix has been removed from the ``sensor_service`` and ``config`` variable
  available on the ``Sensor`` and ``PollingSensor`` class. Those variables are now available via
  ``self.sensor_service`` and ``self.config`` respectively.

  For backward compatibility reasons and ease of migration, old approach will still work for the
  foreseeable future, but you are encouraged to upgrade your sensors to use the new way of
  referencing those variables.
* Support for loading content (sensors, actions and rules) from ``.json`` files has been removed.
  Support for JSON has been deprecated a long time ago and now the only support format is YAML
  files with ``.yaml`` extension).

  If you want to directly save content which you retrieve from the API using CLI on disk, you can
  now use ``--yaml`` flag which available to the ``list`` and ``get`` CLI commands (e.g.
  ``st2 rule get <rule ref> --yaml > packs/<my pack>/my_rule.yaml``).

* Pack config files which are located inside the pack directory (``config.yaml``) have been
  deprecated in favor of the new pack configuration v2. This new configuration approach offers more
  flexibility. In addition to that, those new config files are located outside the pack directory,
  in the ``/opt/stackstorm/configs/`` directory. This makes it easier to follow an infrastructure as code
  approach. Updating packs is also easier since |st2| user doesn't need to directly manipulate
  pack content anymore.

  For more information about the new pack configuration, please see :doc:`/pack_configs`.

* New ``log`` attribute has been added to the action execution object. This attribute is a list
  and contains all the state (status) transitions for executions (e.g. requested -> scheduled
  -> running -> complete, etc.).

  Keep in mind that this attribute will only be populated for new execution objects (ones which
  have been created after the upgrade to v1.5).

* Datastore data model has changed as of v1.5. We've introduced the notion of ``scope`` and
  ``secret``. See :ref:`Scoping items in datastore<datastore-scopes-in-key-value-store>` and
  :ref:`storing secrets in datastore<datastore-storing-secrets-in-key-value-store>` for details.

  A migration tool is provided (``/opt/stackstorm/st2/bin/st2-migrate-datastore-to-include-scope-secret.py``) if you are
  upgrading from older versions.

|st2| v1.4
----------

* ``matchregex`` rule criteria operator has been updated so now the dot character (``.``) also
  matches a new line. This makes the existing criteria patterns which use dot character more greedy.
  Previously, it didn't match new lines so some of the existing ``matchregex`` criteria patterns
  which operate on multi line strings might be affected.

  For example, let's say we have a following criteria pattern - ``.*stackstorm.*``. Previously,
  the following string - ``test\nstackstorm\ntest`` would not match, but now it does.

  If you are affected and you want to revert to the old behavior (less greedy matches), you can do
  so by modifying criteria pattern regular expression so it's less greedy (e.g. by adding ``^`` and
  / or ``$`` character or similar).

  ``matchregex`` is now deprecated in favor of ``regex`` and ``iregex`` operators.

* ``regex`` and ``iregex`` been added to the rule criteria operators list. These behave like
  ``re.search('pattern', trigger_value)`` and ``re.search('pattern',trigger_value, re.IGNORECASE)``
  in Python.  They do not have the DOTALL modifier. To match newline characters, they must be
  explicit in the search pattern.

* To make working with non-string positional parameters in the local and remote runner script
  actions easier, a simple new rules for parameter value serialization have been established.
  Previously all the values were serialized as Python literals which made all the parameters
  which type was not ``string`` very hard to parse and use in the script actions.

  More information about new positional parameter serialization rules can be found in the
  :ref:`documentation<ref-positional-parameters-serialization>`.

* The list of required and optional configuration arguments for the LDAP auth backend has changed.
  The LDAP auth backend supports other login name such as sAMAccountName. This requires a separate
  service account for the LDAP backend to query for the DN related to the login name for bind to
  validate the user password. Also, users must be in one or more groups specified in group_dns to
  be granted access.

* Mistral has deprecated the use of task name (i.e. ``$.task1``) to reference task result. It is
  replaced with a ``task`` function that returns attributes of the task such as id, state, result,
  and additional information (i.e. ``task(task1).result``).

|st2| v1.3
----------


* New ``abandoned`` action execution status has been introduced. State is applied to action execution
  when an actionrunner currently running some executions quits or is killed via TERM.This is therefore
  effectively a failure state as |st2| can no longer validate the state of this execution. Being a
  failure state any code that checks for an action failure should be updated to check for ``abandoned``
  state in addition to ``failed`` and ``timeout``.

|st2| v1.2
----------

* Refactor retries in the Mistral action runner to use exponential backoff. Configuration options
  for Mistral have changed. The options ``max_attempts`` and ``retry_wait`` are deprecated. Please
  refer to the configuration section of docs for more details.
* Change ``headers`` and ``params`` parameters in the ``core.http`` action from ``string`` to
  ``object``. If you have any code or rules which calls this action, you need to update it to
  pass in a new and correct type.
* Local runner has been updated so all the commands which are executed as a different user and
  result in using sudo set ``$HOME`` variable to the home directory of the target user. Previously,
  $HOME variable reflected the home directory of the user which executed sudo and under which
  action runner is running.

  Keep in mind that this condition is only met if action runner is running as root and / or if
  action runner is running a system user (stanley) and a different user is requested when running
  a command using ``user`` parameter.
* Support of default values is added to the API model. As a result, input parameters defined in
  the action metadata that is type of string no longer supports None or null.
* New ``timeout`` action execution status has been introduced. This status is a special type of
  a failure and implies an action timeout.

 All the existing runners (local, remote, python, http, action chain) have been updated to utilize
 this new status when applicable. Previously, if an action timed out, status was set to ``failed``
 and the timeout could only be inferred from the error message in the result object.

 If you have code which checks for an action failure you need to update it to also check for
 ``timeout`` in addition to ``failed`` status.

Upgrading from 1.1
~~~~~~~~~~~~~~~~~~

To upgrade a pre-1.2.0 StackStorm instance provisioned with the :doc:`install/all_in_one`, you will need to perform the following steps:

  1. Back up `/opt/puppet/hieradata/answers.json`.

  2. Update (or insert) the following lines in `/opt/puppet/hieradata/answers.yaml`:

  ```
  st2::version: 1.2.0
  st2::revision: 8
  st2::mistral_git_branch: st2-1.2.0
  hubot::docker: true
  ```

  If `answers.yaml` does not exist, create it. If you changed any install parameters manually (e.g. password, ChatOps token, SSH user), put these values into `answers.yaml` as well, otherwise they'll be overwritten.

  3. If you're running ChatOps, stop the Hubot service with `service hubot stop`.

  4. Remove `/etc/facter/facts.d/st2web_bootstrapped.txt` and execute `update-system`:

  ```
  sudo rm /etc/facter/facts.d/st2web_bootstrapped.txt
  sudo update-system
  ```

  5. After the update is done, restart StackStorm and hubot:

  ```
  sudo st2ctl restart
  sudo service docker-hubot restart
  ```

To verify the upgrade, please follow the link to run the :doc:`self-verification script <troubleshooting/self_verification>`.

|st2| v1.1
----------

Migrating to v1
~~~~~~~~~~~~~~~
The `st2_deploy scripted installer <https://docs.stackstorm.com/1.1/install/st2_deploy.html>`_ will upgrade v0.13 to v1.1. However we encourage to switch to :doc:`install/all_in_one`. To migrate to new All-in-one deployment from the existing pre v1.1 installations:

    1. Install |st2| on a new clean box with :doc:`install/all_in_one`.
    2. Copy the content from the previous installation to `/opt/stackstorm/packs`
       and reload it with `st2ctl reload --register-all`.
    3. Adjust the content according to upgrade notes below. Test and ensure your automations work.
    4. Save the audit log files from ``/var/log/st2/*.audit.log`` for future reference.
       We do not migrate execution history to the new installation, but all the execution data is
       kept in these structured logs for audit purpose.

    .. warning:: Don't run All-in-one installer over |st2| existing st2 deployment.

Changes
~~~~~~~
* Triggers now have a `ref_count` property which must be included in Trigger objects
  created in previous versions of |st2|. A migration script is shipped in
  ${dist_packages}/st2common/bin/migrate_triggers_to_include_ref_count.py on installation.
  The migration script is run as part of st2_deploy.sh when you upgrade from versions >= 0.13 to
  1.1.
* Messaging queues are now exlusive and in some cases renamed from previous versions. To
  remove old queues run the migration script
  ${dist_packages}/st2common/bin/migrate_messaging_setup.py on installation. The migration
  script is run as part of st2_deploy.sh when you upgrade from versions >= 0.13 to 1.1.
* Mistral moves to YAQL v1.0 and earlier versions of YAQL are deprecated. Expect some minor
  syntax changes to YAQL expressions.
* Mistral has implemented new YAQL function for referencing environment variables in the data
  context. The ``env()`` function replaces ``$.__env`` when referencing the environment variables.
  For example, ``$.__env.st2_execution_id`` becomes ``env().st2_execution_id``.
  **WARNING**: Referencing ``$.__env`` will lead to YAQL evaluation errors! Please update your workflows
  accordingly.
* Mistral has implemented new YAQL function for referencing task result. Given task1,
  the function call ``task(task1).result``, replaces ``$.task1`` when referencing result of task1.
  The old reference style will be fully deprecated in the next major release of Mistral, the
  OpenStack Mitaka release cycle.

|st2| v 0.11
------------

* Rules now have to be part of a pack. If you don't specify a pack,
  pack name is assumed to be `default`. A migration script
  (migrate_rules_to_include_pack.py) is shipped in ${dist_packages}/st2common/bin/
  on installation. The migration script
  is run as part of st2_deploy.sh when you upgrade from versions < 0.9 to 0.11.

|st2| v0.9
----------

* Process names for all |st2| services now start with "st2". sensor_container now runs as
  st2sensorcontainer, rules_engine runs as st2rulesengine, actionrunner now runs as
  st2actionrunner. st2ctl has been updated to handle the name change seamlessly. If you have tools
  that rely on the old process names, upgrade them to use new names.

* All |st2| tools now use "st2" prefix as well. rule_tester is now st2-rule-tester, registercontent
  is now st2-register-content.

* Authentication is now enabled by default for production (package based) deployments. For
  information on how to configure auth, see http://docs.stackstorm.com/install/deploy.html.

* For consistency reasons, rename existing runners as described below:

  * ``run-local`` -> ``local-shell-cmd``
  * ``run-local-script`` -> ``local-shell-script``
  * ``run-remote`` -> ``remote-shell-cmd``
  * ``run-remote-script`` -> ``remote-shell-script``
  * ``run-python`` -> ``python-script``
  * ``run-http`` -> ``http-request``

  Note: For backward compatibility reasons, those runners are still available
  and can be referenced through their old names, but you are encouraged to
  update your actions to use the new names.
