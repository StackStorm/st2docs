Packs
=====

Installing packs from st2incubator or st2contrib via ChatOps
------------------------------------------------------------

When you have the bot listening for ChatOps commands in a channel, installing extra packs 
can be done by running a single command:

.. code-block:: bash

    ! pack deploy st2contrib elasticsearch,travis_ci
    bot: Deploying the requested pack(s) from *st2contrib* for you....
    @my_user: Successful deployment of *elasticsearch* *travis_ci* !
    > from https://github.com/StackStorm/st2contrib.git (branch: _master_).

If you're adventurous and wish to install and help develop a pack that's
currently in st2incubator you can install one with the following command:

.. code-block:: bash

    ! pack deploy st2incubator vsphere,debian
    Deploying the requested pack(s) from *st2incubator* for you
    @my_user: Successful deployment of *vsphere* *debian* !
    > from https://github.com/StackStorm/st2incubator.git (branch: _master_).

The command takes the following very simple format:

.. code-block:: bash
 
    ! pack deploy {{repo_name}} {{packs}} {{branch=master}} - Download StackStorm packs via ChatOps

Deploying Custom packs via ChatOps
----------------------------------

The same commands can be used to install your own packs just by adding an entry to `/opt/stackstorm/packs/packs/config.yaml` in the following format:

.. code-block:: yaml

    ---
    repositories:
    NameOfRep:
      repo: "https://github.com/<my-GitHub-user>/my-st2.git"
      subtree: true

This will allow you to install a pack via:

.. code-block:: bash

    ! pack deploy NameOfRep MyAwesomePack

If you don't have multiple packs within the same repository under a `packs` directory, just set `subtree` to `false` and issue the following command:

.. code-block:: bash

    ! pack deploy NameOfRep NameOfRep

Automating Custom Pack Deployment
---------------------------------

Building on the above it's possible to enable auto deployment for a single branch of a 
repository which has has `subtree` set to `false` by adding an `auto_deployment` section as shown below:

.. code-block:: yaml

    ---
    repositories:
       my-st2:
         repo: "https://github.com/<my-GitHub-user>/my-st2.git"
         subtree: false
         auto_deployment:
           branch: "master"
           notify_channel: "my-chatops-channel"

Then you need a rule (or a sensor) that will trigger the `packs.deploy` action with the right 
parameters. The following is based on an post-commit hook from BitBucket Server:

.. code-block:: yaml

    action:
      ref: "packs.deploy"
      parameters:
        auto_deploy: true
        repo_name:  "{{trigger.body.repository.name}}"
        branch:     "{{trigger.body.refChanges[0].refId}}"
        packs:      [ "{{trigger.body.repository.name}}" ]
        message:    "{{trigger.body.changesets.get('values')[0].toCommit.message}}"
        author:     "{{trigger.body.changesets.get('values')[0].toCommit.author.name}}"

