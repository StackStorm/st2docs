Installing StackStorm Enterprise
================================

StackStorm Community Edition is an event-driven DevOps automation platform with all the essential features, suitable for small businesses and teams. It’s free and open source under Apache 2.0 license.

StackStorm Enterprise Edition is installed as an addition to the Community Edition. It adds by adding priority support and enterprise tools such as fine-tuned access control, LDAP integration and Flow, the visual workflow editor.

Learn more about StackStorm Enterprise, request a quote, or get an evaluation license at
`stackstorm.com/product <https://stackstorm.com/product/#enterprise/>`_.

Using DEB/RPM
-------------

To install StackStorm Enterprise with ``DEB or RPM`` packages, obtain your Enterprise licensekey and
proceed to installation steps for :doc:`/install/deb`, :doc:`/install/rhel7`, or
:doc:`/install/rhel6`. The last step of the instructions is installing `st2enterprise`. Use your
license key to get access to enterprise package repositories.

Using AIO installer
-------------------
If you choose to use :doc:`/install/all_in_one` (recommended for evaluation on a clean box), you will be
presented with a screen that prompts for a license key. Check the "Enable enterprise features" and
input the license key in the field.

For unattended AIO installer, place the license key in the answers.yaml file, as described in
:ref:`all_in_one-enterprise_configuration_values` section of :doc:`/install/all_in_one`.

.. figure:: /_static/images/enterprise_enter_license.png

.. include:: /__engage.rst


