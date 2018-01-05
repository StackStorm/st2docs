Mistral
=======

`Mistral <https://docs.openstack.org/mistral/latest/overview.html>`_ is an OpenStack project that
manages and executes workflows as a service. Mistral is automatically installed as a separate
service named "mistral" along with |st2|. A Mistral workflow can be defined as a |st2| action in a
Mistral workbook using the `v2 DSL <https://docs.openstack.org/mistral/latest/user/dsl_v2.html>`_.

Expression languages such as YAQL are used for formatting variables and condition evaluations.
Starting with |st2| v2.2, Jinja2 is also supported where YAQL expressions are accepted. Both
workbook and workflow definitions are supported. 

On action execution, |st2| writes the definition to Mistral and executes the workflow. A workflow
can invoke other |st2| actions natively as subtasks. |st2| handles the translations and calls
transparently in Mistral and actively polls Mistral for execution results. |st2| actions in the
workflow can be traced back to the original parent action that invoked the workflow.

**Essential Mistral Links:**

* Mistral workflow definition language, aka `v2 DSL
  <https://docs.openstack.org/mistral/latest/user/dsl_v2.html>`_
* `YAQL documentation <https://yaql.readthedocs.io/en/latest/>`_ and `YAQL online evaluator
  <http://yaqluator.com/>`_
* `Jinja2 template engine documentation <http://jinja.pocoo.org>`_ and `Jinja2 online evaluator
  <http://jinja2test.tk/>`_


.. note::

    Workflow examples in this documentation use YAQL expressions unless otherwise stated.

Basic Workflow
--------------

Similarly to ActionChains, Mistral workflows have an action metadata file in
``/opt/stackstorm/packs/<mypack>/actions``, and the workflow definition itself in
``/opt/stackstorm/packs/<mypack>/actions/workflows``.

Let's start with a very basic workflow that calls a |st2| action and notifies |st2| when the
workflow is done. The files used in this example are also located under
:github_st2:`/usr/share/doc/st2/examples </contrib/examples>` if |st2| is already installed (see
also :ref:`deploy examples <start-deploy-examples>`).

The first task is named ``run-cmd``. It executes a shell command on the server where |st2| is
installed. A task can reference any registered |st2| action directly. In this example, the
``run-cmd`` task calls ``core.local`` and passing the cmd as input. ``core.local`` is an action
that comes installed with |st2|. When the workflow is invoked, |st2| will translate the workflow
definition appropriately before sending it to Mistral. Let's save this as
``/opt/stackstorm/packs/examples/actions/workflows/mistral-basic.yaml`` on our |st2| server.

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/mistral-basic.yaml
   :language: yaml

This is the corresponding |st2| action metadata for the example above. The |st2| pack for this
workflow action is named "examples". Note that the workflow is named fully qualified as
``<pack>.<action`` in the definition above. The |st2| action runner is ``mistral-v2``. The entry
point for the |st2| action refers to the YAML file of the workflow definition. Let's save this
metadata as ``/opt/stackstorm/packs/examples/actions/mistral-basic.yaml``:

.. literalinclude:: /../../st2/contrib/examples/actions/mistral-basic.yaml
   :language: yaml

The following table list optional parameters that can be defined in the workflow action. In the
example, these optional parameters are set to immutable. It is good practice to set them to
immutable even if they are empty since these are Mistral-specific parameters for the workflow
author.

+------------+--------------------------------------------------------+
| options    | description                                            |
+============+========================================================+
| workflow   | If definition is a workbook containing many workflows, |
|            | this specifies the main workflow to execute.           |
+------------+--------------------------------------------------------+
| task       | If the type of workflow is "reverse", this specifies   |
|            | the task to invoke.                                    |
+------------+--------------------------------------------------------+
| context    | A dictionary containing additional workflow start up   |
|            | parameters.                                            |
+------------+--------------------------------------------------------+

Next, run ``st2 action create /opt/stackstorm/packs/examples/actions/mistral-basic.yaml`` to
create this workflow action. This will register the workflow as ``examples.mistral-basic`` in
|st2|. To execute the workflow, run ``st2 run examples.mistral-basic cmd=date -a`` where ``-a``
tells the command to return and not wait for the workflow to complete. 

If the workflow completed successfully, both the workflow ``examples.mistral-basic`` and the
action ``core.local`` should have a ``succeeded`` status in the |st2| action execution list. By
default, ``st2 execution list`` only returns top level executions. This means subtasks are not
displayed.

.. code-block:: shell

    +--------------------------+--------------+--------------+-----------+-----------------+---------------+
    | id                       | action.ref   | context.user | status    | start_timestamp | end_timestamp |
    +--------------------------+--------------+--------------+-----------+-----------------+---------------+
    | 54ee54c61e2e24152b769a47 | examples     | stanley      | succeeded | Wed, 25 Feb     | Wed, 25 Feb   |
    |                          | .mistral-    |              |           | 2015 23:03:34   | 2015 23:03:34 |
    |                          | basic        |              |           | UTC             | UTC           |
    +--------------------------+--------------+--------------+-----------+-----------------+---------------+

To display subtasks, run ``st2 execution get <execution-id> --show-tasks``:

.. code-block:: shell

    +--------------------------+------------+--------------+-----------+------------------------------+------------------------------+
    | id                       | action.ref | context.user | status    | start_timestamp              | end_timestamp                |
    +--------------------------+------------+--------------+-----------+------------------------------+------------------------------+
    | 54ee54c91e2e24152b769a49 | core.local | stanley      | succeeded | Wed, 25 Feb 2015 23:03:37    | Wed, 25 Feb 2015 23:03:37    |
    |                          |            |              |           | UTC                          | UTC                          |
    +--------------------------+------------+--------------+-----------+------------------------------+------------------------------+

The following is a simple extension of the previous workflow definition. In this example, we have
a second task named "task2". It might be natural to think that "task2" will be executed after
"task1", i.e, in sequential order. However, when no tasks attributes like ``on-complete``,
``on-success`` and ``on-error`` are defined, tasks are run in parallel. This is possible with
Mistral because it provides a join flow control which allows us to synchronize multiple parallel
workflow branches and aggregate their data.

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/mistral-basic-two-tasks-with-notifications.yaml
   :language: yaml

Pausing and Resuming Workflow Execution
---------------------------------------

An execution of a Mistral workflow can be paused by running ``st2 execution pause <execution-id>``.
An execution must be in a running state in order for pause to be successful. The execution will
initially go into a ``pausing`` state, and will go into a ``paused`` state when no more tasks are
in an active state such as ``running``, ``pausing``, or ``canceling``. When a workflow execution
is paused, it can be resumed by running ``st2 execution resume <execution-id>``.

The ``pause`` and ``resume`` operation will cascade down to subworkflows, whether it's another
workflow defined in a workbook or it's another |st2| action that is a Mistral workflow or Action
Chain. If the ``pause`` operation is performed from a subworkflow or subchain, then the ``pause``
will cascade up to the parent workflow or parent chain. However, if the ``resume`` operation is
performed from a subworkflow or subchain, the ``resume`` will not cascade up to the parent workflow
or parent chain. This allows users to resume and troubleshoot branches individually.

Canceling Workflow Execution
----------------------------

An execution of a Mistral workflow can be cancelled by running
``st2 execution cancel <execution-id>``. Workflow tasks that are still running will not be
canceled and will run to completion. No new tasks for the workflow will be scheduled.

Re-running Workflow Execution
-----------------------------

An execution of a Mistral workflow can be re-run on error. The execution either can be re-run from
the beginning or from the task(s) that failed. The latter is useful for long running workflows with
temporary service or network outages. Re-running the workflow execution from the beginning is
exactly like re-running any |st2| execution with the command
``st2 execution re-run <execution-id>``.

The re-run is a completely separate execution with a new execution ID in both |st2| and Mistral.
Re-running the workflow from where it errored is slightly different. To retain context, the
original workflow execution is reused in Mistral but a new |st2| execution will be created to stay
consistent in |st2|. The re-run command has a new ``--tasks`` option that takes a list of task
names to re-run.

For example, given a workflow that fails at task3 and task4 on separate parallel branches, the
command ``st2 execution re-run <execution-id> --tasks task3 task4`` will resume the Mistral
workflow execution and re-run both task3 and task4 using original inputs. Both the workflow and
task execution in Mistral have to be in an ``errored`` state for re-run.

If using a Mistral workbook, tasks of subworkflows can also be re-run. For example, if the main
workflow has a task1 that calls subflow1, then to re-run subtask1 of subflow1, the syntax for the
``st2 execution re-run`` command would be
``st2 execution re-run <execution-id> --tasks task1.subtask1``.

If the task to re-run is a "with-items" task, there is an option to re-run only failed iterations.
For example, task1 is a with-items task with 5 items. Let's say 2 of the items failed. By
specifying the ``st2 execution re-run --tasks task1 task2 --no-reset task1`` option, task1 will
only re-run the 2 items that failed. If the ``--no-reset`` option is not provided, then all 5
items will be re-run.

.. note::

    Re-running workflow execution from the task(s) that failed is currently an experimental
    feature and subject to bug(s) and change(s). Please also note that re-running a subtask nested
    in another |st2| action is not currently supported.

Publishing Variables in Mistral Workflows
-----------------------------------------

A Mistral task can publish results from a task as variables that can be consumed in other tasks:

.. sourcecode:: yaml

    tasks:
        get_hostname:
            action: core.local
            input:
                cmd: "hostname"
            publish:
                hostname: <% task(get_hostname).result.stdout %>

In the above example, ``get_hostname`` is a ``core.local`` action which runs the command
``hostname``. The ``core.local`` action produces output consisting of the fields ``stdout``,
``stderr``, ``exit_code`` etc.

We just want to publish the variable ``stdout`` from it, for the rest of tasks to consume. To
reference the result of the task, use the ``task`` function, which returns a dictionary containing
attributes for the task such as id, state, result, and additional info.

Another example is shown below:

.. sourcecode:: yaml

    tasks:
        create_new_node:
            action: rackspace.create_vm
            input:
              name: <% $.hostname %>
              flavor_id: <% $.vm_size_id %>
              image_id: <% $.vm_image_id %>
              key_material: <% $.ssh_pub_key %>
              metadata:
                asg: <% $.asg %>
            publish:
              ipv4_address: '<% task(create_new_node).result.result.public_ips[1] %>'
              ipv6_address: '<% task(create_new_node).result.result.public_ips[0] %>'

In the above example, the action ``rackspace.create_vm`` is a Python action that produces a result
object. We just want to publish the IP addresses from the ``public_ips`` list field from the
result object.

Please note that ``result.result`` is not a typo. The Python action posts output to a key named
``result`` for the st2 action execution and the Mistral task function puts the result of the Python
action in ``result`` of its output dictionary.

Such published variables are accessible as input parameters to other tasks in the workflow. An
example of using ``ipv4_address`` from the above example in another task is shown below:

.. sourcecode:: yaml

    tasks:
        # ... <snap>

        setup_ipv4_dns:
            action: rackspace.create_dns_record
            wait-before: 1 # delay, in seconds
            input:
              name: '<% $.hostname %>.<% $.asg %>.<% $.domain %>'
              zone_id: <% $.dns_zone_id %>
              type: 'A'
              data: <% $.ipv4_address %>

        # .... </snap>

Stitching Together a More Complex Workflow
------------------------------------------

The following is a mock up of a more complex workflow. In this mock up running simple ``printf``
and ``sleep`` commands, the workflow demonstrates nested workflows, fork, and join:

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/mistral-workbook-complex.yaml
   :language: yaml

Since there are multiple workflows defined in this workbook, the workflow author has to specify which workflow to execute in the metadata:

.. literalinclude:: /../../st2/contrib/examples/actions/mistral-workbook-complex.yaml
   :language: yaml

To test out this workflow, save the metadata file to ``/opt/stackstorm/packs/examples/actions/``
and the workflow file to ``/opt/stackstorm/packs/examples/actions/workflows``. Run
``st2 action create /opt/stackstorm/packs/examples/actions/mistral-workbook-complex.yaml`` to
create the action and run ``st2 run examples.mistral-workbook-complex vm_name="vmtest1" -a`` to
test.

Validation
----------

The Mistral CLI includes tools for performing high-level sanity checks of Mistral workflow YAML
files:

.. code-block:: bash

   # Validate a workflow
   mistral workflow-validate /path/to/workflow.yaml

   # Validate a workbook
   mistral workbook-validate /path/to/workbook.yaml


.. note::

   These sanity checks simply provide a test against the Mistral DSL schema. They do NOT test YAQL
   or Jinja2 expressions.


More Examples
-------------

There are more workflow examples under :github_st2:`/usr/share/doc/st2/examples </contrib/examples/actions/workflows/>`. These include error handling, repeat, and retries.

Check out this step-by-step tutorial on building a workflow in |st2| https://stackstorm.com/2015/07/08/automating-with-mistral-workflow/

More details about Mistral can be found at https://docs.openstack.org/mistral/latest/.


Mistral Workflows Latency and Performance
-----------------------------------------
|st2| interacts with Mistral via HTTP APIs. This applies when kicking off a workflow execution
or collecting the results for a running workflow. |st2| queries Mistral to check on workflow
execution status and the status of individual tasks. This mechanism has a number of configuration settings.

See :ref:`mistral-workflows-latency` section about how to fine-tune
the Mistral workflows completion time opposed to CPU usage.
