REST API access
===============

There might be times when you might want to use |st2| APIs. We do not have a detailed
REST API documentation yet. You can still get info about the REST endpoints by using the |st2| CLI.
The CLI spits out the ``curl`` command as well for convenience.

You can see the actual REST endpoint for a resource in |st2|
by adding a ``--debug`` option to the CLI command for the appropriate resource.

For example, to see the endpoint for getting actions, invoke

  .. code-block:: bash

    st2 --debug action list

You'll see the list of endpoints we hit as well as a curl command for you to try them manually.

If you are trying to access the API from outside the server, note that the URL will look like:
``https://${EXTERNAL_IP}/api/v1/${REST_ENDPOINT}``.

For example:

  .. code-block:: bash

    curl -X GET -H  'Connection: keep-alive' -H  'User-Agent: python-requests/2.9.1' -H  'Accept-Encoding: gzip, deflate' -H  'Accept: */*' -H  'X-Auth-Token: <YOUR_TOKEN>' https://1.2.3.4/api/v1/actions

Similarly, you can connect to the auth REST endpoints using this: ``https://${EXTERNAL_IP}/auth/v1/${AUTH_ENDPOINT}``.

From the server itself, you can use ``localhost`` instead of ${EXTERNAL_IP}.

Unable to access REST APIs
--------------------------

If you are unable to access the API, please go through the following steps:

1. Verify nginx is installed on the |st2| box. Based on the OS, it might just be
``sudo apt-cache policy nginx`` or ``sudo yum list installed nginx``.

2. Verify nginx process is up and running. Based on the OS, it might just be
``sudo service nginx status`` or ``sudo systemctl nginx status``.

3. Verify if you have |st2| specific nginx config in right place. This is usually in
``/etc/nginx/conf.d/``.

4. Verify that no firewall is blocking is ports on the box. It's usually ``ufw`` for ubuntu
or ``SELinux`` policy in RHEL/CentOS.

5. Verify port 443 is being listened on. You can use ``netstat -tupln | grep 443``.


If none of these steps work, please have the ``curl`` command and info you collected for the above
steps before engaging support.
