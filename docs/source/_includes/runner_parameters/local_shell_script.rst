.. NOTE: This file has been generated automatically, don't manually edit it

* ``debug`` (boolean) - Enable runner debug mode.
* ``content_version`` (string) - Git revision of the pack content to use for this action execution (git commit sha / tag / branch). Only applies to packs which are git repositories.
* ``cwd`` (string) - Working directory where the script will be executed in
* ``env`` (object) - Environment variables which will be available to the script(e.g. key1=val1,key2=val2)
* ``kwarg_op`` (string) - Operator to use in front of keyword args i.e. "--" or "-".
* ``sudo`` (boolean) - The command will be executed with sudo.
* ``sudo_password`` (string) - Sudo password. To be used when passwordless sudo is not allowed.
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.