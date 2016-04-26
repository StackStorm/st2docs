Updates and Upgrades
====================


Safe way: Migrate
~~~~~~~~~~~~~~~~~
The safe and reliable way to transition |st2| to newer versions is to provision a
new |st2| instance, and roll over the content. Thanks to the "Infrastructure as code" approach, all |st2| content and artifacts are simple files, and should be kept under source control.
The recommended upgrade path to move from v1.2 to v1.3 is as follows :
1. Install StackStorm ``VERSION_NEW`` on a brand new instance.
2. Package all your packs from the old ``VERSION_OLD`` instance and place them under some SCM like git (you should have done it long ago).
3. Save your key-value pairs from the st2 datastore: ``st2 key list -j > kv_file.json``
4. Grab packs from the SCM.
5. If the SCM is git then it is possible to use st2 run packs.install packs=<pack-list> repo_url=<repo-url>
6. Reconfigure all external services to point to the new StackStorm instance.
7. Load your keys to the datastore: ``st2 key load kv_file.json``
9. Back up audit log from ``VERSION_OLD`` server found under ``/var/log/st2/*.audit.log`` and move to a safe location. Note that history of old executions will be lost during such a transition, but a full audit record is still available in the log files that were transferred over.


Upgrades
~~~~~~~~
If |st2| has been installed from `rpm/deb`, use the standard upgrade procedure for your Linux distribution.

.. warning:: New packages are still in BETA. While we are testing upgrades, we will only commit
   to supporting it from v1.4 forward.

