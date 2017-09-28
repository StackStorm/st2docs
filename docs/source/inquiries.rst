Inquiries
===============================

StackStorm 2.5 introduced a new feature that allows you to pause a workflow
to wait for additional information. This is done by using a new action:
``core.ask``. These are called "Inquiries", and the idea is to allow you
to "ask a question" in the middle of a workflow. This could be a question like
"do I have approval to continue?" or "what is the second factor I should provide
to this authentication service?"

These use cases (and others) require the ability to pause a workflow mid-execution
and wait for additional information. Inquiries make this possible, and their usage will
be explained in this document. 

New ``core.ask`` Action
----------------------------------------

The primary usage of Inquiries is by referencing a new action - ``core.ask`` - in
your workflows. This action is built on a new runner type: ``inquirer``, which performs
the bulk of the logic required to pause workflows and wait for a response.

.. code-block:: bash

    ~$ st2 action get core.ask
    +-------------+----------------------------------------------------------+
    | Property    | Value                                                    |
    +-------------+----------------------------------------------------------+
    | id          | 59a8c27732ed3553ceb2dec4                                 |
    | uid         | action:core:ask                                          |
    | ref         | core.ask                                                 |
    | pack        | core                                                     |
    | name        | ask                                                      |
    | description | Action for initiating an Inquiry (usually in a workflow) |
    | enabled     | True                                                     |
    | entry_point |                                                          |
    | runner_type | inquirer                                                 |
    | parameters  |                                                          |
    | notify      |                                                          |
    | tags        |                                                          |
    +-------------+----------------------------------------------------------+

The ``inquirer`` runner imposes a number of parameters that are, in turn, required by the ``core.ask``
action:

+-------------+---------------------------------------------------------+
| Parameter   | Description                                             |
+=============+=========================================================+
| schema      | A JSON schema that will be used to validate             |
|             | the response data. A basic schema will be provided      |
|             | by default, or you can provide one here. Only valid     |
|             | responses will cause the action to succeed, and the     |
|             | workflow to continue.                                   |
+-------------+---------------------------------------------------------+
| ttl         | Time (in minutes) until an unacknowledged Inquiry is    |
|             | garbage-collected. Inquiry garbage collection is not    |
|             | enabled by default, so this field does nothing unless   |
|             | it is turned on. See "Garbage Collection" for more      |
|             | info.                                                   |
+-------------+---------------------------------------------------------+
| roles       | A list of RBAC roles that are permitted to respond to   |
|             | the action. Defaults to empty list, which permits all   |
|             | roles. **This requires BWC features**                   |
+-------------+---------------------------------------------------------+
| users       | A list of users that are permitted to respond to        |
|             | the action. Defaults to empty list, which permits all   |
|             | users.                                                  |
+-------------+---------------------------------------------------------+
| route       | An arbitrary string that can be used to filter          |
|             | different Inquiries inside rules. This can be helpful   |
|             | for deciding who to notify of an incoming Inquiry.      |
|             | See "Notifying Users of Inquiries using Rules" for      |
|             | more info.                                              |
+-------------+---------------------------------------------------------+

Using ``core.ask`` in a Workflow
----------------------------------------

While it's possible to use this action on its own (i.e. with ``st2 run``), the real value comes
from using it in a Workflow.

The following example shows a simple ActionChain with two tasks. ``task1`` executes the ``core.ask``
action and passes in a few parameters:

.. TODO - The code snippet below is provided because the Inquiry functionality is not merged yet.
   Please convert this to a literalinclude statement, referring to workflows in the examples
   directory of st2, once https://github.com/StackStorm/st2/pull/3653 is merged.

.. code-block:: yaml

    chain:
        - name: task1
          ref: core.ask
          params:
            route: developers
            users:
              - testu

        - name: task2
          ref: core.local
          params:
            cmd: echo "Reached task 2!"

We can run this workflow to see its execution:

.. code-block:: bash

    ~$ st2 run examples.chain-test-inquiry
    .
    id: 59ca9aad32ed3514845e7b0c
    action.ref: examples.chain-test-inquiry
    parameters: None
    status: paused
    result_task: task1
    result:
      roles: []
      schema:
        properties:
          continue:
            description: Would you like to continue the workflow?
            required: true
            type: boolean
        title: response_data
        type: object
      route: developers
      ttl: 1440
      users:
      - testu
    start_timestamp: 2017-09-26T18:21:33.186215Z
    end_timestamp: None
    +--------------------------+---------+-------+----------+-------------------------------+
    | id                       | status  | task  | action   | start_timestamp               |
    +--------------------------+---------+-------+----------+-------------------------------+
    | 59ca9aad32ed35143227fe52 | pending | task1 | core.ask | Tue, 26 Sep 2017 18:21:33 UTC |
    +--------------------------+---------+-------+----------+-------------------------------+

As you can see, the status of our ActionChain is ``paused``. Note that ``task2`` hasn't even been
scheduled, because the use of the ``core.ask`` action prevented further tasks from running. You'll
also notice that the status for ``task1`` is ``pending``. This indicates to us that this particular
Inquiry has not yet received a valid response, and is currently blocking the Workflow execution.

You can also use ``core.ask`` to ask a question within Mistral workflows:

.. code-block:: yaml

    ---
    version: '2.0'

    examples.mistral-ask-basic:
        description: A basic workflow for testing core.ask
        type: direct
        output:
            result: <% task(task1).result.response %>
        tasks:
            task1:
                action: core.ask
                input:
                  route: developers
                  users:
                    - testu
                on-complete:
                  - task2

            task2:
                action: core.local
                input:
                  cmd: date

When encountering an Inquiry, StackStorm will send a request to Mistral to pause execution of a workflow,
just like we saw previously with ActionChains:

.. note::

   Due to the latency involved with sending a pause request to Mistral, you may temporarily see a ``pausing``
   status in your Mistral workflows - especially if running directly with ``st2 run``. This is nothing to be
   concerned about; the status will quickly change to ``paused``, and further tasks will not execute.

.. code-block:: bash

    ~$ st2 run examples.mistral-ask-basic
    .
    id: 59a9c99032ed3553fb738c83
    action.ref: examples.mistral-ask-basic
    parameters: None
    status: paused
    start_timestamp: 2017-09-01T20:56:48.630380Z
    end_timestamp: None
    +--------------------------+---------+-------+----------+-------------------------------+
    | id                       | status  | task  | action   | start_timestamp               |
    +--------------------------+---------+-------+----------+-------------------------------+
    | 59a9c99132ed3553fb738c86 | pending | task1 | core.ask | Fri, 01 Sep 2017 20:56:49 UTC |
    +--------------------------+---------+-------+----------+-------------------------------+

.. note::

    At the time of this writing, the Inquiry ID is the same as the action execution ID that raised it. So if you're curious which workflow a given Inquiry is part of, use the same ID with the ``st2 execution get`` command.


Notifying Users of Inquiries using Rules
----------------------------------------

When a new Inquiry is raised, a dedicated trigger - ``core.st2.generic.inquiry`` - is used. This trigger can be consumed in Rules, and you can use an action or a workflow to provide notification to the relevant party. For instance, using Slack:

.. code-block:: yaml

    ---
    name: "notify_inquiry"
    pack: "examples"
    description: Notify relevant users of an Inquiry action
    enabled: false

    trigger:
      type: core.st2.generic.inquiry

    action:
      ref: slack.post_message
      parameters:
        channel: "#{{ trigger.route }}"
        message: 'Inquiry {{trigger.id}} is awaiting an approval action'


Note how this Rule uses the ``route`` field to determine to which Slack channel the notification should be sent. You could also use this in the Rule criteria as well, and set up different notification actions depending on the value of ``route``.

Responding to an Inquiry
----------------------------------------

In order to resume a Workflow that's been paused by an Inquiry, a response must be provided to that Inquiry, and the response must come in the form of JSON data that validates against the schema in use by that particular Inquiry instance.

In order to respond to an Inquiry, we need its ID. We would already have this if we wrote a Rule like shown in the previous section, but we could also use the ``st2 inquiry list`` command to view all outstanding inquiries:

.. code-block:: bash

    ~$ st2 inquiry list
    +--------------------------+-------+-------+------------+------+
    | id                       | roles | users | route      | ttl  |
    +--------------------------+-------+-------+------------+------+
    | 59ab26af32ed35752062d2dc |       | testu | developers | 1440 |
    +--------------------------+-------+-------+------------+------+

Like most other resources in StackStorm, we can use the ``get`` subcommand to retrieve details about this Inquiry, using its ID provided in the previous output:

.. TODO - Might be worth using a little more compelling example in the future, find a service that
          requires 2FA and provide it using an Inquiry

.. code-block:: bash

    ~$ st2 inquiry get 59ab26af32ed35752062d2dc
    +----------+--------------------------------------------------------------+
    | Property | Value                                                        |
    +----------+--------------------------------------------------------------+
    | id       | 59ab26af32ed35752062d2dc                                     |
    | parent   | 59ab26af32ed3575803bf139                                     |
    | roles    |                                                              |
    | users    | [                                                            |
    |          |     "testu"                                                  |
    |          | ]                                                            |
    | route    | developers                                                   |
    | ttl      | 1440                                                         |
    | schema   | {                                                            |
    |          |     "type": "object",                                        |
    |          |     "properties": {                                          |
    |          |         "continue": {                                        |
    |          |             "type": "boolean",                               |
    |          |             "description": "Would you like to continue the   |
    |          | workflow?"                                                   |
    |          |             "required": true
    |          |         }                                                    |
    |          |     },                                                       |
    |          |     "title": "response_data"                                 |
    |          | }                                                            |
    +----------+--------------------------------------------------------------+

In this view, we see the schema in use requires a single key: ``continue``, whose value must be boolean. Fortunately, the ``st2`` client makes this really easy; when you run the command ``st2 inquiry respond <inquiry id>``, it will step through each of these values, prompting you with the provided description. You simply respond to each prompt:

.. code-block:: bash

    ~$ st2 inquiry respond 59ab26af32ed35752062d2dc
    continue (boolean): True
    Should we continue?

     Response accepted. Successful response data to follow...
    +----------+--------------------------+
    | Property | Value                    |
    +----------+--------------------------+
    | id       | 59ab26af32ed35752062d2dc |
    | response | {                        |
    |          |     "continue": true     |
    |          | }                        |
    +----------+--------------------------+

It's very important that each property in the response schema has a proper description, as shown in the default example, as this is what prompts the user for required values when it's time to respond.

Since the ``st2`` client has a handle on the schema being used for an Inquiry, it can guide you to provide the right datatypes for each attribute, and won't continue until you do:

.. code-block:: bash

    ~$ st2 inquiry respond 59ab26af32ed35752062d2dc
    continue (boolean): 123
    Does not look like boolean. Pick from [false, no, nope, nah, n, 1, 0, y, yes, true]
    Should we continue?

However, not every response can be done interactively. You may even want to script some or all of your Inquiry responses, and may be using tools like `jq` to craft your own JSON payload for a response and wish to simply provide this to the CLI. The ``-r`` flag can be used for this:

.. code-block:: bash

    ~$ st2 inquiry respond -r '{"continue": true}' 59ab26af32ed35752062d2dc

     Response accepted. Successful response data to follow...
    +----------+--------------------------+
    | Property | Value                    |
    +----------+--------------------------+
    | id       | 59ab26af32ed35752062d2dc |
    | response | {                        |
    |          |     "continue": true     |
    |          | }                        |
    +----------+--------------------------+

Note that this effectively bypasses any client-side validation, so it's quite possible to send a JSON payload that doesn't validate against the schema. However, the API is the ultimate authority on validating an Inquiry response, so in this case, you'll still get an error in return:

.. code-block:: bash

    ~$ st2 inquiry respond -r '{"continue": 123}' 59ab26af32ed35752062d2dc
    ERROR: 400 Client Error: Bad Request
    MESSAGE: Response did not pass schema validation. for url: http://127.0.0.1:9101/exp/inquiries/59ab26af32ed35752062d2dc

Once an acceptable response is provided, the workflow resumes:

.. code-block:: bash

    ~$ st2 execution get 59ab26af32ed3575803bf139
    id: 59ab26af32ed3575803bf139
    action.ref: examples.chain-test-inquiry
    parameters: None
    status: succeeded (77s elapsed)
    result_task: task1
    result:
      response:
        continue: true
    start_timestamp: 2017-09-02T21:46:23.165497Z
    end_timestamp: 2017-09-02T21:47:40.093311Z
    +--------------------------+------------------------+-------+----------+-------------------------------+
    | id                       | status                 | task  | action   | start_timestamp               |
    +--------------------------+------------------------+-------+----------+-------------------------------+
    | 59ab26af32ed35752062d2dc | succeeded (0s elapsed) | task1 | core.ask | Sat, 02 Sep 2017 21:46:23 UTC |
    +--------------------------+------------------------+-------+----------+-------------------------------+

.. note::

    In the very near future (definitely before the 2.5 release), an Action for responding
    to an Inquiry, as well as an action-alias for calling this action via chatops, and a rule
    for notifying via chatops, will all be provided in a PR. For the time being (alpha stage)
    the only way to respond is to get the Inquiry ID and use it in the ``st2 inquiry respond``
    command

.. TODO - Update with chatops when the core PR is merged
