Metrics and Instrumentation
===========================

|st2| services and code base contain instrumentation with metrics in various critical places.
This provides better operational visibility and allows operators to detect various infrastructure
or deployment related issues (e.g. long average duration for a particular action could indicate
an issue with that action or similar).

Configuring and Enabling Metrics Collection
===========================================

.. note::

  This feature was added and is available in |st2| v2.8.0 and above.

By default metrics collection is disabled. To enable it, you need to configure ``metrics.driver``
and depending on the driver, also ``metrics.host`` and ``metrics.port`` option in
``/etc/st2/st2.conf``.

Right now, the only supported driver is ``statsd``. To configure it, add the following entries to
``st2.conf``:

.. code-block:: ini

    [metrics]
    driver = statsd
    host = 127.0.0.1  # statsd collection and aggregation server address
    port = 8125  # statsd collection and aggregation server port

After you have configured it, you need to restart all the services using ``st2ctl restart``.

In case your statsd daemon is running on a remote sever and you have a firewall configured, you
also need to make sure that all the servers where |st2| components are running are allowed
outgoing access to the configured host and port.

For debugging and troubleshooting purposes, you can also set driver to ``echo``. This will cause
|st2| to log under ``DEBUG`` log level any metrics operation which would have otherwise be performed
(increasing a counter, timing an operation, etc.) without actually performing it.

Exposed Metrics
===============

.. note::

  Various metrics documented in this section are only available in |st2| v2.9.0 and above.

This section describes which metrics are currently exposed by various |st2| services.

+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| Name                                                       | Type       | Service                     | Description                                                                                                    |
+============================================================+============+=============================+================================================================================================================+
| st2.action.executions                                      | counter    | st2actionrunner             | Number of action executions processed by st2actionrunner service.                                              |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.action.executions                                      | timer      | st2actionrunner             | How long it took to process (run) a particular action execution inside st2actionrunner service.                |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.action.<action ref>.executions                         | counter    | st2actionrunner             | Number of action execution for a particular action processed by st2actionrunner.                               |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.action.<action ref>.executions                         | timer      | st2actionrunner             | How long it took to process (run) action execution for a particular action inside st2actionrunner              |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.action.executions.<execution status>                   | counter    | st2actionrunner             | Counter information for various final execution states (succeeded, failed, timeout).                           |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.rule.processed                                         | counter    | st2rulesengine              | Numbers of rules processed by st2rulesengine service.                                                          |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.rule.processed                                         | timer      | st2rulesengine              | How long it took to process a particular rule (trigger instance) inside st2rulesengine.                        |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.rule.<rule ref>.processed                              | counter    | st2rulesengine              | Number of particular rules processed by st2rulesengine.                                                        |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.trigger.<trigger type ref>.processed                   | counter    | st2rulesengine              | Number of particular trigger types processed by st2rulesengine.                                                |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.requests                             | counter    | st2auth, st2api, st2stream  | Number of requests processed by st2auth / st2api / st2stream.                                                  |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.requests                             | timer      | st2auth, st2api, st2stream  | How long it took to process a particular HTTP request.                                                         |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.requests.method.<method>             | counter    | st2auth, st2api, st2stream  | Number of requests with particular HTTP method processed by st2auth / st2api / st2stream.                      |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.requests.path.<path>                 | counter    | st2auth, st2api, st2stream  | Number of requests to a particular HTTP path (controller endpoint) processed by st2auth / st2api / st2stream.  |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.responses.status.<status code>       | counter    | st2auth, st2api, st2stream  | Number of requests which resulted in a response with a particular HTTP status code.                            |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+

Depending on the metric backend used and metric type, some of those metrics will also be averaged,
aggregated and converted into a rate (operations / seconds for ``counter`` metrics), etc.
