Installing |bwc|
================

StackStorm is an event-driven DevOps automation platform with all the essential features suitable
for small businesses and teams. It’s free and open source under the Apache 2.0 license.

|bwc| (BWC) is the commercial version of the StackStorm automation platform. BWC adds priority
support, advanced features such as fine-tuned access control, LDAP, and Workflow Designer. To
learn more about |bwc|, get an evaluation license, or request a quote, visit `brocade.com/bwc
<http://www.brocade.com/bwc>`_.

You can also add Brocade Network Automation Suites on top of a |bwc| system. See
`bwc-docs.brocade.com/solutions/overview.html <https://bwc-docs.brocade.com/solutions/overview.html>`_
to learn more.

To install |bwc| for a quick evaluation, run the commands below on a clean 64-bit Linux box that
meets the :doc:`/install/system_requirements`. Replace ``${BWC_LICENSE_KEY}`` with the key you
received when registering for evaluation or purchasing BWC.

.. code-block:: bash

  curl -sSL -O https://brocade.com/bwc/install/install.sh && chmod +x install.sh
  ./install.sh --user=st2admin --password='Ch@ngeMe' --license=${BWC_LICENSE_KEY}

Already have a working StackStorm system, and want to add |bwc|? No problem! No need to install a
new system. You can install |bwc| on top of your existing system. Just run these commands, again
replacing ``${BWC_LICENSE_KEY}`` with the license key you received when registering:

* On Ubuntu systems:

  .. code-block:: bash

    # Set up Brocade Workflow Composer repository access
    curl -s https://${BWC_LICENSE_KEY}:@packagecloud.io/install/repositories/StackStorm/enterprise/script.deb.sh | sudo bash
    # Install Brocade Workflow Composer
    sudo apt-get install -y bwc-enterprise


* On RedHat/CentOS systems:

  .. code-block:: bash

    # Set up Brocade Workflow Composer repository access
    curl -s https://${BWC_LICENSE_KEY}:@packagecloud.io/install/repositories/StackStorm/enterprise/script.rpm.sh | sudo bash
    # Install Brocade Workflow Composer
    sudo yum install -y bwc-enterprise

To understand the full details of the installation procedure, or to install |bwc| manually, follow
the installation guide for your Linux version: :doc:`/install/deb`, :doc:`/install/rhel7`, or
:doc:`/install/rhel6`. It will walk you through installing and configuring StackStorm and |bwc|.
The last step of the instructions is "Upgrade to |bwc|".

.. only:: community

    .. include:: /__engage_community.rst

.. only:: enterprise

    .. include:: /__engage_enterprise.rst
