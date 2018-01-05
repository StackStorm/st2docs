.. NOTE: This file has been generated automatically, don't manually edit it

* ``username`` (string) - Username used to log-in. If not provided, default username from config is used.
* ``private_key`` (string) - Private key material or path to the private key file on disk used to log in.
* ``sudo_password`` (string) - Sudo password. To be used when paswordless sudo is not allowed.
* ``env`` (object) - Environment variables which will be available to the command(e.g. key1=val1,key2=val2)
* ``sudo`` (boolean) - The remote command will be executed with sudo.
* ``kwarg_op`` (string) - Operator to use in front of keyword args i.e. "--" or "-".
* ``bastion_host`` (string) - The host SSH connections will be proxied through. Note: This connection is made using the same parameters as the final connection, and is only used in ParamikoSSHRunner.
* ``passphrase`` (string) - Passphrase for the private key, if needed.
* ``password`` (string) - Password used to log in. If not provided, private key from the config file is used.
* ``port`` (integer) - SSH port. Note: This parameter is used only in ParamikoSSHRunner.
* ``cmd`` (string) - Arbitrary Linux command to be executed on the remote host(s).
* ``parallel`` (boolean) - Default to parallel execution.
* ``hosts`` (string) - A comma delimited string of a list of hosts where the remote command will be executed.
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.
* ``cwd`` (string) - Working directory where the script will be executed in
* ``dir`` (string) - The working directory where the script will be copied to on the remote host.