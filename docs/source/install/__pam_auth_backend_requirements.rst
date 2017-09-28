.. note::

    When using the ``pam`` authentication backend you need to make sure that the ``st2auth``
    process runs as ``root`` otherwise authentication will fail. For security reasons ``st2auth``
    process runs under ``st2`` user by default. If you want to use ``pam`` auth backend and change
    it to run as ``root``, you can do that by editing the service manager file for the ``st2``
    auth service.
