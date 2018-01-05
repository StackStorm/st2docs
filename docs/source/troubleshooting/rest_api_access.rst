REST API access
===============

To see the REST endpoints used by the |st2| CLI, add the ``--debug`` flag to your CLI command. This
will display the equivalent ``curl`` commands.

For example, to see the endpoint for listing actions, invoke

.. code-block:: bash

   st2 --debug action list

You will see the list of endpoints we hit as well as a ``curl`` command for you to try them manually.

If you are trying to access the API from outside the server, note that the URL will look like:
``https://${EXTERNAL_IP}/api/v1/${REST_ENDPOINT}``.

For example:

.. code-block:: bash

   curl -X GET -H  'Connection: keep-alive' -H  'User-Agent: python-requests/2.9.1' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'X-Auth-Token: <YOUR_TOKEN>' https://1.2.3.4/api/v1/actions

Similarly, you can connect to the auth REST endpoints using: ``https://${EXTERNAL_IP}/auth/v1/${AUTH_ENDPOINT}``.

From the server itself, you can use ``localhost`` instead of ${EXTERNAL_IP}.

You can see a full API reference at `api.stackstorm.com <https://api.stackstorm.com>`_.

Unable to access REST APIs
--------------------------

If you are unable to access the API, perform the following steps:

1. Verify nginx is installed on the |st2| box. Based on the OS, commands will be
   ``sudo apt-cache policy nginx`` or ``sudo yum list installed nginx``.

2. Verify nginx process is up and running. Based on the OS, it might just be
   ``sudo service nginx status`` or ``sudo systemctl nginx status``.

3. Verify if you have |st2|-specific nginx configuration. This is usually in
   ``/etc/nginx/conf.d/``.

4. Verify that no firewall is blocking the ports on the box. It's usually ``ufw`` for ubuntu
   or ``firewall-cmd`` in RHEL/CentOS.

5. Verify nginx is listening on port 443. You can use ``netstat -tupln | grep 443``.


If none of these steps work, have the ``curl`` command and the information you collected for the above
steps available before engaging our technical support.
