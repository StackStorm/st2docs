SSH Troubleshooting
===================

|st2| remote actions use the ``system_user`` and ``ssh_key_file`` specified in the configuration
file (``/etc/st2/st2.conf``) to authenticate to remote boxes. The default username is ``stanley``,
and the default ``ssh_key_file`` is ``/home/stanley/.ssh/stanley_rsa``.

This can be changed by modifying these values in ``/etc/st2/st2.conf``.

In case of key compromise occurring, revoking the public key for ``system_user`` from target boxes will
revoke access for |st2|. 

.. note::

  If you are changing ``system_user`` or ``ssh_key_file`` configuration values in
  ``/etc/st2/st2.conf``, you must restart |st2| for your changes to take effect. You can just
  restart the st2actionrunner component, e.g. ``sudo service st2actionrunner restart``.

To validate remote actions are working correctly, you can use the following command:

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

If you don't have the right SSH key file, you will see an error and the action will fail:

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

By default, all actions that use remote commands or scripts will use this username and private_key
combination.

If you are not using the default SSH port 22, you can specify the port as part of the host string
in the hosts list, e.g. ``hosts=localhost:55,st2build001:56``. As of |st2| version 2.1, you can also
specify custom ports via an SSH config file.

To use an SSH config file, setup ``/home/stanley/.ssh/config`` for user ``stanley`` on the |st2| action
runner boxes, and add the following configuration lines in ``/etc/st2/st2.conf``:

.. code-block:: ini

  [ssh_runner]
  use_ssh_config = True
  ssh_config_file_path = /home/stanley/.ssh/config

Make sure your ssh config is in the same account as user running the st2actionrunner process. If root is running 
st2actionrunner install it under ``/root/.ssh``. Wherever it is installed, make sure the config and identity files
have proper permissions and ownership, or ``ssh`` will refuse to read them.
 
.. code-block:: bash

  chown -R stanley:stanley /home/stanley/.ssh/*
  chmod 600 /home/stanley/.ssh/config
  chmod 600 /home/stanley/.ssh/id_rsa

If you are using--or planning to use--bastion forwarding to get to target hosts in your network, then you either
need to pass the ``bastion_host`` parameter to each action, or configure ssh to automatically use bastion forwarding.
In the latter case, you to validate that your ssh config file(s) are valid and they include the appropriate
``IdentityFile`` definitions. For example, consider this ssh config file with different ssh keys for the bastion and the
target hosts (``10.1.*`` in our example). This allows SSH to resolve automatically the correct keys based on hostname.

.. code-block:: ini

  Host 10.1.*
    ProxyCommand ssh -o StrictHostKeyChecking=no bastion nc %h %p
    IdentityFile ~/.ssh/id_rsa
    User stanley

  Host bastion
    Hostname bastion.example.com
    IdentityFile ~/.ssh/bastion_rsa
    User stanley

Example output of a successful setup that does not require the ``bastion_host`` parameter.

.. code-block:: bash

  $st2 run core.remote cmd=whoami hosts=10.1.1.2
  .
  id: 5e668e4a811a07014b1c48bd
  status: succeeded
  parameters: 
  cmd: whoami
  hosts: 10.1.1.2:
  result: 
    10.1.1.2:
    failed: false
    return_code: 0
    stderr: ''
    stdout: stanley
    succeeded: true

We do not recommend running actions as arbitrary user + private_key combinations. This
would require you to setup private_key for the users on |st2| action runner boxes and
the public keys of the users in target boxes. This increases the risk surface area and
is discouraged.

However, if you have st2client installed and you want to run one-off commands on the remote
boxes as a different user, you can use:

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

For the above example to work, the key file ``/home/stanley/ssh_keys/.ssh/id_rsa`` has to be
available on the action runner boxes. We also support ``password`` as a parameter. As of version 2.1,
you can also specify custom keys for hosts via SSH config file. A sample SSH config is shown below:

.. code-block:: ini

    Host st2-ssh-test001
      User lakshmi
      IdentityFile /home/vagrant/.ssh/lakshmi_id_rsa

    Host *secret-box
      port 55

If you are running remote actions as ``sudo``, pseudo tty is enabled by default. This means
that ``stdout`` and ``stderr`` streams get combined into one and reported as ``stdout``.

When using a bastion host for running remote actions, the bastion host must have ``AllowTcpForwarding``
enabled. Additionally, the connection to the bastion host is made using the parameters provided for
the connection being tunneled, so the bastion host will require the user to exist with the same
name/password/private_key as the targeted remote box.
