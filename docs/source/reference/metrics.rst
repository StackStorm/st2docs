Metrics and Instrumentation
===========================

|st2| services and code base contain instrumentation with metrics in various critical places.
This provides better operational visibility and allows operators to detect various infrastructure
or deployment related issues (e.g. long average duration for a particular action could indicate
an issue with that action or similar).

Configuring and Enabling Metrics Collection
===========================================

.. note::

  This feature was added and is available in |st2| v2.9.0 and above.

By default metrics collection is disabled. To enable it, you need to configure ``metrics.driver``
and depending on the driver, also ``metrics.host`` and ``metrics.port`` option in
``/etc/st2/st2.conf``.

Right now, the only supported driver is ``statsd``. To configure it, add the following entries to
``st2.conf``:

.. code-block:: ini

    [metrics]
    driver = statsd
    # Optional prefix which is prepended to each metric key. E.g. if prefix is
    # "production" and key is "action.executions" actual key would be
    # "st2.production.action.executions". This comes handy when you want to
    # utilize the same backend instance for multiple environments or similar.
    host = 127.0.0.1  # statsd collection and aggregation server address
    port = 8125  # statsd collection and aggregation server port

After you have configured it, you need to restart all the services using ``st2ctl restart``.

In case your statsd daemon is running on a remote sever and you have a firewall configured, you
also need to make sure that all the servers where |st2| components are running are allowed
outgoing access to the configured host and port.

For debugging and troubleshooting purposes, you can also set driver to ``echo``. This will cause
|st2| to log under ``DEBUG`` log level any metrics operation which would have otherwise be performed
(increasing a counter, timing an operation, etc.) without actually performing it.

Configuring StatsD
==================

|st2| ``statsd`` metrics driver is compatible with any service which exposes statsd compatible
interface for receiving metrics via UDP.

This includes original statsd service written in Node.js, but also compatible projects such as
Telegraf and others.

This provides for a lot of flexibility and allows statsd service to submit those metrics to self
hosted or managed graphite instance or to other compatible projects and services such as InfluxDB
and hostedgraphite.

Configuring those services is out of scope of this documentation, because it's very environment
specific (aggregation resolution, retention period, etc.), but some sample configs which can help
you get started with statsd and self hosted graphite and carbon cache instance
can be found at https://github.com/StackStorm/st2/tree/master/conf/metrics.

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
| st2.action.<action ref>.executions                         | timer      | st2actionrunner             | How long it took to process (run) action execution for a particular action inside st2actionrunner.             |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.action.executions.<execution status>                   | counter    | st2actionrunner             | Number of executions in a particular state (succeeded, failed, timeout, delayed, etc).                         |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.rule.processed                                         | counter    | st2rulesengine              | Number of rules (trigger instances) processed by st2rulesengine service.                                       |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.rule.processed                                         | timer      | st2rulesengine              | How long it took to process a particular rule (trigger instance) inside st2rulesengine.                        |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.rule.<rule ref>.processed                              | counter    | st2rulesengine              | Number of particular rules processed by st2rulesengine.                                                        |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.rule.matched                                           | counter    | st2rulesengine              | Number of trigger instances which matched a rule (criteria).                                                   |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.rule.<rule ref>.matched                                | counter    | st2rulesengine              | Numbers of trigger instances which matched a particular rule (criteria).                                       |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.trigger.<trigger ref>.processed                        | counter    | st2rulesengine              | Number of particular triggers processed by st2rulesengine.                                                     |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.trigger.<trigger ref>.processed                        | timer      | st2rulesengine              | How long it took to process a particular trigger inside st2rulesengine.                                        |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.orquesta.workflow.executions                           | counter    | st2workflowengine           | Number of workflow executions processed by st2workflowengine.                                                  |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.orquesta.workflow.executions                           | timer      | st2workflowengine           | How long it took to process a particular workflow execution inside st2workflowengine.                          |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.orquesta.action.executions                             | counter    | st2workflowengine           | Number of executions processed for workflow task executions by st2workflowengine.                              |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.orquesta.action.executions                             | timer      | st2workflowengine           | How long it took to process a particular workflow task execution inside st2workflowengine.                     |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.request.total                        | counter    | st2auth, st2api, st2stream  | Number of requests processed by st2auth / st2api / st2stream.                                                  |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.request                              | counter    | st2auth, st2api, st2stream  | Number of requests processed by st2auth / st2api / st2stream.                                                  |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.request                              | timer      | st2auth, st2api, st2stream  | How long it took to process a particular HTTP request.                                                         |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.request.method.<method>              | counter    | st2auth, st2api, st2stream  | Number of requests with particular HTTP method processed by st2auth / st2api / st2stream.                      |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.request.path.<path>                  | counter    | st2auth, st2api, st2stream  | Number of requests to a particular HTTP path (controller endpoint) processed by st2auth / st2api / st2stream.  |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| st2.{auth,api,stream}.response.status.<status code>        | counter    | st2auth, st2api, st2stream  | Number of requests which resulted in a response with a particular HTTP status code.                            |
+------------------------------------------------------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+

Depending on the metric backend and metric type, some of those metrics will also be sampled,
averaged, aggregated and converted into a rate (operations / seconds for ``counter`` metrics), etc.

Keep in mind that for the counter metrics, statsd automatically calculates rates. If you are
interested in more than a rate (events per second), you will need to derive those metrics from the
raw "count" metric.

For example, if you are interested in a total number of executions scheduled or a total number of
API requests in a particular time frame, you would use ``integral()`` graphite function (e.g.
``integral(stats.counters.st2.action.executions.scheduled.count)`` and
``integral(stats.counters.st2.api.requests.count)``).
