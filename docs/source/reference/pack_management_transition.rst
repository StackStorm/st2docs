Pack Management Transition
==========================

.. warning:: The introduction of new pack management and
  `StackStorm Exchange <https://exchange.stackstorm.org/>`__ lead to the changes that may require users
  to update their custom :doc:`/packs`. All community packs are updated to work with |st2| 2.1
  (and will still work with older versions of |st2|). Read on for details.


In |st2| 2.1, pack management have received significant overhaul. With new dedicated tools, working with packs becomes very close to the "usual" package management you know from working with
development platforms and Linux flavours. Installing, updating, and managing StackStorm packs has become a smoother, more streamlined experience.

It's a big change, and you will surely enjoy the streamlined workflow for content management. By
assuming `git`, making ``one pack - one git repo`` convention, and building tooling around it,  we
now streamlined pack development and lifecycle. Developing a pack, contributing a fix to Community,
checking deviation between production and upstream origins, handling versions, sharing and
discovering your automations and integrations - all of it is becoming a breeze.

However we had to make some changes that will require you to
update your private packs, or to make or adjusting automation tools might use to
deploy and configure your packs on |st2|.


Good bye st2contrib, long live StackStorm Exchange
--------------------------------------------------

`StackStorm Exchange <https://exchange.stackstorm.org/>`__ is the new pack index maintained by the StackStorm team. Any pack from StackStorm Exchange can be installed with ``st2 pack install <pack>``
in the CLI. No WebUI support yet.

Exchange packs are hosted in the `StackStorm-Exchange  organization
<https://github.com/stackstorm-exchange>`__  on GitHub. To submit **a new pack** to the StackStorm Exchange, follow the instructions in
`exchange-incubator <https://github.com/stackstorm-exchange/exchange-incubator>`__.

All the packs from `st2contrib <https://github.com/stackstorm/st2contrib>`__  have been migrated to
individual repositiroes at `StackStorm-Exchange organization <https://github.com/stackstorm-exchange>`.
The `st2contrib <https://github.com/stackstorm/st2contrib>`__ repository is frozen. It is still
functional, but it will not receive updates anymore, and new submissions are not accepted.


Warnings - check your packs
---------------------------

Please validate your custom packs against these two changes:

* The version field must conform to semver (semantic versioning): ``0.2.5``, not ``0.2``. If it does not, the pack registration will throw an error. Please check and update.
* The name field in pack.yaml should now only contain contain letters, digits, and underscores. No dashes! ``hpe-icsp`` is no good, ``hpe_icsp`` is fine.
* The email attribute, if present in pack.yaml, must contain a properly formatted email address.

Fix your packs to conform to these rules; follow the steps in :doc:`/upgrade_notes` to upgrade.

Subtree repositories (repositories containing multiple packs inside the packs/ subdir) are no longer
supported. The ``subtree`` parameter in packs.install is removed. If you happen to use subtrees with
your private packs on git/GitHub, they will have to be split into multiple single-pack repositories in order for ``st2 pack install`` to be able to install the packs.

Changes to take advantage
-------------------------

.. TODO:: DZ: finish this up...

-------------

.. include:: ../__engage_community.rst
