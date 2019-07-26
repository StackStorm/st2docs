Getting Started
===============

Authoring
---------

Like any |st2| action, an Orquesta workflow requires an action metadata file in
``/opt/stackstorm/packs/<mypack>/actions``. The entry point specified in the action metadata file
is the path relative to ``/opt/stackstorm/packs/<mypack>/actions`` for the workflow definition.

Let's start with a very basic Orquesta workflow named ``examples.orquesta-basic`` for the
``examples`` pack. The workflow definition for this example is provide below. This workflow executes
a shell command on the server where |st2| is installed. A task can reference any registered |st2|
action directly. In this example, the ``task1`` task calls ``core.local``. The command to execute is
passed as input from the workflow to the task. The ``core.local`` action is already installed with
|st2|. Let's save this as ``/opt/stackstorm/packs/examples/actions/workflows/orquesta-basic.yaml``
on the |st2| server.

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/orquesta-basic.yaml
   :language: yaml

As for the corresponding |st2| action metadata file for the example above. The |st2| pack for this
workflow action is named ``examples``. The |st2| action runner is ``orquesta``. The entry
point for the |st2| action is the relative path to the YAML file of the workflow definition. Let's
save this metadata as ``/opt/stackstorm/packs/examples/actions/orquesta-basic.yaml``:

.. literalinclude:: /../../st2/contrib/examples/actions/orquesta-basic.yaml
   :language: yaml

The files used in this example are also located under
:github_st2:`/usr/share/doc/st2/examples <contrib/examples>` if |st2| is already installed (see also
:ref:`deploy examples <start-deploy-examples>`).

To create this action in |st2|, run the command
``st2 action create /opt/stackstorm/packs/examples/actions/orquesta-basic.yaml``. This will
register the workflow as ``examples.orquesta-basic`` in |st2|. The following is what the output
should look like.

.. code-block:: shell

    $ st2 action create  /opt/stackstorm/packs/examples/actions/orquesta-basic.yaml
    +-------------+---------------------------------+
    | Property    | Value                           |
    +-------------+---------------------------------+
    | id          | 5b3150fd8006e627f71c2d34        |
    | name        | orquesta-basic                  |
    | pack        | examples                        |
    | description | Run a local linux command       |
    | enabled     | True                            |
    | entry_point | workflows/orquesta-basic.yaml   |
    | notify      |                                 |
    | parameters  | {                               |
    |             |     "cmd": {                    |
    |             |         "required": true,       |
    |             |         "type": "string"        |
    |             |     },                          |
    |             |     "timeout": {                |
    |             |         "default": 60,          |
    |             |         "type": "integer"       |
    |             |     }                           |
    |             | }                               |
    | ref         | examples.orquesta-basic         |
    | runner_type | orquesta                        |
    | tags        |                                 |
    | uid         | action:examples:orquesta-basic  |
    +-------------+---------------------------------+

Execution
---------

To execute the workflow, run the command ``st2 run examples.orquesta-basic cmd=date -a`` where
``-a`` tells the command to return and not wait for the workflow to complete.

.. code-block:: shell

    $ st2 run examples.orquesta-basic cmd=date -a
    To get the results, execute:
     st2 execution get 5b3151a18006e627f71c2d36

    To view output in real-time, execute:
     st2 execution tail 5b3151a18006e627f71c2d36

If the workflow completed successfully, both the workflow ``examples.orquesta-basic`` and the
action ``core.local`` should be ``succeeded`` under the |st2| action execution list. By default,
``st2 execution list`` only returns top level executions and tasks are not displayed.

.. code-block:: shell

    $ st2 execution list
    +----------------------------+-----------------+--------------+------------------------+-----------------+---------------+
    | id                         | action.ref      | context.user | status                 | start_timestamp | end_timestamp |
    +----------------------------+-----------------+--------------+------------------------+-----------------+---------------+
    | + 5b3151a18006e627f71c2d36 | examples        | stanley      | succeeded (2s elapsed) | Mon, 25 Jun     | Mon, 25 Jun   |
    |                            | .orquesta-      |              |                        | 2018 20:33:36   | 2018 20:33:38 |
    |                            | basic           |              |                        | UTC             | UTC           |
    +----------------------------+-----------------+--------------+------------------------+-----------------+---------------+

Running the command ``st2 execution get <execution-id>`` returns more details about the workflow
execution such as the action executions related to the tasks and the output of the workflow.

.. code-block:: shell

    $ st2 execution get 5b3151a18006e627f71c2d36
    id: 5b3151a18006e627f71c2d36
    action.ref: examples.orquesta-basic
    parameters: 
      cmd: date
    status: succeeded (2s elapsed)
    start_timestamp: Mon, 25 Jun 2018 20:33:36 UTC
    end_timestamp: Mon, 25 Jun 2018 20:33:38 UTC
    result: 
      output:
        stdout: Mon Jun 25 20:33:37 UTC 2018
    +--------------------------+------------------------+-------+------------+-----------------+
    | id                       | status                 | task  | action     | start_timestamp |
    +--------------------------+------------------------+-------+------------+-----------------+
    | 5b3151a18006e627a556b7e4 | succeeded (1s elapsed) | task1 | core.local | Mon, 25 Jun     |
    |                          |                        |       |            | 2018 20:33:37   |
    |                          |                        |       |            | UTC             |
    +--------------------------+------------------------+-------+------------+-----------------+

Inspection
----------

The workflow definition is inspected on execution. In a single pass, Orquesta will inspect the
workflow definition for errors in syntax, YAQL and Jinja expressions, and variables in the context.
The following is an execution with inspection failure. Note that the errors are separated by
categories. Each entry returns the error message, the path to where the error is located in the
workflow definition, and other information specific to the error type.

.. code-block:: shell

    $ st2 run examples.orquesta-fail-inspection
    .
    id: 5b3153d08006e627f71c2d39
    action.ref: examples.orquesta-fail-inspection
    parameters: None
    status: failed
    start_timestamp: Mon, 25 Jun 2018 20:42:55 UTC
    end_timestamp: Mon, 25 Jun 2018 20:42:56 UTC
    result: 
      errors:
        context:
        - expression: <% ctx().foobar %>
          message: Variable "foobar" is referenced before assignment.
          schema_path: properties.tasks.patternProperties.^\w+$.properties.input
          spec_path: tasks.task1.input
          type: yaql
        expressions:
        - expression: <% <% succeeded() %>
          message: 'Parse error: unexpected ''<'' at position 0 of expression ''<% succeeded()'''
          schema_path: properties.tasks.patternProperties.^\w+$.properties.next.items.properties.when
          spec_path: tasks.task2.next[0].when
          type: yaql
        syntax:
        - message: '[{''cmd'': ''echo <% ctx().macro %>''}] is not of type ''object'''
          schema_path: properties.tasks.patternProperties.^\w+$.properties.input.type
          spec_path: tasks.task2.input
      output: null

More Examples
-------------

There are more workflow examples under :github_st2:`/usr/share/doc/st2/examples <contrib/examples/actions/workflows/>` and include workflows that demonstrates branches, joins, decision tree, error handling, rollback/retry, and others.

Additional Tools and Resources
------------------------------

.. note::

    The following tools and resources are not owned by |st2|. Please use at your own risk.

* `YAQL documentation <https://yaql.readthedocs.io/en/latest/>`_ and `YAQL online evaluator
  <http://yaqluator.com/>`_
* `Jinja2 template engine documentation <http://jinja.pocoo.org>`_ and `Jinja2 online evaluator
  <http://jinja.quantprogramming.com/>`_
