Action Runners
==============

An action runner is the execution environment for user-implemented actions. |st2| comes with
pre-canned action runners such as a remote runner and shell runner which provide for
user-implemented actions to be run remotely (via SSH) and locally. The objective is to allow the
Action author to concentrate only on the implementation of the action itself rather than setting up
the environment.

Exit Codes
----------
Normally the exit code of a runner is defined by the exit code of the script or command executed.
All runners return timeout exit code (-9) if the command or script did not complete its execution
within the specified timeout.

Local Command Runner (local-shell-cmd)
--------------------------------------

This is the local runner. This runner executes a Linux command on the host where |st2| is running.

.. note::

    ``stdout`` and ``stderr`` attributes in the runner result object have the last ``\n`` or ``\r``
    or ``\r\n`` characters removed if present. This is done so you can re-use the result of common
    commands that include a trailing line break of carriage return, such as ``uptime``, ``whoami``,
    etc., in other actions and workflows. If you have an action which requires a trailing line
    break character to be present, you can add it explicitly to the result, e.g.
    ``echo -e 'test\n'`` (this will result into two line break characters and only one of
    them will be stripped/removed from the result).

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/local_shell_cmd.rst

Local script runner (local-shell-script)
----------------------------------------

This is the local runner. Actions are implemented as scripts. They are executed on the host where
|st2| is running. The last newline character is stripped from ``stdout`` and ``stderr`` fields in 
the output.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/local_shell_script.rst

Remote Command Runner (remote-shell-cmd)
----------------------------------------

This is a remote runner. This runner executes a Linux command on one or more remote hosts provided
by the user. The last newline character is stripped from ``stdout`` and ``stderr`` fields in the
output.

.. note::

   By default |st2| uses passwordless sudo for to execute commands on local and remote systems, using the
   system user (by default ``stanley``). In addition to passwordless sudo, local and remote runners also
   support password protected sudo via the ``sudo_password`` runner parameter. 
   
   With the remote runner, the sudo password is passed to the sudo command as a command line argument.
   This means it has some security implications - if bash history is enabled for the system user, the sudo
   password will be saved in bash history and any system user with access to that user bash history file
   will be able to view it.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/remote_shell_cmd.rst

.. include:: /_includes/private_key_path_notice.rst

Remote script runner (remote-shell-script)
------------------------------------------

This is a remote runner. Actions are implemented as scripts. They run on one or
more remote hosts provided by the user. The last newline character is stripped
from ``stdout`` and ``stderr`` fields in the output.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/remote_shell_script.rst

.. include:: /_includes/private_key_path_notice.rst

Windows Command Runner (windows-cmd)
------------------------------------

.. include:: /_includes/__windows_runners_deprecation_notice.rst
  
The Windows command runner allows you to run the command-line interpreter (``cmd``) and PowerShell
commands on Windows hosts.

For more information on enabling and setting up the Windows runner, please see the following
section - :doc:`/install/config/windows_runners`.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/windows_cmd.rst

Windows Script Runner (windows-script)
--------------------------------------

.. include:: /_includes/__windows_runners_deprecation_notice.rst
  
Windows script runner allows you to run PowerShell scripts on Windows hosts.

For more information on enabling and setting up the Windows runner, please see the following
section - :doc:`/install/config/windows_runners`.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/windows_script.rst

.. _ref-winrm-runners:
             
WinRM Command Runner (winrm-cmd)
------------------------------------

The WinRM command runner allows you to run the command-line interpreter (``cmd``) commands on Windows hosts using the WinRM protocol.

For more information on enabling and setting up the WinRM runner, please see the following
section - :doc:`/install/config/winrm_runners`.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/winrm_cmd.rst

WinRM PowerShell Command Runner (winrm-ps-cmd)
----------------------------------------------

The WinRM PowerShell command runner allows you to run the PowerShell commands on Windows hosts using the WinRM protocol.

For more information on enabling and setting up the WinRM runner, please see the following
section - :doc:`/install/config/winrm_runners`.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/winrm_ps_cmd.rst
             
WinRM PowerShell Script Runner (winrm-ps-script)
------------------------------------------------

WinRM PowerShell script runner allows you to run PowerShell scripts on Windows hosts.
To specify what script to execute, use the ``entry_point`` option in the
:ref:`Action metadata<ref-action-metadata>` file.

For more information on enabling and setting up the WinRM runner, please see the following
section - :doc:`/install/config/winrm_runners`.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/winrm_ps_script.rst

HTTP Runner (http-request)
--------------------------

HTTP runner works by performing HTTP request to the provided URL.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/http_request.rst

Keep in mind that other parameters such as ``body``, ``method``, ``headers``, etc. are defined
as part of the ``core.http`` action.

Runner Result
~~~~~~~~~~~~~

The result object from this runner contains the following keys:

* ``status_code`` (integer) - Response status code (e.g. 200, 404, etc.)
* ``body`` (string/object) - Response body. If the response body contains JSON and the response
  ``Content-Type`` header is ``application/json``, the body will be automatically parsed as JSON.
* ``parsed`` (boolean) - Flag which indicates if the response body has been parsed.
* ``headers`` - Response headers.

Python Runner (python-script)
-----------------------------

This is a Python runner. Actions are implemented as Python classes with a ``run`` method. They run
locally on the machine where ``st2actionrunner`` is running.

Python runner actions return an execution status (success, failure) by returning a tuple
from the Python action class ``run()`` method. The first item in this tuple is a boolean
flag indicating success/failure and the second one is the result. However, execution status is
optional i.e. the return value from action runner can either be a tuple of success status
and result or just the result object.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/python_script.rst

Runner Result
~~~~~~~~~~~~~

The return value from this action runner is a tuple consisting of a boolean flag indicating
success/failure and the second one is the result:

* ``status`` (boolean) - Flag indicating action's success, i.e. Succeeded status is True/False.
  Note: This is an optional flag.
* ``result`` (object) - result returned by the action based on success or failure.

The status flag allows users to return a result from a failing action. When the status flag is
not used the only way for action to be considered as failed is to throw an exception or exit
with a non-zero exit code.

.. _ref-actionchain-runner:

ActionChain Runner (action-chain)
---------------------------------

ActionChain is a no-frills linear workflow, providing a simple chain of action invocations.
For more information, please refer to the :doc:`Workflows </workflows>` and
:doc:`ActionChain </actionchain>` section of documentation.

Runner Parameters
^^^^^^^^^^^^^^^^^

.. include:: /_includes/runner_parameters/action_chain.rst
