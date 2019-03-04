To use the CLI, use the ``st2 login`` command. If you do not provide a password, it will prompt for
the password:

.. code-block:: bash

    # without password
    st2 login yourusename
    Password:

    # with password
    st2 login yourusername -p 'yourpassword'

    # write password to config file
    st2 login -w yourusername -p 'yourpassword'

.. note::

    If your password contains special characters such as ``$``, they may be interpreted by the shell.
    Wrap your password in single quotes (``'``) as above.

If you need to acquire a token - for example to use with an API call, use the ``st2 auth`` command.
If a password is not provided, it will prompt for the password. If successful, a token is returned
in the response:

.. code-block:: bash

    # with password
    st2 auth yourusername -p 'yourpassword'

    # without password
    st2 auth yourusename
    Password:

The following is a sample API call via ``curl`` using that token:

.. code-block:: bash

    $ curl -H "X-Auth-Token: 4d76e023841a4a91a9c66aa4541156fe" https://myhost.example.com/api/v1/actions

This is the CLI equivalent:

.. code-block:: bash

    # Include the token as command line argument.
    st2 action list -t 4d76e023841a4a91a9c66aa4541156fe

    # Or set the token as an environment variable.
    export ST2_AUTH_TOKEN=4d76e023841a4a91a9c66aa4541156fe
    st2 action list

There may be use-cases where you want a token with a different TTL from the default. You can specify a TTL
(in seconds) when you request a token. For example, to request a token that is valid for 10 minutes:

.. code-block:: bash

    # with TTL and password
    st2 auth yourusername -p 'yourpassword' -l 600

Note that if the TTL requested is greater than the configured maximum allowed TTL, you will get an error.

If you don't want to retrieve a new token and configure the environment variable every time you start a
new shell session, you can put your |st2| credentials in the CLI configuration file. Then the CLI will
automatically authenticate, retrieve and cache the auth token for you.

For information on how to do that, see the :ref:`CLI configuration <cli-configuration>` page.
