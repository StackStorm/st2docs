Workflow Operations
===================

Pausing and Resuming Workflow Execution
---------------------------------------

Orquesta workflow execution can be paused by running ``st2 execution pause <execution-id>``. An
execution must be in a running state in order for pause to be successful. The execution will
initially go into a ``pausing`` state, and will go into a ``paused`` state when no more tasks are
in an active state such as ``running``, ``pausing``, or ``canceling``. When a workflow execution
is paused, it can be resumed by running ``st2 execution resume <execution-id>``.

The ``pause`` and ``resume`` operation will cascade down to subworkflows. Orquesta allows for
finer control to workflow with multiple branches. If the ``pause`` operation is requested from
a subworkflow, the ``pause`` will not cascade up to the parent workflow and down to other peers.
This supports use case where the user wants to pause only a specific branch but let the rest of
the workflow continues. This behavior is the same for resuming from a subworkflow.

Canceling Workflow Execution
----------------------------

A workflow execution can be cancelled by running ``st2 execution cancel <execution-id>``. Workflow
tasks that are still running will be allowed to run to completion. During cancelation, no new tasks
for the workflow will be scheduled. The execution will remain in ``canceling`` status until there
are no more active tasks.

Re-running Workflow Execution
-----------------------------

A workflow execution can be re-run from the beginning. It is exactly like re-running any |st2|
execution with the command ``st2 execution re-run <execution-id>``. The re-run is a completely
separate action execution with a new action execution ID in |st2| and a new workflow execution
is created for the new action execution.

Re-running Workflow Execution from Task(s)
------------------------------------------

There are use cases where users want to re-run the workflow execution for certain task(s). Orquesta
allows workflow execution to be re-run from any task(s) as long as the workflow execution is in a
completed state (succeeded, failed, or canceled). This is different than using a retry in the
workflow definition to tell Orquesta to automatically retry a task execution. Retry is considered
during workflow design time. Rerun allows a user to respond to unexpected issues during runtime.
This feature allows user to rerun a workflow from a specific step without starting from the
beginning especially if the workflow is long running or has many steps.

Given the sequential workflow below, the workflow execution can be re-run from any task with the
command ``st2 execution re-run <execution-id> --tasks <task_name>``.

.. code-block:: none

    task1 --> task2 --> task3

A new action execution is created for the re-run. However, the workflow execution from original
action execution will be reused. If the task to rerun from is a with items task, there is an
additional argument passed to the re-run command that instruct whether to reset the task or re-run
only failed items. By default, the with items task will be reset. But in certain use cases, users
may want to re-run only failed items. In that case, use the command
``st2 execution re-run <execution-id> --tasks <task_name> --no-reset <task_name>``.

For a different use case where there are multiple parallel branches with join. Given the example
below, let's say task2 and task3 failed and the user wants to rerun the workflow from both tasks.

.. code-block:: none

            +--> task2 --+
    task1 --|            |--> task4
            +--> task3 --+

To rerun the workflow execution from both task2 and task3, use the following command
``st2 execution re-run <execution-id> --tasks task2 task3``. Please take note to use space in
between task names.

If user want to rerun from task1 instead, then just specific only task1 for the rerun and the
other tasks will run per the workflow defintion when task1 completes. The command for this case is
``st2 execution re-run <execution-id> --tasks task1``.

If both tasks are with items tasks and user do not want to reset the tasks and only re-run from
failed items, use the command
``st2 execution re-run <execution-id> --tasks task2 task3 --no-reset task2 task3``.

However, for a user case if user only wants to reset task2 but not task3, then only pass task3
to the ``--no-reset`` arg. The command for this case is
``st2 execution re-run <execution-id> --tasks task2 task3 --no-reset task3``.

And in the case if user wants to rerun from task1 instead and task2 and task3 are with items tasks,
both task2 and task3 will be reset when task1 completes regardless of what user passes to the
``--no-reset`` arg.
