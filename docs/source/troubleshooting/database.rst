Database Issues
===============

This section contains information on how to troubleshoot MongoDB database-related issues.

MongoDB Authentication
----------------------

The |st2| installation script automatically creates two new MongoDB users, ``stackstorm`` and ``admin``.
The user ``stackstorm`` is granted the `readWrite <https://docs.mongodb.com/manual/reference/built-in-roles/#readWrite>`_
role on the ``st2`` database. The user ``admin`` is granted the
`dbAdmin <https://docs.mongodb.com/manual/reference/built-in-roles/#dbAdmin>`_ role on the admin db.

The script generates a random password, and assigns it to both users. The password is stored in the
``[database]`` section of ``/etc/st2/st2.conf``, e.g.:

.. code-block:: ini

  [database]
  username = stackstorm
  password = ZXqvqSRejrY6gKO9wvYgJFdh

Here's an example of using that username and password to authenticate using the Mongo CLI:

.. code-block:: bash

  [vagrant@st2vagrant ~]$ mongo -u stackstorm -p ZXqvqSRejrY6gKO9wvYgJFdh st2
  MongoDB shell version: 3.2.16
  connecting to: st2
  >


Troubleshooting Performance and Missing Index-related Issues
------------------------------------------------------------

If some of the API requests are slow, or you receive a "too much data" error, this could be caused
by an inefficient database query or a missing index.

To troubleshoot this issue, you should start the service that has an issue (e.g. ``st2api``) with the
``--debug`` and ``--profile`` flag.

When this flag is used, the service runs in profiling mode. All the executed MongoDB queries and
related profiling information (i.e. which indexes were used, how many records/rows were scanned, how
long the query took, etc.) will be logged in the service log under the DEBUG log level.
