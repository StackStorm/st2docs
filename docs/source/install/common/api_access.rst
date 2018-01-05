If you are trying to access the API from outside the box and you have configured nginx according to
these instructions, use ``https://${EXTERNAL_IP}/api/v1/${REST_ENDPOINT}``.

For example:

.. code-block:: bash

  curl -X GET -H  'Connection: keep-alive' -H  'User-Agent: manual/curl' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'X-Auth-Token: <YOUR_TOKEN>' https://1.2.3.4/api/v1/actions

Similarly, you can connect to auth REST endpoints with ``https://${EXTERNAL_IP}/auth/v1/${AUTH_ENDPOINT}``.

You can see the actual REST endpoint for a resource by adding a ``--debug`` option to the CLI
command for the appropriate resource.

For example, to see the endpoint for getting actions, invoke:

.. code-block:: bash

  st2 --debug action list
