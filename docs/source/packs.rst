Packs
=====

What is a Pack?
---------------

A "pack" is the unit of deployment for integrations and automations that extend |st2|. Typically a
pack is organized along service or product boundaries e.g. AWS, Docker, Sensu etc. A pack can
contain :doc:`Actions </actions>`, :doc:`Workflows </workflows>`, :doc:`Rules </rules>`,
:doc:`Sensors </sensors>`, and :doc:`Aliases <chatops/aliases>`. |st2| content is always part of a
pack, so it's important to understand how to create packs and work with them.

Some packs extend |st2| to integrate it with external systems — like
`AWS <https://github.com/StackStorm-Exchange/stackstorm-aws>`_,
`GitHub <https://github.com/StackStorm-Exchange/stackstorm-github>`_,
or `JIRA <https://github.com/StackStorm-Exchange/stackstorm-jira>`_. We call them "`integration
packs`". Some packs capture automation patterns — they contain workflows, rules, and actions for a
specific automation process — like the `st2 demo pack <https://github.com/StackStorm/st2_demos>`_.
We call them "`automation packs`". This naming is mostly a convention: |st2| itself makes no
distinction between the two.

Integration packs can be shared and reused by anyone who uses the service that pack is built for.
You can find many examples of these at the `StackStorm Exchange <https://exchange.stackstorm.org>`_.
Automation packs are often very site-specific and have little use outside of a particular team or
company; they are usually shared internally.

Managing Packs
--------------

|st2| packs are managed through ``st2 pack <...>`` commands: ``st2 pack -h`` will give you a useful
overview.

Some (such as the ``core`` pack for basic StackStorm actions) come pre-installed with |st2|. All 
other packs need to be installed by you. Luckily this is pretty easy!

``list`` and ``get`` are the primary commands to get information about local packs:

.. code-block:: bash

    # List all installed packs
    st2 pack list

    # Get detailed information about an installed pack
    st2 pack get core

When using |st2| and pack management actions, all packs are installed into the system packs
directory, which defaults to ``/opt/stackstorm/packs``.

Discovering Packs
-----------------

There's over a hundred StackStorm packs already available to you!
`StackStorm Exchange <https://exchange.stackstorm.org>`__  is a collection of ready-made packs
submitted and maintained by the StackStorm community. There are packs for most of the popular
cloud providers and DevOps tools, as well as more peculiar integrations (hello, ``tesla`` and
``hue``).

You can browse the pack listing at `exchange.stackstorm.org <https://exchange.stackstorm.org>`__,
or search the pack index via CLI with ``st2 pack search`` and ``st2 pack show``:

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
    # with the exact name match
    st2 pack show sensu

As of |st2| v2.4, you can also do this via the Web UI! Explore the new "Packs" tab to see more.

Installing a Pack
-----------------

Installing a pack is simple:

.. code-block:: bash

    # Install from the Exchange by pack name
    st2 pack install sensu

    # You can also install multiple packs:
    st2 pack install datadog github

This command will download packs from the `StackStorm Exchange organization on GitHub 
<https://github.com/StackStorm-Exchange>`__, place them under ``/opt/stackstorm/packs``, and
register them with |st2|.

Essentially, ``st2 pack install`` works with git repositories: there is one for every pack in the
Exchange, and you can install your own packs from git just as easily.

.. code-block:: bash

    # Install your own pack from git using http(s)
    st2 pack install https://github.com/emedvedev/chatops_tutorial
    
    # Install your own pack from git using ssh
    st2 pack install git@github.com/emedvedev/chatops_tutorial
    
    # Install your own pack using gitlab URL (added in release 3.4)
    st2 pack install gitlab@gitlab.com:example/examplepack

By default, the latest release of the pack will be installed, but you can specify a particular
version, branch, tag, or even a commit hash. Just use `=`:

.. code-block:: bash

    # Fetch a specific commit
    st2 pack install cloudflare=776b9a4

    # Or a version tag
    st2 pack install cloudflare=0.1.0

    # Or a branch
    st2 pack install https://github.com/emedvedev/chatops_tutorial=testing

Finally, you can install a pack from existing local dir:

.. code-block:: bash

    # Install a pack from '/home/stanley/bitcoin' dir
    st2 pack install file:///home/stanley/bitcoin

.. warning::

    Installing a pack from a directory that is a git repository will only install the latest commit,
    and ignores any subsequent uncommitted changes to the files.

Running ``st2 pack install`` on an already installed pack will **replace** it with the requested
version or **upgrade to latest** if the version is not specified. Your config file will not be
overwritten, so you can revert to an older version just as easily, but for production deployments
we recommend to always specify versions in case there are major changes in ``latest``.


Pack Dependencies
~~~~~~~~~~~~~~~~~

.. note::

    New feature! As of StackStorm 3.2.

If your pack uses actions from other packs, you can specify them in the ``dependencies`` section of
the ``pack.yaml`` file and StackStorm will install them automatically when installing your pack.

Similar to using the ``st2 pack install`` subcommand, you can reference packs from StackStorm
Exchange using just their names, or you can specify a pack's Git repository URL. You can also use
the same syntax to install a specific version, tag, or branch:

.. code-block:: yaml

    dependencies:
      - excel
      - powerpoint=0.2.2
      - https://github.com/StackStorm/stackstorm-ms.git

If you have dependency conflicts, the ``st2 pack install`` subcommand may error out, without
installing any packs. If you would like to forcibly install a pack without installing its
dependencies, you can use the ``--skip-dependencies`` flag:

.. code-block:: bash

    st2 pack install --skip-dependencies my-custom-pack

Uninstalling a Pack
~~~~~~~~~~~~~~~~~~~

To uninstall a pack, use ``remove``:

.. code-block:: bash

    st2 pack remove sensu

Configuring a Pack
------------------

Integration packs often require configuration for your environment. For example, you need to
specify an SMTP server to use the email pack, a puppet master URL to use the Puppet pack, or a
Keystone endpoint and tenant credentials for OpenStack.

Most packs that require configuration can be configured interactively:

.. code-block:: bash

    st2 pack config cloudflare

You will be prompted for configuration parameters in an interactive tool with descriptions,
suggestions, and defaults. You will also be asked to verify your final config file in a text editor
before saving it; it's optional, and most packs don't require more than two or three fields, but we
have to comply with Health and Safety. The generated file will be placed in
``/opt/stackstorm/configs/<pack>.yaml`` and loaded.

.. warning::

    NB: |st2| loads pack configuration into MongoDB. This is automatically loaded when you use
    ``st2 pack config``. But if you manually edit your pack configuration, or use configuration
    management tools to manage those files, you **must** tell |st2| to load the updated config.

    You can do this with: ``sudo st2ctl reload --register-configs``. Otherwise there will be much
    head-scratching as you wonder why |st2| seems to be completely ignoring your updated configuration.

    Trust us. We've all been there.

For more nice tricks on pack configuration, see :doc:`/reference/pack_configs`.

Overriding Pack Defaults
------------------------

When installing a pack the state of the resources is taken from the metadata files in the pack. Occassionally, when installing community packs you might not want all resources enabled, e.g. you only want to use a subset of actions, or want to disable the sensors.

Prior, to |st2| 3.7.0 then this state can be altered, by:

  * using the |st2| APIs to disable the resource. However, this will be forgotten upon a ``st2ctl reload`` or pack reinstall.
  * changing the metadata file manually. This would be lost upon an upgrade, and cannot be easily tracked.

In |st2| 3.7.0 we have introduced the override feature, so that the metadata of a packs resources can be overridden by configuration files. This will always be read upon a reload or pack install. The ST2 APIs will still allow you to override this, but as before any changes made by the |st2| APIs to enable/disable resources is forgotten upon reload or re-install.

The override facility is currently restricted to allowing the enabled property to be overridden only for resources of type: action, alias, rule and sensor. It is controlled by the ``/opt/stackstorm/overrides`` directory.

Upon a pack install or reload resource state is managed as follows:

* State is read from the pack's resource metadata files that reside in ``/opt/stackstorm/packs/<packname>``. These are downloaded from the relevant repository of the pack, e.g. GIT, StackStorm-Exchange.
* If ``/opt/stackstorm/overrides/_global.yaml`` is present, then any global overrides are applied. The ``_global.yaml`` allows you to specify the default state of a particular resource types, e.g. disable all sensors.
  The format of the _global.yaml is as follows (set to disable everything):

.. code-block:: bash

   ---
   sensors:
     defaults:
       enabled: false
   actions:
     defaults:
       enabled: false
   aliases:
     defaults:
       enabled: false
   rules:
     defaults:
       enabled: false

* If ``/opt/stackstorm/overrides/<packname>.yaml`` is present, then any pack defaults, or resource specific overrides are applied. The <pack>.yaml allows you to alter the state of all the resources of a particular type, via the defaults property (e.g. all sensors within the pack), or by individual resource type, via the exceptions property (e.g. only alter state of individual actions). As the pack name is determined by the name of the overrides file, the name of the resource in the file should omit the pack name, e.g. ``action1`` in the ``pack1.yaml`` refers to the resource ``pack1.action1``.
  The format of the ``<pack>.yaml`` is as follows (set to disable everything, except for individual resource of each type):

.. code-block:: bash

   ---
   sensors:
     defaults:
       enabled: false
     exceptions:
       sensorname1:
         enabled: true
   actions:
     defaults:
       enabled: false
     exceptions:
       actionname1:
         enabled: true
   aliases:
     defaults:
       enabled: false
     exceptions:
       aliasname1:
         enabled: true
   rules:
     defaults:
       enabled: false
     exceptions:
       rulename1:
         enabled: true

If overrides are taking place, then the number of resources affected will be output on the ``st2ctl reload`` output, for example:

.. code-block:: bash

   $ st2ctl reload --register-all
   Registering content...[flags = --config-file /etc/st2/st2.conf --register-all]
   2022-02-07 12:56:43,694 INFO [-] Connecting to database "st2" @ "127.0.0.1:27017" as user "None".
   2022-02-07 12:56:43,704 INFO [-] Successfully connected to database "st2" @ "127.0.0.1:27017" as user "None".
   2022-02-07 12:56:44,254 INFO [-] =========================================================
   2022-02-07 12:56:44,254 INFO [-] ############## Registering triggers #####################
   2022-02-07 12:56:44,254 INFO [-] =========================================================
   2022-02-07 12:56:44,549 INFO [-] Registered 1 triggers.
   2022-02-07 12:56:44,549 INFO [-] =========================================================
   2022-02-07 12:56:44,549 INFO [-] ############## Registering sensors ######################
   2022-02-07 12:56:44,549 INFO [-] =========================================================
   2022-02-07 12:56:44,832 INFO [-] Registered 9 sensors.
   2022-02-07 12:56:44,832 INFO [-] 7 sensors had their metadata overridden.
   ...

On a pack install, then the number of resources that have their metadata overridden will be reported in the output of the register_pack action by the "(overridden)" entries. If no resources of that type have their metadata overridden, then there will be no correspdoning overridden entry outputted:


.. code-block:: bash

   {
     "runners": 14,
     "rule_types": 2,
     "policy_types": 3,
     "triggers": 0,
     "sensors": 2,
     "sensors(overridden)": 2,
     "actions": 1,
     "rules": 1,
     "aliases": 0,
     "policies": 0,
     "configs": 0
    }

.. rubric:: Example: Disabling all sensors in one pack

For example, to disable all sensors in an individual pack then we would create a ``/opt/stackstorm/overrides/<packname>.yaml`` that contained:

.. code-block:: bash

   ---
   sensors:
     defaults:
       enabled: false

.. rubric:: Example: Disabling all sensors in all packs, except for one pack

If, instead we wanted to override all sensors except for a single pack, then we would instead create a ``/opt/stackstorm/overrides/_global.yaml`` to disable all sensors:

.. code-block:: bash

    ---
    sensors:
      defaults:
        enabled: false

And an ``/opt/stackstorm/overrides/<packname>.yaml`` to enable the sensors for the one pack we needed:

.. code-block:: bash

    ---
    sensors:
      defaults:
        enabled: true

.. rubric:: Example: Overriding state of individual resources

In this next example, we disable all actions in ``pack1``, except for the actions ``pack1.action1`` and ``pack1.action2``. We also change the state of just a single rule to disabled. To do this, we create a ``/opt/stackstorm/overrides/pack1.yaml`` with:

.. code-block:: bash

    ---
    actions:
      defaults:
        enabled: false
      exceptions:
        action1:
          enabled: true
        action2:
          enabled: true
    rules:
      exceptions:
        rule1:
          enabled: false


Developing a Pack
-----------------

See :doc:`/reference/packs` for details on how to package your integrations and automations in a
pack, how to fork a pack for development or create your own, how to publish it, and how to
contribute it to the |st2| community. If you're planning to develop any |st2| content, we would
strongly suggest getting yourself familiar with that page: every piece of content in StackStorm has
to belong to a pack, and a good understanding of pack workflow will make your development process
much easier!


.. rubric:: What's Next?

* Explore existing packs for many common products and tools: `StackStorm Exchange <https://exchange.stackstorm.org>`__.
* Learn how to write a pack and contribute to the community  - :doc:`/reference/packs`.
* Learn how to write :ref:`custom sensors <ref-sensors-authoring-a-sensor>` and :ref:`custom actions <ref-actions-writing-custom>`.
* Check out `tutorials on stackstorm.com <https://stackstorm.com/category/tutorials/>`__ - a growing set of practical examples of automating with |st2|.
* For information on pack testing, please see the :doc:`Pack Testing </development/pack_testing>` page.

Advanced Topics
---------------

Under the Hood: Pack Basics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``st2 pack`` commands described above are a convenience layer on top of pack basics. Once you
understand the basics, you can work with the pack content directly, which might be preferred if
you work with configuration management or have a very specific deployment workflow.

Packs are placed in the system pack directory - by default ``/opt/stackstorm/packs``. A
``virtualenv`` needs to be created for each pack containing Python actions/sensors under
``/opt/stackstorm/virtualenv``. Python dependencies are installed inside the virtualenv with
``pip -r requirements.txt``. If you use ``st2 pack install``, this is handled automatically for you.

When |st2| loads the content, it looks into the system packs directory (``/opt/stackstorm/packs``)
and any additional directories listed in ``packs_base_paths`` in ``st2.conf``
(typically in :github_st2:`/etc/st2/st2.conf <conf/st2.prod.conf>`).
The value must be a string of directory paths, separated by a colon (think ``$PATH``). For example:

.. code-block:: ini

    [content]
    packs_base_paths=/home/myuser1/packs:/home/myuser2/packs

Directories are always searched from left to right in the order they are specified, with the
system packs directory always searched first.

A pack configuration file must be stored as ``/opt/stackstorm/configs/<pack_ref>.yaml`` and follow
a schema defined in ``/opt/stackstorm/packs/<pack_dir>/config.schema.yaml``. See the
:doc:`/reference/pack_configs` section for details.

When the pack content changes, it has to be registered again (reloaded). To register individual
packs, use ``st2 pack register pack1 pack2``. Packs are provided as positional space-separated arguments.
To register everything at once, use ``sudo st2ctl reload``. Use ``-h`` to explore the fine-tuning flags.

Installing Packs from Private Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are installing a pack from a private repository on GitHub, you can use HTTPS authentication
with a `personal access token 
<https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`__,
or create a `deploy key <https://github.com/blog/2024-read-only-deploy-keys>`__ to use SSH.

Access tokens are used with HTTPS URLs, for example:

.. code-block:: bash

   $ st2 pack install https://<user>:<token>@github.com/username/repo.git

Your token will be logged in |st2|, git, your shell history, and probably other log files, including
git error logs. Using SSH authentication is usually a better choice.

For SSH (URLs starting with ``git@``) authentication you have to create a `deploy key
<https://github.com/blog/2024-read-only-deploy-keys>`__. Note that pack installation is run as
``root`` by default. |st2| will use root's SSH configuration and private keys. Use
``~root/.ssh/config`` to configure a Git-specific private key if you do not want to use root's
default private key. 

Deploy keys are more secure than personal access tokens and can be configured on a per-repo basis.

Python versions in Pack Python Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When installing a pack, a Python virtual environment is created using the Python binary defined by
the ``actionrunner.python_binary`` config option. By default, the same binary which is
used by all the |st2| components and services is used for pack virtual environments, as of |st2| v3.4.0 this is python3.

.. warning ::

   Python 2 support was dropped in |st2| v3.4.0. Please consider updating any Python 2 only packs to work with Python 3.


.. _packs-behind-proxy:

Installing Packs from Behind a Proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your network uses a proxy to connect to the Internet, you must configure |st2| to use that proxy
for pack installation. This is done by setting the ``https_proxy`` or ``http_proxy`` environment
variables for the ``st2actionrunner`` and ``st2api`` processes.

If your proxy is performing SSL `MITM
<http://docs.mitmproxy.org/en/stable/howmitmproxy.html#the-mitm-in-mitmproxy>`__,
decryption/encryption, you may need to pass in the path to the proxy CA cert, using the
``proxy_ca_bundle_path`` environment variable. 

If you are using a Python version < ``2.7.9``, then a MiTM proxy won't work. This is the case with
Ubuntu 14.04. See `CVE-2014-9365
<http://people.canonical.com/~ubuntu-security/cve/2014/CVE-2014-9365.html>`__ for
more info. You will need to use `CONNECT SSL tunnel
<http://wiki.squid-cache.org/Features/HTTPS#CONNECT_tunnel>`__.

Proxy Configuration via Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On Ubuntu systems, edit ``/etc/default/st2actionrunner`` and ``/etc/default/st2api`` to set the
proxy configuration environment variables.
For RHEL/RockyLinux/CentOS systems, edit ``/etc/sysconfig/st2actionrunner`` and ``/etc/sysconfig/st2api``.

|st2| will use these environment variables for pack installation.
The file contents should look as follows:

.. code-block:: ini

    http_proxy=http://proxy.server.io:port
    https_proxy=http://proxy.server.io:port
    no_proxy=localhost,127.0.0.1

For HTTPS proxy with cert specify additional ``proxy_ca_bundle_path`` ENV:

.. code-block:: ini

    http_proxy=http://proxy.server.io:port
    https_proxy=http://proxy.server.io:port
    proxy_ca_bundle_path=/etc/ssl/certs/proxy-ca.pem
    no_proxy=localhost,127.0.0.1

After editing these files, restart the ``st2api`` and ``st2actionrunner`` services:

.. code-block:: bash

    $ sudo st2ctl restart-component st2api
    $ sudo st2ctl restart-component st2actionrunner

When using HTTPS proxy with CA bundle (MITM), you must make sure the proxy CA bundle is an accepted
root CA in your OS. Please refer to your OS instructions to register the proxy CA certificate.

This is required for tools like ``git``, ``curl`` etc to function with a proxy. Some packs
use those tools under the hood and therefore proxy CA registration step is critical for those
packs to work.

Hosting Your Own Pack Index
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you run pack management commands like ``st2 pack install sensu`` or ``st2 pack search git``,
|st2| uses a pack index file to resolve short names and perform searches. A pack index is,
essentially, a JSON object: it contains metadata and URLs for all available packs.

`The StackStorm Exchange index file <https://index.stackstorm.org/v1/index.json>`__
is a default file used by all |st2| instances, and a good example of the index format. The file is
hosted on GitHub (`StackStorm-Exchange/index <https://github.com/stackstorm-exchange/index>`__)
and proxied through CloudFlare CDN.

The index path is specified in ``st2.conf`` as ``content.index_url``. You can replace the default
index, or even use more than one with a comma-separated list:

.. code-block:: ini

    [content]
    index_url=https://my-super-index.org/index.json,https://exchange.stackstorm.org/v1/index.json

Contents from all specified indexes will merge with descending priority (left to right).
In the example above, ``sensu`` pack in your own index would override ``sensu`` pack
from the Exchange.

There are multiple reasons to consider hosting your own index, especially with HA deployments
or multi-server setups:

* mirroring: in case the main index is not available, your mirror will be used.
* forking: if you fork Exchange packs often, you can create an index that is going to list your
  forks.
* enterprise restrictions: if you need pack names to resolve, but can't install from github, you
  can specify your own index as the only source.
* a centralized resolver: in a multi-server deployment, you can host an index to keep repo URLs in
  a centralized location.
* bragging rights: get your own packs resolvable by short names because the cool kids are doing it.

In most cases there are many other ways to solve the same problem, but sometimes a pack index
is a viable alternative. Create your index file and make it accessible over HTTPS, change
``st2.conf``—and you're good!

To monitor index health, the ``/packs/index/health`` API endpoint will show you the state of all
indexes used by your |st2| instance.

.. include:: /__engage_community.rst
