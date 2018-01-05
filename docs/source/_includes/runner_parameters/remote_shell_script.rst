.. NOTE: This file has been generated automatically, don't manually edit it

* ``username`` (string) - Username used to log-in. If not provided, default username from config is used.
* ``private_key`` (string) - Private key material to log in. Note: This needs to be actual private key data and NOT path.
* ``sudo_password`` (string) - Sudo password. To be used when paswordless sudo is not allowed.
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.
* ``env`` (object) - Environment variables which will be available to the script(e.g. key1=val1,key2=val2)
* ``sudo`` (boolean) - The remote command will be executed with sudo.
* ``cwd`` (string) - Working directory where the script will be executed in.
* ``kwarg_op`` (string) - Operator to use in front of keyword args i.e. "--" or "-".
* ``bastion_host`` (string) - The host SSH connections will be proxied through. Note: This connection is made using the same parameters as the final connection, and is only used in ParamikoSSHRunner.
* ``hosts`` (string) - A comma delimited string of a list of hosts where the remote command will be executed.
* ``passphrase`` (string) - Passphrase for the private key, if needed.
* ``parallel`` (boolean) - Default to parallel execution.
* ``password`` (string) - Password used to log in. If not provided, private key from the config file is used.
* ``port`` (integer) - SSH port. Note: This parameter is used only in ParamikoSSHRunner.
* ``dir`` (string) - The working directory where the script will be copied to on the remote host.