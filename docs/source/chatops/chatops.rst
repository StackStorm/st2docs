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

Officially Supported Chat Providers
===================================

We officially provide support for the following chat providers with hubot:

* `Slack <https://github.com/slackapi/hubot-slack>`_
* Microsoft Teams (via `BotFramework <https://github.com/Microsoft/BotFramework-Hubot>`_)
* `Mattermost **version 5** <https://github.com/loafoe/hubot-matteruser>`_
* `Rocket.Chat <https://github.com/RocketChat/hubot-rocketchat>`_
* `Cisco Spark <https://github.com/tonybaloney/hubot-spark>`_

Since
`HipChat is being discontinued <https://www.atlassian.com/blog/announcements/new-atlassian-slack-partnership>`_,
official support for the `HipChat adapter <https://github.com/hipchat/hubot-hipchat>`_ will end when
HipChat reaches end-of-life (as of this writing, this is planned for June 30th, 2020), and it will be
completely removed **without any deprecation period** from the st2chatops project once HipChat itself
is terminated. Administrators of local HipChat servers should **already** be actively migrating to
other chat providers.

For help migrating between chat providers, please see the section on
:ref:`specifying multiple extra keys for different providers <specifying-multiple-extra-keys-for-different-providers>`
for some ideas on how to ease the transition between HipChat and another chat provider.

Officially Unsupported Chat Providers
=====================================

We do not provide support for the following adapters, but they are still bundled in the
st2chatops package, can be configured in ``st2chatops.env``, and still work (as far as we
know).

* `Flowdock <https://github.com/flowdock/hubot-flowdock>`_
* `XMPP <https://github.com/markstory/hubot-xmpp>`_
* `IRC <https://github.com/nandub/hubot-irc>`_

Configuration
=============

.. note:: Microsoft Teams

    Configuring st2chatops with Microsoft Teams is a more involved process. Please see
    `our documentation <msteams_is_a_diva>` specifically for that chat provider.
    All other chat providers can be configured in ``st2chatops.env`` with the instructions
    below.

Package-based Install
~~~~~~~~~~~~~~~~~~~~~

If you installed |st2| following the :doc:`install docs </install/index>`, the ``st2chatops``
package will take care of `almost` everything for you. Hubot with the necessary adapters is already
installed, and StackStorm :ref:`API keys <authentication-apikeys>` have been configured. 

You just need to tell |st2| which Chat service to use - e.g. Slack, MatterMost, etc. You will also need
to give it credentials. Your Chat service may also need configuration. For example, to configure Slack,
you first need to add a new Hubot integration to Slack. You can do this through Slack's admin interface.
Take note of the ``HUBOT_SLACK_TOKEN`` that Slack provides.

Then edit the file ``/opt/stackstorm/chatops/st2chatops.env``. Edit and uncomment the variables for 
your adapter. For example, if you are configuring Slack, look for this section:

.. code-block:: bash

    # Slack settings (https://github.com/slackhq/hubot-slack):
    #
    # export HUBOT_ADAPTER=slack
    # Obtain the Slack token from your app page at api.slack.com, it's the "Bot
    # User OAuth Access Token" in the "OAuth & Permissions" section.
    # export HUBOT_SLACK_TOKEN=xoxb-CHANGE-ME-PLEASE
    # Uncomment the following line to force hubot to exit if disconnected from slack.
    # export HUBOT_SLACK_EXIT_ON_DISCONNECT=1

Edit this file so it looks something like this:

.. code-block:: bash

    # Slack settings (https://github.com/slackhq/hubot-slack):
    #
    export HUBOT_ADAPTER=slack
    # Obtain the Slack token from your app page at api.slack.com, it's the "Bot
    # User OAuth Access Token" in the "OAuth & Permissions" section.
    export HUBOT_SLACK_TOKEN=xoxb-SUPER-SECRET-TOKEN
    # Uncomment the following line to force hubot to exit if disconnected from slack.
    export HUBOT_SLACK_EXIT_ON_DISCONNECT=1

Your specific Chat service may require different settings. Any environment settings needed can be
added to this file. 

Once you have finished making changes, restart ``st2chatops`` with ``sudo service st2chatops restart``.
Check your :ref:`log files<ref_chatops_logging>` to ensure that it is successfully connected. 

If you want the ChatOps messages to include the right hyperlink to execution url for the action
you kicked off via ChatOps, you have to point |st2| to the external address for the host running
the web UI. To do so, edit the ``webui`` section in ``/etc/st2/st2.conf``. For example:

.. code-block:: ini

    [webui]
    webui_base_url = https://st2web001.stackstorm.net

Using an External Adapter
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``st2chatops`` package includes adapters for common chat services, but if an
adapter for a service you use isn't bundled there, don't worry: you can install it manually.

For example, here's how to connect |st2| to Yammer using the ``hubot-yammer`` adapter:

1. Install the adapter.

  .. code-block:: bash

    $ cd /opt/stackstorm/chatops
    $ sudo npm install hubot-yammer


2. Modify ``/opt/stackstorm/chatops/st2chatops.env`` to include
   the necessary adapter settings.

  .. code-block:: bash

    export HUBOT_ADAPTER=yammer
    export HUBOT_YAMMER_ACCESS_TOKEN="secret_access_token"
    export HUBOT_YAMMER_GROUPS="groups list"


3. Restart the service.

  .. code-block:: bash

    $ sudo systemctl restart st2chatops

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

.. _ref_chatops_logging:

Logging
=======

ChatOps logs are written to ``/var/log/st2/st2chatops.log`` on non systemd-based distros. For
systemd-based distros (Ubuntu 16, RHEL/CentOS 7), you can access the logs via
``journalctl --unit=st2chatops``
