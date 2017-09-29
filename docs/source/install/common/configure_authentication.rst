* Enable and configure authentication in ``/etc/st2/st2.conf``:

  .. sourcecode:: ini

    [auth]
    # ...
    enable = True
    backend = flat_file
    backend_kwargs = {"file_path": "/etc/st2/htpasswd"}
    # ...

* Restart the st2api service:

  .. code-block:: bash

    sudo st2ctl restart-component st2api

* Authenticate, set the token environment variable, and check that it works:

  .. code-block:: bash

    # Get an auth token to use in CLI or API
    st2 auth st2admin

    # A shortcut to authenticate and export the token
    export ST2_AUTH_TOKEN=$(st2 auth st2admin -p 'Ch@ngeMe' -t)

    # Check that it works
    st2 action list

Check out the :doc:`/reference/cli` to learn other convenient ways to authenticate via CLI.
