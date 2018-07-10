Windows Runners Configuration
=============================

.. include:: /_includes/__windows_runners_deprecation_notice.rst

Pre-requisites
--------------

The server which is running the action runner service used for executing Windows runners actions
needs to have the following dependencies installed:

* ``smbclient`` >= 4.1 - Command line Samba client (``smbclient`` package on
  Ubuntu and ``samba-client`` package on Fedora).
* ``winexe`` >= 1.1 - Command line tool for executing commands remotely on
  Windows hosts.

Samba client is available in standard APT and Yum repositories. To install it on Ubuntu, run:

.. sourcecode:: bash

    sudo apt-get install smbclient

To install on RHEL/CentOS, run:

.. sourcecode:: bash

    sudo yum install samba-client

``winexe`` is not distributed in normal RHEL/Ubuntu package repositories. You will need to compile it yourself,
or obtain a pre-built binary.

* **Ubuntu**: Instructions and binary packages for 14.04 and 16.04 are available `here <https://doublefault0.wordpress.com/2017/02/21/winexe-1-1-ubuntu-16-04/>`_.

* **RHEL/CentOS**:  `These instructions <https://github.com/beardedeagle/winexe-rpm>`_ explain how to build RPMs for RHEL/CentOS systems.

Supported Windows Versions
--------------------------

Windows runners have been tested on the following versions of Windows:

* Windows Server 2008
* Windows Server 2012

The underlying library we use to talk to the Windows hosts also supports other versions
(2000/XP/2003/Vista), but we haven't tested our runners with those versions, so we can't guarantee
it will work.

Configuring your Window Server for Remote Access
------------------------------------------------

For |st2| to be able to run actions on your Windows servers, you need to configure them as
described below.

Configuring the Firewall
~~~~~~~~~~~~~~~~~~~~~~~~

For |st2| to be able to reach your server, you need to configure Windows Firewall to allow traffic
from the server where |st2| components (notably action runner service) are running.

For safety reasons, you are encouraged to only allow traffic from your |st2| server, but if you
want to allow traffic from all IPs, you can run this command:

.. sourcecode:: none

    netsh firewall set service RemoteAdmin enable

Configuring the Administrator User Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|st2| requires an administrator account on the Windows host where the actions are executed to be
able to upload and run the scripts there. By default, it tries to use ``Administrator`` account to
log in to your server.

Configuring the File Share
~~~~~~~~~~~~~~~~~~~~~~~~~~

Windows script runner needs to upload a local PowerShell script to the remote server before it can
run it. For this to work, file sharing service (SMB - Samba) needs to be enabled and you need to
configure your firewall to allow traffic from the |st2| IPs to the file sharing service ports.

In addition to that, you need to create a share where |st2| can upload the script files. By
default, |st2| tries to upload files to a share named ``C$``. If this share is not available or
you want to use a different share, you need to specify the ``share`` parameter when running a
Windows script runner action.

Configuring PowerShell
~~~~~~~~~~~~~~~~~~~~~~
* Set the PowerShell execution policy to allow execution of the scripts. See
  <https://technet.microsoft.com/en-us/library/ee176961.aspx>
* Ensure that default ``powershell.exe`` is compatible with the script you are planning to run. To
  do so, open PowerShell and run this command:

.. sourcecode:: none

  PS C:\> $PSVersionTable
  Name                           Value
  ----                           -----
  PSVersion                      4.0
  ...


Additional Resources and Links
------------------------------

* `Enable or Disable the File and Printer Sharing Firewall Rule
  <https://technet.microsoft.com/en-us/library/cc737069(v=ws.10).aspx>`_
* `Enable or Disable the Remote Desktop Firewall Rule
  <https://technet.microsoft.com/en-us/library/cc736451(v=ws.10).aspx>`_

.. include:: /__engage_community.rst
