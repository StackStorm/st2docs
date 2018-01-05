Ansible Playbooks
=================

Want to use `Ansible <https://www.ansible.com>`_ to deploy |st2|? Look no further - here's the
details on Ansible playbooks and roles to install |st2|. Perfect for repeatable, configurable, and
idempotent production-friendly |st2| installations.

The source code for all our playbooks is available as a GitHub repo: 
`StackStorm/ansible-st2 <https://github.com/StackStorm/ansible-st2>`_.

.. contents:: Contents
   :local:

---------------------------

Supported Platforms
-------------------

Our Ansible playbooks support the same platforms as manual installation, i.e.:

* Ubuntu Trusty (14.04)
* Ubuntu Xenial (16.04)
* RHEL 6/CentOS 6
* RHEL 7/CentOS 7

The same system size :doc:`requirements </install/system_requirements>` also apply.

Quick Start
-----------

To get started with a single node deployment, and default configuration settings, run these
commands:

.. code-block:: bash

  git clone https://github.com/StackStorm/ansible-st2.git
  cd ansible-st2

  ansible-playbook stackstorm.yml

Roles
-----

Behind the scenes the ``stackstorm.yml`` play is composed of the following Ansible ``roles`` for a
complete installation:

- ``epel`` - Repository with extra packages for ``RHEL/CentOS``.
- ``mongodb`` - Main DB storage engine.
- ``rabbitmq`` - Message broker.
- ``postgresql`` - DB storage engine for Mistral.
- ``st2repos`` - Adds |st2| PackageCloud repositories.
- ``st2`` - Install and configure |st2| itself.
- ``st2mistral`` - Install and configure |st2| Mistral workflow engine.
- ``nginx`` - Dependency for ``st2web``.
- ``st2web`` - Nice & shiny WebUI for |st2|.
- ``nodejs`` - Dependency for ``st2chatops``.
- ``st2chatops`` - Install and configure st2chatops for hubot adapter integration with |st2|.
- ``st2smoketests`` - Simple checks to see if |st2| is working.
- ``bwc`` - Install and configure |bwc|, including ``LDAP`` and ``RBAC``.
- ``bwc_smoketests`` - Simple checks to see if |bwc| is working.

Example Play
---------------------------

Here's a more advanced example showing how to customize your |st2| deployment:

.. sourcecode:: yaml

    - name: Install StackStorm with all services on a single node
      hosts: all
      roles:
        - mongodb
        - rabbitmq
        - postgresql
        - nginx
        - nodejs

        - name: Install StackStorm Packagecloud repository
          role: st2repo
          vars:
            st2repo_name: stable

        - name: Install and configure st2
          role: st2
          vars:
            st2_version: latest
            st2_auth_enable: yes
            st2_auth_username: demo
            st2_auth_password: demo
            st2_save_credentials: yes
            st2_system_user: stanley
            st2_system_user_in_sudoers: yes
            # Dict to edit https://github.com/StackStorm/st2/blob/master/conf/st2.conf.sample
            st2_config: {}

        - name: Install and configure st2mistral
          role: st2mistral
          vars:
            st2mistral_version: latest
            st2mistral_db: mistral
            st2mistral_db_username: mistral
            st2mistral_db_password: StackStorm
            # Dict to edit https://github.com/StackStorm/st2-packages/blob/master/packages/st2mistral/conf/mistral.conf
            st2mistral_config: {}

        - name: Install st2web
          role: st2web

        - name: Install st2chatops with "slack" hubot adapter
          role: st2chatops
          vars:
            st2chatops_version: latest
            st2chatops_st2_api_key: CHANGE-ME-PLEASE # (optional) This can be generated using "st2 apikey create -k"
            st2chatops_hubot_adapter: slack
            st2chatops_config:
              HUBOT_SLACK_TOKEN: xoxb-CHANGE-ME-PLEASE

        - name: Verify StackStorm Installation
          role: st2smoketests

Check out the `full list of Variables <https://github.com/stackstorm/ansible-st2#variables>`_.

Custom SSL Certificate for ``st2web``
--------------------------------------

By default we generate a self-signed certificate for ``nginx`` in ``st2web`` role. If you have your own properly signed certificate, you can use that instead:

.. sourcecode:: yaml

      - name: Configure st2web with custom SSL certificate
        role: st2web
        vars:
          st2web_ssl_certificate: "{{ lookup('file', 'local/path/to/domain-name.crt') }}"
          st2web_ssl_certificate_key: "{{ lookup('file', 'local/path/to/domain-name.key') }}"


Installing Behind a Proxy
-------------------------

If you are installing from behind a proxy, you can use the environment variables ``http_proxy``,
``https_proxy``, and ``no_proxy``. They will be passed through during the execution.

.. sourcecode:: yaml

    ---
    - name: Install st2
      hosts: all
      environment:
        http_proxy: http://proxy.example.net:8080
        https_proxy: http://proxy.example.net:8080
        no_proxy: 127.0.0.1,localhost
      roles:
        - st2


|bwc|
-----

Here's an example showing how to add :doc:`Brocade Workflow Composer </install/bwc>`, with
`LDAP <https://bwc-docs.brocade.com/authentication.html#ldap>`_ authentication and
`RBAC <https://bwc-docs.brocade.com/rbac.html>`_ configuration to allow/restrict/limit |st2|
functionality to specific users:

.. sourcecode:: yaml

    - name: Install StackStorm Enterprise
      hosts: all
      roles:
        - name: Install and configure StackStorm Enterprise (BWC)
          role: bwc
          vars:
            bwc_repo: enterprise
            bwc_license: CHANGE-ME-PLEASE
            bwc_version: latest
            # Configure LDAP backend
            # See: https://bwc-docs.brocade.com/authentication.html#ldap
            bwc_ldap:
              backend_kwargs:
                bind_dn: "cn=Administrator,cn=users,dc=change-you-org,dc=net"
                bind_password: "foobar123"
                base_ou: "dc=example,dc=net"
                group_dns:
                  - "CN=stormers,OU=groups,DC=example,DC=net"
                host: identity.example.net
                port: 389
                id_attr: "samAccountName"
            # Configure RBAC
            # See: https://bwc-docs.brocade.com/rbac.html
            bwc_rbac:
              # Define BWC roles and permissions
              # https://bwc-docs.brocade.com/rbac.html#defining-roles-and-permission-grants
              roles:
                - name: core_local_only
                  description: "This role has access only to action core.local in pack 'core'"
                  enabled: true
                  permission_grants:
                    - resource_uid: "action:core:local"
                      permission_types:
                        - action_execute
                        - action_view
                    - permission_types:
                      - runner_type_list
              # Assign roles to specific users
              # https://bwc-docs.brocade.com/rbac.html#defining-user-role-assignments
              assignments:
                - name: test_user
                  roles:
                    - core_local_only
                - name: stanley
                  roles:
                    - admin
                - name: chuck_norris
                  roles:
                    - system_admin

        - name: Verify BWC Installation
          role: bwc_smoketests

.. note::

    Please refer to https://github.com/StackStorm/ansible-st2 for updates and more detailed
    examples, descriptions and code. Iff you're familiar with Ansible, and think you've found a
    bug, or would like to propose a feature or pull request, your contributions are very welcome!
