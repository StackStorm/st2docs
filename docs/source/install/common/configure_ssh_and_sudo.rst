To run local and remote shell actions, |st2| uses a special system user (by default ``stanley``).
For remote Linux actions, SSH is used. We recommend configuring public key-based SSH access on all
remote hosts. We also recommend configuring SSH access to localhost for running examples and
testing.

* Create |st2| system user, enable passwordless sudo, and set up ssh access to "localhost" so
  that SSH-based actions can be tested locally. You will need elevated privileges to do this:

  .. code-block:: bash

    # Create an SSH system user (default `stanley` user may already exist)
    sudo useradd stanley
    sudo mkdir -p /home/stanley/.ssh
    sudo chmod 0700 /home/stanley/.ssh

    # Generate ssh keys
    sudo ssh-keygen -f /home/stanley/.ssh/stanley_rsa -P ""

    # Authorize key-based access
    sudo sh -c 'cat /home/stanley/.ssh/stanley_rsa.pub >> /home/stanley/.ssh/authorized_keys'
    sudo chown -R stanley:stanley /home/stanley/.ssh

    # Enable passwordless sudo
    sudo sh -c 'echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2'
    sudo chmod 0440 /etc/sudoers.d/st2

    # Make sure `Defaults requiretty` is disabled in `/etc/sudoers`
    sudo sed -i -r "s/^Defaults\s+\+?requiretty/# Defaults +requiretty/g" /etc/sudoers

* Configure SSH access and enable passwordless sudo on the remote hosts which |st2| will be running
  remote actions on via SSH. Using the public key generated in the previous step, follow the
  instructions at :ref:`config-configure-ssh`. To control Windows boxes, configure access for
  :doc:`Windows runners </install/config/winrm_runners>`.

* If you are using a different user, or path to their SSH key, you will need to change this
  section in ``/etc/st2/st2.conf``:

  .. sourcecode:: ini

    [system_user]
    user = stanley
    ssh_key_file = /home/stanley/.ssh/stanley_rsa
