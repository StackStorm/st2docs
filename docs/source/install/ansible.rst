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

        - name: Install and configure st2mistral
          role: st2mistral
          vars:
            st2mistral_version: latest
            st2mistral_db: mistral
            st2mistral_db_username: mistral
            st2mistral_db_password: StackStorm

        - name: Install st2web
          role: st2web

        - name: Install st2chatops with "slack" hubot adapter
          role: st2chatops
          vars:
            st2chatops_version: latest
            st2chatops_st2_api_key: CHANGE-ME-PLEASE # (optional) This can be generated using "st2 apikey create -k"
            st2chatops_hubot_adapter: slack
            st2chatops_config:
              HUBOT_SLACK_TOKEN:xoxb-CHANGE-ME-PLEASE

        - name: Verify StackStorm Installation
          role: st2smoketests

Here is a `full list of Variables <https://github.com/stackstorm/ansible-st2#variables>`_.


.. note::

    Please refer to https://github.com/StackStorm/ansible-st2 for updates and more detailed examples, descriptions and code.
    Additionally if you're familiar with Ansible, found a bug, would like to propose a feature or pull request, - your contributions are very welcome!
