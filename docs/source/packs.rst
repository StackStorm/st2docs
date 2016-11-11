Integration Packs
===================

What is a Pack?
---------------
Pack is the unit of deployment for integrations and automations that extend |st2|. Typically a pack is organized along service or product boundaries e.g. AWS, Docker, Sensu etc. A pack can contain :doc:`Actions </actions>`, :doc:`Workflows </workflows>`,
:doc:`Rules </rules>`, :doc:`Sensors </sensors>`, :doc:`Aliases <chatops/aliases>`.

It is best to view a pack as the means to extend |st2| and allow it to integrate with an external systems. Everything you create will also be part of a pack.

Managing Packs
--------------

.. note::

    Everything about packs got better and easier in |st2| 2.1! Packs are naturally growing into a full package management solution inside |st2|. There are new API endpoints, CLI commands, repository structure for hosting packs, and a pack collection called StackStorm Exchange. Some of the older things are now deprecated. If you're using a previous version, it's time to upgrade or at least read the :doc:`upgrade notes </upgrade_notes>`.

|st2| packs are managed through ``st2 pack ...`` commands: ``st2 pack -h`` will give you a useful overview if you just need a quick start.

A few packs (such as the ``core`` pack for basic StackStorm actions) come pre-installed with StackStorm. ``list`` and ``get`` are primary commands to work with local packs:

.. code-block:: bash

    # List all installed packs
    st2 pack list

    # Get detailed information about an installed pack
    st2 pack get core

When using |st2| and pack management actions, all the packs are installed into the
system packs directory which defaults to ``/opt/stackstorm/packs``.

Discovering Packs
-----------------

There's over a hundred StackStorm packs already available to you! `StackStorm Exchange <https://exchange.stackstorm.org>`__ is a collection of ready-made packs submitted by StackStorm users and engineers, and there are packs for most of the popular cloud providers and DevOps tools.

In addition to the pack listing at `exchange.stackstorm.org <exchange.stackstorm.org>`__, you can search the pack index in CLI with ``st2 pack search`` and ``st2 pack show``:

.. code-block:: bash

    # Search query is applied across all pack parameters.

    # It will search through pack names:
    st2 pack search sensu
    # And keywords:
    st2 pack search monitoring
    # And description (use quotes for multi-word search):
    st2 pack search "Amazon Web Services"
    # And even pack author:
    st2 pack search "Jon Middleton"

    # Show an index entry for the pack
    st2 pack show sensu

Installing a Pack
-----------------

Installing a pack is simple:

.. code-block:: bash

    st2 pack install sensu

    # You can also install multiple packs:
    st2 pack install datadog github

This command will download packs from the `StackStorm Exchange organization on GitHub <https://github.com/StackStorm-Exchange>`__, place them under ``/opt/stackstorm/packs``, and register them with |st2|.

Essentially, ``st2 pack install`` works with git repositories: there is one for every pack in the Exchange, and you can install your own packs from git just as easily.

.. code-block:: bash

    st2 pack install https://github.com/emedvedev/chatops-training

By default, the latest version of a pack will be installed, but you can specify a particular version, branch, tag, or even a commit hash.

.. code-block:: bash

    st2 pack install cloudflare=77ee04e
    st2 pack install cloudflare=0.1.0
    st2 pack install https://github.com/emedvedev/chatops-training=testing

Note that running ``st2 pack install`` on an installed pack will start an upgrade: your pack will be replaced with the version you're asking |st2| to install.

To uninstall a pack, use ``remove``:

.. code-block:: bash

    st2 pack remove sensu

Configuring a Pack
------------------

Integration packs often require configuration to adjust to the environment. e.g. you will need to specify SMTP server for email, a puppet master URL for Puppet, or a Keystone endpoint and tenant credentials for OpenStack.

Most packs that require configuration can be configured interactively:

.. code-block:: bash

    st2 pack config cloudflare

You will be prompted for configuration parameters in a nice interactive tool with descriptions, suggestions, and defaults. You will also be asked to verify your final config file in a text editor before saving it: it's optional, and most packs don't require more than two or three fields, but we have to comply with Health and Safety.

Some packs will require old-school manual configuration: in that case, you will have to edit a ``config.yaml`` file inside the ``/opt/stackstorm/packs/<pack>`` directory and reload the pack with ``st2 pack register <pack>``. Your config will not be overwritten on pack upgrades, and to be extra safe, you can save it as ``/opt/stackstorm/configs/<pack>.yaml`` to keep it away from the pack source, which is something we recommend.

Packs may contain automation rules. Rules are not loaded by default, because you may want to review and adjust them before loading. Use ``st2 pack register`` to register rules in the pack.

.. code-block:: bash

    st2 pack register sensu --types=rule

Developing a Pack
-----------------

See :doc:`/reference/packs` for details on how to package your integrations and automations in a pack, how to fork a pack for development or create your own, how to publish it, and how to contribute it to the |st2| community. If you're planning to develop any |st2| content, we would strongly suggest getting yourself familiar with that page: every piece of content in StackStorm has to belong to a pack, and a good understanding of pack workflow will make your development process much easier!

.. rubric:: What's Next?

* Explore existing packs for many common products and tools: `StackStorm Exchange <https://exchange.stackstorm.org>`__.
* Learn how to write a pack and contribute to the community  - :doc:`/reference/packs`.
* Learn how to write :ref:`custom sensors <ref-sensors-authoring-a-sensor>` and :ref:`custom actions <ref-actions-writing-custom>`.
* Check out `tutorials on stackstorm.com <http://stackstorm.com/category/tutorials/>`__ - a growing set of practical examples of automating with |st2|.
* For information on pack testing, please see the :doc:`Pack Testing </development/pack_testing>` page.

Advanced Topics
---------------

Installing packs from private repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're installing a pack from a private repository on GitHub, you can use https auth with a `personal access token <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`__, or create a `deploy key <https://github.com/blog/2024-read-only-deploy-keys>`__ to use SSH.

Access tokens are used with HTTPS auth: ``st2 pack install https://<user>:<token>@github.com/username/repo.git``.

Deploy keys are used with ``git@`` urls, and require the system user running the command (stanley or root, depending on your configuration) to have a private key, but they are more secure and can be configured on the per-repo basis.

Other git hosting services should also support either SSH or HTTPS auth, and would be configured in a similar fashion.

Pack location
~~~~~~~~~~~~~

When |st2| searches for available packs, it looks into the system packs directory and
into any additional directories which are specified in the ``packs_base_paths`` setting.

To look for packs in additional directories, set the value of ``packs_base_paths`` in ``st2.conf``
(typically in :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>`, as described in
:doc:`Configuration </install/config/config>`). The value must be a colon delimited string of directory paths.

For example:

::

    [content]
    packs_base_paths=/home/myuser1/packs:/home/myuser2/packs

Note: Directories are always searched from left to right in the order they are
specified, with the system packs directory always searched first.

Working with pack indexes
~~~~~~~~~~~~~~~~~~~~~~~~~

When you run pack management commands like ``st2 pack install sensu``  or ``st2 pack search git``, |st2| uses a pack index file to resolve short names and perform searches. A pack index is, essentially, a JSON object: it contains metadata and URLs for all available packs.

`The StackStorm Exchange index file <https://index.stackstorm.org/v1/index.json>`__ is a default file used by all |st2| instances, and a good example of the index format. The file is hosted on GitHub (`StackStorm-Exchange/index <https://github.com/stackstorm-exchange/index>`__) and proxied through CloudFlare CDN.

The index path is specified in ``st2.conf`` as ``content.index_url``. You can replace the default index, or even use more than one with a comma-separated list:

::
    [content]
    index_url=https://my-super-index.org/index.json,https://exchange.stackstorm.org/v1/index.json

Contents from all specified indexes will merge, priority arranged left to right. In the example above, ``sensu`` pack in your own index would override ``sensu`` pack from the Exchange.

There are multiple reasons to consider hosting your own index, especially with HA deployments or multi-server setups:

* mirroring: in case the main index is not available, your mirror will be used;
* forking: if you fork Exchange packs, you can create an index that is going to use your forks;
* enterprise restrictions: if you need pack names to resolve, but can't install from github, you can specify your own index as the only source;
* a centralized resolver: in a multi-server deployment, you can host an index to keep repo URLs in a centralized location;
* bragging rights: get your own packs resolvable by short names because the cool kids are doing it.

In most cases there are many other ways to solve the same problem, but sometimes a pack index is a viable alternative. Create your index file and make it accessible over HTTPS, change the config—and you're good!

When you have to monitor index health, the ``/packs/index/health`` API endpoint will show you the state of all indexes used by your |st2| instance.

.. include:: /__engage_community.rst
