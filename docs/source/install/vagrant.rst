Vagrant & Virtual Appliance
============================
Vagrant / OVA is a quick and easy way to try |st2| in a VM.

It's already pre-installed, configured and tested virtual machine image and so saves time avoiding
time-consuming installation and configuration steps. Perfect for a quick platform overview,
testing, demo or even using |st2| in isolated from the internet air-gapped systems.

We highly recommend using a Vagrant box to get familiar with the |st2| platform.

.. contents:: Contents
   :local:

The source code is available as a GitHub repo:
`StackStorm/packer-st2 <https://github.com/StackStorm/packer-st2>`_

---------------------------

Requirements
------------
`Virtualbox <https://www.virtualbox.org/>`_ is required along with `Vagrant <https://www.vagrantup.com/>`_
when it's used. If you're not familiar with Vagrant, we recommend looking at `Introduction to Vagrant <https://www.vagrantup.com/intro/index.html>`_.

Vagrant Quick Start
-------------------
Starting a |st2| Vagrant VM is easy:

.. code-block:: bash

  vagrant init stackstorm/st2
  vagrant up
  vagrant ssh

This will boot up a fresh |st2| installation along with the Mistral workflow engine on Ubuntu 16.04 LTS.
You can access Web UI at ``https://10.10.10.10/`` or SSH to the box ``vagrant ssh`` if you prefer st2 CLI.

Virtual Appliance / OVA
-----------------------
As alternative to Vagrant box is Virtual appliance which is available for download as ``.OVA``
image from the `StackStorm/packer-st2 Github Releases <https://github.com/StackStorm/packer-st2/releases>`_
page. It might be especially helpful for the isolated from the internet air-gapped environments.

.. note::

  | *Linux login credentials:*
  | Username: ``vagrant``
  | Password: ``vagrant``
  |
  | *StackStorm login details:*
  | Username: ``st2admin``
  | Password: ``Ch@ngeMe``

.. warning::

    If using OVA in production environment, don't forget to change the default credentials
    and delete SSH authorized keys for ``vagrant`` linux user.


At the moment only Virtualbox provider is supported. VMWare-compatible virtual appliance is
available with `StackStorm Enterprise (EWC) <https://stackstorm.com/#product>`_ image.
Ask `StackStorm Support <support@stackstorm.com>`_ for more info.


Tips & Tricks
-------------
Updating the Vagrant box
~~~~~~~~~~~~~~~~~~~~~~~~
Once the newer box version is released, Vagrant will warn you about the available update.
To update the box:

.. code-block:: bash

    vagrant box outdated
    vagrant box remove stackstorm/st2
    vagrant up


Pinning the Vagrant box version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Whether you want to pin |st2|, it's possible to use specific box version.
While adding the box for the first time:

.. code-block:: bash

    vagrant init stackstorm/st2 --box-version 2.7.1-20180507
    vagrant up

Or directly in ``Vagrantfile``:

.. code-block:: ruby

    Vagrant.configure("2") do |config|
      config.vm.box = "stackstorm/st2"
      config.vm.box_version = "2.7.1-20180507"
    end

The list of available box versions can be found at `Vagrant Cloud <https://app.vagrantup.com/stackstorm/boxes/st2>`_.

Debugging
---------
st2-integration-tests
~~~~~~~~~~~~~~~~~~~~~
Sometimes |st2| does not run properly for some reason.

Discovering why at a infra level is the responsibility of ``st2-integration-tests`` which will
perform |st2| infrastructure/integration tests and report back with more detailed info.
This can save time for both you & community to avoid extensive troubleshooting steps.

If something went wrong, - just run ``st2-integration-tests``

Bugs & Issues & Contributions
-----------------------------
The source code is available as a GitHub repo:
`StackStorm/packer-st2 <https://github.com/StackStorm/packer-st2>`_.
We're welcoming your bug reports, feature requests or even better, - pull requests.
