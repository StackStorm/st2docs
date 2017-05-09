Ansible Playbooks
=================
Ansible playbooks and roles to install |st2|.

Allows you to deploy and further configure |st2| installation on local or remote machines with Ansible configuration management tool.

The advantage of using this method, comparing to our demonstrational ``curl | bash`` installer are repeatable, configurable and idempotent production-friendly |st2| installations.

Playbooks source code is available as GitHub repository `StackStorm/ansible-st2 <https://github.com/StackStorm/ansible-st2>`_.

---------------------------

Supported platforms
---------------------------
* Ubuntu Trusty (14.04)
* Ubuntu Xenial (16.04)
* RHEL6 / CentOS6
* RHEL7 / CentOS7

Requirements
---------------------------
At least 2GB of memory and 3.5GB of disk space is required, since |st2| is shipped with RabbitMQ, PostgreSQL, Mongo, nginx and OpenStack Mistral.

Quick Start
---------------------------
Here are basic instructions to get started with a single node deployment and default configuration settings:

.. sourcecode:: bash

    git clone https://github.com/StackStorm/ansible-st2.git
    cd ansible-st2

    ansible-playbook stackstorm.yml

Roles
---------------------------
Behind the scenes ``stackstorm.yml`` play composed of the following Ansible ``roles`` for a complete installation:

- ``epel`` - Repository with extra packages for ``RHEL/CentOS``.
- ``mongodb`` - Main DB storage engine for |st2|.
- ``rabbitmq`` - Message broker for |st2|.
- ``postgresql`` - Main DB storage engine for |st2| Mistral.
- ``st2repos`` - Adds |st2| PackageCloud repositories.
- ``st2`` - Install and configure |st2| itself.
- ``st2mistral`` - Install and configure |st2| Mistral workflow engine.
- ``nginx`` - Dependency for ``st2web``.
- ``st2web`` - Nice & shiny WebUI for |st2|.
- ``nodejs`` - Dependency for ``st2chatops``.
- ``st2chatops`` - Install and configure st2chatops for hubot adapter integration with |st2|.
- ``st2smoketests`` - Simple checks to know if |st2| really works.
- ``bwc`` - Install and configure BWC |st2| enterprise, including ``LDAP`` and ``RBAC``.
- ``bwc_smoketests`` - Small integration tests to check if ``BWC`` really works.

Example Play
---------------------------
Below is more advanced example to customize |st2| deployment:

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

Here is a `full list of Variables <https://github.com/stackstorm/ansible-st2#variables>`_.

Custom SSL Certificate for ``st2web``
--------------------------------------
By default we generate a self-signed certificate for ``nginx`` in ``st2web`` role. It's possible to pass an externally signed SSL certificate instead:

.. sourcecode:: yaml

      - name: Configure st2web with custom SSL certificate
        role: st2web
        vars:
          st2web_ssl_certificate: "{{ lookup('file', 'local/path/to/domain-name.crt') }}"
          st2web_ssl_certificate_key: "{{ lookup('file', 'local/path/to/domain-name.key') }}"


Installing behind a Proxy
--------------------------
If you are installing from behind a proxy, you can use the environment variables ``http_proxy``, ``https_proxy``, and ``no_proxy`` in the play. They will be passed through during the execution.

.. sourcecode:: yaml

    ---
    - name: Install st2
      hosts: all
      environment:
        http_proxy: http://proxy.example.net:8080
        https_proxy: https://proxy.example.net:8080
        no_proxy: 127.0.0.1,localhost
      roles:
        - st2


BWC (|st2| Enterprise)
---------------------------
Example to customize |st2| enterprise (`BWC <https://bwc-docs.brocade.com/>`_) with `LDAP <https://bwc-docs.brocade.com/authentication.html#ldap>`_ auth backend and `RBAC <https://bwc-docs.brocade.com/rbac.html>`_ configuration to allow/restrict/limit different |st2| functionality to specific users:

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

    Please refer to https://github.com/StackStorm/ansible-st2 for updates and more detailed examples, descriptions and code.
    Additionally if you're familiar with Ansible, found a bug, would like to propose a feature or pull request, - your contributions are very welcome!
