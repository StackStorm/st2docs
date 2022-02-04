Using a Specific Version of Pack Content When Running an Action
===============================================================

.. note::

  This functionality is available in |st2| >= 2.7.0 and requires git >= 2.5 to be installed. Using
  the latest stable version of git is recommended.

  If you are using Ubuntu 14.04, the latest stable version of git can be installed directly from the
  `official git ppa <https://launchpad.net/~git-core/+archive/ubuntu/ppa>`_. For RHEL / RockyLinux / CentOS,
  the latest version can be found in the `IUS repos <https://ius.io/>`_.

By default, when running an execution for an action from a pack on disk which is a git repository,
|st2| will use the currently checked out git revision of the pack content. That is the version you
have specified when installing the pack using ``st2 pack install <pack name>[=pack version]``.

If you don't explicitly specify a version, the latest stable version will be installed and used
for the action executions.

|st2| v2.7.0 introduced a new ``content_version`` runner parameter for the local and Python runner
actions.

When running an action, users can specify this parameter, which can be a git revision hash,
tag or a branch. This will cause |st2| to use action content from that git revision.

This is useful in many scenarios, such as when performing consistent zero downtime pack upgrades
and you want to use different version of the action content for different pack executions (e.g. for
some executions you want to use the older version ``v2.2.0`` and for other executions you want to use
version ``v2.3.0`` which has just been deployed).

Example Usage
-------------

The easiest way to demonstrate this functionality is using a pack which was built for purposes of
demonstrating and testing it - https://github.com/StackStorm-Exchange/stackstorm-test-content-version.

This pack contains 3 different actions which sole purpose is to print out the current pack version.
The pack itself contains 4 different versions / tags (v0.1.0, v0.2.0, v0.3.0, v0.4.0). In a standard
|st2| pack git repository layout each pack version should have a corresponding git tag.

Installing the pack
~~~~~~~~~~~~~~~~~~~

.. sourcecode:: bash

    st2 pack install https://github.com/StackStorm-Exchange/stackstorm-test-content-version

    vagrant@local$ st2 pack install https://github.com/StackStorm-Exchange/stackstorm-test-content-version

        [ succeeded ] download pack
        [ succeeded ] make a prerun
        [ succeeded ] install pack dependencies
        [ succeeded ] register pack

    +-------------+-------------------------------------------------------------+
    | Property    | Value                                                       |
    +-------------+-------------------------------------------------------------+
    | name        | test_content_version                                        |
    | description | StackStorm pack for testing "content_version" functionality |
    | version     | 0.4.0                                                       |
    | author      | st2-dev                                                     |
    +-------------+-------------------------------------------------------------+

Running the latest installed and checked out pack version (v0.4.0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, if no version if specified, the latest installed and checked out version is used. This is
the same behavior as before:

.. sourcecode:: bash

    vagrant@local$ st2 run test_content_version.python_runner_print_version

    id: 5ad0ce8b0640fd27f7b97845
    status: succeeded
    parameters: None
    result:
      exit_code: 0
      result: v0.4.0
      stderr: ''
      stdout: 'v0.4.0
        '

Running a specific version
~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case we specify that we want to use git tag ``v0.2.0`` which matches the same pack version:

.. sourcecode:: bash

    vagrant@local$ st2 run test_content_version.python_runner_print_version content_version=v0.2.0

    id: 5ad0cee40640fd27f7b97848
    status: succeeded
    parameters:
      content_version: v0.2.0
    result:
      exit_code: 0
      result: v0.2.0
      stderr: ''
      stdout: 'v0.2.0
        '

Limitations
-----------

Right now only the content (code, metadata) inside the pack directory which is a git repository is
versioned. This means that for Python runner actions, virtual environments and requirements are
not versioned and the latest version of the virtual environments which is installed is always used
when running an action.
