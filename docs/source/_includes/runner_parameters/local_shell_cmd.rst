.. NOTE: This file has been generated automatically, do not manually edit it.
         If you want to update runner parameters, make your changes to the
         runner YAML files in st2/contrib/runners/ and then run

         make docs

         to regenerate the documentation for runners.


* ``cmd`` (string) - Arbitrary Linux command to be executed on the host.
* ``cwd`` (string) - Working directory where the command will be executed in
* ``env`` (object) - Environment variables which will be available to the command(e.g. key1=val1,key2=val2)
* ``kwarg_op`` (string) - Operator to use in front of keyword args i.e. "--" or "-".
* ``sudo`` (boolean) - The command will be executed with sudo.
* ``sudo_password`` (string) - Sudo password. To be used when passwordless sudo is not allowed.
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.