Authentication
==============

.. hint::

   Just need the default password? Try username ``st2admin``, password ``Ch@ngeMe``.

   Need to change the password? Run: ``sudo htpasswd /etc/st2/htpasswd st2admin``.

   Something more complex? Read on to learn about |st2| authentication.


|st2| includes an auth service that is responsible for handling user authentication and generating
time-limited access tokens. When authentication is enabled (the default), those access tokens are
used to authenticate against the |st2| REST APIs.

.. figure:: /_static/images/st2auth_standalone_mode.png
    :align: center


Configuring the Service
-----------------------

By default, the |st2| configuration file is located at ``/etc/st2/st2.conf``. The settings listed
below are configured under the ``auth`` section in the configuration file. The service can be
configured with different backends (i.e. PAM, LDAP, etc.) to handle authentication. If a backend is
not specified, an htpasswd-compatible flat file authentication backend is used. 

We recommend that the service be configured to listen on https (``use_ssl`` option) and be
accessible to st2 clients.

* ``host`` Hostname for the service to listen on.
* ``port`` Port for the service to listen on.
* ``use_ssl`` Set to True to enable SSL/TLS mode.
* ``cert`` Path to the SSL certificate file. Only used when ``use_ssl`` is set to True.
* ``key`` Path to the SSL private key file. Only used when ``use_ssl`` is set to True.
* ``mode`` Mode to use (``proxy`` or ``standalone``). Default is ``standalone``.
* ``backend`` Authentication backend to use in standalone mode (i.e. ``pam``, ``flat_file``).
  Please review the supported list of authentication backends below.
* ``backend_kwargs`` JSON-serialized arguments which are passed to the authentication backend in
  standalone mode.
* ``token_ttl`` The token lifetime, in seconds. By default, the token expires in 24 hours.
* ``api_url`` The authentication service also acts as a service catalog. It returns a URL to the
  API endpoint on successful authentication. This information is used by clients such as the CLI
  and web UI. The setting needs to contain a public base URL to the API endpoint (excluding
  the API version). Example: ``https://myhost.example.com/api/``
* ``enable`` Authentication is not enabled for the |st2| API until this is set to True. If
  running |st2| on multiple servers, please ensure that this is set to True on all |st2| systems.
* ``debug`` Enable debug mode.

If you make any changes, you must restart |st2|:

.. sourcecode:: bash

    $ sudo st2ctl restart


Standalone Auth Mode
--------------------

Standalone mode is the default auth mode where external users authenticate directly with
StackStorm. Under the hood the ``st2auth`` service delegates to the configured
``backend`` to perform the authentication. When the backend service properly
authenticates the user, an auth token is returned. This token can then be used
to make further API calls.


Proxy Auth Mode
---------------

Proxy mode can be used when there is a service (proxy) that sits in front of StackStorm
that performs user authentication (ex: load balancer, apache, nginx, etc). When
the frontend service authenticates a user, it will need to make an API call
``POST https://<stackstorm>/auth/v1/tokens`` to the ``st2auth`` service in order
to obtain an auth token. In this request the following CGI environment variables
need to be set:

* ``REMOTE_ADDR`` - Source of the request (hostname/ip of the user who authenticated against the
  proxy).
* ``REMOTE_USER`` - User identity (username) of proxy authenticated user.

The request will return an auth token that authenticated user can use to make further API calls.

When using a reverse proxy such as Apache in front of st2auth, those two CGI environment variables
are usually set automatically by a proxy upon successful authentication.

.. _ref-auth-backends:

Auth Backends
-------------
The service can be configured with different backends (i.e. PAM, LDAP, etc.) to handle the
authentication. If a backend is not specified, an htpasswd-compatible flat file authentication
backend is used. To use a different backend, select and install the appropriate python package from
the |st2| `community repos <https://github.com/StackStorm?utf8=✓&query=st2-auth>`_ and configure
``st2auth`` accordingly. 

.. note::

    When using the ``pam`` authentication backend you need to make sure that the ``st2auth``
    process runs as ``root`` otherwise authentication will fail. For security reasons ``st2auth``
    process runs under ``st2`` user by default. If you want to use ``pam`` auth backend and change
    it to run as ``root``, you can do that by editing the service manager file for the ``st2``
    auth service.

For example, to install the package for the PAM backend manually, run the
following command on the same server where ``st2auth`` is running:

.. sourcecode:: bash

    $ sudo /opt/stackstorm/st2/bin/pip install git+https://github.com/StackStorm/st2-auth-backend-pam.git@master#egg=st2_auth_backend_pam

.. include:: /_includes/__st2_packages_virtualenv_notice.rst

After the backend is installed, configure the backend at ``/etc/st2/st2.conf``, and restart |st2|.
Specific configuration details for the backend can be found in the README at the corresponding
repo. The following is a sample auth section in the config file for the PAM backend:

.. sourcecode:: ini

    [auth]
    mode = standalone
    backend = pam
    enable = True
    use_ssl = True
    cert = /path/to/ssl/cert/file
    key = /path/to/ssl/key/file
    logging = /etc/st2/logging.auth.conf
    api_url = https://myhost.examples.com/api/
    debug = False

The following is a list of auth backends for the community edition to help get things started:

* `PAM <https://github.com/StackStorm/st2-auth-backend-pam>`_
* `Flat File <https://github.com/StackStorm/st2-auth-backend-flat-file>`_
* `OpenStack Keystone <https://github.com/StackStorm/st2-auth-backend-keystone>`_

LDAP (Enterprise Edition)
-------------------------
|st2|-developed auth backends such as LDAP are only available in |bwc|. For more information on
|bwc|, please visit https://www.extremenetworks.com/product/workflow-composer/
The auth backends included with |bwc| are developed, tested, maintained, and supported by Extreme Networks.

LDAP
^^^^
The LDAP backend authenticates the user against an LDAP server. The following is a list of
configuration options for the backend:

+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| option          | required | default | description                                                                                                                    |
+=++==============+==========+=========+=====++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=======================================================+
| bind_dn         | yes      |         | DN of the service account to bind with the LDAP server                                                                         |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| bind_password   | yes      |         | Password of the service account                                                                                                |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| base_ou         | yes      |         | Base OU to search for user and group entries                                                                                   |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| group_dns       | yes      |         | Which groups user must be member of to be granted access                                                                       |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| group_dns_check | no       | and     | What kind of check to perform when validating user group membership (``and`` / ``or``). When ``and`` behavior is used, user    |
|                 |          |         | needs to be part of all the specified groups and when ``or`` behavior is used, user needs to be part of at least one or more   |
|                 |          |         | of the specified groups.                                                                                                       |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| host            | yes      |         | Hostname of the LDAP server                                                                                                    |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| port            | yes      |         | Port of the LDAP server                                                                                                        |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| use_ssl         | no       | false   | Use LDAPS to connect                                                                                                           |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| use_tls         | no       | false   | Start TLS on LDAP to connect                                                                                                   |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| cacert          | no       | None    | Path to the CA cert used to validate certificate                                                                               |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| id_attr         | no       | uid     | Field name of the user ID attribute                                                                                            |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| scope           | no       | subtree | Search scope (base, onelevel, or subtree)                                                                                      |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| network_timeout | no       | 10.0    | Timeout for network operations (in seconds)                                                                                    |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| chase_referrals | no       | false   | True if the referrals should be automatically chased within the underlying LDAP C lib                                          |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| debug           | no       | false   | Enable debug mode. When debug mode is enabled all the calls (including the results) to LDAP server are logged                  |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+
| client_options  | no       |         | A dictionary with additional Python LDAP client options which can be passed to ``set_connection()`` method                     |
+-----------------+----------+---------+--------------------------------------------------------------------------------------------------------------------------------+

.. note::

  By default a logical ``and`` check is performed when validating user group membership against
  groups defined in ``group_dns`` config option. This means if multiple groups are specified, the
  user needs to be member of **all** the specified groups for authentication to succeed. If you
  want to use ``or`` behavior instead (user needs to be a member of one or more of the specified
  groups), you can achieve that by setting the ``group_dns_check`` config option to ``or``.

The following is a sample auth section for the LDAP backend in the st2 config file:

.. sourcecode:: ini

    [auth]
    mode = standalone
    backend = ldap
    backend_kwargs = {"bind_dn": "CN=st2admin,ou=users,dc=example,dc=com", "bind_password": "foobar123", "base_ou": "dc=example,dc=com", "group_dns": ["CN=st2users,ou=groups,dc=example,dc=com", "CN=st2developers,ou=groups,dc=example,dc=com"], "host": "identity.example.com", "port": 636, "use_ssl": true, "cacert": "/path/to/cacert.pem"}
    enable = True
    use_ssl = True
    cert = /path/to/mycert.crt
    key = /path/to/mycert.key
    logging = /etc/st2/logging.auth.conf
    api_url = https://myhost.example.com:9101/
    debug = False

This will need customization for your environment - e.g. the LDAP server to bind to, and the ``cert`` and ``key`` paths if you are using SSL.

Running the Service
-------------------
``st2auth`` is set up to run as a service. It runs under gunicorn.

The service can be started with one of the options below:

.. sourcecode:: bash

    # Individually
    sudo service st2auth start

    # Individually via st2ctl
    sudo st2ctl start st2auth

    # Collectively with other st2 components
    sudo st2ctl start

    # Using the launcher for debugging purposes
    sudo /usr/bin/st2auth --config-file /etc/st2/st2.conf

Testing
-------

Run the following ``curl`` commands to test:

.. sourcecode:: bash

    # If use_ssl is set to True, the following will fail because SSL is required.
    curl -X POST http://myhost.example.com/auth/v1/tokens

    # The following will fail with 401 unauthorized. Please note that this is executed with "-k" to skip SSL cert verification.
    curl -X POST -k https://myhost.example.com/auth/v1/tokens

    # The following will succeed and return a valid token. Please note that this is executed with "-k" to skip SSL cert verification.
    curl -X POST -k -u yourusername:'yourpassword' https://myhost.example.com/auth/v1/tokens

    # The following will verify the SSL cert, succeed, and return a valid token.
    curl -X POST --cacert /path/to/cacert.pem -u yourusername:'yourpassword' https://myhost.example.com/auth/v1/tokens


.. _authentication-usage:

Usage
-----

Once st2auth is enabled, API calls require the token to be passed via the headers. CLI calls
require the token to be included as a CLI argument or as an environment variable.

.. include:: __auth_usage.rst

.. _authentication-apikeys:

API Keys
--------

|st2| also supports API keys. These differ from tokens in that they do not expire. This makes them
suited for integrations with other applications, e.g. through webhooks.

All API key management is currently available via the |st2| CLI or API.

To create an API key:

.. sourcecode:: bash

   st2 apikey create -k -m '{"used_by": "my integration"}'
   <API_KEY_VALUE>

.. note::

    For security purposes the <API_KEY_VALUE> is only shown at create time. |st2| itself does not
    store this API Key value in its database, only a one-way hash is stored. It is not possible to
    retrieve an API Key after creation. If the API Key is lost or not recorded at the time of
    creation, delete the API Key and create a new one.

The optional ``-m`` attribute allows metadata to be associated with the created key. It is good
practice to assign a meaningful value like the external service which uses this key to authenticate
with |st2|.

The CLI for API keys also support ``get``, ``list``, ``delete``, ``enable`` and ``disable`` commands.

If an API Key is disabled it will disallow access until that API key is enabled again. This is a
good way to temporarily revoke access of an external service to |st2|.

API Key Usage
^^^^^^^^^^^^^

API keys are designed for API access. As of now they cannot be used via clients like the UI and CLI.

The following are sample API calls via ``curl`` using API Keys:

.. sourcecode:: bash

   $ curl -H "St2-Api-Key: <API-KEY-VALUE>" https://myhost.example.com/api/v1/actions
   $ curl https://myhost.example.com/api/v1/actions?st2-api-key=<API-KEY-VALUE>

API Key Migration
^^^^^^^^^^^^^^^^^

API keys can be migrated from one |st2| instance to another. This way external services that have
already been configured with API Keys do not need to be updated with a new set of keys. Follow
these steps to migrate:

1. On the old |st2| instance run the following command to save API keys into a file. Note that
   secrets are masked, based on configuration setting. If masking is enabled an admin can on a
   per-API call basis disable the masking without having to make config changes. 
   See :ref:`mask-secrets` to see how to disable masking on a system wide basis.

  .. sourcecode:: bash

     $ st2 apikey list -dy --show-secrets > apikeys.yaml


2. Transfer the file to the new |st2| instance, and load the keys from file:

  .. sourcecode:: bash

     $ st2 apikey load apikeys.yaml


Using Authentication Tokens or API Keys with the API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To authenticate against the |st2| API, either an authentication token or an API key (but not both)
should be provided in the HTTP request headers. The headers are named ``X-Auth-Token`` and
``St2-Api-Key`` respectively.

If for some reason you can't specify an auth token or API key in the headers (e.g. you are using a
third party service to integrate with |st2| and this service doesn't allow you to specify custom
headers), you can provide it as a query parameter named ``x-auth-token`` and ``st2-api-key``
respectively.

.. note::

    Keep in mind that using HTTP header is preferred since some web servers and third party services
    log query parameters which are sent with each request. This could lead to auth token / api key
    exposure and potentially pose a security risk.

Here's some examples of how to send authentication token and API key in the headers, and as a query
parameter using ``curl``:

* Providing it in the request headers:

  .. sourcecode:: bash

     $ curl -H "X-Auth-Token: <auth token value>" https://myhost.example.com/api/v1/actions
     $ curl -H "St2-Api-Key: <api key value>" https://myhost.example.com/api/v1/actions

* Providing it as a query parameter:

  .. sourcecode:: bash

     $ curl "https://myhost.example.com/api/v1/actions?x-auth-token=<auth token value>"
     $ curl "https://myhost.example.com/api/v1/actions?st2-api-key=<api key value>"
