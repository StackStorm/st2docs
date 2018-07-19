Workflow Operations
===================

Pausing and Resuming Workflow Execution
---------------------------------------

Orchestra workflow execution can be paused by running ``st2 execution pause <execution-id>``. An
execution must be in a running state in order for pause to be successful. The execution will
initially go into a ``pausing`` state, and will go into a ``paused`` state when no more tasks are
in an active state such as ``running``, ``pausing``, or ``canceling``. When a workflow execution
is paused, it can be resumed by running ``st2 execution resume <execution-id>``.

The ``pause`` and ``resume`` operation will cascade down to subworkflows. Orchestra allows for
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

A workflow execution can be re-run on error. In the current beta, the workflow execution can only
be re-run from the beginning. Re-running the workflow execution from the beginning is exactly like
re-running any |st2| execution with the command ``st2 execution re-run <execution-id>``. The re-run
is a completely separate execution with a new execution ID in |st2|.
