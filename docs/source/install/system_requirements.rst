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
