Pack Management Transition
==========================

.. warning:: In 2.1, with the introduction of the new pack management and
  `StackStorm Exchange <https://exchange.stackstorm.org/>`__, |st2| validates
  pack metadata in ``pack.yaml`` and enforces certain versioning and naming
  conventions. These changes may require users to update their custom :doc:`/packs`
  if they do not follow the same standards.
  All packs in StackStorm Exchange have been updated to work with |st2| 2.1 and
  maintain compatibility with older versions of |st2|. Read the details and
  make sure your packs are valid.


In |st2| 2.1, pack management have received a significant overhaul. With new
dedicated tools, working with packs becomes very close to the "usual" package
management you know from working with development platforms and Linux flavors.
Installing, updating, and managing StackStorm packs has become a smoother, more
streamlined experience.

It's a big change, and you will surely enjoy how easy it is to install and maintain your
packs now, especially if you're upgrading from an earlier version. Installing packs,
contributing fixes, handling pack versions, sharing and discovering — nearly everything
about StackStorm packs is better than before.

Some of the changes require special attention: if you create your own packs or deploy
packs from st2contrib — either through configuration management or by
running ``st2 run packs.install`` as a part of your deployment — please read this
section through and through.

StackStorm Exchange
-------------------

`StackStorm Exchange <https://exchange.stackstorm.org/>`__ is a new pack directory
maintained by the StackStorm team. Any pack from the Exchange can be installed with
``st2 pack install <pack>`` in the CLI.

Exchange packs are hosted in the
`StackStorm-Exchange organization <https://github.com/stackstorm-exchange>`__
on GitHub, and you can open PRs against them just as you would open PRs to ``st2contrib``
before. To submit a new pack, follow the instructions in
`exchange-incubator <https://github.com/stackstorm-exchange/exchange-incubator>`__.

All the packs from `st2contrib <https://github.com/stackstorm/st2contrib>`__  have been
transferred to individual repositories inside the
`StackStorm-Exchange organization <https://github.com/stackstorm-exchange>`.
The `st2contrib <https://github.com/stackstorm/st2contrib>`__ repository is frozen: it is still
functional, but it will not receive updates anymore, and new submissions are not accepted.

You can host your own pack index alongside (or even instead of) the Exchange, and get
your |st2| content from multiple indexes. See "Advanced topics" in :doc:`/packs` for
instructions.

Using StackStorm Exchange with pre-2.1 |st2|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use |st2| 2.0 or ealier, you can still get packs from
`StackStorm Exchange <https://exchange.stackstorm.org/>`__ with the old ``packs.install``
action: use ``stackstorm-exchange/<pack name>`` as ``repo_url``, and repeat the pack name in ``packs``.
For the CloudFlare pack, the full CLI command would be:

::

  $ st2 --version
  st2 2.0.1
  $ st2 run packs.install packs=cloudflare repo_url=stackstorm-exchange/cloudflare

Alternatively, you can just ``git clone`` the packs, making sure that the pack
directory name matches the pack ``ref``:

::

  cd /opt/stackstorm/packs
  git clone https://github.com/StackStorm-Exchange/stackstorm-cloudflare.git cloudflare
  chown -R root:st2packs cloudflare
  st2 run packs.setup_virtualenv packs=cloudflare
  st2ctl reload

Deprecation Warnings
--------------------

Validation rules
~~~~~~~~~~~~~~~~

Starting from 2.1, |st2| enforces validation on ``pack.yaml``.
If you create your own packs, please validate them against these rules:

* The ``version`` value in ``pack.yaml`` must conform to `semver <http://semver.org/>`__:
  ``0.2.5``, not ``0.2``.
  In 2.1, the system will attempt to do automatic conversion. If the attempt fails, the pack
  loading will error out. NOTE: there will be no implicit conversions in future releases, and
  pack loading will fail if the version is not in the semver format. Convert the versions and
  update your packs as soon as possible to avoid surprises.
* The ``name`` value in ``pack.yaml`` must only contain letters, digits, and underscores,
  since it is also used as a ref (UID) for the pack. You can set the ``ref`` value explicitly
  in ``pack.yaml``: in this case, ``ref`` is going to be validated against the rule above,
  and ``name`` is going to be used for display only and can contain any characters.
* The email attribute in ``pack.yaml`` must contain a properly formatted email address.

Make sure your custom packs are compatible, then follow the steps in :doc:`/upgrade_notes` to upgrade
to 2.1. All packs in the Exchange have been updated to reflect these changes.

Git repositories for packs
~~~~~~~~~~~~~~~~~~~~~~~~~~

When using ``st2 pack install <URL>``, the URL is assumed to be a valid git repository containing
your pack in its root (see `StackStorm-Exchange on GitHub <https://github.com/stackstorm-exchange>`__).

This structure is required to support most of the newer pack management features, and we strongly
encourage pack developers to follow it. However, if your deployment is different (maybe you don't use
git, or place multiple packs in a repository, or install packs through a configuration management tool),
you aren't required to use the ``st2 pack`` subcommands at all: refer to the
"Under the Hood: Pack Basics" section of the :doc:`pack documentation </packs>`.

Subtree repositories (repositories containing multiple packs inside the ``packs/`` subdir) are no longer
supported, and the ``subtree`` parameter in ``packs.install`` is removed. If you happen to use a single
repository to host multiple packs, it will have to be split into multiple single-pack repositories in order for
``st2 pack install`` to be able to install the packs. Alternatively, deploy them manually as described above.

Changes to take advantage of
----------------------------

Read the :doc:`Pack management </packs>` doc to learn more about the new pack management.

Some highlights:

* A new ``pack install`` command supports getting specific version, hash, branch, or tag of a pack.

* A new ``pack config`` helps create, validate, and load pack configurations conforming to new :doc:`/reference/pack_configs`.

* CLI and API for pack discovery: you can search the pack directory right from CLI.

* You can specify ``stackstorm_version`` in ``pack.yaml``: it should contain a version range to determine if the installed version of |st2| is compatible with your pack (e.g. &gt;=1.6.0, &lt;2.0.0, or just &gt;1.6.0). If your pack relies on functionality which is only available in newer versions of StackStorm, we encourage you to specify the correct range.

* You can specify ``contributors`` in ``pack.yaml``: it is an array that should contains a list of people who have contributed to the pack. These days most of the packs have more than one contributor, and the ``author`` field just isn't enough to give credit where credit is due.

* A pack is no longer named and referenced by its parent directory or git source: the ``name`` (or ``ref``, if specified) field from ``pack.yaml`` will be used. The repository name is entirely up to you (a convention we use in StackStorm Exchange is ``stackstorm-<pack name>``).

-------------

.. include:: ../__engage_community.rst
