* Review and edit the ``/opt/stackstorm/chatops/st2chatops.env`` configuration file to point it to
  your |st2| installation and the Chat Service you are using. At a minimum, you should generate an
  :ref:`API key <authentication-apikeys>` and set the ``ST2_API_KEY`` variable. By default
  ``st2api`` and ``st2auth`` are expected to be on the same host. If that is not the case, please
  update the ``ST2_API`` and ``ST2_AUTH_URL`` variables or just point to the correct host with
  ``ST2_HOSTNAME``.

  The example configuration uses Slack. To set this up, go to the Slack web admin interface, create
  a Bot, and copy the authentication token into ``HUBOT_SLACK_TOKEN``.

  If you are using a different Chat Service, set the corresponding environment variables under the
  ``Chat service adapter settings`` section in ``st2chatops.env``:
  `Slack <https://github.com/slackhq/hubot-slack>`_,
  `HipChat <https://github.com/hipchat/hubot-hipchat>`_,
  `Flowdock <https://github.com/flowdock/hubot-flowdock>`_,
  `IRC <https://github.com/nandub/hubot-irc>`_ ,
  `Mattermost <https://github.com/loafoe/hubot-matteruser>`_,
  `RocketChat <https://github.com/RocketChat/hubot-rocketchat>`_,
  `XMPP <https://github.com/markstory/hubot-xmpp>`_.
