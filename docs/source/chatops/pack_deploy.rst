Packs
=====

Installing packs with ChatOps
-----------------------------

When you have the bot listening for ChatOps commands in a channel, installing extra packs
from StackStorm Exchange can be done by running a single command:

.. code-block:: bash

    !pack install github,slack,trello
    bot: Installing the requested pack(s) for you.
    @my_user:
    > Successful deployment of *github*, *slack*, *trello* packs!

You can install a pack from any github repository just as easily: supply the full URL
to the bot. Pack name is unnecessary, as it will be read from ``pack.yaml`` later:

.. code-block:: bash

    !pack install https://github.com/stackstorm/openstack
    bot: Installing the requested pack(s) for you.

You can even mix the two formats in one string:

.. code-block:: bash

    !pack install github,slack,trello,https://github.com/stackstorm/openstack

.. figure :: /_static/images/pack-chatops-install.png
    :align: center


Getting information about an installed pack
-------------------------------------------

The ``!pack get <pack>`` command shows you information about an installed
pack. There is two sections in the output: the first is pack metadata from
``pack.yaml``, and the optional second is git information, if your pack has
been installed from a git source like StackStorm Exchange or a single repo.

Git status will tell you if there's a difference between your local pack version
and the latest version in the origin repository, and also show the remotes
for your pack.

If a pack is not installed, but available in StackStorm Exchange, the bot will
gallantly offer to install it:

.. figure :: /_static/images/pack-chatops-get.png
    :align: center

Getting information about an available pack
-------------------------------------------

The remote counterpart to ``pack get`` is ``pack show``: it will show an
entry from the StackStorm Exchange, our pack directory, if a pack with the
given name is available.

.. figure :: /_static/images/pack-chatops-show.png
    :align: center

Searching for a pack
--------------------

To search for a pack in StackStorm Exchange, use ``!pack search <query>``. Note that
your query will match results in all pack parameters: for example, you can search for
an author or a keyword, not just name and description. The results are ordered by
relevance: if you search for "cloud", first you will get packs with "cloud" in their
name—because they are the most likely to be what you were looking for—and then packs
with "cloud" in keywords or description. And then packs authored by "Mr. Cloud", if
any.

**Pro-tip:** if you configure an additional pack index (see :doc:`Working with pack indexes`),
it will be queried alongside StackStorm Exchange by commands like ``show`` or ``search``.

.. figure :: /_static/images/pack-chatops-search.png
    :align: center
