Notifications
=============

If you read through the :ref:`ref-chatops` section, you are familiar with notifications. Even
without ChatOps, notifications can be used to post messages to external systems like Chat clients,
send emails etc. Notifications require an action that is registered with |st2| (e.g., the
`post_message <https://github.com/StackStorm-Exchange/stackstorm-slack/tree/master/actions/post_message.yaml>`_ 
action in the ``slack`` pack) and a notification rule to go with it. Notifications are
implemented as triggers, rules, and actions. A special ``core.st2.notifytrigger`` is emitted by the
system on completion of every action. A rule to match the trigger to a notify action results in
notifications being sent out.

How Do I Setup a Notification for an Action?
--------------------------------------------

This is the easiest case. You can do this by specifying a ``notify`` section in the YAML metadata
while registering the action. For example:

.. code-block:: yaml

    ---
    description: Action that executes an arbitrary Linux command on the localhost.
    enabled: true
    entry_point: ''
    name: local-notify
    notify:
      on-complete:
        routes:
        - slack
        message: '"@channel: Action succeeded."'
    parameters:
      cmd:
        description: Arbitrary Linux command to be executed on the remote host(s).
        required: true
        type: string
      sudo:
        immutable: true
    runner_type: "local-shell-cmd"

Above is the same action as a ``local-shell-cmd`` action but with notify. As you can see, there
is a notify section with ``on-complete`` section. You can also specify ``on-success`` and
``on-failure`` sections with different messages. These subsections are all optional but at
least one is required for any meaningful notification. For the sake of clarity, an ``on-success``
case is presented below:

.. code-block:: yaml

   notify:
      on-complete:
        routes:
        - slack
        message: '"@channel: Action succeeded."'
      on-success:
        routes:
        - slack
        message: '"@channel: Woohoo!"'

When the notification triggers are sent out, the message is supplied along with a ``data``
field containing the results of the execution. The rule can use these two fields (``message`` and
``data``), and send it out as part of the action.

How Do I Write a Notification Rule?
-----------------------------------

This resembles the notify rule you are familiar with when you setup ChatOps. An example is below:

.. code-block:: yaml

    ---
    name: "notify_slack"
    pack: "examples"
    description: "Sample rule firing on action completion."
    enabled: true

    trigger:
      type: "core.st2.generic.notifytrigger"
      parameters: {}
    criteria:
      trigger.channel:
        pattern: "slack"
        type: "equals"
    action:
      ref: "slack.post_message"
      parameters:
        message: "{{trigger.message}}"

As you can see, this rule is setup for notification route ``slack``. The action section shows
that ``slack.post_message`` is the one what would be kicked off. We are skipping the ``data`` part
of the trigger for brevity. If you had a slack action that also consumed some data as JSON string,
you could pass ``data: "{{data}}"`` as a parameter.

Jinja Templating in ``message`` and ``data``
--------------------------------------------

Jinja templating is supported for both ``message`` and ``data``. The Jinja contexts available for
use are parameters of the action and runner (``{{action_parameters.cmd}}``),
keys in execution results (for example, ``{{action_results.stdout}}``,
``{{action_results.stderr}}``), anything in the action context (``{{action_context.user}}``) and
anything in the key-value store (``{{st2kv.system.foo}}``).

Some examples are shown below:

.. code-block:: yaml

  on-success:
    routes:
      - slack
    message: '"@channel: Woohoo!". Action run by user {{action_context.user}} succeeded.'

  on-success:
    routes:
      - email
    message: '"@channel: Woohoo!". Action run by user {{action_context.user}} succeeded.'
    data:
      cmd: "{{action_parameters.cmd}}"
      stdout: "{{action_results.stdout}}"

How Do I Setup Notifications in an ActionChain?
-----------------------------------------------

The procedure here is the same if you want the same notification for all tasks in the chain.
Register an action metadata with a notify section. For example:

.. code-block:: yaml

    ---
    # Action definition metadata
    name: "echochain"
    description: "Simple Action Chain workflow"

    # `runner_type` has value `action-chain` to identify that action is an ActionChain.
    runner_type: "action-chain"

    # `entry_point` path to the ActionChain definition file, relative to the pack's action directory.
    entry_point: "chains/echochain.yaml"

    enabled: true

    # Notify section for all tasks in the chain
    notify:
      on-complete:
        message: "\"@channel: Action succeeded.\""
        routes:
          - "slack"

This is mostly useless because you want to control the message in each of the tasks. See the
section below for how to do that.

How Can I Have Different Notifications for Each Task?
-----------------------------------------------------

The ``notify`` subsection is the same format as seen in examples above. Place the subsection in
ActionChain tasks. If there is a notify section for the action metadata, and a notify section in
the task, the task section will override the default. The relevant section of an ActionChain with
task notify is shown below:

.. code-block:: yaml

    -
      name: "make_reqmnts"
      ref: "core.remote"
      parameters:
        cmd: "cd {{repo_target}} && make requirements"
        hosts: "{{build_server}}"
        timeout: 300
      notify:
        on-failure:
          routes:
            - slack
          message: "Pytests failed on installing requirements."
      on-success: "make_lint"
    -
      name: "make_lint"
      ref: "core.remote"
      parameters:
        cmd: "cd {{repo_target}} && make .lint"  # .flake8 and .pylint
        hosts: "{{build_server}}"
        timeout: 180
      on-success: "make_tests"

How do I Setup Notifications for Mistral?
-----------------------------------------

The method for global notifications for the workflow is the same as ActionChain. You have a notify
section in the action meta when registering. See an
`example <https://github.com/StackStorm/st2/blob/master/contrib/examples/actions/mistral-basic-two-tasks-with-notifications.yaml#L24>`_.
Unfortunately, notifications per task are not supported in Mistral as a first class citizen yet.
This will be added in later releases.

How do I Skip Notifications for Tasks in a Workflow?
-----------------------------------------------------------

This is implemented as a runner parameter ``skip_notify``. If your chain or workflow contains
multiple tasks and you want some tasks to be "muted", you can do so by specifying skip_notify
and call out tasks to mute. For example:

.. code-block:: yaml

    ---
    name: mistral-basic-two-tasks-with-notifications
    pack: examples
    description: Run mistral workflow with two tasks.
    runner_type: mistral-v2
    entry_point: workflows/mistral-basic-two-tasks-with-notifications.yaml
    enabled: true
    parameters:
      skip_notify:
        default:
          - "task2"
      context:
        default: {}
        immutable: true
        type: object
      task:
        default: null
        immutable: true
        type: string
      workflow:
        default: null
        immutable: true
        type: string
    notify:
      on-complete:
        message: "\"@channel: Action succeeded.\""
        routes:
          - "slack"

In the above example, notifications for "task2" will not be sent out. This feature is particularly
useful in combination with ChatOps where you don't want noisy tasks to pollute the Chat client.

Note that it is not currently possible to have a default ``skip_notify`` policy.

ChatOps and Notifications
-------------------------

If you enabled ChatOps, you get all the things wired for you. You don't have to edit action
metadata etc. You can still use ``skip_notify`` to skip notifications for certain tasks in a chain
or workflow. If you specified a notify section in metadata or in tasks, those notification routes
will override ChatOps. Therefore, you might not see notifications in the chat client.
See `this issue <https://github.com/StackStorm/st2/issues/2018>`_ for an example.