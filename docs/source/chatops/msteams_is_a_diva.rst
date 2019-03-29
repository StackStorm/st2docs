Using Microsoft Teams (with BotFramework)
=========================================

Configurating st2chatops with Microsoft Teams is **much** more involved than configuring
other chat providers.

.. note:: Caveats

    * There are multiple hubot adapters for Microsoft Teams and/or BotFramework. Only
      two of them (that we found) are production quality, and only the
      BotFramework-Hubot project is the officially supported option.
    * Microsoft BotFramework's "push model" requires bots to have an open port open to
      the internet. This is a limitation of Teams/BotFramework.
      (`source <https://github.com/Microsoft/BotFramework-Hubot#common-differences-in-hubot-running-in-slack-hipchat-other-chat-platforms-and-ms-teams>`_)
    * The BotFramework bot does not receive all messages in a channel. Users MUST
      explicitly at-mention the bot user to send any messages to the bot.
    * Users can alternatively direct message the bot user itself (without
      at-mentioning it) in the bot user's "room". This isn't really considered ChatOps
      though. And it is impossible to disable this "feature" from within Teams itself.
      However, all StackStorm alias executions are logged as normal, although StackStorm's
      RBAC does not work in st2chatops.
    * The `Orky <https://github.com/OfficeDev/Orky>`_ project is meant to run within Azure
      and send events via a websocket. We have investigated this method but we were unable
      to get it working in development.

Setup BotFramework
~~~~~~~~~~~~~~~~~~

1. Note the internet accessible hostname and port for your st2chatops (hubot) server.
2. Register a bot within `BotFramework <https://dev.botframework.com/bots/new>`_.
3. Note your Microsoft App ID and password, you will need these later.
4. Configure the "Messaging endpoint" option to your st2chatops server, and append
   ``/api/messages`` to it.

  .. code-block:: none

    https://<hostname>:<port>/api/messages

  .. warning::

    Ensure that URI path of the messaging endpoint matches the ``BOTBUILDER_ENDPOINT``
    setting in your ``/opt/stackstorm/chatops/st2chatops.env`` configuration file.

Create the bot application manifest zip file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application manifest is a zip folder of a few files:

* ``coloricon.png`` - a 96px by 96px png icon of your bot
* ``outlineicon.png`` - a 20px by 20px png icon of your bot
* ``manifest.json`` - a JSON file that describes your bot

Below is an example of a ``manifest.json`` file. You should copy these contents and
modify them to match your organization. Use the Microsoft App ID you got from the
previous steps to fill in BOTH the ``id`` and ``botId`` values. However, you will NOT
use the Microsoft App password in this file. All information included in this file
will be specific to your deployment of StackStorm.

.. code-block:: json

    {
      "manifestVersion": "1.0",
      "version": "1.0",
      "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee",
      "packageName": "company.division.stackstorm.chatops",
      "developer": {
        "name": "Company",
        "websiteUrl": "https://example.com/Organization/Project",
        "privacyUrl": "https://example.com/Organization/Project/blob/master/privacy.md",
        "termsOfUseUrl": "https://example.com/Organization/Project/blob/master/terms.md"
      },
      "name": {
        "short": "StackStorm (bot)",
        "full": "StackStorm automation platform"
      },
      "description": {
        "short": "You can use StackStorm with ChatOps",
        "full": "You can use StackStorm to implement ChatOps within your organization!"
      },
      "icons": {
        "outline": "outlineicon.png",
        "color": "coloricon.png"
      },
      "accentColor": "#FFFFED",
      "bots": [
        {
          "botId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee",
          "isNotificationOnly": false,
          "scopes": [
            "team",
            "personal"
          ],
          "commandLists":[
            {
              "scopes":[
                "team",
                "personal"
              ],
              "commands":[]
            }
          ]
        }
      ]
    }

If you know what ChatOps commands StackStorm will support, you can specify them in the
``commandLists`` array. This will allow Teams to display better help information, but
it is not possible to dynamically update this information when new aliases are added
to st2chatops, or when aliases are changed. Due to this limitation, it is probably best
to make this the basic st2chatops/hubot help command (which is ``!help`` by default).

Here is a snippet of ``commandLists`` from the Orky project:

.. code-block:: none

    "commandLists":[
      {
        "scopes":[
            "team",
            "personal"
        ],
        "commands":[
          {
              "title":"add ",
              "description":"Adds a bot with the given name."
          },
          {
              "title":"remove ",
              "description":"Removes a bot with the given name."
          },
          {
              "title":"enable ",
              "description":"Enables a bot."
          },
          {
              "title":"disable ",
              "description":"Disables a bot."
          },
          {
              "title":"copy ",
              "description":"Copies a bot and returns the copy key."
          },
          {
              "title":"paste ",
              "description":"Pastes a bot referenced by the copied key."
          },
          {
              "title":"rename ",
              "description":"Renames a bot."
          },
          {
              "title":"status",
              "description":"Shows the status of your bots."
          },
          {
            "title":"tell ",
            "description":"Tells a bot to execute a command."
          }
        ]
      }
    ]

.. warning::

    Make sure that ``id`` and ``botId`` are the same values!

Zip all of those files into the root of a zip file:

.. code-block:: bash

    $ zip manifest.zip manifest.json outlineicon.png coloricon.png

.. warning::

    Make sure that the files themselves are located at the root of the zip file and not in
    a directory in the zip file root!

Sideload the application manifest into Microsoft Teams
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    - You will need to sideload the application manifest into all teams that use ChatOps.
    - You will need to have administrator privileges in your Microsoft Teams tenant to
      sideload application manifests. If you do not see the "Upload a custom app" option
      then you do not have the correct permissions to sideload a bot application.

1. Go to the "Teams" tab on the left column, and click a team you wish to sideload to.
2. Click the three horizontal dots next to the team name in the channel list.
3. Select "Manage team", and go to the "Apps" tab in the main pane.
4. At the bottom right of the main pane, click the "Upload a custom app" link.
5. Upload the application manifest file you created previously.

Configure ``st2chatops.env``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modify your st2chatops configuration file at ``/opt/stackstorm/chatops/st2chatops.env``.
Uncomment the lines for ``HUBOT_ADAPTER=botframework``, but do NOT change this value.
Also uncomment the lines for ``BOTBUILDER_APP_ID`` and ``BOTBUILDER_APP_PASSWORD``, and
change their values to the Microsoft App ID and password from the previous steps.

.. warning::

    Ensure that the ``BOTBUILDER_APP_ID`` is the same as the ``id`` and ``botId`` in your
    manifest file.

If you did not configure the ``/api/messages`` endpoint in your BotFramework configuration,
set the ``BOTBUILDER_ENDPOINT`` to the URI path you used. Set the rest of the options for
Microsoft Teams/BotFramework in ``st2chatops.env``.

.. warning::

    If you do not set ``HUBOT_OFFICE365_TENANT_FILTER``, then ALL Office365 tenants will be
    able to communicate with your hubot instance if they sideload your application manifest.

Restart st2chatops
~~~~~~~~~~~~~~~~~~

Restart st2chatops with the ``st2ctl`` command:

.. code-block:: bash

    st2ctl restart-component st2chatops

Troubleshooting
~~~~~~~~~~~~~~~

Troubleshooting the Microsoft Teams adapter is nearly impossible to do directly. You can
use the test client in the configuration webpage of your BotFramework bot to test the
connection from BotFramework to your bot. If your st2chatops logs show messages received
from the web test client in BotFramework, then the issue is between Microsoft Teams and
BotFramework. Double check the values in your application manifest, and remove and
re-upload your manifest (if you changed it). You can also message your bot directly from
within Microsoft Teams, in its own room.
