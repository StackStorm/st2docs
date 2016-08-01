ChatOps Troubleshooting Guide
=============================

This guide will help you troubleshoot ``st2chatops``, up to the point where Hubot should work, reply to your
commands and send manually triggered messages via ``chatops.post_message``. 

**Note:** Recommended way to install ``st2chatops`` is using the steps mentioned
in :doc:`Installation Section <../install/index>` for the supported OS.

----------------------------------------------
Troubleshooting using Hubot self-check script:
----------------------------------------------

We have a `self-check script <https://github.com/StackStorm/st2chatops/blob/master/scripts/self-check.sh>`_ 
to help you debug chatops issue in StackStorm 1.5 and above.

Just copy and run it on the server. It runs a few essential tests giving you basic troubleshooting steps in
case of a failure.


-------------------------------------------------
Manual troubleshooting stepssame as  the script):
-------------------------------------------------

The assumption is that StackStorm client can connect to the server instance. Authentication is in place and
``st2 run core.local cmd=echo`` succeeds. (This is checked in the script mentioned above.). Following are the
issues that users usually face with chatOps:


Your bot is not online:
-----------------------

You've installed StackStorm, but Hubot didn't come online in your chatOps client (Slack, Hipchat etc..)

    *Possible reasons:*

    - Incorrect adapter settings. Check ``/opt/stackstorm/chatops/st2chatops.env`` for adapter settings.
      For example, for slack adapter, we need to uncomment following lines and update slack token:

        .. code-block:: shell

           # Slack settings (https://github.com/slackhq/hubot-slack):
           # export HUBOT_ADAPTER=slack
           # export HUBOT_SLACK_TOKEN=xoxb-CHANGE-ME-PLEASE

      After changing the adapter settings don't forget to restart the service using this command:
        
        .. code-block:: shell

           $ sudo service st2chatops restart

    - Also, make sure the login credentials and ``ST2_HOSTNAME`` are correct.
    - Check if Hubot-stacksotrm is installed:

        .. code-block:: shell

           $ cd /opt/stackstorm/chatops && npm list | grep hubot-stackstorm

      In case the installation is outdated or corrupt, install hubot-stackstorm:
      
        .. code-block:: shell
        
           $ cd /opt/stackstorm/chatops && npm install hubot-stackstorm


There's no StackStorm commands in `!help`:
--------------------------------------------

Hubot is online, but when you say ``!help``, only default commands are listed (no commands starting with ``st2``).

    *Possible reasons:*

    - Hubot can't connect to StackStorm API. Look in the Hubot logs for errors: ``/var/log/st2/st2chatops.log``
    - Commands aren't registered. Try ``st2ctl reload --register-all``.
    - It's also possible you changed the bot's name or you have not invited your bot to a channel in the chatOps
      client. 


StackStorm commands throw errors:
---------------------------------

Hubot is online, you can see ``st2`` commands, but saying something like ``!st2 list actions``
either throws an error, or gives an acknowledgement message without result, or no response at all.

    *Possible reasons:*

    - Hubot is disconnected from StackStorm stream. Try ``st2ctl reload --register-all``.
    - There's a back-end problem. Make sure other parts of StackStorm are working properly. This is addressed in
      Step 6 and Step 7 of the
      `self-check script <https://github.com/StackStorm/st2chatops/blob/master/scripts/self-check.sh>`_.


StackStorm commands are fine but no manual messages:
----------------------------------------------------

You can run StackStorm commands (and your own aliases) via your bot,
but you can't trigger `chatops.post_message` action manually from CLI or Web UI.

    *Possible reasons:*

    - Some of your action parameters (route, channel, etc) are incorrect. Take a look at ``chatops.post_result`` workflow
      execution from any chat command you issued before, and repeat every parameter in ``post_message`` (the last step of
      the workflow) as is.


By now you should have your bot up and running. If not, then just :doc:`Ask for Help! <ask_for_support>`

