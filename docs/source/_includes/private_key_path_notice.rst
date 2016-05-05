.. note::

    If a value you specify for the ``private_key`` parameter is a path to the private key file, you
    need to make sure that the user under which action runner process is running (``stanley`` by
    default) has read access to this key file.

    In addition to that, if you utilize path to the private key file functionality, you are strongly
    encouraged to disable local runner in the config. If you don't do that, any |st2| user which has
    access to ``core.local`` action will be able to read this key and this can pose a security risk.
