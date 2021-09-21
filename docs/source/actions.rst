Actions
=======

Actions are pieces of code that can perform arbitrary automation or remediation tasks in your
environment. They can be written in any programming language.

To give you a better idea, here is a short list of tasks which can be implemented as actions:

* restart a service on a server
* create a new cloud server
* acknowledge a Nagios/PagerDuty alert
* send a notification or alert via email or SMS
* send a notification to an IRC channel
* send a message to Slack
* start a Docker container
* snapshot a VM
* run a Nagios check

Actions can be executed when a :doc:`Rule </rules>` with matching criteria is triggered. Multiple
actions can be strung together into a :doc:`Workflow </workflows>`. Actions can also be executed
directly from the clients via CLI, API, or UI.

Managing and Running Actions
----------------------------

The CLI provides access to action management commands using the ``st2 action <command>`` format.
To see a list of available commands and their description, run:

.. code-block:: bash

   st2 action --help

To get more information on a particular action command, run: ``st2 action <command> -h``. For
example, the following will provide help for the action list command:

.. code-block:: bash

   st2 action list -h

The following commands show examples of how to obtain information on available actions and their
arguments:

.. code-block:: bash

   # List all available actions (note that output may be lengthy)
   st2 action list

   # List all actions in "linux" pack
   st2 action list -p linux

   # Display information for a particular action linux.check_loadavg
   st2 action get linux.check_loadavg

   # Alternatively, use CLI's run script to obtain information on an action's arguments:
   st2 run linux.check_loadavg -h

To execute an action manually, you can use ``st2 run <action with parameters>`` or
``st2 action execute <action with parameters>``:

.. code-block:: bash

   # Execute action immediately and display the results
   st2 run core.http url="http://httpbin.org/get"

   # Schedule action execution
   st2 action execute core.http url="http://httpbin.org/get"

   # Obtain execution results (the command below is provided as a tip in the output of the above command):
   st2 execution get 54fc83b9e11c711106a7ae01

   # If you want to add a trace tag to execution when you run it, you can use:
   st2 run core.local cmd=date --trace-tag="simple-date-check-`date +%s`"

Modification in Action Delete API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|st2| offers functionality to delete actions/workflows by invoking API. Prior to 3.6 release
this API was only de-registering actions from database. In the 3.6 release, with backward
compatibility retained this API was modified to optionally delete related action files from disk as well.

From CLI ``st2 action delete <pack>.<action>`` will delete only action database entry.
From CLI ``st2 action delete --remove-files <pack>.<action>`` or ``st2 action delete -r <pack>.<action>``
will delete action database entry along with files from disk.

API action DELETE method with ``{"remove_files": true}`` argument in json body will remove database
entry of action along with files from disk.
API action DELETE method with ``{"remove_files": false}`` or no additional argument in json body will
remove only action database entry.

* Usage:

.. code-block:: bash

   st2 action delete [-h] [-t TOKEN] [--api-key API_KEY] [-j] [-y] [-r]
                     ref-or-id

* Positional arguments:

.. code-block:: bash

   # Reference or ID of the action
   ref-or-id

* Optional arguments:

.. code-block:: bash

   -h, --help            show this help message and exit
   -t TOKEN, --token TOKEN
                         Access token for user authentication. Get
                         ST2_AUTH_TOKEN from the environment variables by
                         default
   --api-key API_KEY     Api Key for user authentication. Get ST2_API_KEY from
                         the environment variables by default
   -j, --json            Print output in JSON format
   -y, --yaml            Print output in YAML format
   -r, --remove-files    Delete action files from disk


Action Runners
--------------

An action runner is the execution environment for user-implemented actions. |st2| comes with
pre-canned action runners such as a remote runner and shell runner which provide for
user-implemented actions to be run remotely (via SSH) and locally. The objective is to allow the
action author to concentrate only on the implementation of the action itself rather than setting
up the environment.

Available Runners
~~~~~~~~~~~~~~~~~

The environment in which the action runs is specified by the runner. Currently the system provides
the following runners:

1.  ``local-shell-cmd`` - This is the local runner. This runner executes a Linux command on the
    host where |st2| is running.
2.  ``local-shell-script`` - This is the local runner. Actions are implemented as scripts. They are
    executed on the hosts where |st2| is running.
3.  ``remote-shell-cmd`` - This is a remote runner. This runner executes a Linux command on one or
    more remote hosts provided by the user.
4.  ``remote-shell-script`` - This is a remote runner. Actions are implemented as scripts. They run
    on one or more remote hosts provided by the user.
5.  ``python-script`` - This is a Python runner. Actions are implemented as Python classes with a
    ``run()`` method. They run locally on the same machine where |st2| components are running. The
    return value from the action ``run()`` method is either a tuple of success status flag and the
    result object respectively or it is just the result object. For more information, please refer
    to the :doc:`Action Runners </reference/runners>` section in the documentation.
6.  ``http-request`` - HTTP client which performs HTTP requests for running HTTP actions.
7.  ``action-chain`` - This runner supports executing simple linear work-flows. For more
    information, please refer to the :doc:`Workflows </workflows>` and
    :doc:`ActionChain </actionchain>` documentation.

8.  ``inquirer`` - This runner provides the core logic of the :doc:`Inquiries </inquiries>`
    feature.

    Note: This runner is an implementation detail for the ``core.ask`` action, and in most cases
    should not be referenced in other actions.
9. ``winrm-cmd`` - The WinRM command runner allows you to run the command-line interpreter (``cmd``) commands on Windows hosts using the WinRM protocol.
10. ``winrm-ps-cmd`` - The WinRM PowerShell command runner allows you to run the PowerShell commands on Windows hosts using the WinRM protocol.
11. ``winrm-ps-script`` - WinRM PowerShell script runner allows you to run PowerShell scripts on Windows hosts.
12. ``orquesta`` - This runner supports executing complex work-flows. For more
    information, please refer to the :doc:`Workflows </workflows>` and
    :doc:`Orquesta </orquesta/index>` documentation.


Runners come with their own set of input parameters. When an action is executed, it inherits the
runner parameters, in addition to its own parameters. The built-in parameters can be over-ridden on a per-action basis.

For a complete list of Runners and their parameters, see :doc:`/reference/runners`.


.. _ref-actions-writing-custom:

Writing Custom Actions
----------------------

An action is composed of two parts:

1. A YAML metadata file which describes the action, and its inputs.
2. A script file which implements the action logic

As noted above, an action script can be written in an arbitrary programming language, as long as
it follows these conventions:

1. Script should exit with ``0`` status code on success and non-zero on error
   (e.g. ``1``)
2. All log messages should be printed to standard error

.. _ref-action-metadata:

Action Metadata
~~~~~~~~~~~~~~~

Action metadata is used to describe the action and is defined as YAML. These attributes can be
present in the metadata file:

* ``name`` - Name of the action.
* ``runner_type`` - The type of runner to execute the action.
* ``enabled`` - Action cannot be invoked when disabled.
* ``entry_point`` - Location of the action launch script relative to the
  ``/opt/stackstorm/packs/${pack_name}/actions/`` directory.
* ``parameters`` - A dictionary of parameters and optional metadata describing type and default.
  The metadata is structured data following the `JSON Schema`_ specification draft 4. The common
  parameter types allowed are ``string``, ``boolean``, ``number`` (whole numbers and decimal
  numbers - e.g. ``1.0``, ``1``, ``3.3333``, etc.), ``object``, ``integer`` (whole numbers only -
  ``1``, ``1000``, etc.) and ``array``. If metadata is provided, input args are validated on
  action execution. Otherwise, validation is skipped.
* ``tags`` - An array with tags for this actions for the purpose of providing supplemental
  information

This is a sample metadata file for a Python action which sends an SMS via the Twilio web service:

.. code-block:: yaml

    ---
    name: "send_sms"
    runner_type: "python-script"
    description: "This sends an SMS using twilio."
    enabled: true
    entry_point: "send_sms.py"
    parameters:
        from_number:
            type: "string"
            description: "Your twilio 'from' number in E.164 format. Example +14151234567."
            required: true
            position: 0
        to_number:
            type: "string"
            description: "Recipient number in E.164 format. Example +14151234567."
            required: true
            position: 1
            secret: true
        body:
            type: "string"
            description: "Body of the message."
            required: true
            position: 2
            default: "Hello {% if system.user %} {{ st2kv.system.user }} {% else %} dude {% endif %}!"


This action is using a Python runner (``python-script``). The class that implements a ``run``
method is contained in a file called ``send_sms.py`` which is located in the same directory as the
metadata file. The action takes three parameters (``from_number``, ``to_number``, ``body``).

In the example above, the ``to_number`` parameter contains the attribute ``secret`` with value:
``true``. If an attribute is marked as a secret, the value of that attribute will be masked in the
|st2| service logs.

.. tip::

  Does your parameter only accept certain values? Use ``enum:`` with a list of allowed values. When the
  action is executed, it will only allow those specific values. And the in Web UI, it will be rendered
  as a drop-down list. 

  See the `examples.weather <https://github.com/StackStorm/st2/blob/master/contrib/examples/actions/weather.yaml#L16>`_
  action in the examples pack for how to use this.


Output Schema
~~~~~~~~~~~~~

|st2| supports modeling the output of an action or runner via the ``output_schema`` key
in the action definition. Action developers can create explicit, typed outputs for their actions.
This aids in workflow development and error handling.

For example, you have a python action that returns three keys: ``errors``, ``output``, and
``status_code``. ``error`` should be a list of strings, ``output`` should be a list of floats, and
``status_code`` should be an integer. ``errors`` is optional, whilst the others must be returned.
You can define the schema as follows:

.. code-block:: yaml

    ---
    ...
    output_schema:
        errors:
           type: array
           items:
               type: string
       output:
           required: true
           type: array
           items:
               type: number
       status_code:
           required: true
           type: integer

If the action output does not return the correct fields it will fail validation and the action
itself will fail. This prevents propagating corrupt data to other actions in a workflow, which
could lead to unpredictable results. In future this information will be used for pre-run workflow
validation.

Output schema validation is disabled by default in current versions of |st2|. To enable it, set
``validate_output_schema = True`` under ``[system]`` in ``/etc/st2/st2.conf``. 

If an action does not define any output schema, no enforcement is done. This allows you to
progressively update your actions, rather than doing them all at once.

As with all other input and output schema definitions in Stackstorm, we leverage
JSONschema to define ``output_schema``.


Parameters in Actions
~~~~~~~~~~~~~~~~~~~~~

In the previous example, you probably noticed how you can access parameters from the key-value
store by using the ``st2kv.system`` prefix in the template. You can also get access to variables
from the context of the execution. For example:

.. code-block:: yaml

    parameters:
      user:
        type: "string"
        description: "User of this action."
        required: true
        default: "{{action_context.api_user}}"

The prefix ``action_context`` is used to refer to variables in action context. Depending on how
the execution is executed and nature of action (simple vs workflow), variables in
``action_context`` change.

A simple execution via the API will only contain the variables ``user`` and ``pack``. An execution
triggered  via ChatOps will contain variables such as ``api_user``, ``user``, ``pack``, and
``source_channel``. In the ChatOps case, ``api_user`` is the user who entered the ChatOps command
from the Chat client and ``user`` is the |st2| user configured in hubot. ``source_channel`` is the
channel in which the ChatOps command was entered.

In addition to ``action_context`` you can also access ``config_context`` which contains the
key-value contents of your :doc:`pack configuration </reference/pack_configs>`. The example below
shows how you could use this for the default value for a parameter:

.. code-block:: yaml

    ---
    name: "send_sms"
    runner_type: "python-script"
    description: "This sends an SMS using twilio."
    enabled: true
    entry_point: "send_sms.py"
    parameters:
        from_number:
            type: "string"
            description: "Your twilio 'from' number in E.164 format. Example +14151234567."
            required: false
            position: 0
            default: "{{config_context.from_number}}"
        to_number:
            type: "string"
            description: "Recipient number in E.164 format. Example +14151234567."
            required: true
            position: 1
            secret: true
        body:
            type: "string"
            description: "Body of the message."
            required: true
            position: 2
            default: "Hello {% if system.user %} {{ st2kv.system.user }} {% else %} dude {% endif %}!"

In ActionChains and workflows (see :doc:`Workflow </workflows>`), every task in the workflow can
access the parent's ``execution_id``. For example, a task in an action chain is shown below:

.. code-block:: yaml

    ...
    -
      name: "c2"
      ref: "core.local"
      parameters:
        cmd: "echo \"c2: parent exec is {{action_context.parent.execution_id}}.\""
      on-success: "c3"
      on-failure: "c4"
    ...


Action Registration
~~~~~~~~~~~~~~~~~~~

To register a new action:

1. Place it into the pack content location.
2. Tell the system that the action is available.

The actions are grouped in :doc:`packs </packs>` and located at ``/opt/stackstorm/packs``

For hacking one-off actions, the convention is to use the ``default`` pack - just
create your action in ``/opt/stackstorm/packs/default/actions``. Once you have tested it out, you
should move it to a dedicated pack.

Register an individual action by calling ``st2 action create my_action_metadata.yaml``.
To reload all actions, use ``st2ctl reload --register-actions``


Built-in Parameters
-------------------

Action runners have their own built-in parameters. These are inherited by the action, and be over-ridden either
in the action metadata, or by passing additional parameters when running the action.

Some common parameters include:

* ``timeout`` - (all runners) The default timeout varies by runner type. This is frequently over-ridden
  for long-running actions.
* ``args`` - (``local-shell-script``, ``remote-shell-script``) By default, |st2| will assemble
  arguments based on whether a user defines named or positional arguments. Adjusts the format of
  arguments passed to ``cmd``.
* ``cmd``  - (``local-shell-script``, ``remote-shell-script``) Configure the command to be run
  on the target system.
* ``cwd``  - (``local-shell-script``, ``remote-shell-script``) Configure the directory where
  remote commands will be executed from.
* ``env``  - (``local-shell-script``, ``local-shell-script-script``, ``remote-shell-script``,
  ``remote-shell-script-script``, ``python-script``) Environment variables which will be
  available to the executed command/script.
* ``dir``  - (``local-shell-script``, ``remote-shell-script``) Configure the directory where
  scripts are copied from a pack to the target machine prior to execution.
  Defaults to ``/tmp``.

For a full list of built-in parameters for each runner type, see :doc:`/reference/runners`.

Overriding Runner Parameters
----------------------------

Parameters of runners can be overridden. Sometimes it's necessary to customize and simplify an
action. Take the following ``linux.rsync`` action that is included in the linux pack.

The ``linux.rsync`` action overrides the ``cmd`` parameter in the ``remote-shell-cmd`` runner with
the ``rsync`` command with appropriate args passed from the action parameters defined for the
``linux.rsync`` action:

.. literalinclude:: /../../st2/contrib/linux/actions/rsync.yaml
   :language: yaml

Not all attributes for runner parameters can be overridden. A list of attributes which can be
overriden is included below:

.. include:: _includes/runner_parameters_overridable_attributes.rst

Overriding attributes such as ``type`` and ``position`` are not allowed because overriding them can
potentially break the action since the runner will not be able to consume the type of value being
passed (e.g. runner parameter is expecting an integer but a string is passed).

Environment Variables Available to Actions
------------------------------------------

By default, local, remote and Python runners make the following environment variables available
to the actions:

* ``ST2_ACTION_PACK_NAME`` - Name of the pack to which the currently executed action belongs to.
* ``ST2_ACTION_EXECUTION_ID`` - Execution ID of the action being currently executed.
* ``ST2_ACTION_API_URL`` - Full URL to the public API endpoint.
* ``ST2_ACTION_AUTH_TOKEN`` - Auth token which is available to the action until it completes.
  When the action completes, the token gets revoked.

Here is an example of how you can use these environment variables inside a local shell script
action.

.. sourcecode:: bash

    #!/usr/bin/env bash

    # Retrieve a list of actions by hitting the API using cURL and the information provided
    # via environment variables

    RESULT=$(curl -H "X-Auth-Token: ${ST2_ACTION_AUTH_TOKEN}" ${ST2_ACTION_API_URL}/actions)
    echo ${RESULT}

.. _ref-actions-converting-scripts:

Converting Existing Scripts into Actions
----------------------------------------

If you have an existing standalone script written in an arbitrary programming or scripting
language and you want to convert it to an action, the process is very simple.

Follow these steps:

1. Make sure the script conforms to conventions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You should make sure that the script exits with a zero status code on success and non-zero on
error. This is important since the exit code is used by |st2| to determine if the script has
finished successfully.

2. Create a metadata file
~~~~~~~~~~~~~~~~~~~~~~~~~

You need to create a metadata file which describes the script name, description, entry point,
which runner to use and script parameters (if any).

When converting an existing script, you will want to use either the ``local-shell-script``
or ``remote-shell-script`` runner.

2. Update argument parsing in the script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    If your script doesn't take any arguments, you can skip this step.

Local and remote script runners recognize two types of parameters:

1. ``named`` - those parameters do not include the ``position`` attribute.
2. ``positional`` - those parameters include the ``position`` attribute.

All parameters are passed to the script via command-line arguments.

Named argument are passed to the script in the following format:

.. code-block:: bash

    script.sh --param1=value --param2=value --param3=value

By default, each parameter is prefixed with two dashes (``--``). If you want to use a single dash
(``-``), some other prefix or no prefix at all, you can configure that using the ``kwarg_op``
parameter in the metadata file.

For example:

.. code-block:: yaml

    ---
    name: "my_script"
    runner_type: "remote-shell-script"
    description: "Script which prints arguments to stdout."
    enabled: true
    entry_point: "script.sh"
    parameters:
        key1:
            type: "string"
            required: true
        key2:
            type: "string"
            required: true
        key3:
            type: "string"
            required: true
        kwarg_op:
            type: "string"
            immutable: true
            default: "-"

In this case, arguments are passed to the script in the following format:

.. code-block:: bash

    script.sh -key1=value1 -key2=value2 -key3=value3

Positional arguments are passed to the script ordered by the ``position`` value in the following
format:

.. code-block:: bash

    script.sh value2 value1 value3

.. _ref-positional-parameters-serialization:

If your script only uses positional arguments (which is often the case for existing scripts), you
simply need to declare parameters with the correct value for the ``position`` attribute in the metadata file. Positional arguments are serialized based on the simple rules described below:

1. ``string``, ``integer``, ``float`` - Serialized as a string.
2. ``boolean`` - Serialized as a string ``1`` (true) or ``0`` (false).
3. ``array`` - Serialized as a comma delimited string (e.g. ``foo,bar,baz``).
4. ``object`` - Serialized as JSON.

Using this simple serialization format allows users to easily utilize those values in their
scripts by using standard Bash functionality (``-z`` for check if a value is provided, ``-eq`` for
comparison to 1/0 and ``IFS`` for splitting a string into an array). For working with objects, you
can use a tool such as `jq`_.

If no value is provided for a particular positional parameter, |st2| will pass an empty string
``""`` as a value for that parameter to the script.

For example, if a second positional parameter is optional and user provides no value, the script
will be called like this:

.. code-block:: bash

    script.sh value1 "" value3


The ``immutable`` value defines whether the default value of a parameter can be overridden. This
is particularly important if you expose commands via ChatOps and do not like security related
parameters to be manipulated by user input.


Example 1 - existing Bash script with positional arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say we have a simple Bash script named ``send_to_syslog.sh`` which writes the message
provided via the command line argument to syslog.

The script takes two arguments:

1. The address of the syslog server
2. The message to write

.. sourcecode:: bash

    #!/usr/bin/env bash

    SERVER=$1
    MESSAGE=$2
    logger -n ${SERVER} ${MESSAGE}

Since this script is using positional arguments, you only need to define them in the metadata file:

.. code-block:: yaml

    ---
    name: "send_to_syslog.log"
    runner_type: "remote-shell-script"
    description: "Send a message to a provided syslog server."
    enabled: true
    entry_point: "send_to_syslog.sh"
    parameters:
        server:
            type: "string"
            description: "Address of the syslog server"
            required: true
            position: 0
        message:
            type: "string"
            description: "Message to write"
            required: true
            position: 1

As you can see above, we declare two parameters - ``server`` and ``message``. Both of them declare
a ``position`` attribute (0 for server and 1 for message), which means they will be passed to the
action script as positional arguments, so your script doesn't require any changes.

Writing Custom Python Actions
-----------------------------

In the simplest form, a Python action is a module which exposes a class which inherits from
:class:`st2common.runners.base_action.Action` and implements a ``run`` method.

Sample Python Action
~~~~~~~~~~~~~~~~~~~~

Metadata file (``my_echo_action.yaml``):

.. code-block:: yaml

    ---
    name: "echo_action"
    runner_type: "python-script"
    description: "Print message to standard output."
    enabled: true
    entry_point: "my_echo_action.py"
    parameters:
        message:
            type: "string"
            description: "Message to print."
            required: true
            position: 0


Action script file (``my_echo_action.py``):

.. code-block:: python

    import sys

    from st2common.runners.base_action import Action

    class MyEchoAction(Action):
        def run(self, message):
            print(message)

            if message == 'working':
                return (True, message)
            return (False, message)

This Python action prints text provided via the ``message`` parameter to the standard output. As
you can see, user-supplied action parameters are passed to the ``run`` method as keyword arguments.

If the ``run`` method finishes without exceptions, the execution is successful, and the value
returned by the method (any value: boolean, string, list, dict, etc.) is considered its result.
Raising an exception will report the execution as failed.

Another way to specify the status of an execution is returning a tuple with two items: the first
item is a boolean indicating status, the second item is the result itself.

For example, ``return False`` will result in a successful execution with the result being
``False``, and ``return (False, "Failed!")`` is a failed execution with ``"Failed!"`` as its
result.

In the example above, if the ``message`` parameter passed to the action is ``working``, the action
will be considered as succeeded (first flag in the result indicating action status is ``True``).
If another message is passed in, action will be considered as failed (first flag in the result
tuple indicating action status is ``False``).

For a more complex example, please refer to the `actions in the Libcloud pack in
StackStorm Exchange <https://github.com/StackStorm-Exchange/libcloud/tree/master/actions>`_.

Configuration File
~~~~~~~~~~~~~~~~~~

.. note::

    The configuration file should be used to store "static" configuration options which don't
    change between the action runs (e.g. service credentials, different constants, etc.).

    For options/parameters which are user defined or change often, you should use action
    parameters which are defined in the metadata file.

Python actions can store arbitrary configuration in the configuration file which is global to the whole pack. The configuration is stored in a file named ``<pack_name>.yaml``, in the
``/opt/stackstorm/configs/`` directory.

The configuration file format is YAML. Configuration is automatically parsed and passed to the action class constructor via the ``config`` argument.  See the
:doc:`pack configuration doc</reference/pack_configs>` for more details.

Logging
~~~~~~~

All logging inside the action should be performed via the logger which is specific to this action
and available via the ``self.logger`` class attribute.

This logger is a standard Python logger from the ``logging`` module so all the logger methods work
as expected (e.g. ``logger.debug``, ``logger.info``, etc).

For example:

.. sourcecode:: python

    def run(self):
        ...
        success = call_some_method()

        if success:
            self.logger.info('Action successfully completed')
        else:
            self.logger.error('Action failed...')

Action Service
~~~~~~~~~~~~~~

Similar to sensors, ``action_service`` is available on each action instance after instantiation.

Action service provides different services to the action via public methods. Right now it supports
datastore management methods. This allows actions to utilize the datastore to store arbitrary data
between executions.

The action service provides the same datastore management methods as the ones available on the
sensor service. You can find more details in the
:ref:`sensor datastore management documentation<ref-sensors-datastore-management-operations>`.

Example storing a dict as JSON:

.. sourcecode:: python

    def run(self):
      data = {'somedata': 'foobar'}

      # Add a value to the datastore
      self.action_service.set_value(name='cache', value=json.dumps(data))

      # Retrieve a value
      value = self.action_service.get_value('cache')
      retrieved_data = json.loads(value)

      # Retrieve an encrypted value
      value = self.action_service.get_value('ma_password', decrypt=True)
      retrieved_data = json.loads(value)

      # Delete a value
      self.action_service.delete_value('cache')

Sharing code between Python Sensors and Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Refer to :ref:`documentation <ref-shared-libs-python-sensors-actions>` on sharing common code
between python actions and sensors.

Pre-defined Actions
-------------------

There are several predefined actions that come out of the box with |st2|. These are in the ``core``
pack:

* ``core.local`` : This action allows execution of arbitrary \*nix/shell commands locally. You can
  execute this command via the CLI using:

  .. code-block:: bash

    st2 run core.local cmd='ls -l'

* ``core.remote`` : This action allows execution of arbitrary \*nix/shell commands on a set of
  boxes. Execute this command via the CLI with:

  .. code-block:: bash

    st2 run core.remote cmd='ls -l' hosts='host1,host2' username='user1'

* ``core.http`` : This action allows execution of http requests. Think ``curl`` executed from the
  |st2| box:

  .. code-block:: bash

    st2 run core.http url="http://httpbin.org/get" method="GET"

  Similar to ``curl``, this action supports basic authentication when provided a username and
  password:

  .. code-block:: bash

    st2 run core.http url="http://httpbin.org/get" method="GET" username=user1 password=pass1

To see all actions in the ``core`` pack:

.. code-block:: bash

    st2 action list --pack=core

.. rubric:: What's Next?

* Explore packs and actions contributed by |st2| developers and community in the `StackStorm Exchange <https://exchange.stackstorm.org>`_.
* Check out `tutorials on stackstorm.com <https://stackstorm.com/category/tutorials/>`__ on creating actions, and other practical examples of automating with |st2|.

.. _JSON Schema: http://json-schema.org/documentation.html
.. _jq: https://stedolan.github.io/jq/
