SSH Troubleshooting
===================

Since v0.13, Paramiko runner is the default SSH runner in |st2|. Most of this
documentation assumes you are using paramiko runner. Wherever behavior is different from
fabric runner, it will be called out.

|st2| remote actions use the ``system_user`` and ``ssh_key_file`` in configuration file (
usually /etc/st2/st2.conf) as authentication credentials to remote boxes. This is to lock
down so all remote actions are run as defined user (default is ``stanley``). The ``
ssh_key_file`` is private key file (RSA/DSA) for ``system_user``. You can change the
username and key file by setting appropriate values in the config file. In case of key
compromises, revoking public key for ``system_user`` from target boxes will revoke access
for |st2| from target boxes. We also recommend adding ``system_user`` to a linux group and
control permissions on target boxes as an additional security measure.

.. note::

    If you are changing ``system_user`` or ``ssh_key_file`` configuration values in |st2|
    configuration file (usually /etc/st2/st2.conf), you must restart |st2| to pick up the
    changes. You can just restart st2actionrunner component (E.g. service st2actionrunner restart).

To validate remote actions are working correctly, you can use the following command.

.. code-block:: bash

    # Default run
    $st2 run core.remote cmd=whoami hosts=localhost
    id: 55dff0bd32ed356c736318b0
    status: succeeded
    result:
    {
        "localhost": {
            "succeeded": true,
            "failed": false,
            "return_code": 0,
            "stderr": "",
            "stdout": "stanley"
        }
    }

If you don't have the right SSH key file, you will see an error and action will fail.

.. code-block:: bash

    st2 run core.remote cmd=whoami hosts=localhost
    id: 583e2282d9d7ed38c78b50eb
    status: failed
    parameters:
      cmd: whoami
      hosts: ma-box
      username: putin
    result:
      error: "Unable to connect to any one of the hosts: [u'ma-box'].

     connect_errors={
      "ma-box": {
        "failed": true,
        "traceback": "Traceback (most recent call last):\n  File \"/mnt/src/storm/st2/st2common/st2common/runners/parallel_ssh.py\", line 243, in _connect\n    client.connect()\n  File \"/mnt/src/storm/st2/st2common/st2common/runners/paramiko_ssh.py\", line 138, in connect\n    self.client = self._connect(host=self.hostname, socket=self.bastion_socket)\n  File \"/mnt/src/storm/st2/st2common/st2common/runners/paramiko_ssh.py\", line 634, in _connect\n    raise SSHException(msg)\nSSHException: Error connecting to host ma-box with connection parameters {'username': u'putin', 'key_filename': '/home/stanley/.ssh/id_rsa', 'allow_agent': False, 'hostname': u'ma-box', 'look_for_keys': False, 'timeout': 60, 'port': 22}.Paramiko error: not a valid EC private key file.\n",
        "timeout": false,
        "succeeded": false,
        "stdout": "",
        "stderr": "",
        "error": "Connection error. Error connecting to host ma-box with connection parameters {'username': u'stanley', 'key_filename': '/home/stanley/.ssh/id_rsa', 'allow_agent': False, 'hostname': u'ma-box', 'look_for_keys': False, 'timeout': 60, 'port': 22}.Paramiko error: not a valid EC private key file.",
        "return_code": 255
      }
    }"
      traceback: "  File "/mnt/src/storm/st2/st2actions/st2actions/container/base.py", line 90, in _do_run
        runner.pre_run()
      File "/mnt/src/storm/st2/st2common/st2common/runners/paramiko_ssh_runner.py", line 145, in pre_run
        self._parallel_ssh_client = ParallelSSHClient(**client_kwargs)
      File "/mnt/src/storm/st2/st2common/st2common/runners/parallel_ssh.py", line 61, in __init__
        connect_results = self.connect(raise_on_any_error=raise_on_any_error)
      File "/mnt/src/storm/st2/st2common/st2common/runners/parallel_ssh.py", line 91, in connect
        raise NoHostsConnectedToException(msg)
    "

All automations (rules that kickoff remote actions or scripts) by default will use this
username and private_key combination.

If you are not using default SSH port 22, you can specify port as part of host string in hosts
list like hosts=localhost:55,st2build001:56. As of |st2| version 2.1, you can also specify
custom ports via SSH config file. To use SSH config file, setup ``/home/stanley/.ssh/config`` for
user ``stanley`` on |st2| action runner boxes appropriately and add
following configuration lines in ``/etc/st2/st2.conf``.

.. code-block:: ini

    [ssh_runner]
    use_ssh_config = True
    ssh_config_file_path = /home/stanley/.ssh/config

We do not recommend running automations as arbitrary user + private_key combination. This
would require you to setup private_key for the users on |st2| action runner boxes and
the public keys of the users in target boxes. This increases the surface area for risk and
is highly discouraged.

Said that, if you have st2client installed and want to run one off commands on remote
boxes as a different user, we have a way.

.. code-block:: bash

    $st2 run core.remote cmd=whoami hosts=localhost username=test_user private_key=/home/stanley/ssh_keys/.ssh/id_rsa
    .
    id: 55dff0de32ed356c736318b9
    status: succeeded
    result:
    {
        "localhost": {
            "succeeded": true,
            "failed": false,
            "return_code": 0,
            "stderr": "",
            "stdout": "test_user"
        }
    }

For the above example to work, key file ``/home/stanley/ssh_keys/.ssh/id_rsa`` has to be available
on action runner boxes. We also support ``password`` as a parameter. As of version 2.1, you
can also specify custom keys for hosts via SSH config file. A sample SSH config is shown below:

.. code-block:: ini

    Host st2-ssh-test001
      User lakshmi
      IdentityFile /home/vagrant/.ssh/lakshmi_id_rsa

    Host *secret-box
      port 55

If you are running remote actions as ``sudo``, pseudo tty is enabled by default. This means
that ``stdout`` and ``stderr`` streams get combined into one and reported as ``stdout``. This
is true for both fabric and paramiko ssh runner.

When using a bastion host for running remote actions, the bastion host must have ``AllowTcpForwarding``
enabled. Additionally, the connection to the bastion host is made using the parameters provided for
the connection being tunneled, so the bastion host will require the user to exist with the same
name/password/private_key as the targeted remote box.
