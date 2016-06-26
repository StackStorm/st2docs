Pack Configuration
==================

.. note::

    Support for pack config files which are located outside the pack directory
    in ``/opt/stackstorm/configs/`` directory has been introduced in |st2| v1.5
    and is only available in |st2| v1.5 and above.

Pack configuration file contain common attributes which are usually configured
by a |st2| operator and are available to actions and sensors during run-time.

The difference between pack configuration and action parameters is that
configuration usually contains values which are usually common to all the
resources in the pack (e.g. API credentials, connection details, different
limits and thresholds, etc.) and rarely change. Pack configuration follows
infrastructure as code approach and is stored in a YAML formated file in a
special directory (this means all the files in that directory can be version
controlled, reviewed, audited, etc.).

On the other hand, pack parameters are values which are dynamically provided
for every action invocation. They can be provided by the user when manually
invoking an action or they can come from a triggered based on a mapping inside
a rule.

Basic Concepts and Terminology
------------------------------

Configuration schema
~~~~~~~~~~~~~~~~~~~~

Configuration schema is a YAML formatted file which contains schema for a
configuration file. This schema is usually written by pack author and contains
different information about every available configuration item (name, type, is
value a secret, etc). The file is named ``config.schema.yaml`` and is located
in root of the pack directory.

An example schema file can be found below:

.. sourcecode:: yaml

    ---
      api_key:
        description: "API key"
        type: "string"
        required: true
      api_secret:
        description: "API secret"
        type: "string"
        secret: true
        required: true
      region:
        description: "API region to use"
        type: "string"
        required: true
        default: "us-east-1"
      private_key_path:
        description: "Path to the private key file to use"
        type: "string"
        required: false

In this example, configuration consists of 4 items (``api_key``,
``api_secret``, ``region`` and ``private_key_path``).

``api_secret`` value is marked as secret which means this value will be stored
encrypted in the datastore if a dynamic value is used (more on dynamic values
can be found below).

.. note::

    Right now config schema is optional and it's only required if you wish to
    utilize dynamic config values from datastore (more on that below).

Configuration file
~~~~~~~~~~~~~~~~~~

Configuration file is a YAML formatted file which contains pack configuration.
This file can contain "static" or "dynamic" values. Configuration file is named
by a pack name (``<pack name>.yaml``) and located in ``/opt/stackstorm/configs/``
directory.

For example, for a pack named ``libcloud``, configuration file is located at
``/opt/stackstorm/configs/libcloud.yaml``.

An example configuration which matches the configuration schema above is
provided below:

.. sourcecode:: yaml

    ---
      api_key: "some_api_key"
      api_secret: "{{user.api_secret}}"  # user scoped configuration value which is also a secret as declared in config schema
      region: "us-west-1"
      private_key_path: "{{system.private_key_path}}"  # global datastore value

Configuration files are registered in the same way as other resources by running
``st2ctl reload`` / ``st2-register-content`` script. For configs, you need to run
this script with the ``--register-configs`` flag as shown below.

.. sourcecode:: bash

    st2ctl reload --register-configs

Or:

.. sourcecode:: bash

    st2-register-content --register-configs

Static configuration value
~~~~~~~~~~~~~~~~~~~~~~~~~~

Static configuration value is a value which is loaded from the config file and
used as-is.

In the previous / old configuration file, every value was static since there
was no support for dynamic values.

Dynamic configuration value
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    Right now only strings (string types) are supported for dynamic
    configuration values.

Dynamic configuration value is a config value which contains a Jinja template
expression. This template expression is evaluated during run-time and resolves
to a name (key) of the datastore value. This datastore value is then used as
the configuration value.

Dynamic configuration values offer additional flexibility and they include
support for user-scoped datastore values. This comes handy when you want to use
a different configuration value (e.g. different API credentials) based on the
user who invoked the action.

Dynamic configuration value are stored in the datastore and are configured using
CLI as shown in the section below.

In the config, dynamic configuration values are referred to as shown below:

.. sourcecode:: yaml

    ---
      api_secret: "{{user.api_secret}}"  # user scoped configuration value which is also a secret as declared in config schema
      private_key_path: "{{system.private_key_path}}"  # global datastore value

``api_secret`` is a user-scoped dynamic configuration value which means that
``user`` part will be replaced by the username of the user who triggered the
action execution.

Since that value is marked as secret in the config schema, this value will
need to be stored encrypted in the datastore. This means user who is setting
the value needs to also pass  ``--encrypt`` flag to the CLI command as shown
below (more about --encrypt flag and
:ref:`storing secrets in datastore<datastore-storing-secrets-in-key-value-store>`):

.. sourcecode:: bash

    st2 key set api_secret "my super secret api secret" --scope=user --encrypt

``private_key_path`` is a regular dynamic configuration value which means that
a datastore item which corresponds to this key (``private_key_path``) will be
loaded from the datastore.

In this case, using the CLI, the value would be set as displayed below:

.. sourcecode:: bash

    st2 key set private_key_path "/home/myuser/.ssh/my_private_rsa_key"

Configuration loading and dynamic value resolving
-------------------------------------------------

Configuration file is loaded and dynamic values are resolved during run-time.
For sensors this is when sensor container spawns a subprocess for sensor
instance and for actions that is when action is executed.

Previous versions of |st2| supported pack-local configuration files which were
named ``config.yaml`` and stored in a root of the pack directory. For backward
compatibility and ease of migration, those files are still supported, but
new-style configuration files have precedence over it. If both files are
present, old-style configuration file is loaded first and values from new-style
configuration file are loaded and merged in second.

When resolving and loading user-scoped configuration value, authenticated user
which triggered the action execution is used for the context when resolving the
value.

Configuring dynamic configuration values using the CLI
------------------------------------------------------

Dynamic pack configuration values can be manipulated in the same way as any
other datastore item using ``st2 key`` set of CLI commands.

Configuring a regular (non user-scoped) dynamic configuration value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Regular dynamic configuration value can be configured by an administrator or
any user.

.. sourcecode:: bash

    st2 key set <key name> <key value>

    # For example
    st2 key set private_key_path "/home/myuser/.ssh/my_private_rsa_key"

To view a value, you use get command as shown below:

.. sourcecode:: bash

    st2 key get <key name>

    # For example
    st2 key get private_key_path

Keep in mind that secret values will be masked by default.

Configuring a user-scoped dynamic configuration value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dynamic configuration value can be configured by each user themselves or by an
administrator for any available system user.

.. sourcecode:: bash

    st2 key set --scope=user [--encrypt] <key name> <key value>

    # For example (authenticated as "user1")
    st2 key set --scope=user default_region "us-west-1"
    st2 key set --scope=user --encrypt api_secret user1_api_secret

    # For example (authenticated as "user2")
    st2 key set --scope=user default_region "us-east-1"
    st2 key set --scope=user --encrypt api_secret user2_api_secret

    # For example (authenticated as administrator, setting a value for "user1" and "user2")
    st2 key set --scope=user --user=user1 default_region "us-west-1"
    st2 key set --scope=user --user=user2 default_region "us-east-1"

Similar as above, you can use get command to view the values. Same rules which
apply to ``set`` also apply to ``get`` (users can only see values which are
local to them, administrator can see all the values, secrets are masked by
default).

Limitations
-----------

There are some limitation with the dynamic config values and
``{{user.key_name}}`` context you should be aware of.

Dynamic config values
~~~~~~~~~~~~~~~~~~~~~

Right now only string type is supported for dynamic config values (config items
who's value is retrieved from the datastore). This was done intentionally to
keep the feature simple and fully compatible with the existing datastore
operations (this means you can re-use the same API, CLI commands, etc.).

To work-around this (in case you want to use a non-string value) you can, for
example, store a JSON serialized version of the your value in the datastore and
then de-serialize it in the action / sensor code.

If this turns out to be a big problem for many users, we might consider
introducing support for arbitrary types, but this would most likely mean we
will need to implement a new API and CLI commands for managing dynamic config
values and that's something we want to avoid.

User context
~~~~~~~~~~~~

User context is right now only available for actions which are triggered via
the |st2| API.

This means that dynamic config values which utilize ``{{user.some_value}}``
notation will only resolve to the correct user when an action is triggered
through the API.

The reason for that is that user context is currently only available in the
API. If an action is triggered via rule, user context is not available. This
means ``{{user}}`` will resolve to the system user (``stanley``).

We plan to address this in a future release, but we haven't decided on the
approach yet, so your feedback is welcome. No mater the approach we will go
with, carrying the user context with a trigger and mapping this external user
to the |st2| user will require some additional work on the user-side.
