Puppet Module
=============

If you're ready to take complete control of your StackStorm instances, then the ``stackstorm-st2``
Puppet module is for you! It offers repeatable, configurable, and idempotent
production-friendly StackStorm installations.

The ``stackstorm-st2`` Puppet module is available on Puppet Forge:
`stackstorm-st2 <https://forge.puppet.com/stackstorm/st2>`_

Source code for the module is available as a GitHub repo:
`StackStorm/puppet-st2 <https://github.com/stackstorm/puppet-st2/>`_

.. note::

    This puppet module only supports the open source version of StackStorm. Please contact
    enterprise support if you want more info on using puppet module to install
    Extreme Workflow Composer (EWC).

.. contents:: Contents
   :local:

---------------------------

Supported Platforms
-------------------

The Puppet module supports the same platforms as manual installation, i.e.:

* Ubuntu Trusty (14.04)
* Ubuntu Xenial (16.04)
* RHEL 6/CentOS 6
* RHEL 7/CentOS 7

The same system size :doc:`requirements </install/system_requirements>` also apply.

Quick Start
-----------

The first step is installing Puppet, for this please consult the
`official Puppet installation documentation <https://puppet.com/docs/puppet/latest/install_linux.html>`_

.. note::

  Puppet versions <= 3.x are no longer supported. Please utilize Puppet >= 4.

To get started with a single node deployment, and default configuration settings,
we're going to install the ``stackstorm-st2`` module and its dependencies, then
tell Puppet to perform a full install of StackStorm. In order to accomplish this,
run the following commands as ``root``:

.. code-block:: bash

  puppet module install stackstorm-st2
  puppet apply -e "include ::st2::profile::fullinstall"

.. note::

    The default StackStorm login credentials according to https://github.com/StackStorm/puppet-st2/blob/master/manifests/params.pp are: ``st2admin:Ch@ngeMe``. Don't forget to change them.


Classes
-------

``::st2::profile::fullinstall`` is the quick and easy way to get StackStorm up
and running. The ``stackstorm-st2`` module provides numerous additional classes
in order to configure StackStorm just the way you like it. Below is a list of
classes available for configuration:


- ``::st2`` - The main configuration point for the StackStorm installation.
- ``::st2::profile::client`` - Profile to install all client libraries for StackStorm
- ``::st2::profile::fullinstall`` - Full installation of StackStorm and dependencies
- ``::st2::profile::mistral`` - Install of OpenStack Mistral
- ``::st2::profile::mongodb`` - StackStorm configured MongoDB installation
- ``::st2::profile::nodejs`` - StackStorm configured NodeJS installation
- ``::st2::profile::python`` - Python installed and configured for StackStorm
- ``::st2::profile::rabbitmq`` - StackStorm configured RabbitMQ installation
- ``::st2::proflle::server`` - StackStorm server components
- ``::st2::profile::web`` - StackStorm WebUI components
- ``::st2::profile::chatops`` - StackStorm chatops components


Resource Types
--------------

Along with the configuration classes, there are a number of defined resources
provided that allow installation and configuration of StackStorm's components.

- ``::st2::auth_user`` - Configures a user (and password) in ``flat_file`` auth
- ``::st2::kv`` - Defines a key/value pair in the StackStorm datastore
- ``::st2::pack`` - Installs and configures a StackStorm pack
- ``::st2::user`` - Configures a system-level (linux) user and SSH keys

Installing and Configuring Packs
--------------------------------

StackStorm packs can be installed and configured directly from Puppet. This can
be done via the ``::st2::pack`` and ``st2::pack::config`` defined types.

Installation/Configuration via Manifest:

.. code-block:: puppet

  # install pack from the exchange
  st2::pack { 'linux': }

  # install pack from a git URL
  st2::pack { 'private':
    repo_url => 'https://private.domain.tld/git/stackstorm-private.git',
  }

  # install pack and apply configuration
  st2::pack { 'slack':
    config   => {
      'post_message_action' => {
        'webhook_url' => 'XXX',
      },
    },
  }

Installation/Configuration via Hiera:

.. code-block:: yaml

  st2::packs:
    linux:
      ensure: present
    private:
      ensure: present
      repo_url: https://private.domain.tld/git/stackstorm-private.git
    slack:
      ensure: present
      config:
        post_message_action:
          webhook_url: XXX

Configuring Authentication
--------------------------

StackStorm uses a pluggable authentication system where authentication is delegated to an
external service called a "backend". The ``st2auth`` service can be configured
to use various backends. Note only one is active at any one time. For more information on StackStorm
authentication see the :doc:`authentication documentation </authentication>`.

The following backends are currently available:

- ``flat_file`` - Authenticates against an htpasswd file (default). See the `flat-file backend documentation <https://github.com/StackStorm/st2-auth-backend-flat-file>`_
- ``keystone`` - Authenticates against an OpenStack Keystone service See the `keystone backend documentation <https://github.com/StackStorm/st2-auth-backend-keystone>`_
- ``ldap`` - Authenticates against an LDAP server such as OpenLDAP or Active Directory . See the `LDAP backend documentation <https://github.com/StackStorm/st2-auth-backend-ldap>`_
- ``mongodb`` - Authenticates against a collection named users in MongoDB. See the `MongoDB backend <https://github.com/StackStorm/st2-auth-backend-mongodb>`_
- ``pam`` - Authenticates against the PAM Linux service. See the `PAM backend documentation <https://github.com/StackStorm/st2-auth-backend-pam>`_

By default the ``flat_file`` backend is used. To change this you can configure
it when instantiating the ``::st2`` class in a manifest file:

Configuration via Manifest:

.. code-block:: puppet

  class { '::st2':
    auth_backend => 'ldap',
  }


Configuration via Hiera:

.. code-block:: yaml

  st2::auth_backend: ldap

Each backend has their own custom configuration settings. The settings can be
found by looking at the backend class in the ``manifests/st2/auth/`` directory.
These parameters map 1-for-1 to the configuration options defined in each backend's
GitHub page (links above). Backend configurations are passed in as a hash using
the ``auth_backend_config`` option. This option can be changed when instantiating
the ``::st2`` class in a manifest file:

Configuration via Manifest:

.. code-block:: puppet

  class { '::st2':
    auth_backend        => 'ldap',
    auth_backend_config => {
      ldap_uri      => 'ldaps://ldap.domain.tld',
      bind_dn       => 'cn=ldap_stackstorm,ou=service accounts,dc=domain,dc=tld',
      bind_pw       => 'some_password',
      ref_hop_limit => 100,
      user          => {
        base_dn       => 'ou=domain_users,dc=domain,dc=tld',
        search_filter => '(&(objectClass=user)(sAMAccountName={username})(memberOf=cn=stackstorm_users,ou=groups,dc=domain,dc=tld))',
        scope         => 'subtree'
      },
    },
  }

Configuration via Hiera:

.. code-block:: yaml

  st2::auth_backend: ldap
  st2::auth_backend_config:
    ldap_uri: "ldaps://ldap.domain.tld"
    bind_dn: "cn=ldap_stackstorm,ou=service accounts,dc=domain,dc=tld"
    bind_pw: "some_password"
    ref_hop_limit: 100
    user:
      base_dn: "ou=domain_users,dc=domain,dc=tld"
      search_filter: "(&(objectClass=user)(sAMAccountName={username})(memberOf=cn=stackstorm_users,ou=groups,dc=domain,dc=tld))"
      scope: "subtree"


Configuring ChatOps
-------------------

``stackstorm-st2`` can manage the ChatOps configuration of your StackStorm
installation. We provide support for configuring all Hubot settings, installing
custom ChatOps adapters, and configuring all adapter settings.

Configuration via Manifest:

.. code-block:: puppet

  class { '::st2':
    chatops_hubot_alias  => "'!'",
    chatops_hubot_name   => '"@RosieRobot"',
    chatops_api_key      => '"xxxxyyyyy123abc"',
    chatops_web_url      => '"stackstorm.domain.tld"',
    chatops_adapter      => {
      hubot-adapter => {
        package => 'hubot-rocketchat',
        source  => 'git+ssh://git@git.company.com:npm/hubot-rocketchat#master',
      },
    },
    chatops_adapter_conf => {
      HUBOT_ADAPTER        => 'rocketchat',
      ROCKETCHAT_URL       => 'https://chat.company.com:443',
      ROCKETCHAT_ROOM      => 'stackstorm',
      LISTEN_ON_ALL_PUBLIC => true,
      ROCKETCHAT_USER      => 'st2',
      ROCKETCHAT_PASSWORD  => 'secret123',
      ROCKETCHAT_AUTH      => 'password',
      RESPOND_TO_DM        => true,
    },
  }

Configuration via Hiera:

.. code-block:: yaml

  # character to trigger the bot that the message is a command
  # example: !help
  st2::chatops_hubot_alias: "'!'"

  # name of the bot in chat, sometimes requires special characters like @
  st2::chatops_hubot_name: '"@RosieRobot"'

  # API key generated by: st2 apikey create
  st2::chatops_api_key: '"xxxxyyyyy123abc"'

  # Public URL used by ChatOps to offer links to execution details via the WebUI.
  st2::chatops_web_url: '"stackstorm.domain.tld"'

  # install and configure hubot adapter (rocketchat, nodejs module installed by ::nodejs)
  st2::chatops_adapter:
    hubot-adapter:
      package: 'hubot-rocketchat'
      source: 'git+ssh://git@git.company.com:npm/hubot-rocketchat#master'

  # adapter configuration (hash)
  st2::chatops_adapter_conf:
    HUBOT_ADAPTER: rocketchat
    ROCKETCHAT_URL: "https://chat.company.com:443"
    ROCKETCHAT_ROOM: 'stackstorm'
    LISTEN_ON_ALL_PUBLIC: true
    ROCKETCHAT_USER: st2
    ROCKETCHAT_PASSWORD: secret123
    ROCKETCHAT_AUTH: password
    RESPOND_TO_DM: true


Configuring Key/Value pairs
---------------------------

The puppet type ``::st2::kv`` can manage key/value pairs in the
StackStorm :doc:`datastore </datastore>`:

Configuring via Manifests:

.. code-block:: puppet

  st2::kv { 'my_key_name':
    value => 'SomeValue',
  }

  st2::kv { 'another_key':
    value => 'moreData',
  }

Configuration via Hiera:

.. code-block:: yaml

  st2::kvs:
    my_key_name:
      value: SomeValue
    another_key:
      value: moreData
