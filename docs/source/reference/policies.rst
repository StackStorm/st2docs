Policies
========

Policies allows users to enforce different rules regarding action executions.

To list the types of policy that are available for configuration, run the command
``st2 policy-type list``.

Policy configuration files are expected to be located under the ``policies`` folder in related
packs, similar to actions and rules. Policies can be loaded into |st2| via
``st2ctl reload --register-policies``. Once policies are loaded into |st2|, run the command
``st2 policy list`` to view the list of policies in effect.

Concurrency
-----------

The concurrency policy enforces the number of executions that can run simultaneously for a
specified action.

By default when a threshold is reached, action execution is postponed until a number concurrent
executions of a particular actions falls below the threshold. As an alternative, user can also
specify for execution to be canceled instead of it being delayed / postponed.


There are two forms of concurrency policy: ``action.concurrency`` and
``action.concurrency.attr``.

action.concurrency
~~~~~~~~~~~~~~~~~~

The ``action.concurrency`` policy limits the concurrent executions for the action. The following
is an example of a policy file with concurrency defined for ``demo.my_action``. Please note that
the resource_ref and policy_type are the fully qualified name for the action and policy type
respectively. The ``threshold`` parameter defines how many concurrent instances are allowed. In
this example, no more than 10 instances of ``demo.my_action`` can be run simultaneously. Any
execution requests above this threshold will be postponed.

.. sourcecode:: YAML

    name: my_action.concurrency
    description: Limits the concurrent executions for my action.
    enabled: true
    resource_ref: demo.my_action
    policy_type: action.concurrency
    parameters:
        action: delay
        threshold: 10

If you want further actions to be canceled instead of delayed, ``action`` attribute should be
changed to ``cancel`` as shown below.

.. sourcecode:: YAML

    name: my_action.concurrency
    description: Limits the concurrent executions for my action.
    enabled: true
    resource_ref: demo.my_action
    policy_type: action.concurrency
    parameters:
        action: cancel
        threshold: 1

action.concurrency.attr
~~~~~~~~~~~~~~~~~~~~~~~

The ``action.concurrency.attr`` policy limits the executions for the action by input arguments.
Let's say ``demo.my_remote_action`` has an input argument defined called ``hostname``. This is the
name of the host where the remote command or script runs. By using the policy type
``action.concurrency.attr`` and specifying ``hostname`` as one of the attributes in the policy,
only a number of ``demo.my_remote_action`` up to the defined threshold can run simultaneously on a
given remote host.

.. sourcecode:: YAML

    name: my_remote_action.concurrency
    description: Limits the concurrent executions for my action.
    enabled: true
    resource_ref: demo.my_remote_action
    policy_type: action.concurrency.attr
    parameters:
        action: delay
        threshold: 10
        attributes:
            - hostname

.. note::

    The concurrency policy type is not enabled by default and requires a backend coordination
    service such as ZooKeeper or Redis to work.

Let's assume ZooKeeper or Redis is running on the same network where |st2| is installed. To enable
the concurrency policy type in |st2|, provide the url to connect to the backend service in the
``coordination`` section of ``/etc/st2/st2.conf``.

The following are examples for ZooKeeper and Redis:

ZooKeeper:

::

    [coordination]
    url = kazoo://username:password@host:port


Redis:

::

    [coordination]
    url = redis://password@host:port

Other supported coordination backends include:

* consul
* etcd
* MySQL
* PostgreSQL
* file (for testing when all the services are running on a single host)

For the full list of the supported backends and how to configure them, please visit
`OpenStack tooz documentation <https://docs.openstack.org/developer/tooz/>`_.

Some of these coordination backends also require corresponding client libraries to be installed
in |st2| virtualenv. We do not ship these libraries by default. As an example, to install the client
library in |st2| virtualenv, run:

.. sourcecode:: bash

    sudo su

    # Example when using redis backend
    /opt/stackstorm/st2/bin/pip install redis

    # Example when using consul backend
    /opt/stackstorm/st2/bin/pip install consul

Retry
-----

Retry policy (``action.retry``) allows you to automatically retry (re-run) an action when a
particular failure condition is met. Right now we support retrying actions which have failed or
timed out.

.. note::

    Retry policy is no longer supported for actions that are executed under a workflow as it
    conflicts with retry mechanism within specific workflow engine. Please take advantage of
    retry mechanism provided by the workflow engine where applicable.

The example below shows how to automatically retry the ``core.http`` action up to two times if it
times out:

.. literalinclude:: /../../st2/contrib/hello_st2/policies/retry_core_http_on_timeout.yaml

Keep in mind that retrying an execution results in a new execution which shares all the attributes
from the retried execution (parameters, context, etc).
