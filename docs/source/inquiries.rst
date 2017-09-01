Inquiries
===============================

StackStorm 2.4 introduced a new feature that allows you to pause a workflow
to wait for additional information. This is done by using a new action:
``core.ask``. These are called "Inquiries", and the idea is to allow you
to "ask a question" in the middle of a workflow. This could be a question like
"do I have approval to continue?" or "what is the second factor I should provide
to this authentication service?"

These use cases (and others) require the ability to pause a workflow mid-execution
and wait for additional information. Inquiries make this possible, and their usage will
be explained in this document. 

Inquiry => Response
----------------------------------------

The way this works is that a new action, ``core.ask`` (more on that later)
is used to generate a new Inquiry. This pauses any workflow in which the action is used.

In order to resume this workflow, a valid response must be provided to this Inquiry.



New ``core.ask`` Action
----------------------------------------

The primary usage of Inquiries is by referencing a new action - ``core.ask`` - in
your workflows. This action is built on a new runner type: ``inquirer``, which performs
the bulk of the logic required to pause workflows and wait for a response.

.. code-block:: python

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
| tag         | An arbitrary string that can be used to filter          |
|             | different Inquiries inside rules. This can be helpful   |
|             | for deciding who to notify of an incoming Inquiry.      |
|             | See "Notifying Users of Inquiries using Rules" for      |
|             | more info.                                              |
+-------------+---------------------------------------------------------+

.. note::

   NOTE

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
            tag: developers
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
    id: 59a9c85632ed3553fb738c80
    action.ref: examples.chain-test-inquiry
    parameters: None
    status: paused
    result_task: task1
    result:
      response: {}
    start_timestamp: 2017-09-01T20:51:34.455424Z
    end_timestamp: None
    +--------------------------+---------+-------+----------+-------------------------------+
    | id                       | status  | task  | action   | start_timestamp               |
    +--------------------------+---------+-------+----------+-------------------------------+
    | 59a9c85632ed3553a76aae06 | pending | task1 | core.ask | Fri, 01 Sep 2017 20:51:34 UTC |
    +--------------------------+---------+-------+----------+-------------------------------+

As you can see, the status of our ActionChain is ``paused``. Note that ``task2`` hasn't even been
scheduled, because the use of the ``core.ask`` action prevented further tasks from running. You'll
also notice that the status for `task1` is `pending`. This indicates to us that this particular
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
                  tag: developers
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
    status: pausing
    start_timestamp: 2017-09-01T20:56:48.630380Z
    end_timestamp: None
    +--------------------------+---------+-------+----------+-------------------------------+
    | id                       | status  | task  | action   | start_timestamp               |
    +--------------------------+---------+-------+----------+-------------------------------+
    | 59a9c99132ed3553fb738c86 | pending | task1 | core.ask | Fri, 01 Sep 2017 20:56:49 UTC |
    +--------------------------+---------+-------+----------+-------------------------------+


Notifying Users of Inquiries using Rules
----------------------------------------

    TODO


Responding to an Inquiry
----------------------------------------

    TODO
