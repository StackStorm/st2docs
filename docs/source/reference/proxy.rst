|st2| behind an HTTP proxy
==========================

If your |st2| installation is running behind a proxy, you will need to configure
``git`` and ``pip`` to utilize your proxy otherwise some CLI commands such as
``packs.install`` won't work.

Configuring git
---------------

To configure git you need to set global git ``http.proxy`` option in the
.gitconfig file for the user under which |st2| action runner component is
running.

git config is stored at ``~/.gitconfig``. To configure it, you need to put
the following lines in the config:

.. sourcecode:: ini

    [http]
    proxy = http://user:passwd@proxy.server.com:port

You can achieve the same this by running ``git config`` command which will
write into the config for you.

.. sourcecode:: bash

    git config --global http://user:passwd@proxy.server.com:port

Configuring pip
---------------

To configure pip you need to edit pip config for the user under which |st2|
action runner component is running.

pip config is stored at ``$HOME/.config/pip/pip.conf``. To configure it, you
need to put the following lines in the config:

.. sourcecode:: ini

    [global]
    proxy = [user:passwd@]proxy.server.com:port
