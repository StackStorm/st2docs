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

* Authenticate, and check that it works:

  .. code-block:: bash

    # Login - you will be prompted for password (default 'Ch@ngeMe')
    st2 login st2admin

    # Check that it works
    st2 action list

