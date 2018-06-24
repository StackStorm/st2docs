Workflow Operations
===================

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
