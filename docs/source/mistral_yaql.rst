Mistral + YAQL
==============

YAQL is typically used for simple conditional evaluation and data transformation in Mistral
workflows. There will be many cases where you did not author the actions but there's a need to
decide from the result of the action whether to continue, or there's a need to transform the
result to another value or structure for the next action in the workflow.

Here are use cases where YAQL can be applied in Mistral workflows:

* Define input values that are passed to tasks.
* Define output values published from tasks and workflows.
* Define conditions that determine transitions between tasks.

Knowing where YAQL can be applied in Mistral workflows, the following are some cool things that
you can do with YAQL:

* Select key-value pairs from a list of dictionaries.
* Filter the list where one or more fields match condition(s).
* Transform a list to dictionary or vice versa.
* Simple arithmetic.
* Evaluation of boolean logic.
* Any combination of select, filter, transform, and evaluate.

.. note::

    Please refer to official OpenStack documentation for Mistral and YAQL. The documentation here
    is meant to help |st2| users get started quickly, but does not cover everything.
    `YAQL unit tests <https://github.com/openstack/yaql/tree/master/yaql/tests>`_ are also a great
    reference for how to use and what features are supported in YAQL. They help to cover some gaps
    in OpenStack YAQL documentation.

Basics
------

The following are statements in the workflow and task definition that accept YAQL:

* task action input
* task concurrency
* task on-complete
* task on-error
* task on-success
* task pause-before
* task publish
* task retry break-on
* task retry continue-on
* task retry count
* task retry delay
* task timeout
* task wait-before
* task wait-after
* task with-items
* workflow output

Each of the statements can take a string with one or more YAQL expressions. Each expression in the
string should be encapsulated with ``<% %>``.

.. note::

    Mixing of both YAQL and Jinja expressions in a single statement is not supported.

When evaluating a YAQL expression, Mistral also passes a JSON dictionary (aka context) to the YAQL
engine. The context contains all the workflow inputs, published variables, and result of completed
tasks up to this point of workflow execution, including the current task. The YAQL expression can
refer to one or more variables in the context. The reserved symbol ``$`` is used to reference the
context. For example, given the context ``{"ip": "127.0.0.1", "port": 8080}``, the string
``https://<% $.ip %>:<% $.port>/api`` returns ``https://127.0.0.1:8080/api``. The following is the
same example used in a workflow:

.. code-block:: yaml

    version: '2.0'

    examples.yaql-basic:
        type: direct
        input:
            - ip
            - port
        tasks:
            task1:
                action: examples.call-api
                input:
                    endpoint: https://<% $.ip %>:<% $.port>/api

Certain statements in Mistral such as on-success and on-error can evaluate boolean logic. The
``on-condition`` related statements are used for transition from one task to another. If a
boolean logic is defined with these statements, it can be used to evaluate whether the transition
should continue or not. Complex boolean logic using a combination of ``not``, ``and``, ``or``, and
parentheses is possible. Take the following workflow as an example: Execution of certain branch
in the workflow depends on the value of ``$.path``. If ``$.path = a``, then task ``a`` is executed.
If ``$.path = b``, then task ``b``. Finally task ``c`` is executed if neither.

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/mistral-branching.yaml
   :language: yaml

The statement ``with-items`` in Mistral is used to execute an action over iteration of one or more
list of items. The following is a sample Mistral workflow that iterates over the list of given names
to invoke the action to create individual VM.

.. code-block:: yaml

    version: '2.0'

    examples.create-vms:
        type: direct
        input:
            - names
        tasks:
            task1:
                with-items: name in <% $.names %>
                action: examples.create-vm
                input:
                    name: <% $.name %>

``with-items`` can take more than one list as the following example illustrates. In this case,
a list of VMs and IP addresses are passed as inputs and then iterated through step by step together.

.. code-block:: yaml

    version: '2.0'

    examples.create-vms:
        type: direct
        input:
            - names
            - ips
        tasks:
            task1:
                with-items:
                    - name in <% $.names %>
                    - ip in <% $.ips %>
                action: examples.create-vm
                input:
                    name: <% $.name %>
                    ip: <% $.ip %>

The sections below contain additional YAQL examples of how to work with lists and dictionaries,
that can be used in more advanced ``with-items`` use-cases.

Dictionaries
------------

To create a dictionary, use the ``dict`` function. For example, ``<% dict(a=>123, b=>true) %>``
returns ``{'a': 123, 'b': True}``. Let's say this dictionary is published to the context as
``dict1``. The keys function ``<% $.dict1.keys() %>`` returns ``['a', 'b']`` and
``<% $.dict1.values() %>`` returns the values ``[123, true]``. Concatenating dictionaries can be
done as ``<% dict(a=>123, b=>true) + dict(c=>xyz) %>`` which returns
``{'a': 123, 'b': True, 'c': 'xyz'}``.

A specific key-value pair can be accessed by key name such as ``<% $.dict1.get(b) %>`` which
returns ``True``. Given the alternative ``<% $.dict1.get(b, false) %>``, if the key ``b`` does not
exist, then ``False`` will be returned by default.

Lists
-----

To create a list, use the ``list`` functions. For example, ``<% list(1, 2, 3) %>`` returns
``[1, 2, 3]`` and ``<% list(abc, def) %>`` returns ``['abc', 'def']``. List concatenation can be
done as ``<% list(abc, def) + list(ijk, xyz) %>`` which returns ``['abc', 'def', 'ijk', 'xyz']``.
If this list is published to the context as ``list1``, items can also be accessed via index such
as ``<% $.list1[0] %>``, which returns ``abc``.

Queries
-------

Let's take the following context as an example:

.. code-block:: json

    {
        "vms": [
            {
                "name": "vmweb1",
                "region": "us-east",
                "role": "web"
            },
            {
                "name": "vmdb1",
                "region": "us-east",
                "role": "db"
            },
            {
                "name": "vmweb2",
                "region": "us-west",
                "role": "web"
            },
            {
                "name": "vmdb2",
                "region": "us-west",
                "role": "db"
            }
        ]
    }

The following YAQL expressions are some sample queries that YAQL is capable of:

* ``<% $.vms.select($.name) %>`` returns the list of VM names
  ``['vmweb1', 'vmdb1', 'vmweb2', 'vmdb2']``.
* ``<% $.vms.select([$.name, $.role]) %>`` returns a list of names and roles as
  ``[['vmweb1', 'web'], ['vmdb1', 'db'], ['vmweb2', 'web'], ['vmdb2', 'db']]``.
* ``<% $.vms.select($.region).distinct() %>`` returns the distinct list of regions
  ``['us-east', 'us-west']``.
* ``<% $.vms.where($.region = 'us-east').select($.name) %>`` selects only the VMs in us-east
  ``['vmweb1', 'vmdb1']``.
* ``<% $.vms.where($.region = 'us-east' and $.role = 'web').select($.name) %>`` selects only the
  web server in us-east ``['vmweb1']``.
* ``<% let(myregion => 'us-east', myrole => 'web') -> $.vms.where($.region = $myregion and $.role = $myrole).select($.name) %>``
  selects only the web server in us-east ``['vmweb1']``.

List to Dictionary
------------------

There are cases where it is easier to work with dictionaries rather than lists (e.g. random access
of a value with the key). Let's take the same list of VM records from above and convert it to a
dictionary where VM name is the key and the value is the record.

YAQL can convert a list of lists to a dictionary where each list contains the key and value. For
example, the expression ``<% dict(vms=>dict($.vms.select([$.name, $]))) %>`` returns the following
dictionary:

.. code-block:: json

    {
        "vms": {
            "vmweb1": {
                "name": "vmweb1",
                "region": "us-east",
                "role": "web"
            },
            "vmdb1": {
                "name": "vmdb1",
                "region": "us-east",
                "role": "db"
            },
            "vmweb2": {
                "name": "vmweb2",
                "region": "us-west",
                "role": "web"
            },
            "vmdb2": {
                "name": "vmdb2",
                "region": "us-west",
                "role": "db"
            }
        }
    }

In this expression, we took the original ``vms`` list, returned a list of ``[name, record]``, and then converted it to a dictionary.

Other YAQL Functions
--------------------

YAQL has a list of built-in functions to work with strings, dictionaries, lists, etc. Some of
these are passed through to Python built-in functions (i.e. int, float, pow, regex, round, etc.).

Mistral adds additional workflow-related functions to the list. For example, the call to function
``<% len(foobar) %>`` to get the length of the string ``foobar`` returns the value ``6``. The
following is a curated list of commonly used functions. Please visit the YAQL documentation and
GitHub repo to explore more options.

Built-in
^^^^^^^^

For the full list of built-in functions, see the `Standard Library section in YAQL docs
<https://yaql.readthedocs.io/en/latest/standard_library.html>`_. Some notable examples:

* ``float(value)`` converts value to float.
* ``int(value)`` converts value to integer.
* ``str(number)`` converts number to a string.
* ``len(list)`` and ``len(string)`` returns the length of the list and string respectively.
* ``max(a, b)`` returns the larger value between a and b.
* ``min(a, b)`` returns the smaller value between a and b.
* ``regex(expression).match(pattern)`` returns True if expression matches pattern.
* ``regex(expresssion).search(pattern)`` returns the first instance that matches the pattern.
* ``'some string'.toUpper()`` converts the string to all upper case.
* ``'some string'.toLower()`` converts the string to all lower case.
* ``['some', 'list'].contains(value)`` returns True if list contains value.
* ``"one, two, three, four".split(',').select(str($).trim())`` converts a comma separated string
  to an array, trimming each element.

Mistral
^^^^^^^

* ``env()`` returns the environment variables passed to the workflow execution on invocation such
  as the |st2| Action Execution ID ``st2_execution_id``.

  For example, the expression
  ``<% env().st2_action_api_url %>/actionexecutions/<% env().st2_execution_id %>`` returns the API
  endpoint for the current workflow execution in |st2| as something like
  ``https://127.0.0.1:9101/v1/actionexecutions/874d3d5b3f024c1aa93225ef0bcfcf3a``.

* To access information about the parent action, the following expressions can be used
  ``<% env().get('__actions').get('st2.action').st2_context.parent.api_user %>``,
  ``<% env().get('__actions').get('st2.action').st2_context.parent.source_channel %>`` or
  ``<% env().get('__actions').get('st2.action').st2_context.parent.user %>``.

  Note that this similar to the ActionChain expressions
  ``{{action_context.parent.source_channel}}``, ``{{action_context.parent.user}}`` or
  ``{{action_context.parent.api_user}}``.
* ``task(task_name)`` returns the state, state_info, and the result of the given task_name.

|st2|
^^^^^

``st2kv('st2_key_id')`` queries |st2|'s datastore and returns the value for the given key. For
example, the expression ``<% st2kv('system.shared_key_x') %>`` returns the value for a system
scoped key named ``shared_key_x`` while the expression ``<% st2kv('my_key_y') %>`` returns the
value for the user scoped key named ``my_key_y``.
  
Please note that the key name should be in quotes otherwise YAQL treats a key name with a dot like
``system.shared_key_x`` as a dict access.

.. note::

  If the retrieved value was stored encrypted, ``st2kv`` no longer attempts decryption by default
  (as of version 2.4). To decrypt the retrieved value, you must explicitly enable it through the
  ``decrypt`` parameter: ``st2kv('st2_key_id', decrypt=true)``.

Testing YAQL Expressions
------------------------

The fastest way to test YAQL expressions with your data is to use the online YAQL evaluator at
http://yaqluator.com/.

The website allows you to provide sample data and YAQL expressions which you can evaluate in real
time and see the result. This is especially handy when working with more complex expressions.
