System Requirements
===================

|st2| requires Ubuntu, RHEL or RockyLinux Linux. It is not supported on any other Linux distributions.
The table below lists the supported Linux versions, along with the Vagrant Boxes and Amazon AWS
instances we use for testing. See :ref:`below <ref-os-support-policy>` for more details about
our Linux distribution support policy.

If you are installing from ISO, perform a minimal installation. For Ubuntu, use the "Server"
variant, and only add OpenSSH Server to the base set of packages. All other dependencies will
be automatically added when you install |st2|.

.. note::

  Please note that only 64-bit architecture is supported.


+-----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------+
| Linux (64-bit)                                                                                            | Vagrant Box                                                                               | Amazon AWS AMI                                                                                                |
+===========================================================================================================+===========================================================================================+===============================================================================================================+
| `Ubuntu 20.04 <http://releases.ubuntu.com/focal/ubuntu-20.04.2-live-server-amd64.iso>`_                   | `ubuntu/focal64 <https://portal.cloud.hashicorp.com/vagrant/discover/ubuntu/focal64>`_    | `Ubuntu Server 20.04 LTS Focal  <https://aws.amazon.com/marketplace/pp/prodview-iftkyuwv2sjxi>`_              |
+-----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------+
| `Ubuntu 22.04 <http://releases.ubuntu.com/jammy/ubuntu-22.04.5-live-server-amd64.iso>`_                   | `ubuntu/jammy64 <https://portal.cloud.hashicorp.com/vagrant/discover/ubuntu/jammy64>`_    | `Ubuntu 22.04 LTS - Jammy  <https://aws.amazon.com/marketplace/pp/prodview-f2if34z3a4e3i>`_                   |
+-----------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
| `RHEL 8 <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_ /                     | `rockylinux/8 <https://portal.cloud.hashicorp.com/vagrant/discover/rockylinux/8>`_        | `Red Hat Enterprise Linux (RHEL) 8 (HVM)  <https://aws.amazon.com/marketplace/pp/prodview-kv5mi3ksb2mma>`_    |
| `RockyLinux 8 <https://download.rockylinux.org/pub/rocky/8/isos/x86_64/Rocky-8.10-x86_64-minimal.iso>`_   |                                                                                           |                                                                                                               |
+-----------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
| `RHEL 9 <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_ /                     | `rockylinux/9 <https://portal.cloud.hashicorp.com/vagrant/discover/rockylinux/9>`_        | `Red Hat Enterprise Linux 9 (HVM)  <https://aws.amazon.com/marketplace/pp/prodview-b5psjqk4f5f3k>`_           |
| `RockyLinux 9 <https://download.rockylinux.org/pub/rocky/9/isos/x86_64/Rocky-9.4-x86_64-minimal.iso>`_    |                                                                                           |                                                                                                               |
+-----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------+

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

StackStorm only support Ubuntu and RHEL/RockyLinux/CentOS Linux distributions. In general, it is supported
on the two most recent major supported releases for those distributions. Specifically:

* **Ubuntu**: Current LTS releases are supported.  Today this is ``20.04`` and ``22.04``.

* **RHEL/Rocky**: We currently support RHEL/RockyLinux ``8.x`` and RHEL/RockyLinux ``9.x``. In general, we recommend using
  the most recent version in that series, but any version may be used.
  |st2| is verified on RHEL/RockyLinux distributions, but our RPMs should be compatible with other binary compatible derivatives, e.g. CentOS 8 Stream.
