WinRM Runners Configuration
===========================

.. note::

  WinRM runners are currently in beta which means there might be rough edges and things might
  break.

  If you do encounter an issue, please get in touch and we will do our best to assist you.

Supported Windows Versions
--------------------------

WinRM runners have been tested on the following versions of Windows:

* Windows Server 2008
* Windows Server 2012
* Windows Server 2016

The underlying library, `pywinrm <https://github.com/diyan/pywinrm>`_, we use to talk to the
Windows hosts should work with other versions (2000/XP/2003/Vista/8/10), but we haven't tested
our runners with those versions, so we can't guarantee it will work.

Support Authentication Transports
------------------------------------------------

The `pywinrm <https://github.com/diyan/pywinrm>`_ library supports a variety of different
`transport options <https://github.com/diyan/pywinrm/#valid-transport-options>`_.
Currently the only supported transports are:

* ``basic``
* ``plaintext``
* ``ntlm``

Other transport mechanisms required system-level configuration on the |st2| host and
potentially also on the Windows host. Support for additional transports may be added
in the future.

Configuring your Window Server for Remote Access
------------------------------------------------

For |st2| to be able to run actions on your Windows servers, you need to configure WinRM
by executing the `ConfigureRemotingForAnsible.ps1 <https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1>`_
script from the Ansible project. This script enables WinRM, configures the firewall,
and generates an SSL certificate.

.. sourcecode:: none

   # download the script (feel free to download it manually, if you like)
   (New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1', './ConfigureRemotingForAnsible.ps1')
   
   # execute the script
   ./ConfigureRemotingForAnsible.ps1


We recommend executing this script on your Windows templates, that way WinRM is configured
and available immediately when a new VM is cloned.

.. include:: /__engage_community.rst
