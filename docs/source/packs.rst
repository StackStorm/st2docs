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

    # Install your own pack from git
    st2 pack install https://github.com/emedvedev/chatops_tutorial

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

.. note::

   This functionality is only available in |st2| v2.8.0 and above. Some additional fixes and
   improvements to this functionality were introduced in |st2| v3.0.1.

When installing a pack, a Python virtual environment is created using the Python binary defined by
the ``actionrunner.python_binary`` config option. By default, the same binary which is
used by all the |st2| components and services is used for pack virtual environments. On CentOS/RHEL 7 and Ubuntu 16.04 the Python binary currently used is Python 2.7, on all other distributions Python 3 is used.

.. warning ::

   Python 2 support will be dropped from |st2| in future releases. Please consider updating any Python 2 only packs to work with Python 3.

On CentOS/RHEL 7 and Ubuntu 16.04 if you want to use Python 3 for running your pack Python actions, you can do that by passing  the
``--use-python3`` flag to the ``st2 pack install`` command (e.g. ``st2 pack install libcloud
--use-python3``).

This will create the pack virtual environment using the Python 3 binary specified by
``actionrunner.python3_binary`` config option. This value defaults to ``/usr/bin/python3``. For
this to work, Python 3 needs to be installed on your system.

When installing Python 3, default prefix of ``/usr`` or ``/usr/local`` should be used and base
Python 3 libraries should be installed and available in either ``/usr/lib/python3.6`` or
``/usr/local/lib/python3.6``. If a custom prefix was used when compiling / installing Python 3
(e.g. ``./configure --prefix=/opt/lib``) you also need to configure
``actionrunner.python3_prefix`` option in ``st2.conf`` to match that value.

Keep in mind that this feature only means Python runner actions will be executed using Python 3
binary. All the |st2| components and services, including the action runner will still use the
default ST2 python binary.


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
For RHEL/CentOS systems, edit ``/etc/sysconfig/st2actionrunner`` and ``/etc/sysconfig/st2api``.

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
