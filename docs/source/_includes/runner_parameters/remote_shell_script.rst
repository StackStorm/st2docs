.. NOTE: This file has been generated automatically, do not manually edit it.
         If you want to update runner parameters, make your changes to the
         runner YAML files in st2/contrib/runners/ and then run

         make docs

         to regenerate the documentation for runners.


* ``bastion_host`` (string) - The host SSH connections will be proxied through. Note: This connection is made using the same parameters as the final connection.
* ``cwd`` (string) - Working directory where the script will be executed in.
* ``dir`` (string) - The working directory where the script will be copied to on the remote host.
* ``env`` (object) - Environment variables which will be available to the script(e.g. key1=val1,key2=val2)
* ``hosts`` (string) - A comma delimited string of a list of hosts where the remote command will be executed. For example: example1.com,example2.com,example3.com:5555
* ``kwarg_op`` (string) - Operator to use in front of keyword args i.e. "--" or "-".
* ``parallel`` (boolean) - Default to parallel execution.
* ``passphrase`` (string) - Passphrase for the private key, if needed.
* ``password`` (string) - Password used to log in. If not provided, private key from the config file is used.
* ``port`` (integer) - SSH port. If not specified as part of the hosts list, default port will be used (22).
* ``private_key`` (string) - Private key material to log in. Note: This needs to be actual private key data and NOT path.
* ``sudo`` (boolean) - The remote command will be executed with sudo.
* ``sudo_password`` (string) - Sudo password. To be used when passwordless sudo is not allowed.
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.
* ``username`` (string) - Username used to log-in. If not provided, default username from config is used.