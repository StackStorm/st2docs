.. _ref-chatops:

What is ChatOps?
================

ChatOps is a new operational paradigm - work that is already happening in the background today is
brought into a common chatroom. By doing this, you are unifying the communication about what work
should get done with the actual history of the work being done. Things like deploying code from
Chat, viewing graphs from a TSDB or logging tool, or creating new Jira tickets...all of these are
examples of tasks that can be done via ChatOps.

Architecture
============

.. figure:: /_static/images/chatops_architecture.png
    :align: center

    |st2| ChatOps Integration Overview

ChatOps leverages two components within |st2| in order to provide a fluid user experience. These
subsystems are the :doc:`aliases` and :doc:`notifications` subsystems. You can learn more about
each of these individual components in their corresponding sub-sections.

StackStorm-flavored ChatOps
===========================

Our goal with ChatOps is to take common patterns and make them consumable by teams of all makeups.
Behind our implementation of ChatOps lies the operational scalability and stability of |st2|,
allowing you to grow and unleash the latent power of your existing teams. In addition to allowing
integration with a plethora of existing plugins and patterns available in the larger |st2| and
ChatOps communities, we've added these features to the tool-belt:

* History and Audit. Get complete history and audit trails of all commands executed via ChatOps.
  Learn and understand how people are consuming the automation via ChatOps. Enhance your
  understanding.
* Workflow. Get real with workflow. Go beyond linear Bash scripts and upgrade to parallel task
  execution.
* Bring your favorite tools! Each bot comes with its own requirement to learn their language.
  Forget that mess! Bring the tools that make you productive.

We want to make ChatOps approachable by every team in every circumstance. This means an
understanding of how teams of all sizes run, in many different types of verticals. Issues like
compliance, security, reliability: these concerns are at the forefront of our minds when we think
about what ChatOps means to us, and how it provides real-world value to you.

.. _chatops-configuration:

Configuration
=============

Package-based Install
~~~~~~~~~~~~~~~~~~~~~

If you installed StackStorm following the :doc:`install docs </install/index>`, the ``st2chatops``
package will take care of everything for you. Hubot with the necessary adapters is already bundled,
and environment variables are sourced from ``/opt/stackstorm/chatops/st2chatops.env``.

Edit the file to specify your Chat service and bot credentials. If you need extra environment
settings for Hubot, you should store them in ``st2chatops.env`` as well.

If you want the ChatOps messages to include the right hyperlink to execution url for the action
you kicked off via ChatOps, you have to point |st2| to the external address for the host running
the web UI. To do so, edit the ``webui`` section in ``/etc/st2/st2.conf``. For example:

.. code-block:: ini

    [webui]
    webui_base_url = https://st2web001.stackstorm.net

Using an External Adapter
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``st2chatops`` package has an extensive list of built-in adapters for chat services, but if an
adapter for a service you use isn't bundled there, you can install it manually.

For example, here's how to connect StackStorm to Mattermost using the ``hubot-mattermost`` adapter:

1. Install the adapter.

  .. code-block:: bash

    $ cd /opt/stackstorm/chatops
    $ sudo npm install hubot-mattermost


2. Modify ``/opt/stackstorm/chatops/st2chatops.env`` to include
   the necessary adapter settings.

  .. code-block:: bash

    export HUBOT_ADAPTER=mattermost
    export MATTERMOST_ENDPOINT=/hubot/incoming
    export MATTERMOST_INCOME_URL=http://mm:31337/hooks/ncwc66caqf8d7c4gnqby1196qo
    export MATTERMOST_TOKEN=oqwx9d4khjra8cw3zbis1w6fqy


3. Restart the service.

  .. code-block:: bash

    $ sudo service st2chatops restart

Hubot should now connect to your chat service. Congratulations!

Please note that while we always try to help the best we can, we can't support adapters that are
not bundled into ``st2chatops`` since they are too numerous. If you run into trouble with an
external adapter, it's usually best to open an issue in the adapter's GitHub repo or contact the
authors.

Hubot developers maintain a list of adapters on the
`Hubot documentation website <https://hubot.github.com/docs/adapters/>`_.

Bring Your Own Hubot
~~~~~~~~~~~~~~~~~~~~

If you already have a Hubot instance, you'll need the ``hubot-stackstorm`` module installed and
the following environment variables set up:

-  ``ST2_API`` FQDN + port to |st2| endpoint. Typically: ``https://<host>:443/api``
-  ``ST2_AUTH_URL`` FQDN + port to |st2| Auth endpoint: ``https://<host>:443/auth``
-  ``ST2_API_KEY`` |st2| API key

Once done, start your Hubot instance. Validate that things are working correctly and that Hubot
is connecting to your client by issuing the default ``help`` command:

.. figure:: /_static/images/chatops_demo.gif

By default, commands from the ``st2`` pack are installed. They are useful for getting info from
your |st2| instance.

.. note::

    You can issue Hubot commands in channels by using either ``!`` or the bot's nickname. If your
    bot is named ``@ellie`` in Slack, you can use both ``!help`` and ``@ellie: help``.

    Note that if you send your command as a private message, you should just write ``help``
    without an alias or a nickname. Your bot already knows you're talking to her and not someone
    else!

If successful, proceed to the next section.

Adding New ChatOps Commands
===========================

ChatOps uses :doc:`/chatops/aliases` to define new ChatOps commands.

.. code-block:: bash

    $ cd /opt/stackstorm/packs/
    $ mkdir -p my-chatops/{actions,rules,sensors,aliases}

Now, let's setup an alias. For the purpose of this setup aliases are stored in the directory
``/opt/stackstorm/packs/my-chatops/aliases``. We have already created this directory in a previous
step. 

This alias will execute commands on hosts through SSH with the ``core.remote`` action. Create a
new file called ``remote.yaml``, and add the following contents:

.. code-block:: yaml

    # packs/my-chatops/aliases/remote.yaml
    ---
    name: "remote_shell_cmd"
    action_ref: "core.remote"
    description: "Execute a command on a remote host via SSH."
    formats:
      - "run {{cmd}} on {{hosts}}"

Once this is all done, register the new files we created and reload Hubot:

.. code-block:: bash

    $ sudo st2ctl reload --register-aliases
    $ sudo service st2chatops restart

This will register the aliases we created, and tell Hubot to go and refresh its command list.

You should now be able to go into your chatroom, and execute the command
``!run date on localhost``, and StackStorm will take care of the rest.

.. figure:: /_static/images/chatops_command_out.png

To customize the command output you can use Jinja templates as described in :doc:`aliases`.

Logging
=======

ChatOps logs are written to ``/var/log/st2/st2chatops.log`` on non systemd-based distros. For
systemd-based distros (Ubuntu 16, RHEL/CentOS 7), you can access the logs via
``journalctl --unit=st2chatops``