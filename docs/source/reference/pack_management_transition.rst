Pack Management Transition
==========================

.. warning:: With new pack management and
  `StackStorm Exchange <https://exchange.stackstorm.org/>`__, |st2| begins to validate and enforce
  pack schema and conventions. These changes may require users
  to update their custom :doc:`/packs` which do not confirm.
  All community packs are updated to work with |st2| 2.1,
  while still work with older versions of |st2|). Read the details and check your packs.


In |st2| 2.1, pack management have received significant overhaul. With new dedicated tools, working with packs becomes very close to the "usual" package management you know from working with
development platforms and Linux flavors. Installing, updating, and managing StackStorm packs has become a smoother, more streamlined experience.

It's a big change, and you will surely enjoy the streamlined workflow for content management. By
assuming `git`, making `one pack - one git repo` convention, and building tooling around it,  we
now streamlined pack development and life-cycle. Developing a pack, contributing a fix to Community,
checking deviation between production and upstream origins, handling versions, sharing and
discovering your automations and integrations - all of it is now streamlined.

However some changes introduced in 2.1 may require you to
update your custom packs, or to make or adjusting automation tools might use to
deploy and configure your packs on |st2|.


Good bye st2contrib, long live StackStorm Exchange
--------------------------------------------------

`StackStorm Exchange <https://exchange.stackstorm.org/>`__ is the new pack index maintained by the StackStorm team. Any pack from StackStorm Exchange can be installed with ``st2 pack install <pack>``
in the CLI.

Exchange packs are hosted in the `StackStorm-Exchange  organization
<https://github.com/stackstorm-exchange>`__  on GitHub. To submit **a new pack** to the StackStorm Exchange, follow the instructions in
`exchange-incubator <https://github.com/stackstorm-exchange/exchange-incubator>`__.

All the packs from `st2contrib <https://github.com/stackstorm/st2contrib>`__  have been migrated to
individual repositiroes at `StackStorm-Exchange organization <https://github.com/stackstorm-exchange>`.
The `st2contrib <https://github.com/stackstorm/st2contrib>`__ repository is frozen. It is still
functional, but it will not receive updates anymore, and new submissions are not accepted.

You can host your own pack index, or even your own `Exchange`, and get your |st2| content
from multiple indexes. See "Advanced topics" in :doc:`/packs` for instructions.

Using StackStorm Exchange with pre-2.1 |st2|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are on 2.0 or ealier versions of |st2|, you can still get the packs
from `StackStorm Exchange <https://exchange.stackstorm.org/>`__. Using ``st2 run pack install``,
specify ``repo_url`` as ``http://index.stackstorm.org/repos/PACK_REF``, where
``PACK_REF`` matches a ``ref`` field of the pack. For example, for "cloudflare" pack, it
will be: ::

  st2 --version
  st2 2.0.1
  st2 run packs.install packs=cloudflare repo_url="http://index.stackstorm.org/repos/cloudflare"

Or you can just `git clone` them in place, making sure that the pack
directory name matches the pack ``ref``: ::

  cd /opt/stackstorm/packs
  git clone https://github.com/StackStorm-Exchange/stackstorm-cloudflare.git cloudflare
  st2 run packs.setup_virtualenv cloudflare
  st2ctl reload


Deprecation Warnings - check your packs
---------------------------------------

From 2.1 on, |st2| enforces validation on ``pack.yaml``.
Please check and adjust your custom packs against these rules:

* The version field must conform to semver (semantic versioning): ``0.2.5``, not ``0.2``.
  In 2.1, the system will attempt to automatically convert it to semver. If the attempt
  fails, the pack loaing will error out. NOTE: In future releases there will be no auto-correct.
  Save yourself surprises: convert your custom packs to `semver` yourself.
* The ``ref`` in ``pack.yaml`` should now only contain contain letters, digits, and underscores. No
  dashes! ``hpe-icsp`` is no good, ``hpe_icsp`` is fine. If ``ref`` is not present, the same rule
  applies to the ``name`` attribute. If validation fails, pack load will error out.
* The email attribute in ``pack.yaml`` must contain a properly formatted email address.
  If validation fails, pack loading will error out.

Fix your custom packs to conform to these rules; follow the steps in :doc:`/upgrade_notes` to upgrade.
Exchange community packs have been updated to reflect these changes, please get the newer versions
of community pack from `st2contrib <https://github.com/stackstorm/st2contrib>`__

New pack management assumes each pack to be a vaild git repo. If this is not for your case, it's OK:
rely on |st2| basics, and use your favorite tools to place the packs under ``/opt/stackstorm/packs``,
set virtualenv per pack if they are Python, and tell the system to load the content.

Subtree repositories (repositories containing multiple packs inside the packs/ subdir) are no longer
supported. The ``subtree`` parameter in ``packs.install`` is removed. If you happen to use subtrees with
your private packs on git/GitHub, they will have to be split into multiple single-pack repositories in order for ``st2 pack install`` to be able to install the packs.

Changes to take advantage
-------------------------

Read :doc:`Pack management </packs>` doc to learn the benefits of the new pack management.
Some highlights:

* ``pack install`` CLI supports getting specific version, hash, or tag of a pack.

* ``pack config`` helps create, validate, and load pack configurations conforming to new :doc:`/reference/pack_configs`.

* There is a CLI and API for pack discovery: you can search the packs right from CLI.

* The ``stackstorm_version`` field has been added. It is optional and can contain a semver string which tells with which versions of StackStorm this pack works with (e.g. &gt;= 1.6.0, &lt; 2.0.0, or just &gt; 1.6.0). If your pack relies on functionality which is only available in newer versions of StackStorm you can now specify that and users won’t be able to install a pack unless they are running a version which is compatible with the pack.

* Packs are no longer named and referenced by the parent directory or git repository containing the pack: name or ref field from pack.yaml is used. Name your repository as you pleased (the recommended form for StackStorm Exchange is stackstorm-pack_name).

* Pack metadata ``pack.yaml`` file can now contain a new optional contributors field. This field is an array and contains a list of people who have contributed to the pack. These days most of the packs have more than one contributor so author field is not sufficient anymore and we want to give credit where credit is due.

-------------

.. include:: ../__engage_community.rst
