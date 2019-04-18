Inquiries
=========

Inquiries allow you to pause a workflow to wait for additional information. This is done by using 
the ``core.ask`` action. The idea is to allow you to "ask a question" in the middle of a workflow.
This could be a question like "do I have approval to continue?" or "what is the second factor I
should provide to this authentication service?"

These use cases (and others) require the ability to pause a workflow mid-execution and wait for
additional information. Inquiries make this possible. This document explains how to use them.

``core.ask``
------------

The best way to get started using Inquiries is to check out the core action - ``core.ask`` - 
and start using it in your workflows. This action is built on the ``inquirer`` runner type,
which performs the bulk of the logic required to pause workflows and wait for a response.

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

The ``inquirer`` runner imposes a number of parameters that are, in turn, required by the
``core.ask`` action:

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
|             | garbage-collected. Set to 0 to disable garbage          |
|             | collection for this Inquiry. NOTE - Inquiry garbage     |
|             | collection is not enabled by default, so this field     |
|             | does nothing unless it is turned on. See                |
|             | `Garbage Collection for Inquiries`_ for more info.      |
+-------------+---------------------------------------------------------+
| roles       | A list of RBAC roles that are permitted to respond to   |
|             | the action. Defaults to empty list, which permits all   |
|             | roles. **This requires enterprise features**            |
+-------------+---------------------------------------------------------+
| users       | A list of users that are permitted to respond to        |
|             | the action. Defaults to empty list, which permits all   |
|             | users.                                                  |
+-------------+---------------------------------------------------------+
| route       | An arbitrary string that can be used to filter          |
|             | different Inquiries inside rules. This can be helpful   |
|             | for deciding who to notify of an incoming Inquiry.      |
|             | See `Notifying Users of Inquiries using Rules`_ for     |
|             | more info.                                              |
+-------------+---------------------------------------------------------+

Using ``core.ask`` in a Workflow
--------------------------------

While you can use this action on its own (i.e. with ``st2 run``), the real value comes from using
it in a :doc:`Workflow</workflows>`.

The ``core.ask`` action supports a number of parameters, but the most important one by far is the
``schema`` parameter. This parameter defines exactly what kind of responses will satisfy the
Inquiry, and allow the workflow to continue. When users respond to this Inquiry, their response
must come in the form of a JSON payload that will satisfy this schema. We cover responses in
:ref:`Responding to an Inquiry<ref_responding_inquiry>` below - the ``st2`` client makes this
pretty easy.

Now we'll use this action in an example workflow. The following example shows a simple ActionChain
with two tasks. ``task1`` executes the ``core.ask`` action and passes in a few parameters:

.. literalinclude:: /../../st2/contrib/examples/actions/chains/chain_test_inquiry.yaml
   :language: yaml

Note that we're using a Jinja snippet in ``task2`` to access and make use of the value that we're
asking for. In this example we're simply printing this to the screen, but the
``<task>.result.response`` dictionary will contain all of the values that satisfy our schema. More
on this later.

We can run this workflow to see its execution:

.. code-block:: bash

    ~$ st2 run examples.chain-test-inquiry
    .
    id: 59d1ecb632ed353f1f340898
    action.ref: examples.chain-test-inquiry
    parameters: None
    status: paused
    result_task: task1
    result:
      roles: []
      route: developers
      schema:
        properties:
          secondfactor:
            description: Please enter second factor for authenticating to "foo" service
            required: true
            type: string
        type: object
      ttl: 1440
      users: []
    start_timestamp: 2017-10-02T07:37:26.854217Z
    end_timestamp: None
    +--------------------------+---------+-------+----------+-------------------------------+
    | id                       | status  | task  | action   | start_timestamp               |
    +--------------------------+---------+-------+----------+-------------------------------+
    | 59d1ecb732ed353ec4aa9a5a | pending | task1 | core.ask | Mon, 02 Oct 2017 07:37:27 UTC |
    +--------------------------+---------+-------+----------+-------------------------------+

As you can see, the status of our ActionChain is ``paused``. Note that ``task2`` hasn't even been
scheduled, because the use of the ``core.ask`` action prevented further tasks from running. You'll
also notice that the status for ``task1`` is ``pending``. This indicates to us that this particular
Inquiry has not yet received a valid response, and is currently blocking the Workflow execution.

You can also use ``core.ask`` to ask a question within Orquesta workflows:

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/orquesta-ask-basic.yaml
   :language: yaml

When encountering an Inquiry, StackStorm will send a request to Orquesta to pause execution of a
workflow, just like we saw previously with ActionChains:

.. code-block:: bash

    ~$ st2 run examples.orquesta-ask-basic
    .
    id: 59a9c99032ed3553fb738c83
    action.ref: examples.orquesta-ask-basic
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

    At the time of this writing, the Inquiry ID is the same as the action execution ID that raised
    it. So if you're curious which workflow a given Inquiry is part of, use the same ID with the
    ``st2 execution get`` command.


Notifying Users of Inquiries using Rules
----------------------------------------

When a new Inquiry is raised, a dedicated trigger - ``core.st2.generic.inquiry`` - is used. This
trigger can be consumed in Rules, and you can use an action or a workflow to provide notification
to the relevant party. For instance, using Slack:

.. literalinclude:: /../../st2/contrib/examples/rules/notify_inquiry.yaml
   :language: yaml

Note how this Rule uses the ``route`` field to determine to which Slack channel the notification
should be sent. You could also use this in the Rule criteria as well, and set up different
notification actions depending on the value of ``route``.

.. _ref_responding_inquiry:

Responding to an Inquiry
------------------------

In order to resume a Workflow that's been paused by an Inquiry, a response must be provided to
that Inquiry, and the response must come in the form of JSON data that validates against the
schema in use by that particular Inquiry instance.

In order to respond to an Inquiry, we need its ID. We would already have this if we wrote a Rule
like shown in the previous section, but we could also use the ``st2 inquiry list`` command to view
all outstanding inquiries:

.. code-block:: bash

    ~$ st2 inquiry list
    +--------------------------+-------+-------+------------+------+
    | id                       | roles | users | route      | ttl  |
    +--------------------------+-------+-------+------------+------+
    | 59d1ecb732ed353ec4aa9a5a |       |       | developers | 1440 |
    +--------------------------+-------+-------+------------+------+

Like most other resources in StackStorm, we can use the ``get`` subcommand to retrieve details
about this Inquiry, using its ID provided in the previous output:

.. code-block:: bash

    ~$ st2 inquiry get 59d1ecb732ed353ec4aa9a5a
    +----------+--------------------------------------------------------------+
    | Property | Value                                                        |
    +----------+--------------------------------------------------------------+
    | id       | 59d1ecb732ed353ec4aa9a5a                                     |
    | roles    |                                                              |
    | users    |                                                              |
    | route    | developers                                                   |
    | ttl      | 1440                                                         |
    | schema   | {                                                            |
    |          |     "type": "object",                                        |
    |          |     "properties": {                                          |
    |          |         "secondfactor": {                                    |
    |          |             "required": true,                                |
    |          |             "type": "string",                                |
    |          |             "description": "Please enter second factor for   |
    |          | authenticating to "foo" service"                             |
    |          |         }                                                    |
    |          |     }                                                        |
    |          | }                                                            |
    +----------+--------------------------------------------------------------+

In this view, we see the schema in use requires a single key: ``secondfactor``, whose value must
be a string.

.. note::

    You can omit the ``schema`` parameter when using ``core.ask``, and a basic schema will be used
    as default - only requiring a single boolean value to continue the workflow. In this example,
    we've provided our own schema that allows us to use the retrieved value in a later task of the
    workflow. This allows you to "inject" data into a workflow mid-execution, rather than rely
    solely on parameters.

Fortunately, the ``st2`` client makes it easy to provide a valid response; when you run the
command ``st2 inquiry respond <inquiry id>``, it will step through each of these values, prompting
you with the provided description. You simply respond to each prompt:

.. code-block:: bash

    ~$ st2 inquiry respond 59d1ecb732ed353ec4aa9a5a
    secondfactor: bar
    Please enter second factor for authenticating to "foo" service

     Response accepted. Successful response data to follow...
    +----------+---------------------------+
    | Property | Value                     |
    +----------+---------------------------+
    | id       | 59d1ecb732ed353ec4aa9a5a  |
    | response | {                         |
    |          |     "secondfactor": "bar" |
    |          | }                         |
    +----------+---------------------------+

It's very important that each property in the response schema has a proper description, as shown
in the default example, as this is what prompts the user for required values when it's time to
respond.

Since the ``st2`` client has a handle on the schema being used for an Inquiry, it can guide you to
provide the right datatypes for each attribute, and won't continue until you do. For instance, if
our schema required a ``boolean`` value, an integer would be rejected client-side:

.. code-block:: bash

    ~$ st2 inquiry respond 59ab26af32ed35752062d2dc
    continue (boolean): 123
    Does not look like boolean. Pick from [false, no, nope, nah, n, 1, 0, y, yes, true]
    Should we continue?

However, not every response can be done interactively. You may even want to script some or all of
your Inquiry responses, and may be using tools like `jq` to craft your own JSON payload for a
response and wish to simply provide this to the CLI. The ``-r`` flag can be used for this:

.. code-block:: bash

    ~$ st2 inquiry respond -r '{"secondfactor": "bar"}' 59d1ecb732ed353ec4aa9a5a

     Response accepted. Successful response data to follow...
    +----------+---------------------------+
    | Property | Value                     |
    +----------+---------------------------+
    | id       | 59d1ecb732ed353ec4aa9a5a  |
    | response | {                         |
    |          |     "secondfactor": "bar" |
    |          | }                         |
    +----------+---------------------------+

Note that this effectively bypasses any client-side validation, so it's possible to send a JSON
payload that doesn't validate against the schema. However, the API is the ultimate authority on
validating an Inquiry response, so in this case, you'll still get an error in return:

.. code-block:: bash

    ~$ st2 inquiry respond -r '{"secondfactor": 123}' 59d1ecb732ed353ec4aa9a5a
    ERROR: 400 Client Error: Bad Request
    MESSAGE: Response did not pass schema validation. for url: http://127.0.0.1:9101/exp/inquiries/59ab26af32ed35752062d2dc

Once an acceptable response is provided, the workflow resumes:

.. code-block:: bash

    ~$ st2 execution get 59d1ecb632ed353f1f340898
    id: 59d1ecb632ed353f1f340898
    action.ref: examples.chain-test-inquiry
    parameters: None
    status: succeeded (468s elapsed)
    result_task: task2
    result:
      failed: false
      return_code: 0
      stderr: ''
      stdout: We can now authenticate to foo service with bar
      succeeded: true
    start_timestamp: 2017-10-02T07:37:26.854217Z
    end_timestamp: 2017-10-02T07:45:14.123405Z
    +--------------------------+------------------------+-------+------------+-------------------------------+
    | id                       | status                 | task  | action     | start_timestamp               |
    +--------------------------+------------------------+-------+------------+-------------------------------+
    | 59d1ecb732ed353ec4aa9a5a | succeeded (0s elapsed) | task1 | core.ask   | Mon, 02 Oct 2017 07:37:27 UTC |
    | 59d1ee8932ed353ec4aa9a5d | succeeded (1s elapsed) | task2 | core.local | Mon, 02 Oct 2017 07:45:12 UTC |
    +--------------------------+------------------------+-------+------------+-------------------------------+

Note that the ``stdout`` for ``task2`` (and subsequently, this ActionChain) is "We can now
authenticate to foo service with bar". If you recall, this was because we were using a Jinja
snippet to print the value of ``secondfactor`` in our response. We just printed the phrase to the
screen in this example, but you can just as easily use this to pass a value into another action in
your workflow.

The ``st2`` pack also now contains an ``inquiry.respond`` action, which may be useful for
responding to inquiries within another workflow:

.. code-block:: bash

    ~$ st2 inquiry get 5a1f4411c4da5f4486b09364
    +----------+--------------------------------------------------------------+
    | Property | Value                                                        |
    +----------+--------------------------------------------------------------+
    | id       | 5a1f4411c4da5f4486b09364                                     |
    | roles    |                                                              |
    | users    |                                                              |
    | route    | developers                                                   |
    | ttl      | 1440                                                         |
    | schema   | {                                                            |
    |          |     "type": "object",                                        |
    |          |     "properties": {                                          |
    |          |         "secondfactor": {                                    |
    |          |             "required": true,                                |
    |          |             "type": "string",                                |
    |          |             "description": "Please enter second factor for   |
    |          | authenticating to "foo" service"                             |
    |          |         }                                                    |
    |          |     }                                                        |
    |          | }                                                            |
    +----------+--------------------------------------------------------------+
    vagrant@st2vagrant:~$ st2 run st2.inquiry.respond id=5a1f4411c4da5f4486b09364 response='{"secondfactor": "foo"}'
    .
    id: 5a1f444ec4da5f4486b09366
    status: succeeded
    parameters:
    id: 5a1f4411c4da5f4486b09364
    response:
        secondfactor: '********'
    result:
    exit_code: 0
    result: null
    stderr: ''
    stdout: ''

.. note::

    You'll notice that the value for the key ``secondfactor`` is masked within  the response body
    in the execution output for this action. The ``st2.inquiry.respond`` action doesn't actually
    know the inquiry response schema at all - it is merely a thin layer on top of the |st2|
    client. As a result, it doesn't know which fields are marked with the ``secret`` attribute.
    To avoid potentially leaking secrets, all field values are masked in this way for the output
    of this action, regardless of whether or not the schema has declared them as secrets.

The ``st2`` pack also contains an action alias for responding to Inquiries via ChatOps. Using this
alias, you can respond to an Inquiry within Slack, as an example:

.. code-block:: text

    !st2 respond to inquiry 5a1f4860c4da5f4486b093bf with {“secondfactor”: “supersecret”}

.. _ref-securing-inquiries:

Securing Inquiries
------------------

Inquiries work a little differently from other system resources with it comes to granting permissions
to them via :doc:`RBAC</rbac>`. The ``users`` and ``roles`` parameters for the ``core.ask`` action
allow you to control who can respond to a specific inquiry, right in the workflow. With this granularity
being offered in parameters, RBAC for Inquiries is a bit simpler, focusing broadly on who has access
to Inquiries in general, leaving specific access control to the action parameters.

For example, rather than specifying a particular Inquiry when constructing a role, all Inquiry
UIDs should be specified as ``inquiry:``. Whatever permissions are granted in the role are granted
to all inquiries:

.. code-block:: yaml

    ---
    name: "inquiry_role_respond"
    description: "Role which grants inquiry powers"

    permission_grants:

    - resource_uid: "inquiry:"
      permission_types:
        - "inquiry_respond"

Inquiries also honor execution permissions for the workflow they were generated from. For
instance, if user ``inherit`` has ``action_execute`` permissions on the workflow
``examples.orquesta-ask-basic``, they don't need to be explicitly granted ``inquiry_respond``
permissions - this is done automatically.

The following is an example role that only grants permissions to execute a workflow that contains
a ``core.ask`` action, but doesn't explicitly grant ``inquiry_respond`` permissions. However, any
user that's been assigned to this role will still be permitted to respond.

.. code-block:: yaml

    ---
    name: "inquiry_role_inherit"
    description: "Role which only grants action powers - will inherit inquiry_respond"

    permission_grants:

    # Grant to run the workflow
    - resource_uid: "action:examples:orquesta-ask-basic"
      permission_types:
        - "action_execute"
        - "action_view"

    # Grant to run the core.ask action
    - resource_uid: "action:core:ask"
      permission_types:
        - "action_execute"
        - "action_view"

    # Grant to list runners (allows us to test this with `st2 run`)
    - resource_uid: "runner_type:orquesta"
      permission_types:
        - "runner_type_list"


To lock down a specific Inquiry to a set of users or RBAC roles (the latter of which is only
available with :doc:`enterprise features</install/ewc>`), the ``users`` and ``roles`` parameters
should be used. These offer additional restriction on a per-Inquiry basis, but they don't remove
any restrictions imposed on the aforementioned RBAC settings, if any. These parameter-based
restrictions are cumulative with any existing RBAC restrictions.

The ``users`` parameter is a list of users that are permitted to respond to this specific instance
of an Inquiry. Similarly, ``roles`` controls which RBAC roles (assuming enterprise features) are
allowed to respond to this specific Inquiry. The default value for both of these parameters is an
empty list, which permits all. The following ActionChain invokes a ``core.local`` action, passing
a list into the ``users`` parameter that specifies only ``st2responduser`` is able to respond:

.. code-block:: yaml

    chain:

      - name: task1
        ref: core.ask
        params:
          route: developers
          users:
           - st2responduser
          schema:
            type: object
            properties:
              secondfactor:
                type: string
                description: Please enter second factor for authenticating to "foo" service
                required: True
        on-success: "task2"

      - name: task2
        ref: core.local
        params:
          cmd: echo "We can now authenticate to "foo" service with {{ task1.result.response.secondfactor }}"

All other users attempting to respond will be rejected, even if they are granted
``inquiry_respond`` RBAC permissions.


Garbage Collection for Inquiries
--------------------------------

As alluded to in :doc:`Purging Old Operational Data </troubleshooting/purging_old_data>`, the
``st2garbagecollector`` service is also responsible for cleaning up old Inquiries. This is done by
comparing the ``ttl`` parameter of an Inquiry with its start time. The ``ttl`` field is the number
of minutes since the start time the Inquiry will be allowed to receive responses, before it is
cleaned up.

Unlike garbage collection for trigger-instances, or action executions, Inquiries are not deleted
when they're "cleaned up". Rather, they're marked as "timed out". This allows workflows to make
different decisions based on whether or not an Inquiry was responded to successfully, or if the
TTL expired waiting for a response.

To configure garbage collection for Inquiries, you first need to enable this globally. Unlike
trigger-instances and action executions, ``/etc/st2/st2.conf`` only requires a single boolean
parameter to enable Inquiry garbage colllection:

.. code-block:: ini

    [garbagecollector]

    # By default, this value is False
    purge_inquiries = True

Once done, each Inquiry has its own ``ttl`` configured via parameters. The default is 1440 - 24
hours. However, this can be easily overridden for a inquiry by specifying the ``ttl`` in a
parameter for the ``core.ask`` action, like in the following Orquesta workflow:

.. code-block:: yaml

    version: 1.0

    description: A basic workflow that demonstrates inquiry.

    tasks:
      start:
        action: core.echo message="Automation started."
        next:
          - when: <% succeeded() %>
            do: get_approval

      get_approval:
        action: core.ask
        input:
          ttl: 60
          route: developers
        next:
          - when: <% succeeded() %>
            do: finish
          - when: <% failed() %>
            do: stop

      finish:
        action: core.echo message="Automation completed."

      stop:
        action: core.echo message="Automation stopped."
        next:
          - do: fail

.. note::

    Even if Inquiry garbage collection is enabled globally in the st2 config, you can use a TTL
    value of 0 to disable garbage collection for a specific Inquiry.

Once this option has been enabled, and the ``st2garbagecollector`` service is started, it will
begin periodically looking for Inquiries that have been in a ``pending`` state beyond their
configured ``ttl``. If we didn't respond to the above inquiry within 60 minutes, then ``task``
would be marked "timeout", and the workflow would fail (since ``task2`` is listed under
``on-success``).
