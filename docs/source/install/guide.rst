Installation Guide
===================
This guide provides step-by step instructions on installing StackStorm on a single box per :doc:`Reference deployment </install/overview>` on a Ubuntu/Debian or Redhat/CentOS.

Dependencies
--------------

* Install MongoDB

* Install RabbitMQ

* Install PostgreSQL


Minimal installation
--------------------
Install components
~~~~~~~~~~~~~~~~~~

* update system, set up repositories
* sudo apt-get st2, st2-mistral


check this works...

Configure Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~
Reference deployment uses File Based auth provider for simplicity. To use PAM or LDAP, see :doc:`/authentication`.

check this works...

Configure SSH
~~~~~~~~~~~~~
* SSH, stanley user, SUDO... (instructions, pointer to a script)

check this works...

-----------------


At this point you have a minimal installation, and can happily play with StackStorm, do quickstart, deploy examples (see ) and so on.

But there is no joy without WebUI, no security without SSL termination, no fun without ChatOps, and no money without Enterprise edition. Read on, move on!


-----------------

Install WebUI and configure SSL termination
-------------------------------------------

* install nginx
* generate certificate (instructions, pointer to a script)
* configure nginx - copy files to site-enabled loosly explain what we are doing which is
		* http-https redirect
		* SSL termination and HTTPS
		* serve the client as static content
		* serve API and AUTH off  HTTPS and reverse-proxy them so that less ports and no CORS issues


Set up ChatOps
--------------

* just run docker? The secret there is in upstart script(s)
* Or manual installation, see instructions under :ref:`Chatops Configuration <chatops-configuration>`.


Upgrade to Enterprise Edition
-----------------------------
Enterprise Edition is deployed as an addition on top of StackStorm. Detailed instructions coming up;
meantime if you are an enterprise customer call support and we walk you through.