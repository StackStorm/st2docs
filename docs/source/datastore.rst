Datastore
===============================

The goal of the datastore service is to allow users to store common
parameters and their values within |st2| for reuse in the definition
of sensors, actions, and rules. The datastore service store the data as
a key value pair and they can be get/set using the |st2| CLI or the |st2|
python client. From the sensor and action plugins, since they are
implemented in python, the key value pairs are accessed from the |st2|
python client. For rule definitions in YAML/JSON, the key value pairs are
referenced with a specific string substitution syntax and the references
are resolved on rule evaluation.

Storing and Retrieving Key Value Pairs from CLI
-----------------------------------------------

Set a value of a key value pair.

::

    st2 key set os_keystone_endpoint http://localhost:5000/v2.0
    st2 key set aws_cfn_endpoint https://cloudformation.us-west-1.amazonaws.com

Load a list of key value pairs from a JSON file. The following is the
JSON example using the same keys from the create examples above.

::

    [
        {
            "os_keystone_endpoint": "http://localhost:5000/v2.0",
            "aws_cfn_endpoint": "https://cloudformation.us-west-1.amazonaws.com"
        }
    ]

    st2 key load mydata.json

The load command also allows you to directly load the output of "key list -j"
command. This is useful if you want to migrate datastore items from a different
cluster or if you want to version control the datastore items and load the from
version controlled files.

::

    st2 key list -j > mydata.json
    st2 key load mydata.json

Get individual key value pair or list all.

::

    st2 key list
    st2 key get os_keystone_endpoint
    st2 key get os_keystone_endpoint -j

Update an existing key value pair.

::

    st2 key set os_keystone_endpoint http://localhost:5000/v3

Delete an existing key value pair.

::

    st2 key delete os_keystone_endpoint

Storing and Retrieving from Python Client
-----------------------------------------

Create new key value pairs. The |st2| API endpoint is set either via
the Client init (base\_url) or from environment variable
(ST2\_BASE\_URL). The default ports for the API servers are assumed.

::

    >>> from st2client.client import Client
    >>> from st2client.models import KeyValuePair
    >>> client = Client(base_url='http://localhost')
    >>> client.keys.update(models.KeyValuePair(name='os_keystone_endpoint', value='http://localhost:5000/v2.0'))

Get individual key value pair or list all.

::

    >>> keys = client.keys.get_all()
    >>> os_keystone_endpoint = client.keys.get_by_name(name='os_keystone_endpoint')
    >>> os_keystone_endpoint.value
    u'http://localhost:5000/v2.0'

Update an existing key value pair.

::

    >>> os_keystone_endpoint = client.keys.get_by_name(name='os_keystone_endpoint')
    >>> os_keystone_endpoint.value = 'http://localhost:5000/v3'
    >>> client.keys.update(os_keystone_endpoint)

Delete an existing key value pair.

::

    >>> os_keystone_endpoint = client.keys.get_by_name(name='os_keystone_endpoint')
    >>> client.keys.delete(os_keystone_endpoint)

Referencing Key Value Pair in Rule Definition
---------------------------------------------

Key value pairs are referenced via specific string substitution syntax
in rules. In general, variable for substitution is enclosed with double
brackets (i.e. **{{var1}}**). To refer to a key value pair, prefix the
variable name with "system" (i.e.
**{{system.os\_keystone\_endpoint}}**). An example rule is provided
below. Please refer to the documentation section for Rules on rule
related syntax.

::

    {
        "name": "daily_clean_up_rule",
        "trigger": {
            "name": "st2.timer.daily"
        },
        "enabled": true,
        "action": {
            "name": "daily_clean_up_action",
            "parameters": {
                "os_keystone_endpoint": "{{system.os_keystone_endpoint}}"
            }
        }
    }

Securing secrets in key value store (admin only)
------------------------------------------------

.. note::

    This guide and the corresponding implementation is alpha quality. We are working on the feature
    and feedback is welcome. Until the feature matures and deployment issues identified and fixed,
    no guarantee is made w.r.t ``security`` of the credentials stored in key value store.

Key value store now allows users to store encrypted credentials via a global symmetric key set
by the StackStorm admin. It goes without saying that admin can decrypt the credentials if they
want to.

To generate a symmetric crypto key (AES256 used for both encryption and decryption) as an admin,
please run

.. code-block:: bash

    /opt/stackstorm/st2/tools/st2-generate-symmetric-crypto-key.py --key-path /path/to/key/file.json

It is recommended that the key is placed in a private location such as /etc/st2/keys/ and
permissions are appropriately modified so that only StackStorm API process owner (usually ``st2``) can
read and admin can read/write to that file.

Once the key is generated, |st2| needs to be made aware of the key. To do this, edit st2
configuration file (usually /etc/st2/st2.conf) and add the following lines:

[keyvalue]
encryption_key_path=/path/to/key/file.json

Now as an admin, you are all set with configuring |st2| server side.

Storing secrets in key value store
----------------------------------

Please note that if an admin has not setup encryption keys, you will not be allowed to save
secrets in the key value store. Contact your |st2| admin to setup encryption keys as per the section
above.

To save a secret in key value store:

.. code-block:: bash

    st2 key set api_token SECRET_TOKEN --encrypt

By default, getting a key tagged as secret (via --encrypt) will always return encrypted values only.
To get plain text, please run with command --decrypt flag.

.. code-block:: bash

    st2 key get api_token --decrypt

.. note::

    RBAC is still being worked on for this feature. For now, anyone with access to the encryption
    key (including admin) will be able to decrypt the secrets.

Security notes
--------------

|st2| wishes to discuss security details and be transparent about the implementation and limitations
of the security practices to attract more eyes to it and therefore build better quality into
security implementations. For the key value store, we have settled on AES256 symmetric encryption
for simplicity. We use python library keyczar for doing this.

We have made a trade off that |st2| admin is allowed to decrypt the secrets in key value store.
This made our implementation simpler. We are looking into how to let users pass their own keys
for encryption every time they want to consume a secret from key value store. This requires more
UX thought and also moves the responsibility of storing keys to the users.
Your ideas are welcome here.

Please note that the global encryption key still disables users with direct access to databases
to still see only encrypted secret in database. Still the onus is on |st2| admin to restrict
access to database via network daemons only and not allow physical access to the box (or run
databases on different boxes as st2). Note that several layers of security needs to be in place
that is beyond the scope of this document. While we can help people with deployment questions
on stackstorm slack community, please follow your own best security practices guide.
