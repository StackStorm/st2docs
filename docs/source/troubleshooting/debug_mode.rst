Enabling Debug Mode
===================

You can enable debug mode for a particular service by starting it with a ``--debug`` command line
flag or by editing ``st2.conf`` config file and setting ``system.debug`` setting to ``True`` as
shown below and restarting all the services using ``st2ctl restart``.

.. sourcecode:: ini

    [system]
    debug = True

When running a service in the debug mode, all the log messages logged under ``DEBUG`` log level
will also be included in the logs which should make troubleshooting different issues easier. In
addition to that, when debug mode is enabled, all the API JSON responses are pretty-formatted and
a traceback will also be included in the logs for all the API requests which result in an
exception.

Running Single-threaded Services
--------------------------------

If you are debugging issues with ``st2api`` or ``st2auth``, it may be useful to start a
single-threaded worker. You can do so with these commands:

.. sourcecode:: bash

   /opt/stackstorm/st2/bin/gunicorn_pecan /opt/stackstorm/st2/lib/python2.7/site-packages/st2api/gunicorn_config.py -k eventlet -b 127.0.0.1:9101 --workers 1 --threads 1 --graceful-timeout 10 --timeout 30

   /opt/stackstorm/st2/bin/gunicorn_pecan /opt/stackstorm/st2/lib/python2.7/site-packages/st2auth/gunicorn_config.py -k eventlet -b 127.0.0.1:9100 --workers 1 --threads 1 --graceful-timeout 10 --timeout 30

