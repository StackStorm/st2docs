.. NOTE: This file has been generated automatically, don't manually edit it.
         Edit st2common/st2common/constants/triggers.py and rebuild the
         documentation.

Action
~~~~~~

+--------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| Reference                      | Description                                                     | Properties                                                                                                  |
+================================+=================================================================+=============================================================================================================+
| core.st2.generic.actiontrigger | Trigger encapsulating the completion of an action execution.    | execution_id, status, start_timestamp, action_name, action_ref, runner_ref, parameters, result              |
+--------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| core.st2.generic.notifytrigger | Notification trigger.                                           | execution_id, status, start_timestamp, end_timestamp, action_ref, runner_ref, channel, route, message, data |
+--------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| core.st2.action.file_written   | Trigger encapsulating action file being written on disk.        | ref, file_path, host_info                                                                                   |
+--------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| core.st2.generic.inquiry       | Trigger indicating a new "inquiry" has entered "pending" status | id, route                                                                                                   |
+--------------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+

Sensor
~~~~~~

+-------------------------------+--------------------------------------------------+------------+
| Reference                     | Description                                      | Properties |
+===============================+==================================================+============+
| core.st2.sensor.process_spawn | Trigger indicating sensor process is started up. | object     |
+-------------------------------+--------------------------------------------------+------------+
| core.st2.sensor.process_exit  | Trigger indicating sensor process is stopped.    | object     |
+-------------------------------+--------------------------------------------------+------------+

Key Value Pair
~~~~~~~~~~~~~~

+--------------------------------------+---------------------------------------------------------+------------------------+
| Reference                            | Description                                             | Properties             |
+======================================+=========================================================+========================+
| core.st2.key_value_pair.create       | Trigger encapsulating datastore item creation.          | object                 |
+--------------------------------------+---------------------------------------------------------+------------------------+
| core.st2.key_value_pair.update       | Trigger encapsulating datastore set action.             | object                 |
+--------------------------------------+---------------------------------------------------------+------------------------+
| core.st2.key_value_pair.value_change | Trigger encapsulating a change of datastore item value. | old_object, new_object |
+--------------------------------------+---------------------------------------------------------+------------------------+
| core.st2.key_value_pair.delete       | Trigger encapsulating datastore item deletion.          | object                 |
+--------------------------------------+---------------------------------------------------------+------------------------+
