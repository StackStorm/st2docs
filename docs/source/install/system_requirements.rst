System Requirements
===================

|st2| requires Ubuntu, RHEL or CentOS Linux. It is not supported on any other Linux distributions.
The table below lists the supported Linux versions, along with the Vagrant Boxes and Amazon AWS
instances we use for testing. 

If you are installing from ISO, perform a minimal installation. For Ubuntu, use the "Server"
variant, and only add OpenSSH Server to the base set of packages. All other dependencies will
be automatically added when you install |st2|.

.. note::

  Please note that only 64-bit architecture is supported.


+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Linux (64-bit)                                                                                        | Vagrant Box                                                                  | Amazon AWS AMI                                                                                                                                                    |
+=======================================================================================================+==============================================================================+===================================================================================================================================================================+
| `Ubuntu 14.04 <http://releases.ubuntu.com/trusty/ubuntu-14.04.5-server-amd64.iso>`_                   | `bento/ubuntu-14.04 <https://atlas.hashicorp.com/bento/boxes/ubuntu-14.04>`_ | `Ubuntu Server 14.04 LTS (HVM)  <https://aws.amazon.com/marketplace/pp/B00JV9TBA6/ref=srh_res_product_title?ie=UTF8&sr=0-3&qid=1457037882965>`_                   |
+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `Ubuntu 16.04 <https://www.ubuntu.com/download/server/thank-you?version=16.04.3&architecture=amd64>`_ | `bento/ubuntu-16.04 <https://atlas.hashicorp.com/bento/boxes/ubuntu-16.04>`_ | `Ubuntu 16.04 LTS - Xenial (HVM)  <https://aws.amazon.com/marketplace/pp/B01JBL2M0O/>`_                                                                           |
+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `RHEL 7 <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_ /                 | `bento/centos-7.2 <https://atlas.hashicorp.com/bento/boxes/centos-7.2>`_     | `Red Hat Enterprise Linux (RHEL) 7.2 (HVM)  <https://aws.amazon.com/marketplace/pp/B019NS7T5I/ref=srh_res_product_title?ie=UTF8&sr=0-2&qid=1457037671547>`_       |
| `CentOS 7 <http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1708.iso>`_     |                                                                              |                                                                                                                                                                   |
+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `RHEL 6 <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_ /                 | `bento/centos-6.7 <https://atlas.hashicorp.com/bento/boxes/centos-6.7>`_     | `Red Hat Enterprise Linux (RHEL) 6 (HVM)  <https://aws.amazon.com/marketplace/pp/B00CFQWLS6/ref=srh_res_product_title?ie=UTF8&sr=0-8&qid=1457037733401>`_         |
| `CentOS 6 <http://mirror.centos.org/centos/6/isos/x86_64/>`_                                          |                                                                              |                                                                                                                                                                   |
+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Alternatively, you can use the |st2| Docker image. You will need at least version 1.13.0 of Docker
engine, and optionally ``docker-compose``. See our :doc:`Docker <docker>` guide for more
information.

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
* postgresql (5432)
* st2auth (9100)
* st2api (9101)
* st2stream (9102) 

If any other services are currently using these ports, |st2| may fail to install or run correctly.
