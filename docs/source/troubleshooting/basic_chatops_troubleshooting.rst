ChatOps Troubleshooting Guide
=============================

This guide will help you troubleshoot ``st2chatops``, up to the point where Hubot should work,
reply to your commands and send manually triggered messages via ``chatops.post_message``. 

.. note::
    
    The recommended way to install ``st2chatops`` is using the steps mentioned 
    in :doc:`Installation Section <../install/index>` for your OS.

----------------------------------------------
Troubleshooting Using Hubot Self-check Script:
----------------------------------------------

We have a `self-check script <https://github.com/StackStorm/st2chatops/blob/master/scripts/self-check.sh>`_ 
to help you debug ChatOps issues in StackStorm 1.5 and above.

Just copy the script and run it on your server. It will run a few essential tests that will provide you basic troubleshooting steps in
case of a failure.

-----------------------------
Manual Troubleshooting Steps:
-----------------------------

These are the issues that users usually face with ChatOps:

----------

Your bot is not Online:
-----------------------

You have installed StackStorm, however Hubot did not come online in your ChatOps client (Slack, HipChat, etc.)

**Possible reasons:**

- Incorrect adapter settings. Check the settings in ``/opt/stackstorm/chatops/st2chatops.env`` to verify if correct.
  For example, for the Slack adapter, we need to uncomment the following lines and update the
  Slack token:

  .. code-block:: shell

     # Slack settings (https://github.com/slackhq/hubot-slack):
     # export HUBOT_ADAPTER=slack
     # export HUBOT_SLACK_TOKEN=xoxb-CHANGE-ME-PLEASE

  After changing the adapter settings don't forget to restart the service using this command:
        
  .. code-block:: shell

     $ sudo service st2chatops restart

- Make sure the login credentials and ``ST2_HOSTNAME`` are correct.
- After you made sure ``st2chatops.env`` settings are correct, check if the service is running:

  .. code-block:: shell

    $ service st2chatops status

In case the installation is outdated or became corrupted, reinstall the ``st2chatops`` package with
``apt-get`` or ``yum`` depending on your distro.

Note that in most chat services you have to manually invite the bot into your chatroom first: for example,
`in Slack <https://get.slack.help/hc/en-us/articles/201980108-Inviting-team-members-to-a-channel>`_.

----------

There is no StackStorm Commands in ``!help``:
---------------------------------------------

Hubot is online and present in your room, however when you say ``!help``, there are no commands listed except ``!help`` itself. (The ``pack`` and ``st2`` sets of commands should be installed by default).

**Possible reasons:**

- Hubot can not connect to StackStorm API. Look in the st2chatops logs for errors: 
  ``/var/log/st2/st2chatops.log`` or for systemd based distros ``journalctl --unit=st2chatops``
- Actions and/or ChatOps aliases aren't registered. Try running ``st2ctl reload --register-all``.
- It is also possible you may have changed the bot's name or you have not invited your bot to a channel in
  the chat client.
- If you are sending the bot a private message instead of messaging it in a channel, do not prepend
  ``!`` (a known Hubot limitation). In private messages, ``help`` will work, however ``!help`` will not;
  in channels it works the other way around. 

---------------------------------

StackStorm Commands Throw Errors:
---------------------------------

Hubot is online, you can see ``st2`` commands, however, it is saying something like ``!st2 list actions``
either throws an error, or gives an acknowledgement message without result, or no response at all.

**Possible reasons:**

1. No response at all:
     Usually the command you're trying to run has a typo, or the syntax is incorrect.
     Double-check it, and glance over the alias yaml definition to check what the
     command syntax is exactly.
    
2. Throws an error (no acknowledgement):
     Should be debugged according to the error, could be both client-side and server-side,
     or an alias problem. Normally, a look into an error or logs will provide you ideas on
     how to proceed.

3. Gives an acknowledgement message without result:
     If you get an acknowledgement message, but then nothing happens, Hubot is most likely 
     disconnected from the StackStorm stream. The main reason for it is a wrong
     networking setup (Hubot can't connect to your StackStorm instance); check nginx
     configuration and the parameters in ``/opt/stackstorm/chatops/st2chatops.env`` 
     (most importantly, ``ST2_HOSTNAME``).
     Another reason is that either the StackStorm action you're trying to launch or your alias
     fails with an unexpected error that the bot can't process. This can be checked in 
     StackStorm execution history through CLI or Web UI.

4. Gives an acknowledgement message, then an error:
     If the default commands (like ``!st2 list actions``) run fine, but your own
     aliases throw errors, the format of your alias or the underlying action is most
     likely the problem. Debug according to the error.

5.  Bonus: have you tried turning StackStorm off and on again?
     ``sudo st2ctl restart`` or ``sudo st2ctl reload --register-all`` sometimes seem to 
     magically fix problems, often quite unexpectedly. Restarting just the
     ``st2chatops`` service also works sometimes: ``sudo service st2chatops restart``.

If the problem persists, there's likely a back-end problem. Make sure other parts of StackStorm
are working properly. Try Step 6 and Step 7 of the
`self-check script <https://github.com/StackStorm/st2chatops/blob/master/scripts/self-check.sh>`_ :

----------

StackStorm Commands are Fine but no Manual Messages:
----------------------------------------------------

You can run StackStorm commands (and your own aliases) via your bot,
but you can't trigger ``chatops.post_message`` action manually from CLI or Web UI.

**Possible reasons:**

- Some of your action parameters (route, channel, etc) are incorrect. Take a look at
  ``chatops.post_result`` workflow execution from any chat command you issued before, and repeat
  every parameter in ``chatops.post_message`` (the last step of the workflow) as is. 

- ``st2 run chatops.post_message channel=<channel_name>`` to post on a channel. This step
  assumes that a bot was created and is invited it to the channel on ChatOps application.

- ``st2 run chatops.post_message channel=<username> whisper=True`` to post to a user. Note 
  that some chat services have limitations on private messages from bots to users (e.g. in 
  Slack a bot can't initiate a new conversation).

By now you should have your bot up and running. If not, then just :doc:`ask for help! <ask_for_support>`
