Enabling Debug Mode
===================

You can enable debug mode for a particular service by starting it with a ``--debug`` command line
flag or by editing ``st2.conf`` config file and setting ``system.debug`` setting to ``True`` as
shown below and restarting all the services using ``st2ctl restart``.

.. sourcecode:: ini
    ...
    [system]
    debug = True

When running a service in the debug mode, all the log messages logged under ``DEBUG`` log level
will also be included in the logs which should make troubleshooting different issues easier. In
addition to that, when debug mode is enabled, all the API JSON responses are pretty-formatted and
the traceback will also be included in the logs for all the API requests which result in an
exception.
