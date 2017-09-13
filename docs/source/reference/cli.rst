CLI Reference
=============

The |st2| command line client (CLI) ``st2`` allows you to operate your |st2| system using the
command line. It communicates with the |st2| processes using public APIs.

Installation
------------

The CLI client is installed by default on your |st2| system. It can also be installed on a client
system using ``pip``:

.. sourcecode:: bash

    pip install st2client


.. _cli-configuration:

Configuration
-------------

The command line client can be configured using one or more of the approaches
listed below:

* Configuration file (``~/.st2/config``)
* Environment variables (``ST2_API_URL``, etc.)
* Command line arguments (``st2 --cacert=... action list``, etc.)

Command line arguments have highest precedence, followed by environment variables, and then
configuration file values. 

If the same value is specified in multiple places, the value with the highest precedence will be
used. For example, if ``api_url`` is specified in the configuration file and in an environment
variable (``$ST2_API_URL``), the environment variable will be used.

Configuration File
~~~~~~~~~~~~~~~~~~

The CLI can be configured through an ini-style configuration file. By default, ``st2`` will
use the file at ``~/.st2/config``.

If you want to use configuration from a different file (e.g. you have one config per deployment
or environment), you can select which file to use using the ``ST2_CONFIG_FILE`` environment
variable or the ``--config-file`` command line argument.

For example (environment variable):

.. sourcecode:: bash

    ST2_CONFIG_FILE=~/.st2/prod-config st2 action list

For example (command line argument):

.. sourcecode:: bash

    st2 --config-file=~/.st2/prod-config action list

An example configuration file with all the options and the corresponding explanations is
included below:

.. literalinclude:: ../../../st2/conf/st2rc.sample.ini
    :language: ini

If you want the CLI to skip parsing of the configuration file, you can do that by passing the
``--skip-config`` flag to the CLI:

.. sourcecode:: bash

    st2 --skip-config action list

.. _cli-auth-token-caching:

Authentication and Auth Token Caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The previous section showed an option for storing your password in plaintext in your configuration
file. The ``st2 login`` command offers an alternative that does not store the password in plaintext.
Similar to ``st2 auth``, you must provide your username and password:

.. sourcecode:: bash

    st2 login st2admin --password 'Password1!'

This command caches your authentication token, but also modifies the CLI configuration to include
the referenced username. This way, future commands will know which cached token to use for
authentication, since tokens are cached using the ``token-<username>`` format. The password itself
does not need to be stored in the config file.

.. WARNING::
   ``st2 login`` will overwrite the "credentials" section of the configuration.
   It will overwrite the configured username and will remove any configured password.

These auth tokens are by default cached on the local filesystem (in the ``~/.st2/token-<username>``
file) and re-used for subsequent requests to the API service. You will need to re-login once the
generated token has expired, or use of the ``--write-password`` flag, which writes the password to
the config.

The ``st2 whoami`` command will tell you who is the currently authenticated user.

You can switch between users by re-running the ``st2 login`` command. Any existing users' token
cache files will remain, but the CLI configuration will be changed to point to the new username.

.. NOTE::
   As with many other ``st2`` commands, ``st2 login`` will not create the configuration file
   for you. Keep this in mind especially if you're leveraging the ``--config-file`` CLI option,
   or similar.

You can still use the "old" method of supplying both username and password in the configuration
file. If both a username and password are present in the configuration, then the client will
automatically try to authenticate with these credentials.

If you want to disable auth token caching and want the CLI to retrieve a new auth token on each
invocation, set ``cache_token`` to ``False``:

.. sourcecode:: ini

    [cli]
    cache_token = False

The CLI will by default also try to retrieve a new token if an existing one has expired.

If you have manually deleted or revoked a token before expiration you can clear the cached token
by removing the ``~/.st2/token`` file.

If the configuration file has an API key as authentication credentials, the CLI will use that as
the primary method of authentication instead of auth token.

.. sourcecode: ini

    [credentials]
    api_key = ZDAwTQx...ZTI3ZQ

Using Debug Mode
----------------

The command line tools accepts the ``--debug`` flag. When this flag is provided,
debug mode will be enabled. Debug mode consists of the following:

* On error/exception, full stack trace and client settings (API URL, auth URL, proxy information,
  etc.) are printed to the console.
* The equivalent ``curl`` command for each request is printed to the console. This makes it easy
  to reproduce actions performed by the CLI using ``curl``.
* Raw API responses are printed to the console.

For example:

.. sourcecode:: bash

    st2 --debug action list --pack=core

Example output (no error):

.. sourcecode:: bash

    st2 --debug action list --pack=core
    # -------- begin 140702450464272 request ----------
    curl -X GET -H  'Connection: keep-alive' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'User-Agent: python-requests/2.5.1 CPython/2.7.6 Linux/3.13.0-36-generic' 'http://localhost:9101/v1/actions?pack=core'
    # -------- begin 140702450464272 response ----------
    [
        {
            "runner_type": "http-runner",
            "name": "http",
            "parameters": {
            ...

Example output (error):

.. sourcecode:: bash

    st2 --debug action list --pack=core
    ERROR: ('Connection aborted.', error(111, 'Connection refused'))

    Client settings:
    ----------------
    ST2_BASE_URL: http://localhost
    ST2_AUTH_URL: https://localhost:9100
    ST2_API_URL: http://localhost:9101/v1

    Proxy settings:
    ---------------
    HTTP_PROXY:
    HTTPS_PROXY:

    Traceback (most recent call last):
      File "./st2client/st2client/shell.py", line 175, in run
        args.func(args)
      File "/data/stanley/st2client/st2client/commands/resource.py", line 218, in run_and_print
        instances = self.run(args, **kwargs)
      File "/data/stanley/st2client/st2client/commands/resource.py", line 37, in decorate
        return func(*args, **kwargs)
        ...

Using CLI in Scripts
--------------------

The CLI returns a non-zero return code for any erroneous operation. You can capture
the return code of CLI commands to check whether the command succeeded.

For example:

.. sourcecode:: bash

    st2 action get twilio.send_sms

    +-------------+--------------------------------------------------------------+
    | Property    | Value                                                        |
    +-------------+--------------------------------------------------------------+
    | id          | 54bfff490640fd2f6224ac1a                                     |
    | ref         | twilio.send_sms                                              |
    | pack        | twilio                                                       |
    | name        | send_sms

Now, let's get the exit code of the previous command:

.. sourcecode:: bash

    echo $?

    0

Now, let's run a command that we know will fail:

.. sourcecode:: bash

    st2 action get twilio.make_call

    Action "twilio.make_call" is not found.

Let's check the exit code of the last command:

.. sourcecode:: bash

    echo $?

    2

Obtaining an Authentication Token in Scripts
--------------------------------------------

If you want to authenticate and obtain an authentication token inside your (shell) scripts, you can
use the ``st2 auth`` CLI command in combination with the ``-t`` flag.

This flag will cause the command to only print the token to ``stdout`` on successful
authentication. This means you don't need to deal with parsing JSON or CLI output format.

Example usage:

.. sourcecode:: bash

    st2 auth test1 -p 'testpassword' -t

    0280826688c74bb9bd541c26631df298

Example usage inside a Bash script:

.. sourcecode:: bash

    TOKEN=$(st2 auth test1 -p 'testpassword' -t)

    # Now you can use the token (e.g. pass it to other commands, set an
    # environment variable, etc.)
    echo ${TOKEN}

Changing the CLI Output Format
------------------------------

By default, the CLI returns and prints results in a user-friendly table-oriented
format:

.. sourcecode:: bash

    st2 action list --pack=slack

    +--------------------+-------+--------------+-------------------------------+
    | ref                | pack  | name         | description                   |
    +--------------------+-------+--------------+-------------------------------+
    | slack.post_message | slack | post_message | Post a message to the Slack   |
    |                    |       |              | channel.                      |
    +--------------------+-------+--------------+-------------------------------+

If you want a raw JSON result as returned by the API (e.g. you are using the CLI as part of your
script and you want the raw result which you can parse), you can pass the ``-j`` flag:

.. sourcecode:: bash

    st2 action list -j --pack=slack

    [
        {
            "description": "Post a message to the Slack channel.",
            "name": "post_message",
            "pack": "slack",
            "ref": "slack.post_message"
        }
    ]

Only Displaying a Particular Attribute
--------------------------------------

By default, when retrieving the action execution result using ``st2 execution get``,
the whole result object will be printed:

.. sourcecode:: bash

    st2 execution get 54d8c52e0640fd1c87b9443f

    STATUS: succeeded
    RESULT:
    {
        "failed": false,
        "stderr": "",
        "return_code": 0,
        "succeeded": true,
        "stdout": "Mon Feb  9 14:33:18 UTC 2015"
    }

If you only want to retrieve a specific result attribute, use the ``-k <attribute name>`` flag:

.. sourcecode:: bash

    st2 execution get -k stdout 54d8c52e0640fd1c87b9443f

    Mon Feb  9 14:33:18 UTC 2015

If you only want to retrieve and print out a specific attribute of the execution,
you can do that using ``--attr <attribute name>`` flag.

For example, if you only want to print ``start_timestamp`` attribute of the result
object:

.. sourcecode:: bash

    st2 execution get 54d8c52e0640fd1c87b9443f -a start_timestamp

    start_timestamp: 2015-02-24T23:01:15.088293Z

You can also specify multiple attributes:

.. sourcecode:: bash

    st2 execution get 54d8c52e0640fd1c87b9443f --attr status result.stdout result.stderr

    status: succeeded
    result.stdout: Mon Feb  9 14:33:18 UTC 2015

    result.stderr:

Similarly for the ``execution list`` command:

.. sourcecode:: bash

    st2 execution list -a id status result

    +--------------------------+-----------+---------------------------------+
    | id                       | status    | result                          |
    +--------------------------+-----------+---------------------------------+
    | 54eb51000640fd34e0a9a2ce | succeeded | {u'succeeded': True, u'failed': |
    |                          |           | False, u'return_code': 0,       |
    |                          |           | u'stderr': u'', u'stdout':      |
    |                          |           | u'2015-02-23                    |
    |                          |           | 16:10:39.916375\n'}             |
    | 54eb51000640fd34e0a9a2d2 | succeeded | {u'succeeded': True, u'failed': |
    |                          |           | False, u'return_code': 0,       |
    |                          |           | u'stderr': u'', u'stdout':      |
    |                          |           | u'2015-02-23                    |
    |                          |           | 16:10:40.444848\n'}             |


Escaping Shell Variables
------------------------

When you use local and remote actions (e.g. ``core.local``, ``core.remote``, etc.), you need to
wrap ``cmd`` parameter values in a single quote or escape the variables. Otherwise, the shell
variables will be expanded locally which is something you usually don't want.

Using single quotes:

.. sourcecode:: bash

    st2 run core.local env='{"key1": "val1", "key2": "val2"}' cmd='echo "ponies ${key1} ${key2}"'

Escaping the variables:

.. sourcecode:: bash

    st2 run core.remote hosts=localhost env='{"key1": "val1", "key2": "val2"}' cmd="echo ponies \${key1} \${key2}

Specifying Parameters with Type "array"
---------------------------------------

When running an action using ``st2 run`` command, you specify the value of parameters with type
``array`` as a comma delimited string.

Inside the CLI, this string gets split on commas and passed to the API as a list.

Example 1 - Simple Case (Array of Strings)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sourcecode:: bash

    st2 run mypack.myaction parameter_name="value 1,value2,value3"

In this case, the ``parameter_name`` value would get passed to the API as a list (JSON array) with
three items - ``["value 1", "value2", "value3"]``.

Example 2 - Complex Case (Array of Objects)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you want to pass more complex type (e.g. arrays of objects) value to an action, you can do it
like this:

.. sourcecode:: bash

    st2 run mypack.set_interfaces \
      nic_info="target:eth0,ipaddr:192.168.0.10,netmask:255.255.255.0,mtu=1454" \
      nic_info="target:eth1,ipaddr:192.168.0.11,netmask:255.255.255.0,mtu=2000"

In this case, the ``nic_info`` value passed to the ``mypack.set_interfaces`` action would be parsed
and look like this:

.. sourcecode:: bash

    [{'netmask': '255.255.255.0', 'ipaddr': '192.168.0.10', 'target': 'eth0', 'mtu': 1454},
     {'netmask': '255.255.255.0', 'ipaddr': '192.168.0.11', 'target': 'eth1', 'mtu': 2000}]

To parse each value in the object as an expected type, you need to specify the type of each value
in the action metadata, like this.

.. sourcecode:: bash

    parameters:
      nic_info:
        type: array
        properties:
          target:
            type: string
          ipaddr:
            type: string
          netmask:
            type: string
          mtu:
            type: integer

Or you can use JSON notation:

.. sourcecode:: bash

    st2 run mypack.myaction parameter_name='[{"Name": "MyVMName"}]'

.. include:: ../_includes/_cli_json_string_escaping.rst

Specifying Parameters with Type "object"
----------------------------------------

When running an action using ``st2 run`` command, you can specify the value of parameters with type
``object`` using two different approaches:

JSON String Notation
~~~~~~~~~~~~~~~~~~~~

For complex objects, you should use JSON notation:

.. sourcecode:: bash

    st2 run core.remote hosts=localhost env='{"key1": "val1", "key2": "val2"}' cmd="echo ponies \${key1} \${key2}

.. include:: ../_includes/_cli_json_string_escaping.rst

Comma-delimited ``key=value`` Pairs String Notation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For simple objects (such as specifying a dictionary where both keys and values are simple strings),
use this notation:

.. sourcecode:: bash

    st2 run core.remote hosts=localhost env="key1=val1,key2=val2" cmd="echo ponies \${key1} \${key2}"

Reading Parameter Values From a File
------------------------------------

The CLI also supports the special ``@parameter`` notation which makes it read parameter
values from a file.

An example of when this might be useful is when you are using http runner actions, or when you want
to read information such a private SSH key content from a file.

Example:

.. sourcecode:: bash

    st2 run core.remote hosts=<host> username=<username> @private_key=/home/myuser/.ssh/id_rsa cmd=<cmd>

Re-running an Action
--------------------

To re-run a particular action, you can use the ``st2 execution re-run <existing
execution id>`` command.

By default, this command re-runs an action with the same set of input parameters
which were used with the original action.

The command takes the same arguments as the ``run``/``action execute`` command. This means you can
pass additional runner or action specific parameters to the command. Those parameters are then
merged with the parameters from the original action and used to run a new action.

For example:

.. sourcecode:: bash

    st2 run core.local env="VAR=hello" cmd='echo $VAR; date'
    .
    +-----------------+--------------------------------+
    | Property        | Value                          |
    +-----------------+--------------------------------+
    | id              | 54e37a3c0640fd0bd07b1930       |
    | context         | {                              |
    |                 |     "user": "stanley"          |
    |                 | }                              |
    | parameters      | {                              |
    |                 |     "cmd": "echo $VAR; date",  |
    |                 |     "env": {                   |
    |                 |         "VAR": "hello"         |
    |                 |     }                          |
    |                 | }                              |
    | status          | succeeded                      |
    | start_timestamp | Tue, 17 Feb 2015 17:28:28 UTC  |
    | result          | {                              |
    |                 |     "failed": false,           |
    |                 |     "stderr": "",              |
    |                 |     "return_code": 0,          |
    |                 |     "succeeded": true,         |
    |                 |     "stdout": "hello           |
    |                 | Tue Feb 17 17:28:28 UTC 2015   |
    |                 | "                              |
    |                 | }                              |
    | action          | core.local                     |
    | callback        |                                |
    | end_timestamp   | Tue, 17 Feb 2015 17:28:28 UTC  |
    +-----------------+--------------------------------+

    st2 run re-run 54e37a3c0640fd0bd07b1930
    .
    +-----------------+--------------------------------+
    | Property        | Value                          |
    +-----------------+--------------------------------+
    | id              | 54e37a630640fd0bd07b1932       |
    | context         | {                              |
    |                 |     "user": "stanley"          |
    |                 | }                              |
    | parameters      | {                              |
    |                 |     "cmd": "echo $VAR; date",  |
    |                 |     "env": {                   |
    |                 |         "VAR": "hello"         |
    |                 |     }                          |
    |                 | }                              |
    | status          | succeeded                      |
    | start_timestamp | Tue, 17 Feb 2015 17:29:07 UTC  |
    | result          | {                              |
    |                 |     "failed": false,           |
    |                 |     "stderr": "",              |
    |                 |     "return_code": 0,          |
    |                 |     "succeeded": true,         |
    |                 |     "stdout": "hello           |
    |                 | Tue Feb 17 17:29:07 UTC 2015   |
    |                 | "                              |
    |                 | }                              |
    | action          | core.local                     |
    | callback        |                                |
    | end_timestamp   | Tue, 17 Feb 2015 17:29:07 UTC  |
    +-----------------+--------------------------------+

    st2 run re-run 7a3c0640fd0bd07b1930 env="VAR=world"
    .
    +-----------------+--------------------------------+
    | Property        | Value                          |
    +-----------------+--------------------------------+
    | id              | 54e3a8f50640fd140ae20af7       |
    | context         | {                              |
    |                 |     "user": "stanley"          |
    |                 | }                              |
    | parameters      | {                              |
    |                 |     "cmd": "echo $VAR; date",  |
    |                 |     "env": {                   |
    |                 |         "VAR": "world"         |
    |                 |     }                          |
    |                 | }                              |
    | status          | succeeded                      |
    | start_timestamp | Tue, 17 Feb 2015 20:47:49 UTC  |
    | result          | {                              |
    |                 |     "failed": false,           |
    |                 |     "stderr": "",              |
    |                 |     "return_code": 0,          |
    |                 |     "succeeded": true,         |
    |                 |     "stdout": "world           |
    |                 | Tue Feb 17 20:47:49 UTC 2015   |
    |                 | "                              |
    |                 | }                              |
    | action          | core.local                     |
    | callback        |                                |
    | end_timestamp   | Tue, 17 Feb 2015 20:47:49 UTC  |
    +-----------------+--------------------------------+

Cancel an Execution
-------------------

When dealing with long running executions, you may want to cancel some of them before they have
completed.

To cancel an execution, run:

.. sourcecode:: bash

    st2 execution cancel <existing execution id>


Passing Environment Variables to Runner as ``env`` Parameter
------------------------------------------------------------

Local, remote and Python runners support the ``env`` parameter. This parameter tells the runner
which environment variables should be accessible to the action which is being executed.

User can specify environment variables manually using the ``env`` parameter in the same manner as
other parameters:

.. sourcecode:: bash

    st2 run core.remote hosts=localhost env="key1=val1,key2=val2" cmd="echo ponies \${key1} \${key2}"

In addition to that, users can pass the ``-e``/``--inherit-env`` flag to the ``action run``
command.

This flag will cause the command to inherit all the environment variables which are accessible to
the CLI and send them as an ``env`` parameter to the action.

Keep in mind that some global shell login variables such as ``PWD``, ``PATH`` and others are
ignored and not inherited. The full list of ignored variables can be found in the
`action.py file <https://github.com/StackStorm/st2/blob/master/st2client/st2client/commands/action.py>`_.

For example:

.. sourcecode:: bash

    st2 run --inherit-env core.remote cmd=...
