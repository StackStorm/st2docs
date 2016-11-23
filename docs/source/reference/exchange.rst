:orphan:

StackStorm Exchange
===================

Integration packs have received significant overhaul in StackStorm 2.1: with new dedicated tools, working with packs becomes very close to the "usual" package management you know from working with programming languages and operating systems. Installing, updating, and managing StackStorm packs has become a smoother, more streamlined experience.

This page serves as a migration guide, as well as the list of features that are being changed or deprecated. If you are upgrading from 2.0 and earlier versions, read on.


StackStorm Exchange
-------------------

`StackStorm Exchange <https://exchange.stackstorm.org/>`__ is the new pack directory maintained by the StackStorm team. Any pack from StackStorm Exchange can be installed with ``st2 pack install <pack>`` in CLI.

All Exchange packs are hosted in the StackStorm-Exchange organization on GitHub: `StackStorm-Exchange <https://github.com/stackstorm-exchange>`__.

To submit your own pack to Exchange, follow the instructions in `exchange-incubator <https://github.com/stackstorm-exchange/exchange-incubator>`__.


Earlier StackStorm versions
---------------------------

The old `st2contrib <https://github.com/stackstorm/st2contrib>`__ repository is frozen: it is still functional, but it will not receive updates anymore, and new submissions are not accepted. This can be an inconvenience for people using the old StackStorm versions, but we want to make sure StackStorm packs is maintained in the best possible way; unfortunately, this also means we cannot support two separate pack directories. We strongly encourage everyone to update to 2.1 and try out the new pack experience.

In case a StackStorm upgrade is not an option, the packs from the `StackStorm-Exchange <https://github.com/stackstorm-exchange>`__ organization can still be installed with the ``packs.install`` action even on pre-2.1.


Migration notes
---------------

* The ``packs`` pack is deprecated: it is present in 2.1, but everyone is strongly encouraged to use the new CLI commands ``st2 pack <...>`` or API endpoints.

* The ``packs.install`` parameters have been streamlined: ``subtree`` is not supported anymore, and the ``packs`` parameter now supports both pack names (resolved through Exchange) and pack URLs, as well as installing particular versions with the `=` separator.

* Subtree repositories (repositories containing multiple packs inside the ``packs/`` subdir) are not supported anymore. Subtrees will have to be split into multiple single-pack repositories in order for StackStorm to be able to install the packs.

* Pack versions in ``pack.yaml`` are finally required to conform to semver: ``0.1.0`` is acceptable, ``0.1`` is not.

* Dashes in pack refs should be replaced with underscores. Note that you can now separate the ``name`` and ``ref`` attributes: if you don't like the short reference name, your pack can have a beautiful display name visible in Web UI and Flow.

-------------

.. include:: ../__engage_community.rst
