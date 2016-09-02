Installation
============

That's OK! You're busy, we get it. How do you just get started? Get yourself a clean 64-bit Linux
box that fits the :doc:`system requirements <system_requirements>`. Make sure that ``curl`` is up to date
using ``sudo apt-get install curl`` on Ubuntu, or ``sudo yum install curl nss`` on RHEL/CentOS. Then run
this command:

.. code-block:: bash

   curl -sSL https://stackstorm.com/packages/install.sh | bash -s -- --user=st2admin --password=Ch@ngeMe

It will install and configure the stable version of StackStorm, as per the
:doc:`single host reference deployment <./overview>`.
The installation takes about 4 minutes.
Once it completes successfully, you will see the following output:

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

.. rubric:: Installations

.. toctree::
    :maxdepth: 1

    Reference Deployment Overview <overview>
    system_requirements
    Ubuntu (Trusty) <deb>
    RHEL 7 / CentOS 7 <rhel7>
    RHEL 6 / CentOS 6 <rhel6>
    Brocade Workflow Composer <bwc>
    config/index
    upgrades

