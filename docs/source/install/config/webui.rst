Web UI
======

st2web is an Angular-based HTML5 web application. It allows you to control the whole process of
execution, from running an action to seeing the results of the execution. It also helps you to
explore workflow executions up to the results of individual tasks. All in real time.

Deployment
-----------

st2web is installed via the st2web RPM or deb package. This is installed by default when using the
one-line :doc:`install method </install/index>`. You can access the UI by pointing your browser to
``https://<server hostname>/``. If you are using st2vagrant, it would be https://192.168.16.20/.

st2web is a pure HTML5 application and consists only of js scripts, html templates, css styles and
static files including custom fonts and svg images. For the application to work correctly, all
files should be served to the browser. By default they are served by nginx. For your custom
deployments, you can also use Apache or a similar dedicated web server.

Note that the |st2| API endpoint should be accessible from the browser, not the web server running
static content.

Configuration
-------------

For the UI to work properly, both the web client and |st2| server side should be configured
appropriately.

On the web client side, the file ``config.js`` in the project contains the list of servers this UI
can connect to. This is typically ``/opt/stackstorm/static/webui/config.js``. The file consists of
an array of objects, each with ``name``, ``url`` and ``auth`` properties.

.. code-block:: js

   hosts: [{
     name: 'Express Deployment',
     url: 'http://172.168.90.50:9101',
     auth: true
   },{
     name: 'Development Environment',
     url: 'http://:9101'
     auth: 'https://:9100'
   }]


Multiple servers can be configured for the user to pick from. To disconnect from the current server
and return to login screen, pick 'Disconnect' from the drop down at the top right corner of the UI.

On the |st2| side, `CORS <https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`__ should
also be configured. In ``st2.conf``, the ``allow_origin`` property of the ``[api]`` section should
contain the Origin header the browser sends with every request. For example, if you have deployed
the UI on its own server and are accessing it using ``http://webui.example.com``, your config
should look like this:

.. code-block:: ini

   [api]
   # Host and port to bind the API server.
   host = 0.0.0.0
   port = 9101
   logging = st2api/conf/logging.conf
   # List of allowed origins for CORS, use when deploying st2web client
   # The URL must match the one the browser uses to access the st2web
   allow_origin = http://webui.example.com

Origin consists of scheme, hostname and port (if it isn't 80). Path (including trailing slash)
should be omitted.

Please note that some of the origins are already included by default and do not require additional
configuration:

* ``http://localhost:3000`` - development version of ``gulp`` running locally
* ``http://localhost:9101,http://127.0.0.1:9101`` - ``st2api`` pecan deployment
* ``api_url`` from ``[auth]`` section of ``st2.conf``

Although this is not recommended and will undermine your security, you can allow every web UI
deployment to connect to your server by setting ``allow_origin = *``.

Authentication
--------------

To configure st2web to support authentication, edit ``config.js`` and add ``auth:true`` to every
server that supports authentication. To enable authentication on the server side, please refer to
:doc:`/authentication`.
