.. note::

    When using ``pam`` authentication backend you need to make sure that
    ``st2auth`` process runs as ``root`` system user otherwise the
    authentication will fail. For security reasons ``st2auth`` process runs
    under ``st2`` user by default. If you want to use ``pam`` auth backend and
    change it to run as ``root``, you can do that by editing service manager
    file for the ``st2`` auth service.
