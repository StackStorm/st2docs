Pack Configuration
==================

.. include:: /_includes/config_yaml_deprecation_notice.rst

Packs can use a configuration file to set values that are common to resources in the pack, e.g.
API credentials, connection details, limits, and thresholds. These values are available to actions
and sensors at run-time. 

The difference between pack configuration and action parameters is that configuration usually
contains values which are common to all the resources in the pack, and rarely change. Action
parameters are dynamically provided with each action invocation, and may change - e.g. they may
come from a rule mapping some input event.

Pack configuration follows an infrastructure as code approach, and is stored in a YAML format file
in a special directory (by default ``/opt/stackstorm/configs``). Each pack defines its own schema
for this configuration file.

Basic Concepts and Terminology
------------------------------

Configuration Schema
~~~~~~~~~~~~~~~~~~~~

The configuration schema is a YAML formatted file which defines the schema for that pack's
configuration file. This schema is written by the pack author and contains information about every
available configuration item (name, type, is value a secret, etc). The file is named
``config.schema.yaml`` and is located in the root of the pack directory
(``/opt/stackstorm/packs/<mypack>/``).

Here is an example schema file:

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

In this example, the configuration consists of 4 items (``api_key``, ``api_secret``, ``region``
and ``private_key_path``).

Note that ``api_secret`` value is marked as **secret** which means this value will be stored
encrypted in the datastore if a dynamic value is used (more on dynamic values can be found below).

In addition to 'flat' configs as shown above, schemas also support nested objects. For example:

.. sourcecode:: yaml

    ---
      consumer_key:
        description: "Your consumer key."
        type: "string"
        required: true
        secret: true
      consumer_secret:
        description: "Your consumer secret."
        type: "string"
        required: true
        secret: true
      access_token:
        description: "Your access token."
        type: "string"
        required: true
        secret: true
      access_token_secret:
        description: "Your access token secret."
        type: "string"
        required: true
        secret: true
      sensor:
        description: "Sensor specific settings."
        type: "object"
        required: false
        additionalProperties: false
        properties:
          device_uids:
            type: "array"
            description: "A list of device UIDs to poll metrics for."
            items:
              type: "string"
            required: false

In this example, the config file can contain a ``sensor`` item which is an object with a single
``device_uuids`` attribute.

Configuration File
~~~~~~~~~~~~~~~~~~

The configuration file is a YAML formatted file which contains site-specific configuration values.
This file can contain 'static' or 'dynamic' values. The configuration file is named
``<pack name>.yaml`` and located in the ``/opt/stackstorm/configs/`` directory. File ownership
should be ``st2:st2``.

For example, for a pack named ``libcloud``, the configuration file is located at
``/opt/stackstorm/configs/libcloud.yaml``.

This example configuration matches the configuration schema above:

.. sourcecode:: yaml

    ---
      api_key: "some_api_key"
      api_secret: "{{st2kv.user.api_secret}}"  # user-scoped configuration value which is also a secret as declared in config schema
      region: "us-west-1"
      private_key_path: "{{st2kv.system.private_key_path}}"  # global datastore value

Configuration files are **not** read dynamically at run-time. Instead, they must be registered, and
values are then loaded into the |st2| DB. They are registered in the same way as other resources by
running ``st2ctl reload``/``st2-register-content`` script. For configs, you need to run this script
with the ``--register-configs`` flag:

.. sourcecode:: bash

    sudo st2ctl reload --register-configs

Or:

.. sourcecode:: bash

    sudo st2-register-content --register-configs

When loading and registering configs using the commands described above, static values in the
config file are validated against the schema. If no schema exists, validation is not performed.

Keep in mind that only static values in the config are validated. Dynamic values (those using
Jinja notation to reference values in the datastore) are resolved during run-time, so they can't be
validated during the register/load phase.

Static Configuration Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A static configuration value is one which is loaded from the config file and used as-is.

Dynamic Configuration Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    Currently, only strings (string types) support dynamic configuration values.

A dynamic configuration value is one that contains a Jinja template expression. This template
expression is evaluated during run-time and resolves to a name (key) of the :doc:`/datastore`
value. This datastore value is then used as the configuration value.

Dynamic configuration values offer additional flexibility, and include support for user-scoped
datastore values. This is useful when you want to use different configuration values, based upon
the user who invoked the action.

In the config, dynamic configuration values are referred to as shown below:

.. sourcecode:: yaml

    ---
      api_secret: "{{st2kv.user.api_secret}}"  # user-scoped configuration value which is also a secret as declared in config schema
      private_key_path: "{{st2kv.system.private_key_path}}"  # global datastore value

``api_secret`` is a user-scoped dynamic configuration value which means that the ``user`` part will
be replaced by the username of the user who triggered the action execution.

Dynamic configuration values are stored in the datastore and are configured using the CLI or API.

If a value is marked as secret in the config schema, it will need to be stored encrypted in the
datastore. When setting the value, the ``--encrypt`` flag should be used, as shown below:

.. sourcecode:: bash

    st2 key set api_secret "my super secret api secret" --scope=user --encrypt

See more about :ref:`storing secrets in datastore here<datastore-storing-secrets-in-key-value-store>`).

In the above example, ``private_key_path`` is a regular dynamic configuration value, which means
that a datastore item corresponding to this key (``private_key_path``) will be loaded from the
datastore.

In this case, using the CLI, the value would be set as displayed below:

.. sourcecode:: bash

    st2 key set private_key_path "/home/myuser/.ssh/my_private_rsa_key"

Configuration Loading and Dynamic Value Resolving
-------------------------------------------------

The configuration file is loaded at registration. Dynamic values are resolved during run-time.
For sensors, this is when the sensor container spawns a subprocess for a sensor instance and for
actions it is when the action is executed.

When resolving and loading user-scoped configuration values, the authenticated user who triggered
the action execution is used for the context when resolving the value.

Configuring Dynamic Configuration Values Using the CLI
------------------------------------------------------

Dynamic pack configuration values can be manipulated in the same way as any other datastore item
using the ``st2 key`` set of CLI commands.

Configuring a Regular (non user-scoped) Dynamic Configuration Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Regular dynamic configuration values can be configured by an administrator or
any user:

.. sourcecode:: bash

    st2 key set <key name> <key value>

    # For example
    st2 key set private_key_path "/home/myuser/.ssh/my_private_rsa_key"

To view a value, use the ``st2 key get`` command:

.. sourcecode:: bash

    st2 key get <key name>

    # For example
    st2 key get private_key_path

Keep in mind that secret values will be masked by default.

Configuring a User-scoped Dynamic Configuration Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dynamic configuration values can be configured by each user themselves or by an administrator for
any available system user:

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

Similarly to above, you can use the ``st2 key get`` command to view values. The same rules which
apply to ``set`` also apply to ``get`` (users can only see values which are local to them,
administrators can see all the values, secrets are masked by default).

Limitations
-----------

There are some limitation with dynamic config values and the ``{{st2kv.user.key_name}}`` context
you should be aware of.

Dynamic Config Values
~~~~~~~~~~~~~~~~~~~~~

Right now only the ``string`` type is supported for dynamic config values. This was done
intentionally to keep the feature simple and fully compatible with the existing datastore
operations (this means you can re-use the same API, CLI commands, etc.).

To work around this (in case you want to use a non-string value) you can store a JSON serialized
version of your value in the datastore and then de-serialize it in the action/sensor code.

If this turns out to be a big problem for many users, we will consider introducing support for
arbitrary types, but this would most likely mean we will need to implement a new API and CLI
commands for managing dynamic config values. That's something we want to avoid.

User Context
~~~~~~~~~~~~

User context is right now only available for actions which are triggered via the |st2| API.

This means that dynamic config values which utilize ``{{st2kv.user.some_value}}`` notation will
only resolve to the correct user when an action is triggered through the API.

The reason for that is that the user context is currently only available in the API. If an action
is triggered via a rule, user context is not available. In this case, ``{{st2kv.user}}`` will
resolve to the system user (by default, ``stanley``).

We plan to address this in a future release, but we haven't decided on the best approach yet, so
your feedback is welcome. Whatever approach we go with, carrying the user context with a trigger
and mapping this external user to the |st2| user will require some additional work on the user
side.
