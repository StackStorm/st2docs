Create and Contribute a Pack
=============================

Think you'd like to create a |st2| pack? Great! Here's how to do it, and contribute it to the 
community.

:doc:`Packs </packs>` have a defined structure. You must follow this structure when creating your
own pack. It is also helpful to know while debugging issues with packs.

.. contents:: :local:

Anatomy of a Pack
-----------------

The canonical pack filesystem layout looks like this:

.. code-block:: bash

    # contents of a pack folder
    actions/                 #
    rules/                   #
    sensors/                 #
    aliases/                 #
    policies/                #
    tests/                   #
    etc/                     # any additional things (e.g code generators, scripts...)
    config.schema.yaml       # configuration schema
    packname.yaml.example    # example of config, used in CI
    pack.yaml                # pack definition file
    requirements.txt         # requirements for Python packs
    requirements-tests.txt   # requirements for python tests
    icon.png                 # 64x64 .png icon

At the topmost level are the main folders ``actions``, ``rules``, ``sensors``, ``aliases`` and
``policies``, as well as some shared files:

* ``pack.yaml`` - Metadata file that describes and identifies the folder as a pack.
* ``config.schema.yaml`` - Schema that defines configuration elements used by a pack.
* ``requirements.txt`` - File containing a list of Python dependencies. Each pack has its own Python
  virtualenv. If you need any specific Python libraries, specify them here, and they will be
  automatically installed at pack install time.

  .. note::

    You should write all dependent libraries of your pack in this ``requirements.txt`` to prevent a
    runtime error because of unexpected dependencies problem.

    When an action of python-script in your pack is going to load a module which is not in the
    pack's virtualenv, that will try to load it from the |st2|'s library path that has `these
    libraries <https://github.com/StackStorm/st2/blob/master/requirements.txt>`_ impliedly. If these
    libraries are used from your pack's dependent libraries without concern for the dependencies,
    a runtime error might be happen when these are incompatible with your pack's libraries.

    The libraries which are specified in the ``requirements.txt`` are prioritized to be loaded over
    |st2|'s ones. Therefore it's better to write every libraries, with specifying version, that are
    called directly or indirectly in your pack's ``requirements.txt``.

Site-specific pack configuration files are stored at ``/opt/stackstorm/configs/``. See
:doc:`configuration schema</reference/pack_configs>` for more information.

**Actions:**

.. code-block:: bash

   # contents of actions/
   actions/
      lib/
      action1.yaml
      action1.py
      action2.yaml
      action1.sh
      workflow1.yaml
      workflow2.yaml
      workflows/
        workflow1.yaml
        workflow2.yaml

The ``actions`` folder contains action script files and action metadata files. See
:doc:`Actions </actions>` and :doc:`Workflows </workflows>` for specifics on writing actions. Since
metadata files and workflow definitions can both be written as YAML, it's good practice to put the
workflow definitions in a separate directory. Note that the ``lib`` sub-folder is often used for
storing common Python code used by pack actions.

**Rules**:

.. code-block:: bash

   # contents of rules/
   rules/
      rule1.yaml
      rule2.yaml

The ``rules`` folder contains rules. See :doc:`Rules </rules>` for specifics on writing rules.

**Sensors:**

.. code-block:: bash

   # contents of sensors/
   sensors/
      common/
      sensor1.py
      sensor1.yaml
      sensor2.py
      sensor2.yaml

The ``sensors`` folder contains sensors. See :doc:`Sensors </sensors>` for specifics on writing
sensors and registering TriggerTypes.

**Aliases:**

.. code-block:: bash

   # contents of aliases/
   aliases/
      alias1.yaml
      alias2.yaml

The ``aliases`` folder contains Action Aliases. See :doc:`Action Aliases </chatops/aliases>` for
specifics on writing Action Aliases.

**Policies:**

.. code-block:: bash

   # contents of policies/
   policies/
      policy1.yaml
      policy2.yaml

The ``policies`` folder contains Policies. See :doc:`Policies </reference/policies>` for specifics
on writing Policies.

Creating Your First Pack
------------------------

In the example below, we will create a simple pack named **hello_st2**. The full example is also
available at :github_st2:`st2/contrib/hello_st2 <contrib/hello_st2>`.

1. Create the pack folder structure and related files. Let's keep the metadata files such as
   ``pack.yaml``, ``config.schema.yaml``, and ``requirements.txt`` empty for now:

  .. code-block:: bash

    # Use the name of the pack for the folder name.
    mkdir hello_st2
    cd hello_st2
    mkdir actions
    mkdir rules
    mkdir sensors
    mkdir aliases
    mkdir policies
    touch pack.yaml
    touch requirements.txt


  Note: All folders are optional. It is safe to skip a folder or keep it empty. Only create the
  ``config.schema.yaml`` file if it is required. An empty schema file is not valid.

2. Create the pack definition file, ``pack.yaml``:

  .. literalinclude:: /../../st2/contrib/hello_st2/pack.yaml
     :language: yaml

  .. note::

     A note on metadata: |st2| enforces certain rules about metadata. The ``version`` value in
     ``pack.yaml`` must conform to `semver <http://semver.org/>`__:``0.2.5``, not ``0.2``. The
     ``name`` value in ``pack.yaml`` must only contain lowercase letters, digits, and underscores,
     unless you set the ``ref`` value explicitly in ``pack.yaml``. Finally the email attribute in
     ``pack.yaml`` must contain a properly formatted email address.
     
     From |st2| 3.7.0, the name ``_global`` is reserved, and cannot be used as a pack name.

     The ``python_versions`` field declares which Python versions this pack supports. As |st2| 
     only supports Python **3** from version 3.4.0 onwards, packs submitted to the StackStorm
     Exchange will run CI checks for Python version **3** only. |st2| will
     check this field when installing packs, and not allow installation with unsupported major Python
     versions. If this field is missing, |st2| assumes both Python **2** and **3** are supported.

3. Create the :doc:`action </actions>`. An action consists of meta data, and entrypoint. The following
   example simply echoes a greeting.

  Copy the following content to ``actions/greet.yaml``:

  .. literalinclude:: /../../st2/contrib/hello_st2/actions/greet.yaml
     :language: yaml

  Copy the following content to ``actions/greet.sh``:

  .. literalinclude:: /../../st2/contrib/hello_st2/actions/greet.sh
     :language: bash

4. Create a sensor. The sample sensor below publishes an event to |st2| every 60 seconds.

  Copy the following content to ``sensors/sensor1.yaml``:

  .. literalinclude:: /../../st2/contrib/hello_st2/sensors/sensor1.yaml
     :language: yaml

  Copy the following content to ``sensors/sensor1.py``:

  .. literalinclude:: /../../st2/contrib/hello_st2/sensors/sensor1.py
     :language: python

5. Create a rule. The sample rule below is triggered by an event from the sensor and invokes the
   action from the samples above.

  Copy the following content to ``rules/rule1.yaml``:

  .. literalinclude:: /../../st2/contrib/hello_st2/rules/rule1.yaml
     :language: yaml

6. Create an action alias. The sample action alias below aliases the ``greet`` action and makes it
   accessible from ChatOps.

  Copy the following content to ``aliases/alias1.yaml``:

  .. literalinclude:: /../../st2/contrib/hello_st2/aliases/alias1.yaml
     :language: yaml

7. Create a policy. The sample policy below limits concurrent operation of the ``greet`` action.

  Copy the following content to ``policies/policy1.yaml``:

  .. literalinclude:: /../../st2/contrib/hello_st2/policies/policy1.yaml
     :language: yaml

8. Install the pack. We encourage using ``git``. If you do so, ``st2 pack`` will greatly simplify
   your pack management. Of course, you can define your own tools and workflow for editing and
   versioning packs. You'll need to place the files in ``/opt/stackstorm/packs`` and [re-]load the
   content.

  8.1 Use git and ``pack install`` (**recommended**):

  .. code-block:: bash

    # Get the code under git
    cd hello_st2
    git init && git add ./* && git commit -m "Initial commit"
    # Install from local git repo
    st2 pack install file://$PWD

  When you make code changes, run ``st2 pack install`` again: it will do the upgrade.
  Once you push it to GitHub, you will install and update it right from there:

  .. code-block:: bash

    st2 pack install https://github.com/MY/PACK

  8.2 Copy over and register (if you have special needs and know what you're doing).

  .. code-block:: bash

    mv ./hello_st2 /opt/stackstorm/packs
    st2ctl reload

Congratulate yourself: you have created your first pack. Commands like ``st2 pack list``,
``st2 action list``, ``st2 rule list`` and ``st2 trigger list`` will show you the loaded content. To
check if the sensor triggering action is working, run ``st2 execution list``, there should be an
entry for executing ``hello_st2.greet`` every minute.

Take it from there. Write an awesome automation, or an inspiring integration pack with your
favorite tool. Happy hacking!


Submitting a Pack to the Community
----------------------------------

Now that you forged this awesome pack in |st2| it's time, and good form, to share your awesomeness
with the community. `StackStorm Exchange <https://exchange.stackstorm.org>`__  is the place for you
and everyone else to share and pull :doc:`integration packs </packs>`.

To feature your pack on the `StackStorm Exchange <https://exchange.stackstorm.org>`__,
submit a GitHub pull request to the
`StackStorm Exchange Incubator repository <https://github.com/StackStorm-Exchange/exchange-incubator>`__.
Our team will review the PR, accept it to the incubator, graduate it to the main "Exchange", and
help you promote it.

.. hint:: 

  If you are new to git/GitHub, check this `excellent interactive learning resource
  <https://try.github.io/levels/1/challenges/1>`__, a `guide for submitting a GitHub pull request
  <https://guides.github.com/activities/forking/>`__ and a `more detailed Fork-Branch-PullRequest
  <http://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/>`__ workflow tutorial.

Contributors License Agreement
--------------------------------

By contributing you agree that these contributions are your own (or approved by your employer) and
you grant a full, complete, irrevocable copyright license to all users and developers of the
project, present and future, pursuant to the license of the project.
