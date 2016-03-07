Updates and Upgrades
====================


Safe way: Migrate
~~~~~~~~~~~~~~~~~
The safe and reliable way to transition |st2| to newer versions to provision a
new |st2| instance, and roll over the content. Thanks to the "Infrastructure as code" approach, all |st2| content and artifacts are simple files, and should be kept under source control.
The recommended upgrade path to move from ``VERSION_OLD`` to ``VERSION_NEW`` is as follows :

1. Install StackStorm ``VERSION_NEW`` on a brand new instance.
2. Package all your pack from the old ``VERSION_OLD`` instance and place them under some SCM like git (you should have done it long ago).
3. Save your key-value pairs from the st2 datastore: ``st2 key list -j > kv_file.json``
4. Grab packs from the SCM. If the SCM is git then it is possible to use ``st2 run packs.install packs=<pack-list> repo_url=<repo-url>``
5. Reconfigure all external services to point to the new StackStorm instance.
6. Load your keys to the datastore: ``st2 key load kv_file.json``
7. Back up audit log from ``VERSION_OLD`` server found under ``/var/log/st2/*.audit.log`` and move to a safe location. Note that history of old executions will be lost during such a transition, but a full audit record is still available in the log files that were transferred over.


Upgrades
~~~~~~~~
If |st2| has been installed from new ``rpm/deb`` packages, use the standard upgrade procedure for your Linux distribution.

.. warning:: New packages are still in BETA. While we are testing upgrades, we will only commit
   to supporting it from v1.4 forward.


All-In-One Installer in-place upgrade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
All-In-One Installer wiring is complex, and while we did the best effort to ensure that the basic upgrade works, there are few things that we know may break. Here is the procedure that works in most common cases:

1. Remove ``st2::version`` and ``st2::revision``, if present, from ``/opt/puppet/hieradata/answers.json`` or ``/opt/puppet/hieradata/answers.yaml`` depending on which is present on your system. This step is a no-op in most installations.
2. Run ``update-system`` and answer ``Y`` when prompted to overwrite existing version.
3. StackStorm service need a restart to pick up new code. Do this by running ``st2ctl restart`` after ``update-system`` completes.
4. Run self verification, and your own validation.
5. If self verification passes we are all good. Cleanup the packs installed by self verification by running the command st2 run packs.uninstall packs=examples, tests, fixtures, asserts
6. In case of failures on any of the tests find us on StackStorm community on Slack and ask about the errors. During 9am-6am PST Mon-Fri you will find a StackStorm team member hanging out and answering questions. You can also reach us at support@stackstorm.com.
