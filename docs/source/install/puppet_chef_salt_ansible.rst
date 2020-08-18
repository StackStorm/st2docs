:orphan:

Installing |st2| with Configuration Management Tools
#########################################################

.. warning::

    Some of the installation methods described on this page might be out of date. If you experience
    issues, please follow distribution-specific package based installation instructions.

This section has pointers to using StackStorm with configuration management tools. Some are used internally by |st2|, some
are contributed by our users, some others are community contributions. Maintaining this section is a community effort,
thus if you are a Chef, Ansible, Puppet, or Salt expert, your contributions here are very welcome.

.. contents::
    :depth: 2

Ansible
=======

We use Ansible playbooks internally to deploy |st2|, and you can too. See :doc:`/install/ansible` for details on how to use these
playbooks.

Puppet
======

|st2| provides a community-supported Puppet module. This module is actively maintained, and sees frequent updates.

See :doc:`/install/puppet` for details on how to get started.

Chef
====

We don't have documentation for Chef yet. If you'd like to help us fill in this section, pull requests are gladly accepted. In the meantime, here are some resources to get you started:

   * |st2| Cookbook: https://supermarket.chef.io/cookbooks/stackstorm
   * OpenStack Mistral Cookbook: https://supermarket.chef.io/cookbooks/openstack-mistral


Salt
====

We don't have a Salt States or Documentation for Salt. If you'd like to help us fill in this section, pull requests are gladly accepted. In the meantime, here are some resources that we do have to get you started.

   * Integrating SaltStack and |st2|: https://stackstorm.com/2015/07/29/getting-started-with-stackstorm-and-saltstack/ - a blog post on how to integrate the two systems.
