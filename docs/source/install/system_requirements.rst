System Requirements
===================

|st2| requires Ubuntu, RHEL or CentOS Linux. It is not supported on any other Linux distributions.
The table below lists the supported Linux versions, along with the Vagrant Boxes and Amazon AWS
instances we use for testing. See :ref:`below <ref-os-support-policy>` for more details about
our Linux distribution support policy.

If you are installing from ISO, perform a minimal installation. For Ubuntu, use the "Server"
variant, and only add OpenSSH Server to the base set of packages. All other dependencies will
be automatically added when you install |st2|.

.. note::

  Please note that only 64-bit architecture is supported.


+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Linux (64-bit)                                                                                        | Vagrant Box                                                                  | Amazon AWS AMI                                                                                                                                                    |
+=======================================================================================================+==============================================================================+===================================================================================================================================================================+
| `Ubuntu 18.04 <http://cdimage.ubuntu.com/releases/18.04.2/release/ubuntu-18.04.2-server-amd64.iso>`_  | `bento/ubuntu-18.04 <https://app.vagrantup.com/bento/boxes/ubuntu-18.04>`_   | `Ubuntu Server 18.04 LTS Bionic  <https://aws.amazon.com/marketplace/pp/B07CQ33QKV/>`_                                                                            |
+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `Ubuntu 20.04 <http://releases.ubuntu.com/focal/ubuntu-20.04.2-live-server-amd64.iso>`_               | `bento/ubuntu-20.04 <https://app.vagrantup.com/bento/boxes/ubuntu-20.04>`_   | `Ubuntu Server 20.04 LTS Focal  <https://aws.amazon.com/marketplace/pp/B087QQNGF1>`_                                                                              |
+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `RHEL 8 <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_ /                 | `bento/centos-8.2 <https://app.vagrantup.com/bento/boxes/centos-8.2>`_       | `Red Hat Enterprise Linux (RHEL) 8 (HVM)  <https://aws.amazon.com/marketplace/pp/B07T4SQ5RZ?qid=1581005023484&sr=0-5&ref_=brs_res_product_title>`_                |
| `CentOS 8.2 <http://mirrors.rit.edu/centos/8.2.2004/isos/x86_64/>`_                                   |                                                                              |                                                                                                                                                                   |
+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `RHEL 7 <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_ /                 | `bento/centos-7.4 <https://app.vagrantup.com/bento/boxes/centos-7.4>`_       | `Red Hat Enterprise Linux (RHEL) 7.2 (HVM)  <https://aws.amazon.com/marketplace/pp/B019NS7T5I/ref=srh_res_product_title?ie=UTF8&sr=0-2&qid=1457037671547>`_       |
| `CentOS 7 <http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1708.iso>`_     |                                                                              |                                                                                                                                                                   |
+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+

This is the recommended minimum sizing for testing and deploying |st2|:

+--------------------------------------+-----------------------------------+
|            Testing                   |         Production                |
+======================================+===================================+
|  * Dual CPU                          | * Quad core CPU                   |
|  * 2GB RAM                           | * >16GB RAM                       |
|  * 10GB storage                      | * 40GB storage                    |
|  * Recommended EC2: **t2.medium**    | * Recommended EC2: **m4.xlarge**  |
+--------------------------------------+-----------------------------------+

.. note::

  If you are planning to add the `DC Fabric Automation Suite <https://ewc-docs.extremenetworks.com/solutions/dcfabric/>`_
  to your system later, you will need additional RAM. Check the `DC Fabric Automation Suite System Requirements
  <https://ewc-docs.extremenetworks.com/solutions/dcfabric/install.html#system-requirements>`_

If you split your filesystem into multiple partitions and mount points, ensure you have at least
1GB of free space in ``/var`` and ``/opt``. RabbitMQ and MongoDB may not operate correctly without
sufficient free space.

By default, |st2| and related services use these TCP ports:

* nginx (80, 443)
* mongodb (27017)
* rabbitmq (4369, 5672, 25672)
* redis (6379) or zookeeper (2181, 2888, 3888)
* st2auth (9100)
* st2api (9101)
* st2stream (9102)

If any other services are currently using these ports, |st2| may fail to install or run correctly.

.. _ref-os-support-policy:

Linux Distribution Support Policy
---------------------------------

StackStorm only support Ubuntu and RHEL/CentOS Linux distributions. In general, it is supported
on the two most recent major supported releases for those distributions. Specifically:

* **Ubuntu**: Current LTS releases are supported. Today this is ``18.04`` and ``20.04``.

* **RHEL/CentOS**: We currently support RHEL/CentOS ``7.x`` and ``8.x``. In general, we recommend using
  the most recent version in that series, but any version may be used.

  Support for RHEL/CentOS ``6.x`` has been removed. |st2| 3.2  is the last release that supported RHEL/CentOS ``6.x``.

  Support for Ubuntu ``16.04`` has been removed. |st2| 3.4  is the last release that supported RHEL/CentOS ``16.04``.
