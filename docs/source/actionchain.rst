ActionChain
===========

ActionChain is a no-frills linear workflow. It is a simple chain of action invocations. The result
of each action (success or failure) is checked and used to determine the next action to run. This
provides for simple branching logic, based upon success or failure.

Data can be passed between actions, and results are published for each action.

From the perspective of |st2|, an ActionChain is itself an action. So it has the same operations
and features, such as definition, registration, execution from CLI, usage from Rules, etc. An
ActionChain can also be called as an Action from another ActionChain, or from an Orquesta workflow.

.. note::

   If you need more complex workflow logic, such as forks, joins, retries, delays and policies
   for error handling, use :doc:`Orquesta <orquesta/index>` instead.

Creating an ActionChain
-----------------------

ActionChains are defined in packs, under the ``/opt/stackstorm/packs/<pack>/actions/`` directory.
An ActionChain needs two files: a YAML metadata file, the same as used for simple actions, and the
ActionChain definition itself. The metadata file lives in the ``<pack>/actions`` directory, while
the ActionChain definition is placed in the ``<pack>/actions/chains`` directory.

ActionChain Metadata
~~~~~~~~~~~~~~~~~~~~

The ActionChain metadata is very similar to that used for :doc:`any other action<actions>`.
The key differences are that it specifies ``action-chain`` as the ``runner_type``, and the
``entry_point`` points to the workflow definition file.

Here is an example showing the action definition metadata :github_st2:`echochain.meta.yaml
<contrib/examples/actions/echochain.meta.yaml>` for an ActionChain :github_st2:`echochain.yaml
<contrib/examples/actions/chains/echochain.yaml>`:

.. literalinclude:: /../../st2/contrib/examples/actions/echochain.meta.yaml
   :language: yaml

ActionChain Definition
~~~~~~~~~~~~~~~~~~~~~~

This :github_st2:`echochain.yaml <contrib/examples/actions/chains/echochain.yaml>`: is the
corresponding ActionChain workflow definition referenced above:

.. literalinclude:: /../../st2/contrib/examples/actions/chains/echochain.yaml
   :language: yaml

Definition Details:
+++++++++++++++++++

* ``chain`` is the array property that contains tasks, which encapsulate action invocation.
* Tasks are named action execution specifications provided in the form of a list. The name is
  scoped to an ActionChain and is used as a reference to a task.
* The ``ref`` property of a task points to an Action registered in |st2|. This could be in any
  pack.
* ``on-success`` is the link to a task to invoke next upon successful action execution. If not
  provided, the ActionChain will terminate with status set to ``success``.
* ``on-failure`` is an optional link to a task to invoke next in case of a  failed action execution.
  If not provided, the ActionChain will terminate with the status set to ``error``.
* ``default`` is an optional top level property that specifies the start of an ActionChain. If
  ``default`` is not explicitly specified, the ActionChain starts from the first action.


Registering the ActionChain
---------------------------

Once action definition and metadata files are created, load the action:

.. code-block:: bash

    # Register the action
    st2 action create /opt/stackstorm/packs/examples/actions/echochain.meta.yaml
    # Check it is available
    st2 action list --pack=examples
    # Run it
    st2 run examples.echochain

Any changes in the ActionChain workflow definition are picked up automatically. However if you
change the action metadata (e.g. rename or add parameters), you will have to update the action with
``st2 action update <action.ref> <action.metadata.file>```. Alternatively, a full reload with
``st2ctl reload --register-all`` will pick up all the changes.

Providing Input
---------------

To provide input to an ActionChain, input parameters must be defined in the action metadata:

.. literalinclude:: /../../st2/contrib/examples/actions/echochain_param.meta.yaml
   :language: yaml

The input parameter ``input1`` can now be referenced in the parameters field of a task in the
ActionChain definition:

.. code-block:: yaml

   ---
      # ...
      chain:
         -
            name: "action1"
            ref: "core.local"
            parameters:
               action1_input: "{{input1}}"
      # ...

``action1_input`` has value ``{{input1}}``. This syntax is variable referencing as supported by
`Jinja templating <http://jinja.pocoo.org/docs/dev/templates/>`__.

Similar constructs are also used in :doc:`Rule </rules>` criteria and action fields.

Variables
---------

ActionChain offers the convenience of named variables. Global vars are set at the top of the
definition with the ``vars`` keyword.

Tasks publish new variables with the ``publish`` keyword. Variables are handy when you need to mash
up a reusable value from the input, globals, datastore values, and results of multiple action
executions.

All variables are referred to using Jinja syntax. The cumulative published variables are also
available in the result of an ActionChain execution under the ``published`` property if the
``display_published`` property is supplied to the :ref:`ActionChain Runner <ref-actionchain-runner>`.

.. code-block:: yaml

    ---
    vars:
        domain: "{{ st2kv.system.domain }}" # Global Var
        port: 9101

    chain:
        -
            name: get_service_data
            ref:  my_pack.get_services
            publish:
                url_1: http://"{{ get_service_data.result[0].host.name }}.{{ domain }}:{{ port }}"

The :github_st2:`publish_data.yaml <contrib/examples/actions/chains/publish_data.yaml>` workflow in
the `examples` pack shows a complete working example of using ``vars`` and ``publish``:

.. literalinclude:: /../../st2/contrib/examples/actions/chains/publish_data.yaml
   :language: yaml
   :lines: 1-29

Passing Data between Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~

The output of previous tasks can be referenced in a similar manner to input to an ActionChain.

This example :github_st2:`echochain_param.yaml <contrib/examples/actions/chains/echochain_param.yaml>`
shows input and data passing down the workflow:

.. literalinclude:: /../../st2/contrib/examples/actions/chains/echochain_param.yaml
   :language: yaml

Details:
++++++++

* Output of a task is always prefixed by the task name. e.g. in ``{"cmd":"echo c2 {{c1.stdout}}"}``,
  ``c1.stdout`` refers to the output of 'c1' and further drills down into properties of the output.
  The reference point is the ``result`` field of ``action execution`` object.
* A special ``__results`` key provides access to the entire result of the whole chain up to that
  point of execution.

Passing Data Between Different Workflows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In |st2|, a workflow is just an action. This means you pass data from one workflow to another in
exactly the same manner was you would pass data to an action - you use action parameters.

In the example below, we have two workflows - ``workflow1`` and ``workflow2``. The task named
``task2`` inside ``workflow1`` calls ``workflow2`` and passes the variable ``date`` to it as an
action parameter. ``workflow2`` then uses this value and prints it to standard output.

``workflow1.yaml``

.. code-block:: yaml

    ---
        chain:
            -
                name: "task1"
                ref: "core.local"
                parameters:
                    cmd: "date"
                on-success: "task2"
            -
                name: "task2"
                ref: "mypack.workflow2"
                parameters:
                    date: "{{ task1.stdout }}"  # Here we pass result from "task1" as a "date" action parameter to the action "workflow2"

``workflow2.meta.yaml``

.. code-block:: yaml

    ---
    name: "workflow2"
    description: "..."
    runner_type: "action-chain"
    entry_point: "workflow2.yaml"
    enabled: true
    parameters:
     date:
        type: "string"
        description: "Date which show be printed to stdout"
        required: True

``workflow2.yaml``

.. code-block:: yaml

    ---
        chain:
            -
                name: "task1"
                ref: "core.local"
                parameters:
                    cmd: "echo {{ date }}"  # Here we echo the variable "date" which was passed to the workflow as an action parameter

The example above applies to a scenario where you have two related workflows and one calls another.

If you have two independent workflows and you want to pass data between them or use data from one
workflow in another, the most common approach to that is using the built-in key-value
:doc:`datastore <datastore>`.

Inside the first workflow you store data in the datastore and inside the second workflow you retrieve
this data from a datastore. This approach creates tighter coupling between two workflows and makes
them less re-usable and harder to run independently of each other. Where possible, we encourage you
to design the workflow in such a way that you can pass data using action parameters instead.

Using action parameters means the second workflow can still be re-used and run independently of the
first one - you simply need to pass the required parameters to it.

Pausing and Resuming Action Chain Execution
-------------------------------------------

An execution of an ActionChain can be paused by running ``st2 execution pause <execution-id>``. An
execution must be in a running state in order for pause to be successful. The execution will initially
go into a ``pausing`` state, then will go into a ``paused`` state when no more tasks are in an active
state such as ``running``, ``pausing``, or ``canceling``. When an Action Chain is paused, it can be
resumed by running ``st2 execution resume <execution-id>``.

Published variables are saved in the execution context on pause and restored on resume. 

.. note::

   In this version, the published variables are stored unencrypted in the execution context.

The ``pause`` and ``resume`` operation will cascade down to subworkflows, whether it's another |st2|
action that is an Orquesta workflow or ActionChain. If the ``pause`` operation is performed from a
subworkflow or subchain, then the ``pause`` will cascade up to the parent workflow or parent chain.
However, if the ``resume`` operation is performed from a subworkflow or subchain, the ``resume``
will not cascade up to the parent workflow or parent chain. This allows users to resume and
troubleshoot branches individually.

Gotchas
-------

Using YAML and Jinja implies some constraints on how to name and reference variables:

* Variable names can use letters, underscores, and numbers. No dashes! This applies to all
  variables: global vars, input parameters, :doc:`DataStore keys <datastore>`, and published
  variables.
* The same naming rules apply to task names: ``this-task-name-is-wrong``! Use
  ``task_names_with_underscores``.
* Always quote variable references ``"{{ my_variable.or.expression }}"`` (remember that ``{ }`` is
  a YAML dictionary). The types are respected inside the Jinja template but converted to strings
  outside: ``"{{ 1 + 2 }} + 3"`` resolves to ``"3 + 3"``.

Error Reporting
---------------

ActionChain errors are classified as:

* Errors reported by a specific task in the chain. In this case the error is reported as per
  behavior of the particular action in the task.

  Sample output:

  .. code-block:: json

   {    
        "result": {
            "tasks": [
                {
                    "created_at": "2015-02-27T19:29:02.057885+00:00",
                    "execution_id": "54f0c57e0640fd177f278052",
                    "id": "c1",
                    "name": "c1",
                    "result": {
                        "failed": true,
                        "return_code": 127,
                        "stderr": "bash: borg: command not found\n",
                        "stdout": "",
                        "succeeded": false
                    },
                    "state": "failed",
                    "updated_at": "2015-02-27T19:29:03.149547+00:00",
                    "workflow": null
                }
            ]
        }
    }

* Errors experienced by the ActionChain runtime while determining the flow. In this case the error
  is reported as the error property of the ActionChain result.

  Sample output:

  .. code-block:: json

    {
        "result": {
            "error": "Failed to run task \"c2\". Parameter rendering failed: 's1' is undefined",
            "traceback": "Traceback (most recent call last):...",
            "tasks": [
                {
                    "created_at": "2015-02-27T19:19:34.536558+00:00",
                    "execution_id": "54f0c3460640fd15a843957d",
                    "id": "c1",
                    "name": "c1",
                    "result": {
                        "failed": false,
                        "return_code": 0,
                        "stderr": "",
                        "stdout": "Fri Feb 27 19:19:34 UTC 2015\n",
                        "succeeded": true
                    },
                    "state": "succeeded",
                    "updated_at": "2015-02-27T19:19:35.591297+00:00",
                    "workflow": null
                }
            ]
        }
    }
