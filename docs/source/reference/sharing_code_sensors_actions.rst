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
them inside sensors and actions.


Note that this pack ``lib`` folder is different from shell actions' ``lib`` folder which is
inside ``/opt/stackstorm/packs/some_pack/actions/lib/``. The pack ``lib`` folder is never
copied to a remote machine and is strictly for sharing code between sensors and actions.
