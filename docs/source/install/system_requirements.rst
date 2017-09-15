System Requirements
===================

|st2| requires Ubuntu, RHEL or CentOS. The table below lists the supported
Linux versions, along with Vagrant Boxes and Amazon AWS instances we use for
testing. Yes, using exactly the same boxes will improve your experience.

+-------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Linux (64 bit)    | Vagrant Box                                                                  | Amazon AWS AMI                                                                                                                                                    |
+===================+==============================================================================+===================================================================================================================================================================+
| Ubuntu 14.04      | `bento/ubuntu-14.04 <https://atlas.hashicorp.com/bento/boxes/ubuntu-14.04>`_ | `Ubuntu Server 14.04 LTS (HVM)  <https://aws.amazon.com/marketplace/pp/B00JV9TBA6/ref=srh_res_product_title?ie=UTF8&sr=0-3&qid=1457037882965>`_                   |
+-------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Ubuntu 16.04      | `bento/ubuntu-16.04 <https://atlas.hashicorp.com/bento/boxes/ubuntu-16.04>`_ | `Ubuntu 16.04 LTS - Xenial (HVM)  <https://aws.amazon.com/marketplace/pp/B01JBL2M0O/>`_                                                                           |
+-------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| RHEL 7 / CentOS 7 | `bento/centos-7.2 <https://atlas.hashicorp.com/bento/boxes/centos-7.2>`_     | `Red Hat Enterprise Linux (RHEL) 7.2 (HVM)  <https://aws.amazon.com/marketplace/pp/B019NS7T5I/ref=srh_res_product_title?ie=UTF8&sr=0-2&qid=1457037671547>`_       |
+-------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| RHEL 6 / CentOS 6 | `bento/centos-6.7 <https://atlas.hashicorp.com/bento/boxes/centos-6.7>`_     | `Red Hat Enterprise Linux (RHEL) 6 (HVM)  <https://aws.amazon.com/marketplace/pp/B00CFQWLS6/ref=srh_res_product_title?ie=UTF8&sr=0-8&qid=1457037733401>`_         |
+-------------------+------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Alternatively, you can use the |st2| Docker image. You will need at least version 1.13.0 of
``docker-compose`` and Docker engine. See our :doc:`Docker Image <docker>` guide for more information.

.. include:: __64bit_note.rst

While the system can operate with lower specs, these are the recommendations
for the best experience while testing or deploying |st2|:

+--------------------------------------+-----------------------------------+
|            Testing                   |         Production                |
+======================================+===================================+
|  * Dual CPU system                   | * Quad core CPU system            |
|  * 2GB RAM                           | * >16GB RAM                       |
|  * 10GB storage                      | * 40GB storage                    |
|  * Recommended EC2: **t2.medium**    | * Recommended EC2: **m4.xlarge**  |
+--------------------------------------+-----------------------------------+

If you split your filesystem into multiple partitions and mount points, ensure you
have at least 1GB of free space in ``/var`` and ``/opt``. RabbitMQ and MongoDB may not
operate correctly without sufficient free space. 

By default, |st2| and related services use these ports: nginx (80, 443), mongodb (27017), rabbitmq (4369, 5672, 25672), postgresql (5432) and st2 (9100-9102). If any other services are currently using these ports, |st2| may fail to install or run correctly.
