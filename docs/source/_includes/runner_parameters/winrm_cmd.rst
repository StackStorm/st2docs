.. NOTE: This file has been generated automatically, don't manually edit it

* ``username`` (string) - Username used to log-in.
* ``password`` (string) - Password used to log in.
* ``env`` (object) - Environment variables which will be available to the command (e.g. key1=val1,key2=val2)
* ``cmd`` (string) - Arbitrary Command Prompt command to be executed on the remote host.
* ``cwd`` (string) - Working directory where the command will be executed in
* ``kwarg_op`` (string) - Operator to use in front of keyword args i.e. "-" or "/".
* ``host`` (string) - A host where the command will be run
* ``transport`` (string) - The type of transport that WinRM will use to communicate. See https://github.com/diyan/pywinrm#valid-transport-options
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.
* ``scheme`` (string) - Scheme to use in the WinRM URL. If using scheme "http" port must be 5985
* ``port`` (integer) - WinRM port to connect on. If using port 5985 scheme must be "http"
* ``verify_ssl_cert`` (boolean) - Certificate for HTTPS request is verified by default using requests CA bundle which comes from Mozilla. Verification using a custom CA bundle is not yet supported. Set to False to skip verification.