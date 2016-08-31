Installing |bwc|
================

StackStorm is an event-driven DevOps automation platform with all the essential features suitable for small businesses and teams. It’s free and open source under the Apache 2.0 license.

|bwc| (BWC) is the commercial version of the StackStorm automation platform.
BWC adds priority support, advanced features such as fine-tuned access control, LDAP,
and Workflow Designer. To learn more about |bwc|, get an evaluation license,
or request a quote, visit `brocade.com/bwc <http://www.brocade.com/bwc>`_.

To install |bwc| for a quick evaluation, run the commands below on a clean 64bit Linux box,
replacing ``${BWC_LICENSE_KEY}``
with the key you received when registering for evaluation or purchasing BWC.

.. code-block:: bash

  curl -sSL -O https://brocade.com/bwc/install/install.sh && chmod +x install.sh
  ./install.sh --user=st2admin --password=Ch@ngeMe --license=${BWC_LICENSE_KEY}


To understand the details of the installation procedure,
or to install |bwc| manually, follow the installation guide for your Linux version:
:doc:`/install/deb`, :doc:`/install/rhel7`, or :doc:`/install/rhel6`. It will walk you through
installing and configuring components per :doc:`single box reference deployment <overview>`.
The last step of the instructions is "Upgrade to |bwc|".

.. only:: community

    .. include:: /__engage_community.rst

.. only:: enterprise

    .. include:: /__engage_enterprise.rst
