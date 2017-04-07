Secrets Masking
---------------

|st2| offers functionality for masking secrets in API responses and log. Secret masking
is disabled by default and can be enabled by setting ``api.mask_secrets`` and
``logging.mask_secrets`` option to ``True``.

.. sourcecode:: ini

    [api]
    mask_secrets = True

    ...

    [logging]
    mask_secrets = True

Masking Secrets in API Responses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When secret masking is enabled for API responses, |st2| will mask values for secret parameters in
all the API responses which operate on the following system entities:

* Action Executions
* Live Actions
* Datstore (key value) Items

|st2| will determine if a particular action parameter is a secret based on the parameter definition
in the action metadata file.

Any action parameter which has ``secret: true`` attribute will be considered and treated as a secret
for masking purposes.

Masking can be disabled on per API request basis, by a user which is an administrator by passing
``?show_secrets=True`` query parameter to all of the supported API endpoints.

Below you can find an example of secret parameter ``cmd`` being masked in the response of the
``/v1/executions/`` API endpoint.

Default response with masking enabled:

.. sourcecode:: json

  curl -X GET 'http://127.0.0.1:9101/v1/executions/?limit=1'
  [
      {
          "status": "requested",
          "start_timestamp": "2017-04-07T13:01:50.953242Z",
          "log": [
              {
                  "status": "requested",
                  "timestamp": "2017-04-07T13:01:50.970000Z"
              }
          ],
          "parameters": {
              "cmd": "********"
          },
          ...
          "id": "58e78dbe0640fd765ca74896"
      }
  ]

Operating as a user with an admin role and disabling making on per request basis:

.. sourcecode:: json

  curl -X GET 'http://127.0.0.1:9101/v1/executions/?limit=1&show_secrets=True'
  [
      {
          "status": "requested",
          "start_timestamp": "2017-04-07T13:01:50.953242Z",
          "log": [
              {
                  "status": "requested",
                  "timestamp": "2017-04-07T13:01:50.970000Z"
              }
          ],
          "parameters": {
              "cmd": "********"
          },
          ...
          "id": "58e78dbe0640fd765ca74896"
      }
  ]

Masking Secrets in Log Messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When secret masking is enabled for log messages, |st2| uses a static blacklist of attribute and
parameter names which are considered as secrets and tries to mask them in the log messages. By
default, this blacklist contains the following names:

* ``password``
* ``auth_token``
* ``token``
* ``secret``
* ``credentials``
* ``st2_auth_token``

Values for all the masked parameters are replaced with ``********``.

For example, for a log method call in the code which looks like this:

.. sourcecode:: python

  LOG.info('User authenticated', extra={'username': 'dummy', 'password': 'supersecret', 'token': 'supersecret'})

The actual log line in the log file would look like that.

With masking disabled:

.. sourcecode:: python

  2017-04-07 12:20:09,368 INFO [-] User authenticated (username=dummy, token=supersecret)

With masking enabled:

.. sourcecode:: python

  2017-04-07 12:20:09,368 INFO [-] User authenticated (username=dummy, token=********)

Limitations
~~~~~~~~~~~

API response and log message secret masking use best effort approach and as such, have multiple
limitations.

You are strongly encouraged to not rely on secret masking functionality alone, but use it in
combination with other security related primitives available in |st2| such as RBAC and encrypted
datastore values (defence in depth principle).

The best approach when dealing with secrets is to store secret and / or potentially sensitive
values encrypted in a datastore. Then you should directly retrieve and decrypt those secret values
only in the actions where you need to access them.

Doing that instead of passing those values around as action parameters makes actions and workflows
a bit more tightly coupled and harder to re-use and troubleshoot, but it decreases the surface area
where those values could potentially be leaked / exposed and as such makes it more secure - you are
trading readability and re-use for security.

In addition to that, you should be careful to not use ``DEBUG`` log level or ``debug`` mode in
production deployments. When debug mode is enabled / debug log level is set all, log verbosity is
increased and a lot of data which is helpful when debugging, but could also contain sensitive
information is included in the log messages and no masking is performed.
