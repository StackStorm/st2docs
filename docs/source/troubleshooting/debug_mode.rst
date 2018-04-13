Enabling Debug Mode
===================

You can enable debug mode for a particular service by starting it with the ``--debug`` command line
flag. You can also edit the ``st2.conf`` config file and set ``system.debug`` to ``True`` as shown
below:

.. sourcecode:: ini

    [system]
    debug = True

After making this change, restart all services with ``sudo st2ctl restart``.

When running a service in the debug mode, all log messages logged under the ``DEBUG`` log level
will also be included in the |st2| logs at ``/var/log/st2/``.

In addition to that, when debug mode is enabled, all the API JSON responses are pretty-formatted
and a traceback will also be included in the logs for all the API requests which result in an
exception.

If you are using a custom logging setup (e.g. messages are sent to syslog) you will also need to
edit logging config for a service for which you want to enable debug logging. Logging config
files are located in ``/etc/st2/logging.<service name>.conf``.

For example, if you want to set log level to ``DEBUG`` for action runner services, you would change
the config (``/etc/st2/logging.actionrunner.conf``) from:

.. sourcecode:: ini
   :emphasize-lines: 11,16,22

    [loggers]
    keys=root

    [handlers]
    keys=consoleHandler, fileHandler, auditHandler

    [formatters]
    keys=simpleConsoleFormatter, verboseConsoleFormatter, gelfFormatter, jsonFormatter

    [logger_root]
    level=INFO
    handlers=consoleHandler, fileHandler, auditHandler

    [handler_consoleHandler]
    class=StreamHandler
    level=INFO
    formatter=simpleConsoleFormatter
    args=(sys.stdout,)

    [handler_fileHandler]
    class=st2common.log.FormatNamedFileHandler
    level=INFO
    formatter=verboseConsoleFormatter
    args=('/var/log/st2/st2actionrunner.{pid}.log',)

    [handler_auditHandler]
    class=st2common.log.FormatNamedFileHandler
    level=AUDIT
    formatter=jsonFormatter
    args=('/var/log/st2/st2actionrunner.{pid}.audit.log',)

    [formatter_simpleConsoleFormatter]
    class=st2common.logging.formatters.ConsoleLogFormatter
    format=%(asctime)s %(levelname)s [-] %(message)s
    datefmt=

    [formatter_verboseConsoleFormatter]
    class=st2common.logging.formatters.ConsoleLogFormatter
    format=%(asctime)s %(thread)s %(levelname)s %(module)s [-] %(message)s
    datefmt=

    [formatter_gelfFormatter]
    class=st2common.logging.formatters.GelfLogFormatter
    format=%(message)s

    [formatter_jsonFormatter]
    class=pythonjsonlogger.jsonlogger.JsonFormatter
    format=%(asctime) %(thread) %(levelname) %(module) %(message)

To:

.. sourcecode:: ini
   :emphasize-lines: 11,16,22

    [loggers]
    keys=root

    [handlers]
    keys=consoleHandler, fileHandler, auditHandler

    [formatters]
    keys=simpleConsoleFormatter, verboseConsoleFormatter, gelfFormatter, jsonFormatter

    [logger_root]
    level=DEBUG
    handlers=consoleHandler, fileHandler, auditHandler

    [handler_consoleHandler]
    class=StreamHandler
    level=DEBUG
    formatter=simpleConsoleFormatter
    args=(sys.stdout,)

    [handler_fileHandler]
    class=st2common.log.FormatNamedFileHandler
    level=DEBUG
    formatter=verboseConsoleFormatter
    args=('/var/log/st2/st2actionrunner.{pid}.log',)

    [handler_auditHandler]
    class=st2common.log.FormatNamedFileHandler
    level=AUDIT
    formatter=jsonFormatter
    args=('/var/log/st2/st2actionrunner.{pid}.audit.log',)

    [formatter_simpleConsoleFormatter]
    class=st2common.logging.formatters.ConsoleLogFormatter
    format=%(asctime)s %(levelname)s [-] %(message)s
    datefmt=

    [formatter_verboseConsoleFormatter]
    class=st2common.logging.formatters.ConsoleLogFormatter
    format=%(asctime)s %(thread)s %(levelname)s %(module)s [-] %(message)s
    datefmt=

    [formatter_gelfFormatter]
    class=st2common.logging.formatters.GelfLogFormatter
    format=%(message)s

    [formatter_jsonFormatter]
    class=pythonjsonlogger.jsonlogger.JsonFormatter
    format=%(asctime) %(thread) %(levelname) %(module) %(message)

After that you need to restart the corresponding service or services with ``st2ctl
restart-component st2actionrunner`` / ``st2ctl restart`` for changes to take an affect.

Running Single-threaded Services
--------------------------------

If you are debugging issues with ``st2api`` or ``st2auth``, it may be useful to start a
single-threaded worker. You can do so with these commands:

.. sourcecode:: bash

   /opt/stackstorm/st2/bin/gunicorn_pecan /opt/stackstorm/st2/lib/python2.7/site-packages/st2api/gunicorn_config.py -k eventlet -b 127.0.0.1:9101 --workers 1 --threads 1 --graceful-timeout 10 --timeout 30

   /opt/stackstorm/st2/bin/gunicorn_pecan /opt/stackstorm/st2/lib/python2.7/site-packages/st2auth/gunicorn_config.py -k eventlet -b 127.0.0.1:9100 --workers 1 --threads 1 --graceful-timeout 10 --timeout 30
