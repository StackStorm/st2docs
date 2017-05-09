Action Runners
==============

An action runner is the execution environment for user-implemented
actions. |st2| comes with pre-canned action runners such as a
remote runner and shell runner which provide for user-implemented
actions to be run remotely (via SSH) and locally. The objective is to
allow the Action author to concentrate only on the implementation of the
action itself rather than setting up the environment.

Exit Codes
----------
Normally an exit code of a runner is defined by an exit code of a script or
a command they execute. All runners return timeout exit code (-9) if a
command or a script did not complete its execution within the specified timeout.

Local command runner (local-shell-cmd)
---------------------------------------

This is the local runner. This runner executes a Linux command on the same host
where |st2| components are running.

.. note::

    ``stdout`` and ``stderr`` attributes in the runner
    result object have the last '\n' or '\r' or '\r\n' characters removed if present.
    This is done so you can re-use the result of common commands that include a trailing
    line break of carriage return, such as ``uptime``, ``whoami``, etc.,
    in other actions and workflows. If you have an action which requires a trailing line
    break character to be present, you can add it explicitly to the result, e.g.
    ``echo -e 'test\n'`` (this will result into two line break characters and only one of
    them will be stripped/removed from the result).

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/local_shell_cmd.rst

Local script runner (local-shell-script)
----------------------------------------

This is the local runner. Actions are implemented as scripts. They are executed
on the same hosts where |st2| components are running. The last newline
character is stripped from `stdout` and `stderr` fields in the output.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/local_shell_script.rst

Remote command runner (remote-shell-cmd)
----------------------------------------

This is a remote runner. This runner executes a Linux command on one or more
remote hosts provided by the user. The last newline character is stripped
from `stdout` and `stderr` fields in the output.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/remote_shell_cmd.rst

.. include:: /_includes/private_key_path_notice.rst

Remote script runner (remote-shell-script)
------------------------------------------

This is a remote runner. Actions are implemented as scripts. They run on one or
more remote hosts provided by the user. The last newline character is stripped
from `stdout` and `stderr` fields in the output.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/remote_shell_script.rst

.. include:: /_includes/private_key_path_notice.rst

Windows command runner (windows-cmd)
------------------------------------

Windows command runner allows you to run you to run command-line interpreter
(cmd) and PowerShell commands on Windows hosts.

For more information on enabling and setting up the Windows runner, please see
the following section - :doc:`/install/config/windows_runners`.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/windows_cmd.rst

Windows script runner (windows-script)
--------------------------------------

Windows script runner allows you to run PowerShell scripts on Windows hosts.

For more information on enabling and setting up the Windows runner, please see
the following section - :doc:`/install/config/windows_runners`.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/windows_script.rst

HTTP runner (http-request)
--------------------------

HTTP runner works by performing HTTP request to the provided URL.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/http_request.rst

Keep in mind that other parameters such as ``body``, ``method``, ``headers``, etc. are defined
as part of the ``core.http`` action.

Runner result
~~~~~~~~~~~~~

The result object from this runner contains the following keys:

* ``status_code`` (integer) - Response status code (e.g. 200, 404, etc.)
* ``body`` (string / object) - Response body. If the response body contains JSON
  and the response Content-Type header is ``application/json``, the body will be
  automatically parsed as JSON.
* ``parsed`` (boolean) - Flag which indicates if the response body has been parsed.
* ``headers`` - Response headers.

Python runner (python-script)
-----------------------------

This is a Python runner. Actions are implemented as Python classes with a
``run`` method. They run locally on the same machine where |st2| components are
running.

Python runner actions return an execution status (success, failure) by returning a tuple
from the Python action class ``run()`` method. First item in this tuple is a boolean
flag indicating a success and the second one is the result. However, execution status is
optional i.e. the return value from action runner can either be a tuple of success status
and result or just the result object.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/python_script.rst

Runner result
~~~~~~~~~~~~~

The return value from this action runner is a tuple consisting of a boolean flag indicating
a success and the second one is the result:

* ``status`` (boolean) - Flag indicating action's success, i.e. Succeeded status is True/False.
  Note: This is an optional flag.
* ``result`` (object) - result returned by the action based on success or failure.

The status flag allows users to return a result from a failing action. When the status flag is
not used the only way for action to be considered as failed is to throw an exception or exit
with a non-zero exit code.

.. _ref-actionchain-runner:

ActionChain runner (action-chain)
---------------------------------

ActionChain is a no-frills linear workflow, a simple chain of action invocations.
For more information, please refer to the :doc:`Workflows </workflows>` and
:doc:`ActionChain </actionchain>` section of documentation.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/action_chain.rst

Mistral runner (mistral-v2)
---------------------------

Those runners are built on top of the Mistral OpenStack project and support
executing complex work-flows. For more information, please refer to the
:doc:`Workflows </workflows>` and :doc:`Mistral </mistral>` sections of the documentation.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/mistral_v2.rst

CloudSlang runner (cloudslang)
------------------------------

This runner is built on top of the CloudSlang project and supports
executing complex workflows. For more information, please refer to the
:doc:`Workflows </workflows>` and :doc:`CloudSlang </cloudslang>` sections of the documentation.

Note: This runner is currently in an experimental phase which means that there
might be bugs and the external user facing API might change.

Runner parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/cloudslang.rst
