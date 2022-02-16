Role Based Access Control
=========================

.. note::

   Prior to StackStorm 3.3, Extreme Networks provided a commercial version of the StackStorm automation
   platform which included Role Based Access Control (RBAC). As these enterprise features were donated to
   the Linux Foundation, RBAC is now available in StackStorm Open Source since 3.4.

Role Based Access Control (RBAC) allows system administrators to restrict users' access and limit
the operations they can perform. For instance, you could give your database operator access only
to the database-related actions.

Read through the detailed overview below, or jump straight to a :ref:`usage example <rbac-using_rbac>`.
The source code for the RBAC module can be accessed at https://github.com/stackstorm/st2-rbac-backend.

Terminology
-----------

This section describes basic concepts with which you need to familiarize yourself, in order to
understand and efficiently utilize RBAC.

User
~~~~

A user represents an entity (person/system) which needs to be authenticated and interacts with
|st2| through the API.

User permissions are represented as a union of permission grants which are assigned to all the user
roles.

By default when a new |st2| user is created, this user has no roles assigned to it, meaning it
doesn't have access to perform any API operation which is behind the RBAC wall.

Role
~~~~

A role contains a set of permissions (permission grants) which apply to the resources. Permission
grants are usually grouped together in a role using specific criteria (e.g. by project, location,
team, responsibility, etc.).

Roles are assigned to the users. Each user can have multiple roles assigned to it and each role can
be assigned to multiple users.

System Roles
------------

System roles are roles which are available by default and can't be manipulated (modified and/or
deleted).

Currently, the following system roles are available:

+--------------------------+------------------+---------------------------------------------------------------------------------------------------+
| Role                     | Value            | Description                                                                                       |
+==========================+==================+===================================================================================================+
| **Administrator**        | ``admin``        | All permissions on all the resources                                                              |
+--------------------------+------------------+---------------------------------------------------------------------------------------------------+
| **System Administrator** | ``system_admin`` | Same as ``admin``, but this role is assigned to the first user in the system and can't be revoked |
+--------------------------+------------------+---------------------------------------------------------------------------------------------------+
| **Observer**             | ``observer``     | ``view`` permission on all the resources                                                          |
+--------------------------+------------------+---------------------------------------------------------------------------------------------------+

Permission Grant
~~~~~~~~~~~~~~~~

Permission grant grants a particular permission (permission type) to a particular resource. For
example, you could grant an execute/run permission (``action_execute``) to an action
``core.local``.

In general, there are five permission types available for each supported resource type:

* ``view`` - Ability to view a specific resource or ability to list all the
  resources of a specific type.
* ``create`` - Ability to create a new resource.
* ``modify`` - Ability to modify (update) an existing resource.
* ``delete`` - Ability to delete a specific resource.
* ``all`` - Ability to perform all the supported operations on a specific resource. For example,
  if you grant ``action_all`` on a particular action this implies the following permissions:
  ``action_view``, ``action_create``, ``action_modify``, ``action_delete`` and ``action_execute``.

In addition to that, there is also a special ``execute`` (``action_execute``) permission type
available for actions. This permission allows users to execute (run) a particular action.

Keep in mind that in |st2| a workflow is just an action so if you want someone to be able to
execute a particular workflow, you simply need to grant them ``action_execute`` permission on that
workflow.

As described in the table below, ``create``, ``modify``, ``delete`` and ``execute`` permissions
also implicitly grant corresponding ``view`` permission. This means that, for example, if you
grant ``action_execute`` permission on a particular action, the user will also be able to view and
retrieve details for this particular action.

.. _ref-rbac-available-permission-types:

Available Permission Types
~~~~~~~~~~~~~~~~~~~~~~~~~~

The table below contains a list of all the available permission types.

.. include:: _includes/available_permission_types.rst

This list can also be retrieved using the RBAC meta API (``GET /v1.0/rbac/permission_types``).

User Permissions
~~~~~~~~~~~~~~~~

User permissions (also called effective user permission set) are represented as a union of all
the permission grants which are assigned to the user roles.

For example, if a user has the following two roles assigned to it:

.. literalinclude:: ../../st2/st2tests/st2tests/fixtures/rbac/roles/role_five.yaml
    :language: yaml

.. literalinclude:: ../../st2/st2tests/st2tests/fixtures/rbac/roles/role_six.yaml
    :language: yaml

The effective user permission set is:

* ``action_execute`` on ``action:dummy_pack_1:my_action_1``
* ``action_execute`` on ``action:dummy_pack_1:my_action_2``

RBAC system uses a whitelist approach which means there is no possibility of conflicting and
contradictory permission grants in different roles (e.g. one role granting a particular
permission and another role revoking it).

Resource
~~~~~~~~

In the context of RBAC, a resource refers to the resource to which the permission grant applies to.
Permission grants can be applied to the following resource types:

* packs
* sensors
* actions
* action aliases
* rules
* executions
* webhooks
* inquiries
* key value pairs

.. note::
    The support of key value pairs is only available in |st2| v3.7.0 and above.

A resource is identified by a ``uid``, and referenced as such in permission grants. UID is an
identifier which is unique for each resource in the |st2| installation. UIDs follow this format:
``<resource type>:<resource specific identifier value>`` (e.g. ``pack:libcloud``,
``action:libcloud:list_vms``, ``key_value_pair:st2kv.system:key1``, ``key_value_pair:st2kv.user:key2`` etc.).

You can retrieve the UID of a particular resource by listing all the resources of a particular
type or by retrieving details of a single resource using either API or CLI.

For example:

.. sourcecode:: bash

    st2 action list
    +-------------------------+-------------------------+-----------+-------------------------+-------------------------+
    | uid                     | ref                     | pack      | name                    | description             |
    +-------------------------+-------------------------+-----------+-------------------------+-------------------------+
    | action:core:remote      | core.remote             | core      | remote                  | Action to execute       |
    |                         |                         |           |                         | arbitrary linux command |
    |                         |                         |           |                         | remotely.               |
    +-------------------------+-------------------------+-----------+-------------------------+-------------------------+

How it Works
------------

User permissions are checked when a user performs an operation using the API. If the user has the
necessary permissions the API operation proceeds normally, otherwise an access denied error is
returned and the error is logged in the audit log.

Permission Inheritance
~~~~~~~~~~~~~~~~~~~~~~

**Pack resources**

Pack resources inherit all the permissions from a pack. This means that if you grant
``action_execute`` permission to a pack, the user will be able to execute all the actions inside
that pack. Similarly, if you grant ``rule_create`` permission to a pack, the user will be able to
create new rules in that pack.

**Executions**

Executions inherit permissions from the action they belong to and from the action's parent pack. This
means that if you grant ``action_view`` permission on a particular action, the user will be able to
view all the executions which belong to that action. Similarly, if you grant ``action_view`` to the
parent pack which the action execution belongs to, the user will be able to view all the executions
which belong to the action with that parent pack.

On top of that, granting ``action_execute`` on a particular pack or action also grants
``execution_rerun`` and ``execution_stop`` to all the executions which belong to that action.

**Rule enforcements**

Rule enforcements (models that represent when a rule evaluated actually resulted in an action)
inherit permissions from the rule they belong to and from the rule's parent pack. This means, if
a user has a ``rule_view`` permission on a particular rule, then they also have permissions to
view the rule enforcement model for the rule. Similarly, if you grant ``rule_view`` to the
parent pack of the rule, users will be able to see all enforcements of rules belonging to that
pack.

Note that rule enforcements are ``operational models``. You cannot create/modify/delete them
via API. So permissions other than ``view`` and ``list`` do not make sense.

**Inquiries**

Inquiries inherit response permissions based on execution permissions of the workflow
that generated them. This is useful for ensuring that anyone that has rights to execute a
workflow that generates an Inquiry is also automatically granted permissions to respond to
that Inquiry.

Specifically, granting ``action_execute`` on a workflow action, or its parent pack, also grants
``inquiry_respond`` permissions for any Inquiries generated from that Workflow.

For detailed examples, see :ref:`Securing Inquiries<ref-securing-inquiries>`.


Permissions and Executions Which Are Not Triggered via the API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Normally when an execution is triggered via the API (POST to ``/actionexecutions/``), the
authenticated |st2| user who triggered the execution is the effective user for RBAC purposes.
There are some exceptions, described below:

**Rules** - Effective user for executions which are triggered by a rule is the system user
(by default, ``stanley``).

**ChatOps** - Effective user for executions which are triggered via ChatOps (POST to
``/aliasexecutions/``) using hubot is the |st2| user that is configured in hubot
(``ST2_AUTH_USERNAME`` - by default that is ``chatops_bot``).

Enabling RBAC
-------------

To configure RBAC you will need to manually enable it in ``st2.conf`` and assign ``admin`` privileges to default 
user ``stanley``.

To enable rbac, add this section to ``/etc/st2/st2.conf``:

.. code-block:: ini

   [rbac]
   enable = True
   backend = default

Run ``sudo st2ctl restart-component st2api`` to apply that change.

To assign ``admin`` privileges to ``stanley`` and ``st2admin``, create these two files:

* ``/opt/stackstorm/rbac/assignments/stanley.yaml``:
  
  .. code-block:: yaml

    ---
    username: "stanley"
    roles:
      - "admin"
* ``/opt/stackstorm/rbac/assignments/st2admin.yaml``:
  
  .. code-block:: yaml

    ---
    username: "st2admin"
    roles:
      - "admin"

Run ``sudo st2-apply-rbac-definitions --config-file /etc/st2/st2.conf`` to apply those changes.

Defining Roles and Assignments
------------------------------

To follow the infrastructure as code approach, roles and user role assignments are defined in YAML
files which are stored in ``/opt/stackstorm/rbac/``.

Those definitions are simple YAML files means you can (and should) version control and manage
them in the same way you version control and manage other source code and infrastructure artifacts.

Both roles and user role assignments are loaded in lexicographical order based on the filename.
For example, if you have two role definitions in the files named ``role_b.yaml`` and
``role_a.yaml``, ``role_a.yaml`` will be loaded before ``role_b.yaml``.

Defining Roles and Permission Grants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Roles and permission grants are defined in YAML files which are stored in
``/opt/stackstorm/rbac/roles/``. Each file defines role information and associated permission
grants for a single role which means that if you want to define **n** roles you will need **n** files.

Example role definition (``/opt/stackstorm/rbac/roles/role_sample.yaml``):

.. literalinclude:: ../../st2/st2tests/st2tests/fixtures/rbac/roles/role_sample.yaml
    :language: yaml

The example above contains a variety of permission grants with corresponding explanations
(comments).

Defining User Role Assignments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

User role assignments are defined in YAML files which are located in
``/opt/stackstorm/rbac/assignments/``. Each file defines assignments for a single user
which means that if you want to define assignments for **n** users, you will need **n** files.

Example role definition (``/opt/stackstorm/rbac/assignments/user4.yaml``):

.. literalinclude:: ../../st2/st2tests/st2tests/fixtures/rbac/assignments/user4.yaml
    :language: yaml

In the example above we assign two roles to the user named ``user4``:

* ``role_one`` (a custom role which needs to be defined as described above) and
* ``observer`` (system role).

Key Value Pairs
~~~~~~~~~~~~~~~

.. note::
    This functionality is only available in |st2| v3.7.0 and above.

Users with admin and system_admin roles have all access to system scoped KVPs. In v3.6.0
and before, users with admin role have full access to other users' KVPs. This behavior is
unchanged.

By default, a user has access to his/her own user scoped KVPs without requiring specific
permission grants. A non-admin user by default cannot access system scoped KVPs or other
users' KVPs. A non-admin user can be explicitly granted permission to one or more system
scoped KVPs similar to how access to other resources are granted to users. Currently, 
there is no option or plan to grant non-admin user access to another user's set of KVPs. 

The following is an example to assign a ``system scoped`` KVP to a role. 
Create ``/opt/stackstorm/rbac/roles/key1_write_role.yaml`` with the
following content. Assign this role to a user and then apply the RBAC definitions.

.. sourcecode:: yaml

    ---
    name: key1_write_role
    description: Role that allow users to set system key1
    enabled: true
    permission_grants:
        - resource_uid: "key_value_pair:st2kv.system:key1"
          permission_types:
            - "key_value_pair_set"

Applying RBAC Definitions
-------------------------

As described above, RBAC definitions are defined in YAML files located in the
``/opt/stackstorm/rbac/`` directory. For those definitions to take effect, you need to apply them
using the ``st2-apply-rbac-definitions`` script.

Usually, you will want to run this script every time you modify the RBAC definitions.

For example:

.. code-block:: bash

    st2-apply-rbac-definitions --config-file=/etc/st2/st2.conf

    2015-08-12 22:30:18,439 - INFO - Synchronizing roles...
    2015-08-12 22:30:18,441 - DEBUG - New roles: set([])
    2015-08-12 22:30:18,442 - DEBUG - Updated roles: set(['role_two', 'role_one', 'role_three'])
    2015-08-12 22:30:18,442 - DEBUG - Removed roles: set([])
    2015-08-12 22:30:18,443 - DEBUG - Deleting 3 stale roles
    2015-08-12 22:30:18,444 - DEBUG - Deleted 3 stale roles
    2015-08-12 22:30:18,446 - DEBUG - Deleting 5 stale permission grants
    2015-08-12 22:30:18,447 - DEBUG - Deleted 5 stale permission grants
    2015-08-12 22:30:18,448 - DEBUG - Creating 3 new roles
    2015-08-12 22:30:18,454 - DEBUG - Created 3 new roles
    2015-08-12 22:30:18,458 - INFO - Synchronizing users role assignments...
    2015-08-12 22:30:18,460 - DEBUG - New assignments for user "user1": set([])
    2015-08-12 22:30:18,461 - DEBUG - Updated assignments for user "user1": set(['role_two', 'role_one'])
    2015-08-12 22:30:18,461 - DEBUG - Removed assignments for user "user1": set([])
    2015-08-12 22:30:18,462 - DEBUG - Removed 2 assignments for user "user1"
    2015-08-12 22:30:18,464 - DEBUG - Created 2 new assignments for user "user1"

.. _rbac-using_rbac:

Automatically Granting Roles Based on LDAP Group Membership
------------------------------------------------------------

.. note::

   This functionality is only available in |st2| v2.3.0 and above, with the LDAP auth backend
   used for authentication.

In addition to manually assigning roles to the users based on the definitions in the
``/opt/stackstorm/rbac/assignments/`` directory, |st2| also supports automatically granting roles
to users upon authentication, based on LDAP groups membership.

This comes handy in enterprise environments and makes |st2| user provisioning easier and faster.
It means administrators don't need to manually write and manage RBAC role assignment files on disk,
because roles are automatically granted to the users based on their LDAP group membership and
mappings files in ``/opt/stackstorm/rbac/mappings/`` directory.

To be able to utilize this feature it first needs to be enabled in ``st2.conf`` by setting
``rbac.sync_remote_groups`` option to ``True``.

.. code-block:: ini

  [rbac]
  sync_remote_groups = True

After this feature is enabled, the |st2| administrator needs to write mapping files that tell |st2|
which roles to automatically grant to users, based upon LDAP group membership.

Mapping files are located in the ``/opt/stackstorm/rbac/mappings/`` directory and map an LDAP group
to one or more |st2| roles.

Two examples of such mapping files can be found below:

.. note::

  LDAP group names referenced in the ``group`` attribute are case-sensitive.

* ``/opt/stackstorm/rbac/mappings/stormers.yaml``

  .. literalinclude:: ../../st2/st2tests/st2tests/fixtures/rbac/mappings/stormers.yaml
     :language: yaml

  Each user who is a member of the ``CN=stormers,OU=groups,DC=stackstorm,DC=net`` LDAP group will
  automatically be granted ``admin`` |st2| role when they successfully authenticate with |st2|.

* ``/opt/stackstorm/rbac/mappings/testers.yaml``

  .. literalinclude:: ../../st2/st2tests/st2tests/fixtures/rbac/mappings/testers.yaml
     :language: yaml

  Each user who is a member of the ``CN=testers,OU=groups,DC=stackstorm,DC=net`` LDAP group will
  automatically be granted ``observer`` and ``qa_admin`` |st2| roles when they successfully
  authenticate with |st2|.

Once the mapping definitions files are written, the |st2| administrator needs to run the
``st2-apply-rbac-definitions`` tool to store those definitions in the database. This tool also
needs to be run after any change or removal of mappings files.

How LDAP Group-Based Role Assignments Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Role assignments based on the LDAP group to |st2| role mappings are synchronized each time a user
authenticates with the |st2| auth API and receives a fresh auth token.

If for some reason you want user roles to be synchronized before the existing auth token expires
(default TTL is 24 hours), you can simply ask the user to re-authenticate to retrieve a new auth
token. Alternatively, administrators can manually expire or disable an active auth token which will
force the user to re-authenticate.

A similar workflow can be used when removing a user from your system. By default, when a user is
removed from LDAP they will still be able to use |st2| if they have a valid auth token, until that
auth token expires. If you want user access to be revoked as soon as they are removed from LDAP,
you can manually purge active auth tokens for a particular user from the user database.

Restricting Users to Only View Resources They Own or Created
------------------------------------------------------------

.. note::

   This functionality is disabled by default and is only available in |st2| v2.7.0 and above.

   To enable it, you need to set the ``rbac.permission_isolation`` config option in
   ``/etc/st2/st2.conf`` to ``True`` and restart the API service (``sudo st2ctl restart-component
   st2api``).

   Currently it is only supported by the ``/v1/executions`` and ``/v1/rules`` API endpoints.

By default, a user needs ``RESOURCE_LIST`` (e.g. ``EXECUTION_LIST``) permission type to be able to
use "get all" API endpoints and view all the resources of a specific type.

The same applies to viewing a single resource (using "get one" API endpoint) - the user needs
``RESOURCE_VIEW`` (e.g. ``RULE_VIEW``) permission on a specific resource (or on a parent pack).

When this feature is enabled, non-admin users can only view resources which belong to or are owned by
them (resource ``context.user`` matches the currently authenticated user) when using "get all" and
"get one" API endpoints (that is in addition to needing ``RESOURCE_LIST``/``RESOURCE_VIEW``
permission).

Examples with this feature enabled:

1. Admin user (can view all the resources)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Authenticated as a user with admin role.

.. sourcecode:: javascript

    curl "https://localhost/api/v1/rules"

    [
        {
            "name": "rule1",
            "ref": "examples.rule1",
            ...
            "context": {
                "user": "admin"
            },
        },
        {
            "name": "rule2",
            "ref": "examples.rule2",
            ...
            "context": {
                "user": "user2"
            },
        },
        {
            "name": "rule3",
            "ref": "examples.rule3",
            ...
            "context": {
                "user": "user2"
            },
        },
        {
            "name": "rule4",
            "ref": "examples.rule4",
            ...
            "context": {
                "user": "user3"
            },
        },
        {
            "name": "rule5",
            "ref": "examples.rule5",
            ...
            "context": {
                "user": "user3"
            },
        }
    ]

2. User "user2" can only view their own resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Authenticated as "user2".

.. sourcecode:: javascript

    curl "https://localhost/api/v1/rules"

    [
        {
            "name": "rule2",
            "ref": "examples.rule2",
            ...
            "context": {
                "user": "user2"
            },
        },
        {
            "name": "rule3",
            "ref": "examples.rule3",
            ...
            "context": {
                "user": "user2"
            },
        }
    ]


3. User "user3" can only view their own resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Authenticated as "user3".

.. sourcecode:: javascript

    curl "https://localhost/api/v1/rules"

    [
        {
            "name": "rule4",
            "ref": "examples.rule4",
            ...
            "context": {
                "user": "user3"
            },
        },
        {
            "name": "rule5",
            "ref": "examples.rule5",
            ...
            "context": {
                "user": "user3"
            },
        }
    ]

Using RBAC Example
------------------

**Possible scenarios:**

1. A user owns a pack i.e is able to view, create, delete, modify and where applicable execute
   various resources like actions, rules, sensors.
2. A user can create rules, execute actions and view a handful of actions.
3. A user is capable of viewing actions in a pack but cannot execute any action.

This example provides a walk-through of scenario 1 i.e configuring a user as a pack owner. The
steps to be followed are by a |st2| Administrator, on a system running |st2|.

User Creation
~~~~~~~~~~~~~

All user and password management is kept outside of |st2|. Read the
:doc:`authentication <authentication>` docs to see how to configure to configure |st2| with various
identity providers.

For sake of this example let us assume that the identity provider is managed by the OS on which
|st2| runs.

On most Linux systems, to create a user and set their password, run this:

.. sourcecode:: bash

    $ useradd rbac_user1
    $ passwd rbac_user1

Once this user is created |st2| will allow access to this user. (Optional) To validate, try:

.. sourcecode:: bash

    $ st2 login rbac_user1 -p '<RBACU1_PASSWORD>'
    $ st2 action list

Role Creation
~~~~~~~~~~~~~

A newly created user has no assigned permissions. Each permission must be explicitly assigned to a
user. To assign permission grants requires creation of a role and then associating this role
with a user. In this case we are trying to create a pack owner role.

Lets first make sure there is a pack ``example`` we can use to experiment.

.. sourcecode:: bash

    $ cd /opt/stackstorm/packs/
    $ mkdir example
    $ mkdir example/actions example/rules example/sensors
    $ touch example/pack.yaml
    $ touch /opt/stackstorm/configs/example.yaml
    $ touch example/requirements.txt
    $ cp core/icon.png example/icon.png

Now we setup a role. Create ``/opt/stackstorm/rbac/roles/example_pack_owner.yaml`` with the
following content:

.. sourcecode:: yaml

    ---
    name: "example_pack_owner"
    description: "Owner of pack example"
    enabled: true
    permission_grants:
        -
            resource_uid: "pack:example"
            permission_types:
               - "pack_all"
               - "sensor_type_all"
               - "rule_all"
               - "action_all"
        # Note: To be able to create a rule, the user also needs to have an "action_execute" permission
        # on the action used inside the rule. In this example, the rule created calls core.local action
        -
            resource_uid: "action:core:local"
            permission_types:
               - "action_execute"
        # Need runner_type_list on relevant runners
        -
            resource_uid: "runner_type:local-shell-cmd"
            permission_types:
               - "runner_type_list"


A ``pack owner`` role would require the user to be able to view, create, modify and delete all
contents of a pack. Again, let's pick the pack ``example`` as the target of ownership.

See :ref:`available permission types<ref-rbac-available-permission-types>` for a full list of
permission types.

Role Assignment
~~~~~~~~~~~~~~~

Creation of a role is followed by assignment of a role to the user. Create the file
``/opt/stackstorm/rbac/assignments/rbac_user1.yaml`` with the following content:


.. sourcecode:: yaml

    ---
    username: "rbac_user1"
    description: "Grant example_pack_owner role to rbac_user1 user."
    enabled: true
    roles:
        - "example_pack_owner"

Applying RBAC
~~~~~~~~~~~~~

As a |st2| administrator, run:

.. sourcecode:: bash

    st2-apply-rbac-definitions --config-file=/etc/st2/st2.conf

This command will sync the |st2| RBAC state with the filesystem state. Only after running this
command does |st2| know of the latest changes to RBAC permission grants.

Validation
~~~~~~~~~~

Lets take this for a spin using the |st2| CLI.

1. Setup Authentication token:

  .. sourcecode:: bash

    $ st2 login rbac_user1 -p '<RBACU1_PASSWORD>'

2. Validate rule visibility and creation:

  .. sourcecode:: bash

    $ cd /opt/stackstorm/packs/example
    $ cp /usr/share/doc/st2/examples/rules/sample_rule_with_timer.yaml rules/
    $ sed -i 's/pack: "examples"/pack: "example"/g' rules/sample_rule_with_timer.yaml
    $ st2 rule create rules/sample_rule_with_timer.yaml
    $ st2 rule get example.sample_rule_with_timer
    $ st2 rule delete example.sample_rule_with_timer

    # Expect Failure
    $ st2 rule get <EXISTING_RULE_REF>

3. Validation action visibility, creation and execute:

  .. sourcecode:: bash

    $ cd /opt/stackstorm/packs/example
    $ cp /usr/share/doc/st2/examples/actions/local.yaml actions/
    $ echo "pack: example" >> actions/local.yaml
    $ st2 action create actions/local.yaml
    $ st2 action get example.local-notify
    $ st2 run example.local-notify hostname
    $ st2 action delete example.local-notify

    # Expect failure
    $ st2 action get core.echo
    $ st2 run core.echo hello
