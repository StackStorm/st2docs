Rules
=====

|st2| uses rules and workflows to capture operational patterns as automations. Rules map triggers
to actions (or workflows), apply matching criteria, and map trigger payloads to action inputs.

.. note::
   
   Rules not working as expected? Check the :doc:`Rules Troubleshooting </troubleshooting/rules>`
   documentation. This walks through rules testing, checking enforcements, logging and troubleshooting.

Rule Structure
--------------

Rules are defined in YAML. Rule definition structure, as well as required and optional elements are
listed below:

.. code-block:: yaml

    ---
        name: "rule_name"                      # required
        pack: "examples"                       # optional
        description: "Rule description."       # optional
        enabled: true                          # required

        trigger:                               # required
            type: "trigger_type_ref"

        criteria:                              # optional
            trigger.payload_parameter_name1:
                type: "regex"
                pattern : "^value$"
            trigger.payload_parameter_name2:
                type: "iequals"
                pattern : "watchevent"

        action:                                # required
            ref: "action_ref"
            parameters:                        # optional
                foo: "bar"
                baz: "{{ trigger.payload_parameter_1 }}"

The generic form of a rule is:

* The ``name`` of the rule.
* The ``pack`` that the rule belongs to. ``default`` is assumed if a pack is not specified.
* The ``description`` of the rule.
* The ``enabled`` state of a rule (``true`` or ``false``).
* The type of ``trigger`` emitted from sensors to monitor, and optionally parameters associated
  with that trigger.
* An optional set of ``criteria``, consisting of:

  * An attribute of the trigger payload.
  * The ``type`` of criteria comparison.
  * The ``pattern`` to match against.

* The ``action`` to execute when a rule is matched, consisting of:

  * The ``ref`` (action/workflow) to execute.
  * An optional set of ``parameters`` to pass to the action execution.
  
  .. note::

    Each rule can only have one single ``action`` section. If you need to run multiple actions when a rule is matched, either configure multiple rules, or create a workflow, and call that.

Trigger
-------

The trigger in a rule specifies which incoming events should be inspected for potential match
against this rule. View all the triggers configured on a system via the command line with the
``st2 trigger list`` command:

.. code-block:: shell

    vagrant@st2vagrant:~$ st2 trigger list
    +--------------------------------+-----------+---------------------------+---------------------------------------------------------------------------------+
    | ref                            | pack      | name                      | description                                                                     |
    +--------------------------------+-----------+---------------------------+---------------------------------------------------------------------------------+
    | core.st2.webhook               | core      | st2.webhook               | Trigger type for registering webhooks that can consume arbitrary payload.       |
    | core.st2.generic.actiontrigger | core      | st2.generic.actiontrigger | Trigger encapsulating the completion of an action execution.                    |
    | core.st2.IntervalTimer         | core      | st2.IntervalTimer         | Triggers on specified intervals. e.g. every 30s, 1week etc.                     |
    | core.st2.DateTimer             | core      | st2.DateTimer             | Triggers exactly once when the current time matches the specified time. e.g.    |
    |                                |           |                           | timezone:UTC date:2014-12-31 23:59:59.                                          |
    | core.st2.CronTimer             | core      | st2.CronTimer             | Triggers whenever current time matches the specified time constaints like a     |
    |                                |           |                           | UNIX cron scheduler.                                                            |
    | core.st2.sensor.process_spawn  | core      | st2.sensor.process_spawn  | Trigger encapsulating spawning of a sensor process.                             |
    | autoscale.ScaleDownPulse       | autoscale | ScaleDownPulse            | Pulse trigger emitted when an ASG is eligible for deflation                     |
    | autoscale.ScaleUpPulse         | autoscale | ScaleUpPulse              | Pulse trigger emitted when an ASG is eligible for expansion                     |
    | slack.message                  | slack     | message                   | Trigger which indicates a new message has been posted to a channel              |
    | linux.file_watch.line          | linux     | file_watch.line           | Trigger which indicates a new line has been detected                            |
    | core.st2.sensor.process_exit   | core      | st2.sensor.process_exit   | Trigger encapsulating exit of a sensor process.                                 |
    | newrelic.WebAppAlertTrigger    | newrelic  | WebAppAlertTrigger        |                                                                                 |
    | newrelic.WebAppNormalTrigger   | newrelic  | WebAppNormalTrigger       |                                                                                 |
    | newrelic.ServerAlertTrigger    | newrelic  | ServerAlertTrigger        |                                                                                 |
    | newrelic.ServerNormalTrigger   | newrelic  | ServerNormalTrigger       |                                                                                 |
    | dripstat.alert                 | dripstat  | alert                     | Trigger representing an active alert                                            |
    +--------------------------------+-----------+---------------------------+---------------------------------------------------------------------------------+


To learn more about Sensors/Triggers, check the :doc:`sensors` page.

Criteria
--------

Rule criteria are the rule(s) needed to be matched against (logical ``AND``). Criteria in the rule
are expressed as:

.. code-block:: yaml

        # more variables
        criteria:
            trigger.payload_parameter_name1:
                type: "regex"
                pattern : "^value$"
            trigger.payload_parameter_name2:
                type: "iequals"
                pattern : "watchevent"

.. note::

    You can achieve logical ``OR`` behavior (any one of multiple criteria expressions needs to
    match for the action execution to be triggered) by creating multiple independent rules (one per
    criteria expression).

``type`` specifies which criteria comparison operator to use and ``pattern`` specifies a pattern
which gets passed to the operator function.

In the ``regex`` case, ``pattern`` is a regular expression pattern which the trigger value
needs to match.

A list of all the available criteria operators is described below. 

If the criteria key contains any special characters (like ``-``) then use the dictionary lookup
format for specifying the criteria key. In case of a webhook based rule it is typical for the
header of the posted event to contain such values:

.. code-block:: yaml

    criteria:
        trigger.headers['X-Custom-Header']:
            type: "eq"
            pattern : "customvalue"

The ``pattern`` value can also reference a datastore value using Jinja variable access syntax:

.. code-block:: yaml

    criteria:
        trigger.payload.build_number:
            type: "equals"
            pattern : "{{ st2kv.system.current_build_number }}"

In this example we are referencing the value of a datastore item with the name
``current_build_number``.

.. warning::

    Each criteria key must be unique.

Due to a `known <https://github.com/yaml/pyyaml/issues/41>`_,
`reported <https://github.com/yaml/pyyaml/issues/165>`_ issue in PyYAML, criteria keys must be
unique. This sometimes becomes relevant when you want to apply different operators (like
``contains`` and ``ncontains``) to the same trigger data:

.. code-block:: yaml

    criteria:
        trigger.payload.commit.tags:  # duplicate key - ignored!
          type: ncontains
          pattern: StackStorm
        trigger.payload.commit.tags:  # duplicate key - evaluated
          type: contains
          pattern: pull request
        trigger.payload.commit.message:  # unique key - evaluated
          type: ncontains
          pattern: ST2

In this example, only the last of the duplicate keys in the criteria will be evaluated.

As a workaround, criteria tags can be used to refer to the same criteria key multiple times. Criteria tags make
a key unique and can provide context to the criteria. To create a criteria tag, include a ``#`` symbol 
and some text at the end of the criteria key. On evaluation the ``#`` and the text after the ``#`` will be ignored.
(e.g. ``trigger.payload.level#upper``, ``trigger.payload.level#lower``):

.. code-block:: yaml

    criteria:
        trigger.payload.commit.tags#1:
          type: ncontains
          pattern: StackStorm
        trigger.payload.commit.tags#2:
          type: contains
          pattern: pull request
        trigger.payload.commit.message:
          type: ncontains
          pattern: ST2

In this example, since the criteria keys are all unique, all of them will be evaluated, even though
``trigger.payload.commit.tags#1`` and ``trigger.payload.commit.tags#2`` specify the same value in
the trigger data.

Criteria Comparison
-------------------

This section describes all the available operators which can be used in the criteria.

.. note::

    **For Developers:** The criteria comparison functions are defined in
    :github_st2:`st2/st2common/st2common/operators.py <st2common/st2common/operators.py>`.

================= =================================================================
 Operator          Description
================= =================================================================
``equals``        Values are equal (for values of arbitrary type).
``nequals``       Values are not equal (for values of arbitrary type).
``lessthan``      Trigger value is less than the provided value.
``greaterthan``   Trigger value is greater than the provided value.
``matchwildcard`` Trigger value matches the provided wildcard-like string. This
                  operator provides support for Unix shell-style wildcards which
                  means you can use characters such as ``*`` and ``?``. This
                  operator is preferred over ``regex`` for simple string
                  matches.
``regex``         Trigger value matches the provided regular expression
                  pattern. This operator behaves like
                  ``re.search('pattern', trigger_value)``.
``iregex``        Trigger value matches the provided regular expression
                  pattern case insensitively. This operator behaves like
                  ``re.search('pattern', trigger_value, re.IGNORECASE)``.
``matchregex``    Trigger value matches the provided regular expression
                  pattern. This operator is deprecated in favor of ``regex`` and
                  ``iregex``
``iequals``       String trigger value equals the provided value case
                  insensitively.
``contains``      Trigger value contains the provided value. Keep in mind that
                  the trigger value can be either a string or an array (list).
``ncontains``     Trigger value does not contain the provided value. Keep in mind
                  that the trigger value can be either a string or an array (list).
``icontains``     String trigger value contains the provided value case
                  insensitively.
``incontains``    String trigger value does not contain the provided string
                  value case insensitively.
``startswith``    Beginning of the string trigger value matches the provided
                  string value.
``istartswith``   Beginning of the string trigger value matches the provided
                  string value case insensitively.
``endswith``      End of the string trigger value matches the provided string
                  value.
``iendswith``     End of the string trigger value matches the provided string
                  value case insensitively.
``timediff_lt``   Time difference between trigger value and current time is
                  less than the provided value.
``timediff_gt``   Time difference between trigger value and current time is
                  greater than the provided value.
``exists``        Key exists in payload.
``nexists``       Key doesn't exist in payload.
``inside``        Trigger payload is inside provided value. (e.g. testing if
                  "``trigger.payload`` in ``provided_value``"). Reverse of ``contains``.
                  (where ``contains`` would test for "``trigger.payload`` contains
                  ``provided_value``").
``ninside``       Trigger payload is not inside provided value. (e.g. testing if
                  "``trigger.payload`` not in ``provided_value``"). Reverse of
                  ``ncontains`` (where ``contains`` would test for "``trigger.payload``
                  does not contain ``provided_value``").
``search``        Search an array (list) in the trigger payload that matches child
                  criteria.
                  See the `Advanced Comparison`_ section for more information and
                  examples.
================= =================================================================

Advanced Comparison
-------------------

.. warning::

    The ``search`` operator has some complexity and performance caveats to using
    it. Ensure that you understand all of the implications before attempting to use it.
    Remember that it is very easy to create complex criteria or a slow rule when you use
    it. See the `Search Operator Caveats`_ subsection below for more.

The ``search`` operator is slightly more complex than any of the other operators. It
takes an additional ``condition`` parameter as well as additional nested criteria that it
applies to each element of the search list.

The ``condition`` parameter controls how the ``search`` operator matches the list.
With the ``any`` condition, if *at least one* item in the trigger payload list matches
all of the child criteria, the search operator will return a successful match.
With the ``all`` condition, every single item in the trigger payload list
must match all of the child criteria for the search operator to return a successful
match. The ``any2any`` condition returns a successful match if any payload items matches any criteria items.
Finally, the ``all2any`` condition, returns a successful match if all payload items matches any criteria items.

Here's an example criteria that uses the ``search`` operator with the ``any`` condition:

.. code-block:: yaml

    ---
    criteria:
      trigger.issue_fields:
        type: "search"
        # Controls whether all items in the trigger payload must match the child criteria,
        # or if any single item matching the child criteria is sufficient
        condition: any  # <- *At least one* item must match all child patterns
        pattern:
          # Here our context is each item of the list
          # All of these patterns must match the item for the item to be considered a match
          # These are simply other operators applied to each item of the list
          item.field_name:
            type: "equals"
            pattern: "Status"

          item.to_value:
            type: "equals"
            pattern: "Approved"

This criteria would match the following trigger payload, because the ``Status`` field was
changed to ``Approved``:

.. code-block:: json

    {
      "issue_fields": [
        {
          "field_type": "Custom",
          "field_name": "Status",
          "to_value": "Approved"
        }, {
          "field_type": "Custom",
          "field_name": "Signed off by",
          "to_value": "Stanley"
        }
      ]
    }

Here's another example where the ``condition`` parameter is ``all``, in which case all of the items in the list
must match all of the child pattern:

.. code-block:: yaml

    ---
    criteria:
      trigger.issue_fields:
        type: "search"
          condition: all  # <- *All* items must match all patterns
          pattern:
            item.field_type:
              type: "equals"
              pattern: "Custom"

That criteria would also match the trigger payload from above.

However, the following trigger payload would not match with the ``all`` condition because the
``Summary`` field is not a custom field:

.. code-block:: json

    {
      "issue_fields": [
        {
          "field_type": "Built-in",
          "field_name": "Summary",
          "to_value": "Lorem Ipsum"
        }, {
          "field_type": "Custom",
          "field_name": "Status",
          "to_value": "Approved"
        }, {
          "field_type": "Custom",
          "field_name": "Signed off by",
          "to_value": "Stanley"
        }
      ]
    }

Here's an example where the ``condition`` parameter is ``any2any``.
This will return true in cases where any payload items match any part of the pattern.
This example uses Criteria Tags described in the `Criteria`_ section above.

.. code-block:: yaml

    ---
    criteria:
      trigger.body.data.tank:
        type: "search"
        condition: any2any
        pattern:
          item.chemicalLevel#1:
            type: "lessthan"
            pattern: 40
          item.chemicalLevel#2:
            type: "greaterthan"
            pattern: 50

Payload:

.. code-block:: json

    {
      "tanks": [
        {
          "id": 1,
          "chemicalLevel": 43
        }, {
          "id": 2,
          "chemicalLevel": 55
        }
      ]
    }

Since the second tank has a chemical level over 50, this criteria resolves to true
and the action, such as a notification sent to the operator, will be triggered.
If the second tank had a chemical level of 45, the criteria would resolve to false and no action
would occur.

Here's an example where the ``condition`` parameter is ``all2any``.
This will return true in cases where all payload items match any part of the pattern:

.. code-block:: yaml

    ---
    criteria:
      trigger.body.data.equipment:
        type: "search"
        condition: all2any
        pattern:
          item.latitude.value#1:
            type: "lessthan"
            pattern: 40
          item.latitude.value#2:
            type: "greaterthan"
            pattern: 50
          item.longitude.value#1:
            type: "lessthan"
            pattern: -100
          item.longitude.value#2:
            type: "greaterthan"
            pattern: -90

Payload:

.. code-block:: json

    {
    
      "equipment": [
        {
          "latitude": {
            "value": 43
          }
          "longitude": {
            "value": -95
          }
        }, {
          "latitude": {
            "value": 44
          }
          "longitude": {
            "value": -96
          }
        }
      ]
    }

In this example all of the equipment coordinates are within the ranges specified by the criteria
and no action would be taken. If the first equipment latitude were set to 53, there would still
be no action. If say the second equipment longitude value were set to -106 then the action would
trigger because ALL of the equipment would be violating at least one of the parts of the pattern.
This could trigger a notification when the last equipment leaves an area.


Single Payload Mode:
If only a single element is expected in the payload the search parameter can still be used to test the criteria of a rule
if the payload is a dictionary.

Criteria:

.. code-block:: yaml

    ---
    criteria:
      trigger.body.data:
        type: "search"
        condition: all2any
        pattern:
          item.latitude.value#1:
            type: "lessthan"
            pattern: 40
          item.latitude.value#2:
            type: "greaterthan"
            pattern: 50
          item.longitude.value#1:
            type: "lessthan"
            pattern: -100
          item.longitude.value#2:
            type: "greaterthan"
            pattern: -90

Payload:

.. code-block:: json

    {
      "data": {
        "latitude": {
          "value": 43
        }
        "longitude": {
          "value": -95
        }
      }
    }

.. warning::

    When using Single Payload Mode, all2any and any2any has the same result since picking all of one thing is the 
    same as picking any of one thing.

The search operator is very powerful, but more options for the ``condition`` parameter are
possible. At this point, only the ``any``, ``all``, ``any2any`` and ``all2any`` conditions are implemented, but
future improvements could include:

* ``count``
* ``count_gt``
* ``count_gte``
* ``count_lt``
* ``count_lte``

Search Operator Caveats
~~~~~~~~~~~~~~~~~~~~~~~

The ``search`` operator has some caveats regarding its usage.

First, it turns the rules engine into a recursive descent parser, which can reduce
the performance of the rules engine. So if you have a rule that must remain fast regardless
of system load, you should avoid using the ``search`` operator unless you absolutely have
to.

Second, the cognitive complexity of the ``search`` operator makes it a little difficult to
grasp at a glance. If you are sharing your code with others you may need to extensively
document your rules and patterns to explain your intent more clearly.

Lastly, the algorithmic complexity of the ``search`` operator is much different
than the other operators:

* O(n\ :sub:`patterns`) in terms of n\ :sub:`patterns`, the number of child patterns
* O(n\ :sub:`payloads`) in terms of n\ :sub:`payloads`, the number of trigger payload fields

However, it has O(n\ :sub:`patterns` * n\ :sub:`payloads`) algorithmic complexity overall.

It is therefore **very easy to write a slow rule when using this operator** if you have a
large number of child criteria or if you are searching through a long list in your trigger
payload.

Usage of the ``search`` operator should largely be limited to trying to match a small number
of child criteria, and a small number of expected payload list items. However, as slow as
the ``search`` operator might make the rules engine, it will still be faster and more
lightweight to use the ``search`` operator in your rules than it would be to run the rules
engine, unconditionally run a workflow, and do the filtering there.

Action
------

This section describes the subsequent action/workflow to be executed on successful match of a
trigger and an optional set of criteria. At a minimum, a rule should specify the action to
execute. A rule can also specify parameters that will be supplied to an action upon execution.

.. code-block:: yaml

        action:                                # required
            ref: "action_ref"
            parameters:                        # optional
                foo: "bar"
                baz: 1

Variable Interpolation
----------------------

Occasionally, it will be necessary to pass along context of a trigger to an action when a rule is \
matched. The rules engine is able to interpolate variables by leveraging `Jinja templating syntax
<http://jinja.pocoo.org/docs/dev/templates/>`__.

.. code-block:: yaml

        action:
            ref: "action_ref"
            parameters:
                foo: "bar"
                baz: "{{ trigger.payload_parameter_1 }}"

.. note::

    The value of a trigger attribute can be ``null`` and ``None``. It is also a valid value of the action parameter in question. You need to use the ``use_none`` Jinja template filter to make sure that ``null``/``None`` values are correctly serialized when invoking an action.

.. code-block:: yaml

            action:
                ref: "action_ref"
                parameters:
                    foo: "bar"
                    baz: "{{ trigger.payload_parameter_1 | use_none }}"

This workaround is required because of the limitation of our current Jinja templating system which
doesn't support non-string types. We are forced to perform type casting based on the action
parameters definition before invoking an action.

Managing Rules
--------------

To deploy a rule, use the CLI command: ``st2 rule create ${PATH_TO_RULE}``,  for example:

.. code-block:: bash

    st2 rule create /usr/share/doc/st2/examples/rules/sample_rule_with_webhook.yaml

To reload all rules, use ``st2ctl reload --register-rules``.

If a rule with the same name already exists, the above command will return an error:

.. code-block:: bash

    ERROR: 409 Client Error: Conflict
    MESSAGE: Tried to save duplicate unique keys (E11000 duplicate key error index: st2.rule_d_b.$uid_1  dup key: { : "rule:examples:sample_rule_with_webhook" })

To update a rule, edit the rule definition file and run the command: ``st2 rule update``, as in
the following example:

.. code-block:: bash

    st2 rule update examples.sample_rule_with_webhook /usr/share/doc/st2/examples/rules/sample_rule_with_webhook.yaml

.. note::

    **Hint:** It is a good practice to always edit the original rule file, so that keep your infrastructure in code. You still can get the rule definition from the system by ``st2 rule get <rule name> -j``, update it, and load it back.

To see all rules, or to get an individual rule, use commands below:

.. code-block:: bash

    st2 rule list
    st2 rule get examples.sample_rule_with_webhook

To undeploy a rule, run ``st2 rule delete ${RULE_NAME_OR_ID}``. For example, to undeploy the
``examples.sample_rule_with_webhook`` rule we deployed previously, run:

.. code-block:: bash

    st2 rule delete examples.sample_rule_with_webhook


Rule Location
-------------

Custom rules can be placed in any accessible folder on the local system. By convention, custom rules
are placed in the ``/opt/stackstorm/packs/<pack_name>/rules`` directory. 

.. _testing-rules:

Testing Rules
-------------

To make testing rules easier, we provide a ``st2-rule-tester`` tool which can evaluate rules against
trigger instances without running any of the |st2| components.

The tool works by taking a path to the file which contains the rule definition and a file which
contains a trigger instance definition:

.. code-block:: bash

    st2-rule-tester --rule=${RULE_FILE} --trigger-instance=${TRIGGER_INSTANCE_DEFINITION} --config-file=/etc/st2/st2.conf
    echo $?

Both files need to contain definitions in YAML or JSON format. For the rule, you can use the same
file you are planning to deploy.

For the trigger instance, the definition file needs contain the following keys:

* ``trigger`` - Full reference to the trigger (e.g. ``core.st2.IntervalTimer``,
  ``slack.message``, ``irc.pubmsg``, ``twitter.matched_tweet``, etc.).
* ``payload`` - Trigger payload. The payload itself is specific to the trigger in question. To
  figure out the trigger structure you can look at the pack README or look for the
  ``trigger_types`` section in the sensor metadata file which is located in the
  ``packs/<pack_name>/sensors/`` directory.

If the trigger instance matches, ``=== RULE MATCHES ===`` will be printed and the tool will exit
with ``0`` status code. If the rule doesn't match, ``=== RULE DOES NOT MATCH ===`` will be printed
and the tool will exit with status code ``1``.

Here are some examples of how to use the tool:

``my_rule.yaml``:

.. code-block:: yaml

    ---
      name: "relayed_matched_irc_message"
      pack: "irc"
      description: "Relay IRC message to Slack if the message contains word StackStorm"
      enabled: true

      trigger:
        type: "irc.pubmsg"
        parameters: {}

      criteria:
          trigger.message:
              type: "icontains"
              pattern: "StackStorm"

      action:
        ref: "slack.post_message"
        parameters:
            message: "{{ trigger.source.nick }} on {{ trigger.channel }}: {{ trigger.message }}"
            channel: "#irc-relay"

``trigger_instance_1.yaml``:

.. code-block:: yaml

    ---
        trigger: "irc.pubmsg"
        payload:
          source:
              nick: "Kami_"
              host: "gateway/web/irccloud.com/x-uvv"
          channel: "#stackstorm"
          timestamp: 1419166748,
          message: "stackstorm is cool!"

``trigger_instance_2.yaml``:

.. code-block:: yaml

    ---
        trigger: "irc.pubmsg"
        payload:
          source:
              nick: "Kami_"
              host: "gateway/web/irccloud.com/x-uvv"
          channel: "#stackstorm"
          timestamp: 1419166748,
          message: "blah blah"

.. code-block:: bash

    st2-rule-tester --rule=./my_rule.yaml --trigger-instance=./trigger_instance_1.yaml
    echo $?

Output:

.. code-block:: bash

    2015-12-11 14:35:03,249 INFO [-] Connecting to database "st2" @ "0.0.0.0:27017" as user "None".
    2015-12-11 14:35:03,318 INFO [-] Validating rule irc.relayed_matched_irc_message for pubmsg.
    2015-12-11 14:35:03,331 INFO [-] 1 rule(s) found to enforce for pubmsg.
    2015-12-11 14:35:03,333 INFO [-] === RULE MATCHES ===
    0

.. code-block:: bash

    st2-rule-tester --rule=./my_rule.yaml --trigger-instance=./trigger_instance_2.yaml
    echo $?

Output:

.. code-block:: bash

    2015-12-11 14:35:57,380 INFO [-] Connecting to database "st2" @ "0.0.0.0:27017" as user "None".
    2015-12-11 14:35:57,444 INFO [-] Validating rule irc.relayed_matched_irc_message for pubmsg.
    2015-12-11 14:35:57,459 INFO [-] Validation for rule irc.relayed_matched_irc_message failed on -
      key: trigger.message
      pattern: StackStorm
      type: icontains
      payload: blah blah
    2015-12-11 14:35:57,461 INFO [-] 0 rule(s) found to enforce for pubmsg.
    2015-12-11 14:35:57,462 INFO [-] === RULE DOES NOT MATCH ===
    1


.. _ref-rule-tester-post-mortem-debug:

``st2-rule-tester`` further allows a kind of post-mortem debugging where you can answer the
question ``Why did my rule not match the trigger that just fired?``. This means there is a known
``Rule`` identifiable by its reference loaded in |st2| and similarly a TriggerInstance with a
known id.

Lets say we have rule reference ``my_pack.fire_on_execution`` and a trigger instance
``566b4be632ed352a09cd347d``:

.. code-block:: bash

    st2-rule-tester --rule-ref=my_pack.fire_on_execution --trigger-instance-id=566b4be632ed352a09cd347d --config-file=/etc/st2/st2.conf
    echo $?

Output:

.. code-block:: bash

    2015-12-11 15:24:16,459 INFO [-] Connecting to database "st2" @ "0.0.0.0:27017" as user "None".
    2015-12-11 15:24:16,527 INFO [-] Validating rule my_pack.fire_on_execution for st2.generic.actiontrigger.
    2015-12-11 15:24:16,542 INFO [-] Validation for rule my_pack.fire_on_execution failed on -
      key: trigger.status
      pattern: succeeded
      type: iequals
      payload: failed
    2015-12-11 15:24:16,545 INFO [-] 0 rule(s) found to enforce for st2.generic.actiontrigger.
    2015-12-11 15:24:16,546 INFO [-] === RULE DOES NOT MATCH ===


The output also identifies the source of the mismatch i.e. whether it was the trigger type that
did not match or one of the criteria.

If you are debugging and would like to see the list of trigger instances sent to |st2|,
you can use the CLI:

.. code-block:: bash

  st2 trigger-instance list

You can also filter trigger instances by trigger:

.. code-block:: bash

  st2 trigger-instance list --trigger=core.f9e09284-b2b1-4127-aedd-dcde7a752819

Also, you can get trigger instances within a time range by using ``timestamp_gt`` and
``timestamp_lt`` filter options:

.. code-block:: bash

  st2 trigger-instance list --trigger="core.f9e09284-b2b1-4127-aedd-dcde7a752819" -timestamp_gt=2015-06-01T12:00:00Z -timestamp_lt=2015-06-02T12:00:00Z

Note that you can also specify one of ``timestamp_lt`` or ``timestamp_gt`` too. You can get
details about a trigger instance by using ``get``:

.. code-block:: bash

  st2 trigger-instance get 556e135232ed35569ff23238

Something that might be useful in debugging a rule is to re-send a trigger instance into |st2|. You
can use the ``re-emit`` command for that.

.. code-block:: bash

  st2 trigger-instance re-emit 556e135232ed35569ff23238

.. _ref-rule-timers:

Timers
------

Timers allow running a particular action repeatedly based on a defined time interval, or at one
particular date and time. You can think of them as cron jobs, but with additional flexibility,
e.g. the ability to run actions only once, at the provided date and time.

Currently, we support the following timer trigger types:

* ``core.st2.IntervalTimer`` - Run an action at predefined time intervals (e.g. every 30 seconds,
  every 24 hours, every week, etc.).
* ``core.st2.DateTimer`` - Run an action at the specified date and time.
* ``core.st2.CronTimer`` - Run an action when current time matches the time constraint
  defined in UNIX cron format.

Timers are implemented as triggers, which means you can use them inside the rules. In the section
below, you can find some examples of how to use timers in the rule definitions.

core.st2.IntervalTimer
~~~~~~~~~~~~~~~~~~~~~~

Available parameters:``unit``, ``delta``.

Supported values for ``unit`` parameter: ``seconds``, ``minutes``, ``hours``, ``days``, ``weeks``.

Run action every 30 seconds
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.IntervalTimer"
    parameters:
        unit: "seconds"
        delta: 30

  action:
    ...

Run action every 24 hours
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.IntervalTimer"
    parameters:
        unit: "hours"
        delta: 24

  action:
    ...

Run action every 2 weeks
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.IntervalTimer"
    parameters:
        unit: "weeks"
        delta: 2

  action:
    ...

core.st2.DateTimer
~~~~~~~~~~~~~~~~~~

Available parameters: ``timezone``, ``date``.

Run action on a specific date
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.DateTimer"
    parameters:
        timezone: "UTC"
        date: "2014-12-31 23:59:59"

  action:
    ...

core.st2.CronTimer
~~~~~~~~~~~~~~~~~~

This timer supports cron-like expressions. For a full list of supported expressions, please see
http://apscheduler.readthedocs.org/en/3.0/modules/triggers/cron.html#api.

By default, if no value is provided for a particular parameter, ``*`` is assumed, which means
fire on every value.

.. note::

    Unlike with cron where the first day (``0``) in ``day_of_week`` is a Sunday, in |st2| CronTimer
    first day of the week is always Monday. To make it more explicit and avoid confusion, you are
    encouraged to use the name of the weekdays instead (e.g. ``mon-fri`` instead of ``0-4``, or in
    cron case, ``1-5``).

Available parameter ``timezone``, ``year``, ``month``, ``day``, ``week``, ``day_of_week``,
``hour``, ``minute``, ``second``.
Note ``timezone`` use the pytz format, e.g. ``Asia/Shanghai``.

Run action every Sunday at midnight
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.CronTimer"
    parameters:
        timezone: "UTC"
        day_of_week: 6 # or day_of_week: "sun"
        hour: 0
        minute: 0
        second: 0

  action:
    ...

Run action every day at midnight
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.CronTimer"
    parameters:
        timezone: "UTC"
        day_of_week: "*"
        hour: 0
        minute: 0
        second: 0

  action:
    ...

As noted above, ``*`` is assumed if no value is provided for a particular parameter, which means
the following is equivalent to the above:

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.CronTimer"
    parameters:
        timezone: "UTC"
        hour: 0
        minute: 0
        second: 0

  action:
    ...

Run action Monday through Friday (every day except weekends) at midnight
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.CronTimer"
    parameters:
        timezone: "UTC"
        day_of_week: "mon-fri"
        hour: 0
        minute: 0
        second: 0

  action:
    ...

Run action every full hour every day of the week
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

  ---
  ...

  trigger:
    type: "core.st2.CronTimer"
    parameters:
        timezone: "UTC"
        hour: "*"
        minute: 0
        second: 0

  action:
    ...


Troubleshooting Rule Enforcements
---------------------------------

Rules not working as expected? Or just want to see which rules have been enforced? 

Run ``st2 rule-enforcement list`` to see all rule enforcements. You can filter this output by rule to narrow it down.

For further troubleshooting steps, check the :doc:`Rules Troubleshooting </troubleshooting/rules>` documentation.

-------------------------------

.. rubric:: What's Next?

* Explore automations in the `StackStorm Exchange <https://exchange.stackstorm.org>`_.
* Learn more about :doc:`sensors`.
* Check out `tutorials on stackstorm.com <https://stackstorm.com/category/tutorials/>`__ - a
  growing set of practical examples of automating with |st2|.
