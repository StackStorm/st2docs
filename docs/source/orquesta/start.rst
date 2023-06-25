Getting Started
===============

Authoring
---------

Like any |st2| action, an Orquesta workflow requires an action metadata file in
``/opt/stackstorm/packs/<mypack>/actions``. The entry point specified in the action metadata file
is the path relative to ``/opt/stackstorm/packs/<mypack>/actions`` for the workflow definition.

Let's start with a very basic Orquesta workflow named ``examples.orquesta-sequential`` for the
``examples`` pack. The workflow definition for this example is provided below. This workflow is a
very simple example that runs a few echoes, pieces together the output, and returns a response. A task
can reference any registered |st2| action directly. In this example, the task calls ``core.echo``,
an action in |st2| that just echoes back the message, like the shell echo command. The ``core.echo``
action is already installed by default with |st2|. Let's save this workflow definition as
``/opt/stackstorm/packs/examples/actions/workflows/orquesta-sequential.yaml`` on the |st2| server.

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/orquesta-sequential.yaml
   :language: yaml

As for the corresponding |st2| action metadata file for the example above. The |st2| pack for this
workflow action is named ``examples``. The |st2| action runner is ``orquesta``. The entry
point for the |st2| action is the relative path to the YAML file of the workflow definition. Let's
save this metadata as ``/opt/stackstorm/packs/examples/actions/orquesta-sequential.yaml``:

.. literalinclude:: /../../st2/contrib/examples/actions/orquesta-sequential.yaml
   :language: yaml

The files used in this example are also located under
:github_st2:`/usr/share/doc/st2/examples <contrib/examples>` if |st2| is already installed (see also
:ref:`deploy examples <start-deploy-examples>`).

To create this action in |st2|, run the command
``st2 action create /opt/stackstorm/packs/examples/actions/orquesta-sequential.yaml``. This will
register the workflow as ``examples.orquesta-sequential`` in |st2|. The following is what the output
should look like.

.. code-block:: shell

    $ st2 action create /opt/stackstorm/packs/examples/actions/orquesta-sequential.yaml
    +---------------+------------------------------------+
    | Property      | Value                              |
    +---------------+------------------------------------+
    | id            | 5d3a08a00a08a41a995221a0           |
    | name          | orquesta-sequential                |
    | pack          | examples                           |
    | description   | A basic sequential workflow.       |
    | enabled       | True                               |
    | entry_point   | workflows/orquesta-sequential.yaml |
    | metadata_file |                                    |
    | notify        |                                    |
    | output_schema |                                    |
    | parameters    | {                                  |
    |               |     "name": {                      |
    |               |         "default": "Lakshmi",      |
    |               |         "required": true,          |
    |               |         "type": "string"           |
    |               |     }                              |
    |               | }                                  |
    | ref           | examples.orquesta-sequential       |
    | runner_type   | orquesta                           |
    | tags          |                                    |
    | uid           | action:default:orquesta-sequential |
    +---------------+------------------------------------+

Execution
---------

Before we run the example, let's run the help command ``st2 run examples.orquesta-sequential -h``
to see what input parameters are required. The following is what the help command returns. The
workflow requires a value for the input parameter named ``name``. There is an optional parameter
named ``notify`` which we can ignore for now.

.. code-block:: shell

    $ st2 run examples.orquesta-sequential -h

    A basic sequential workflow.

    Required Parameters:
        name
            Type: string
            Default: Lakshmi

    Optional Parameters:
        notify
            List of tasks to trigger notifications for.
            Type: array
            Default: []

To execute the workflow, run the command ``st2 run examples.orquesta-sequential name=Earthling -a``
where the ``-a`` option tells the command to return and not wait for the workflow to complete.

.. code-block:: shell

    $ st2 run examples.orquesta-sequential name=Earthling -a
    To get the results, execute:
     st2 execution get 5d3a0a890a08a41a995221a3

    To view output in real-time, execute:
     st2 execution tail 5d3a0a890a08a41a995221a3

If the workflow completed successfully, both the workflow ``examples.orquesta-sequential`` and the
sequence of ``core.echo`` should be ``succeeded`` under the |st2| action execution list. By default,
``st2 execution list`` only returns top level executions and tasks are not displayed.

.. code-block:: shell

    $ st2 execution list
    +--------------------------+-----------------+--------------+------------------------+-----------------+---------------+
    | id                       | action.ref      | context.user | status                 | start_timestamp | end_timestamp |
    +--------------------------+-----------------+--------------+------------------------+-----------------+---------------+
    | 5d3a0a890a08a41a995221a3 | examples        | stanley      | succeeded (4s elapsed) | Thu, 25 Jul     | Thu, 25 Jul   |
    |                          | .orquesta-      |              |                        | 2019 20:01:13   | 2019 20:01:17 |
    |                          | sequential      |              |                        | UTC             | UTC           |
    +--------------------------+-----------------+--------------+------------------------+-----------------+---------------+

Running the command ``st2 execution get <execution-id>`` returns more details about the workflow
execution such as the action executions related to the tasks and the output of the workflow.

.. code-block:: shell

    $ st2 execution get 5d3a0a890a08a41a995221a3
    id: 5d3a0a890a08a41a995221a3
    action.ref: examples.orquesta-sequential
    parameters: 
      name: Earthling
    status: succeeded (4s elapsed)
    start_timestamp: Thu, 25 Jul 2019 20:01:13 UTC
    end_timestamp: Thu, 25 Jul 2019 20:01:17 UTC
    result: 
      output:
        greeting: Earthling, All your base are belong to us!
    +--------------------------+------------------------+-------+-----------+-----------------+
    | id                       | status                 | task  | action    | start_timestamp |
    +--------------------------+------------------------+-------+-----------+-----------------+
    | 5d3a0a890a08a41a426722d5 | succeeded (1s elapsed) | task1 | core.echo | Thu, 25 Jul     |
    |                          |                        |       |           | 2019 20:01:13   |
    |                          |                        |       |           | UTC             |
    | 5d3a0a8a0a08a41a426722d8 | succeeded (1s elapsed) | task2 | core.echo | Thu, 25 Jul     |
    |                          |                        |       |           | 2019 20:01:14   |
    |                          |                        |       |           | UTC             |
    | 5d3a0a8b0a08a41a426722db | succeeded (1s elapsed) | task3 | core.echo | Thu, 25 Jul     |
    |                          |                        |       |           | 2019 20:01:15   |
    |                          |                        |       |           | UTC             |
    +--------------------------+------------------------+-------+-----------+-----------------+

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

There are more workflow examples under :github_st2:`/usr/share/doc/st2/examples <contrib/examples/actions/workflows/>`, including workflows that demonstrate branches, joins, decision tree, error handling, rollback/retry, and others.

Additional Tools and Resources
------------------------------

.. note::

    The following tools and resources are not owned by |st2|. Please use at your own risk.

* `YAQL documentation <https://yaql.readthedocs.io/en/latest/>`_ and `YAQL online evaluator
  <http://yaqluator.com/>`_
* `Jinja2 template engine documentation <https://jinja.palletsprojects.com/en/2.11.x/>`_ and `Jinja2 online evaluator
  <http://jinja.quantprogramming.com/>`_
* `Workflow visualization tool <http://www.orquestaedit.com/>`_
