Mistral + Jinja
===============

Starting in |st2| v2.2, Jinja expressions are also supported where YAQL expressions are accepted.
Jinja expressions can be used for simple conditional evaulation and data transformation in Mistral
workflows. There will be many cases where you did not author the actions but there's a need to
decide from the result of the action whether to continue or there's a need to transform the
result to another value or structure for the next action in the workflow.

Here are use cases where Jinja can be applied in Mistral workflows:

* Define input values that are passed to tasks.
* Define output values published from tasks and workflows.
* Define conditions that determine transitions between tasks.

Knowing where Jinja can be applied in Mistral workflows, the following are some cool things
that you can do with Jinja:

* Access values from list and dictionary.
* Simple arithmetic.
* Evaluation of boolean logic.
* Use conditional logic and builtin filters to evaluate and transform data.

.. note::

    Please refer to offical documentation for Mistral and Jinja. The documentation here
    is meant to help |st2| users get a quick start.

Basics
++++++
The following are statements in the workflow and task definition that accepts Jinja:

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

Each of the statements can take a string with one or more Jinja expressions. Each expression in the
string should be encapsulated with ``{{ }}``. Code block using ``{% %}`` is also supported. Please
note that the symbols ``{`` and ``}`` will conflict with JSON and Jinja expressions must always be
encapsulated with quotes or double quotes in the workflow definition.

.. note::

    Mixing of both YAQL and Jinja expressions in a single statement is not supported.

When evaluating a Jinja expression, Mistral also passes a JSON dictionary (aka context) to the
Jinja templating engine. The context contains all the workflow inputs, published variables, and
result of completed tasks up to this point of workflow execution including the current task. The
Jinja expression can refer to one or more variables in the context. The reserved symbol ``_`` is
used to reference the context. For example, given the context ``{"ip": "127.0.0.1", "port": 8080}``,
the string ``https://{{ _.ip }}:{{ _.port }}/api`` returns ``https://127.0.0.1:8080/api``. The
following is the same example used in a workflow:

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
                    endpoint: https://{{ _.ip }}:{{ _.port }}/api

.. note::

    The reserved symbol to reference the workflow context for Jinja is different than YAQL
    expressions. This is due to the differences in the limitation between the two engines.
    As mentioned above, the symbol ``_`` is used to access context in Jinja whereas the symbol
    ``$`` is used in YAQL.

The following is a more complex workbook example with a few more Jinja expressions. There are
variables passed to input parameters and being published after task completion. Please take
note of the ``install_apps`` task in the ``configure_vm`` workflow. The input parameter ``cmd``
is given the value formatted by the Jinja for loop. Unlike YAQL, a string in a Jinja
expression must be explicitly encapsulated in quotes (i.e. ``{{ 'this is a string.' }}``).

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/mistral-jinja-workbook-complex.yaml

Certain statements in Mistral such as on-success and on-error can evaluate boolean logic. The
``on-condition`` related statements are used for transition from one task to another. If a
boolean logic is defined with these statements, it can be used to evaluate whether the transition
should continue or not. Complex boolean logic using a combination of ``not``, ``and``, ``or``, and
parentheses is possible. Take the following workflow as an example: Execution of certain branch
in the workflow depends on the value of ``_.path``. If ``_.path == a``, then task ``a`` is executed.
If ``_.path == b``, then task ``b``. Finally task ``c`` is executed if neither.

.. literalinclude:: /../../st2/contrib/examples/actions/workflows/mistral-jinja-branching.yaml

The statement ``with-items`` in Mistral is used to execute an action over iteration of one or more
lists of items. The following is a sample Mistral workflow that iterates over the list of given names
to invoke the action to create individual VM.

.. code-block:: yaml

    version: '2.0'

    examples.create-vms:
        type: direct
        input:
            - names
        tasks:
            task1:
                with-items: "name in {{ _.names }}"
                action: examples.create-vm
                input:
                    name: "{{ _.name }}"

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
                    - "name in {{ _.names }}"
                    - "ip in {{ _.ips }}"
                action: examples.create-vm
                input:
                    name: "{{ _.name }}"
                    ip: "{{ _.ip }}"

.. note::

    The Jinja expression(s) passed to with-items is slightly different than YAQL expression(s).
    If using Jinja, the entire statement (i.e. ``"name in {{ _.names }}"``) require quotation
    because the symbols ``{`` and ``}`` for the delimiters conflict with JSON. Whereas if using YAQL,
    the statement does not necessarily require quotation.

Jinja Filters
+++++++++++++
Jinja has a list of built-in filters to work with strings, dictionaries, lists, etc. Please
refer to Jinja `documentation <http://jinja.pocoo.org/docs/latest/templates/#list-of-builtin-filters>`_
for the list of available filters.

A number of Mistral and |st2| specific custom functions (aka filters in Jinja) such as ``st2kv``, ``task``,
``env``, and ``execution`` that are available in YAQL are also made available in Jinja.

**Mistral**

* ``env()`` returns the environment variables passed to the workflow execution on invocation such as the |st2| Action Execution ID ``st2_execution_id``. For example, the expression ``{{ env().st2_action_api_url }}/actionexecutions/{{ env().st2_execution_id }}`` returns the API endpoint for the current workflow execution in |st2| as something like ``https://127.0.0.1:9101/v1/actionexecutions/874d3d5b3f024c1aa93225ef0bcfcf3a``.
* To access infomation about the parent action like in an ActionChain with ``{{action_context.parent.source_channel}}``, ``{{action_context.parent.user`` or ``{{action_context.parent.api_user}}``. The following expressions can be used ``{{ env()['__actions']['st2.action']['st2_context']['parent']['api_user'] }}``, ``{{ env()['__actions']['st2.action']['st2_context']['parent']['source_channel'] }}`` or ``{{ env()['__actions']['st2.action']['st2_context']['parent']['user'] }}``.
* ``task('task_name')`` returns the state, state_info, and result of task given task_name.

**StackStorm**

* ``st2kv('st2_key_id')`` queries |st2|'s datastore and returns the value for the given key. For example, the expression ``{{ st2kv('system.shared_key_x') }}`` returns the value for a system scoped key named ``shared_key_x`` while the expression ``{{ st2kv('my_key_y') }}`` returns the value for the user scoped key named ``my_key_y``. The ``st2kv`` function will always decrypt the value of the key if it is encrypted when the key value pair was set. Please note that the key name should be in quotes otherwise Jinja treats key name with a dot like ``system.shared_key_x`` as a dict access.

Testing Expressions
+++++++++++++++++++
Somtimes Jinja expressions can become complex and the need to verify the expression
outside of StackStorm is necessary. To accomplish this there are a few options:

- `Jinja2 online evaluator <http://jinja2test.tk/>`_
- Write a small test script
  
  .. code-block:: python

    #!/usr/bin/env python
    import jinja2
    import os


    class JinjaUtils:
    
        @staticmethod
        def render_file(filename, context):
            path, filename = os.path.split(filename)
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(path or './'))
            tmpl = env.get_template(filename)
            return tmpl.render(context)

        @staticmethod
        def render_str(jinja_template_str, context):
            env = jinja2.Environment()
            tmpl = env.from_string(jinja_template_str)
            return tmpl.render(context)


    if __name__ == "__main__":
        context = {'results': {'name': 'Stanley'}}
        template = "Hello {{ results.name }}"
        print JinjaUtils.render_str(template, context)

.. note::

    The test script does NOT include the custom StackStorm Jinja filters or functions
    such as ``st2kv``.

  
More Examples
+++++++++++++
More workflow examples using Jinja expressions can be found at :github_st2:`/usr/share/doc/st2/examples </contrib/examples/actions/workflows/>`. The examples are prefixed with ``mistral-jinja``.
