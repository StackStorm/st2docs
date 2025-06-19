Installation
============

That's OK! You're busy, we get it. How do you just get started? Get yourself a **clean** 64-bit Linux
box that fits the :doc:`system requirements <system_requirements>`. Make sure that ``curl`` is up to date
using ``sudo apt-get install curl`` on Ubuntu, or ``sudo yum install curl nss`` on RHEL/CentOS. Then run
this command:

.. code-block:: bash

   curl -sSL https://stackstorm.com/packages/v2.3/install.sh | bash -s -- --user=st2admin --password='Ch@ngeMe'

.. danger::

  The installation script is an opinionated installation of |st2|. It assumes that you have a clean, basic
  installation of Ubuntu or RHEL/CentOS, similar to what you get with a basic installation from ISO. If
  you are trying to install |st2| on a server with other applications running, you may run into problems.

  The same applies for VMs that are built from special 'templates' provided by your IT department.
  If they have customised $HOME locations, or changed default authentication methods, then the script may
  break. Don't worry though! Scroll down for the manual instructions for your specific OS. Follow those,
  with any site-specific modifications you need.
  
  The script itself is not idempotent. If you try to re-run the script on top of a failed installation, it
  will almost certainly fail. Start again with a clean system, or switch to a manual install.

It will install and configure the stable version of StackStorm, as per the
:doc:`single host reference deployment <./overview>`. The installation takes about 4 minutes. Once it
completes successfully, you will see the following output:

::

  For more information, please refer to documentation at
  https://docs.stackstorm.com/install/deb.html#setup-chatops
  ########################################################


  ███████╗████████╗██████╗      ██████╗ ██╗  ██╗
  ██╔════╝╚══██╔══╝╚════██╗    ██╔═══██╗██║ ██╔╝
  ███████╗   ██║    █████╔╝    ██║   ██║█████╔╝
  ╚════██║   ██║   ██╔═══╝     ██║   ██║██╔═██╗
  ███████║   ██║   ███████╗    ╚██████╔╝██║  ██╗
  ╚══════╝   ╚═╝   ╚══════╝     ╚═════╝ ╚═╝  ╚═╝

    st2 is installed and ready to use.

  Head to https://YOUR_HOST_IP/ to access the WebUI

  Don't forget to dive into our documentation! Here are some resources
  for you:

  * Documentation  - https://docs.stackstorm.com
  * Knowledge Base - https://stackstorm.reamaze.com

  Thanks for installing StackStorm! Come visit us in our Slack Channel
  and tell us how it's going. We'd love to hear from you!

.. include:: __installer_passwords.rst

If you want to install |st2| on a host that does not have Internet access,
`this guide <https://stackstorm.com/2017/02/10/installing-stackstorm-offline-systems/>`_
shows how to do it using a mirror. 

If you have problems accessing the Web UI on a RHEL 7/CentOS 7 system, check the
:ref:`system firewall settings <ref-rhel7-firewall>`.

.. rubric:: Installations

For more detail on reference deployments, or OS-specific manual installation instructions, see below:

.. toctree::
    :maxdepth: 1

    Reference Deployment Overview <overview>
    system_requirements
    Ubuntu 14.04 / 16.04 <deb>
    RHEL 7 / CentOS 7 <rhel7>
    RHEL 6 / CentOS 6 <rhel6>
    Ansible Playbooks <ansible>
    Brocade Workflow Composer <bwc>
    config/index
    upgrades
