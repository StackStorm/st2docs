StackStorm Runtime
==================

StackStorm Context
------------------

During workflow execution, runtime information on the StackStorm action execution cooresponding to
this workflow execution can be access via ``ctx().st2`` or ``ctx("st2")``. The following is a list
of attributes available under the st2 context. For example, to reference action_execution_id, use
the expression ``ctx().st2.action_execution_id``.

+----------------------+---------------------------------------------------------------------+
| Attribute            | Description                                                         |
+======================+=====================================================================+
| action_execution_id  | Action execution ID corresponding to the workflow execution.        |
+----------------------+---------------------------------------------------------------------+
| api_url              | URL of the st2 API endpoint.                                        |
+----------------------+---------------------------------------------------------------------+
| api_user             | The user who runs the ChatOps command from the client.              |
+----------------------+---------------------------------------------------------------------+
| pack                 | The pack that the action and corresponding workflow belongs to.     |
+----------------------+---------------------------------------------------------------------+
| source_channel       | The ChatOps channel associated with the action execution.           |
+----------------------+---------------------------------------------------------------------+
| user                 | The user that invoked the action execution for this workflow.       |
+----------------------+---------------------------------------------------------------------+

StackStorm Functions
--------------------

task
""""

The ``task`` function can be used to access the task execution record during runtime. The
following is the list of input parameters for the function.

+-----------+----------+---------------------------------------------------------------------+
| Parameter | Required | Description                                                         |
+===========+==========+=====================================================================+
| task_name | No       | Valid name of any tasks in the workflow. Default to current task    |
|           |          | if task_name is not given.                                          |
+-----------+----------+---------------------------------------------------------------------+

This task function can be used wherever YAQL or Jinja expression is accepted in the workflow
definition. The YAQL expression ``<% task() %>`` returns the record for the current task. The
YAQL expression ``<% task("xyz") %>`` returns the record for a task named "xyz" under the
same execution branch. The function returns a dictionary with the following list of
attributes. To reference the task result, use ``task("xyz").result``.

+-----------------------+--------------------------------------------------------------------+
| Attribute             | Description                                                        |
+=======================+====================================================================+
| task_execution_id     | Task execution ID for the referenced task.                         |
+-----------------------+--------------------------------------------------------------------+
| workflow_execution_id | Workflow execution ID where this task belongs to.                  |
+-----------------------+--------------------------------------------------------------------+
| task_name             | Name of the task.                                                  |
+-----------------------+--------------------------------------------------------------------+
| task_id               | Unique ID for the task. This may be different than task_name.      |
+-----------------------+--------------------------------------------------------------------+
| route                 | Route ID for the branch of workflow execution.                     |
+-----------------------+--------------------------------------------------------------------+
| result                | Result of the action execution for the task.                       |
+-----------------------+--------------------------------------------------------------------+
| status                | Status of the task execution.                                      |
+-----------------------+--------------------------------------------------------------------+
| start_timestamp       | Timestamp when the task execution started.                         |
+-----------------------+--------------------------------------------------------------------+
| end_timestamp         | Timestamp when the task execution ended.                           |
+-----------------------+--------------------------------------------------------------------+

st2kv
"""""

The ``st2kv`` function queries the StackStorm datastore and returns the value for the given
key. The following is the list of input parameters for the function.

+-----------+----------+---------------------------------------------------------------------+
| Parameter | Required | Description                                                         |
+===========+==========+=====================================================================+
| key       | Yes      | Name of the key.                                                    |
+-----------+----------+---------------------------------------------------------------------+
| decrypt   | No       | Decrypt the value if True. Default to False if not given.           |
+-----------+----------+---------------------------------------------------------------------+
| default   | No       | Returns this default value if key does not exist.                   |
+-----------+----------+---------------------------------------------------------------------+ 

For example, the expression ``<% st2kv('system.shared_key_x') %>`` returns the value for a system
scoped key named ``shared_key_x`` while the expression ``<% st2kv('my_key_y') %>`` returns the
value for the user scoped key named ``my_key_y``. Please note that the key name should be in quotes
otherwise YAQL treats a key name with a dot like ``system.shared_key_x`` as a dict access. The value
can be encrypted in the StackStorm datastore. To decrypt the retrieved value, the input argument
``decrypt`` must be set to true such as ``st2kv('st2_key_id', decrypt=>true)``.
