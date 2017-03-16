.. NOTE: This file has been generated automatically, don't manually edit it

* ``kwarg_op`` (string) - Operator to use in front of keyword args i.e. "--" or "-".
* ``cmd`` (string) - Arbitrary Linux command to be executed on the host.
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.
* ``env`` (object) - Environment variables which will be available to the command(e.g. key1=val1,key2=val2)
* ``sudo`` (boolean) - The command will be executed with sudo.
* ``cwd`` (string) - Working directory where the command will be executed in