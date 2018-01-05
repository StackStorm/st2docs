.. _ref-shared-libs-python-sensors-actions:


Sharing code between Sensors and Python Actions
-----------------------------------------------

You can create a python package called ``lib`` with a ``__init__.py`` file and place it
in ``${pack_dir}/`` to share code between Sensors and Python actions. For example, the path
``/opt/stackstorm/packs/my_pack/lib/`` can contain library code
you want to share between Sensors and Actions in pack ``my_pack``. Note, if you want to
share common code across packs, the recommended approach is to pin the dependency in the packs'
requirements.txt and push the dependency to ``pypi`` to be installable via pip.
The ``lib`` feature is restricted to scope of individual packs only. The ``lib`` folder can
contain any number of python files. These files can in turn contain library code, common utility
functions and the like. You can then use import statements in sensors and actions like


.. sourcecode:: python

    from common_lib import base_function

to import base_function from a file named ``common_lib.py`` inside
``/opt/stackstorm/packs/examples/lib/`` folder. You can call code from dependencies
in pack's requirements.txt from inside the files in the ``lib`` folder as you are able to call
them inside sensors and actions. Due to how python module loading works, files inside the lib
folder cannot have the same names as standard python module names. Actions may fail with
weird errors if you named your files same as standard python module names.

Note that this pack ``lib`` folder is different from shell actions' ``lib`` folder which is
inside ``/opt/stackstorm/packs/some_pack/actions/lib/``. The pack ``lib`` folder is never
copied to a remote machine and is strictly for sharing code between sensors and actions.

This feature is turned off by default to avoid potential issues that might arise due to existing
pack structures and lib imports. You may require to refactor your pack if enabling this feature
breaks your packs. To enable this feature, simply set the following config option in
``/etc/st2/st2.conf``:

.. sourcecode:: ini

    [packs]
    enable_common_libs = True

You have to restart st2 via ``st2ctl restart`` for the config change to be picked up.
