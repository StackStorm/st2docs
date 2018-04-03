.. NOTE: This file has been generated automatically, don't manually edit it

* ``sudo_password`` (string) - Sudo password. To be used when paswordless sudo is not allowed.
* ``env`` (object) - Environment variables which will be available to the script(e.g. key1=val1,key2=val2)
* ``sudo`` (boolean) - The command will be executed with sudo.
* ``kwarg_op`` (string) - Operator to use in front of keyword args i.e. "--" or "-".
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.
* ``debug`` (boolean) - Enable runner debug mode.
* ``content_version`` (string) - Git revision of the pack content to use for this action execution (git commit sha / tag / branch). Only applies to packs which are git repositories.
* ``cwd`` (string) - Working directory where the script will be executed in