Jinja
=====

|st2| uses `Jinja <http://jinja.pocoo.org/>`_ extensively for templating. Jinja allows you to
manipulate parameter values in |st2| by allowing you to refer to other parameters, applying filters
or refer to system specific constructs (like datastore access). This document is here to help you
with Jinja in the context of |st2|. Please refer to the `Jinja docs 
<http://jinja.pocoo.org/docs/>`_ for Jinja-focused information.

.. _applying-filters-with-jinja:

Referencing Datastore Keys in Jinja
------------------------------------

You can use ``{{st2kv.system.foo}}`` to access key ``foo`` from datastore. Note that until
v2.1, the expression to access key ``foo`` from datastore used to be ``{{system.foo}}``
but is now deprecated, and the leading ``st2kv.`` namespace is required.

.. _jinja-jinja-filters:

Applying Filters with Jinja
----------------------------

To use a filter ``my_filter`` on ``foo``, you use the pipe operator, e.g.: ``{{foo | my_filter}}``.
Please pay attention to the data type and available filters for each data type. Since Jinja is a
text templating language, all your input is converted to text and then manipulations happen on that
value. The necessary casting at the end is done by |st2| based on information you provide in YAML
(for example, ``type`` field in action parameters). The casting is a best-effort casting.

|st2| supports `Jinja variable templating <http://jinja.pocoo.org/docs/dev/templates/#variables>`__
in Rules, Action Chains, and Actions etc. Jinja templates support
`filters <http://jinja.pocoo.org/docs/dev/templates/#list-of-builtin-filters>`__
to allow some advanced capabilities in working with variables.

.. _referencing-datastore-keys-in-jinja:

Custom Jinja Filters
--------------------

In addition to the `standard filters <http://jinja.pocoo.org/docs/dev/
templates/#builtin-filters>`_ available in Jinja, |st2| also comes with some custom filters.

**For Developers:** These filters are defined in
:github_st2:`st2/st2common/st2common/jinja/filters/ </st2common/st2common/jinja/filters/>`.
The equivalent Mistral filters are located in the ``st2mistral`` repo at
:github_st2mistral:`st2mistral/st2mistral/filters/ </st2mistral/st2mistral/filters/>`.
To ensure filters maintain parity across StackStorm workflows, changes to one location must be
replicated to the other in a separate PR.

For brevity, only simple Jinja patterns for each filter are documented below. "Real-world" usage
will depend on the type of content where the filters are being applied (sensors, triggers, rules,
action and workflows) and their syntax. More detailed examples can be found in the ActionChains
in the ``examples`` pack:
:github_st2:`st2/contrib/examples/actions/chains/ </contrib/examples/actions/chains/>`.

..  TODO We should consider separating each specific usage into individual ActionChains and refer to
    it using literalinclude (i.e. .. literalinclude:: /../../st2/contrib/examples/actions/workflows/mistral-jinja-branching.yaml)
    so we can just use the code as the source of truth. Then, we can remove the above note.

In |st2| 2.4, all custom filters were made available to Mistral workflows as well, with one notable
exception: the ``decrypt_kv`` filter. That filter is not necessary in Mistral, as the ``st2kv``
function in Mistral workflows natively supports decryption via the ``decrypt`` parameter.

.. note::

    Because of a bug in Mistral, these filters do not currently support the "pipe" operator filter
    format (`|`) So, instead of ``'{{ _.input_str | regex_match(_.regex_pattern)}}'`` you would
    call the filter like a regular function, moving the previously input value into the first
    positional argument position: ``'{{ regex_match(_.input_str, _.regex_pattern)}}'``. This will
    be addressed in a future release.


json_escape
~~~~~~~~~~~

Adds escape characters to JSON strings.

.. code-block:: bash

    {{value_key | json_escape}}

regex_match
~~~~~~~~~~~

Search for the pattern at beginning of the string. Returns True if found, False if not.

.. code-block:: bash

    {{value_key | regex_match('x')}}
    {{value_key | regex_match("^v(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)$")}}

regex_replace
~~~~~~~~~~~~~

Replaces substring that matches pattern with provided replacement value (backreferences possible).

.. note::

    When using backreferences you need to escape two \\'s in Jinja, hence the 4 \\'s.

.. code-block:: bash

    {{value_key | regex_replace("x", "y")}}
    {{value_key | regex_replace("(blue|white|red)", "beautiful color \\\\1")}}

regex_search
~~~~~~~~~~~~

Search for pattern anywhere in the string. Returns True if found, False if not.

.. code-block:: bash

    {{value_key | regex_search("y")}}
    {{value_key | regex_search("^v(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)$")}}

regex_substring
~~~~~~~~~~~~~~~

Searches for the provided pattern in a string, and returns the first matched regex group
(alternatively, you can provide the desired index). 

.. code-block:: bash

    {{value_key | regex_substring("y")}}
    {{value_key | regex_substring("^v(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)$")}}

to_complex
~~~~~~~~~~

Convert data to JSON string (see ``to_json_string`` for a more flexible option)

.. code-block:: bash

    {{value_key | to_complex}}

to_human_time_from_seconds
~~~~~~~~~~~~~~~~~~~~~~~~~~

Given time elapsed in seconds, this filter converts it to human readable form like 3d5h6s.

.. code-block:: bash

    {{ value_key | to_human_time_from_seconds}}

to_json_string
~~~~~~~~~~~~~~

Convert data to JSON string.

.. code-block:: bash

    {{value_key | to_json_string}}

to_yaml_string
~~~~~~~~~~~~~~

Convert data to YAML string.

.. code-block:: bash

    {{value_key | to_yaml_string}}

use_none
~~~~~~~~

If value being filtered is None, this filter will return the string ``%*****__%NONE%__*****%``

.. code-block:: bash

    {{value_key | use_none}}

version_bump_major
~~~~~~~~~~~~~~~~~~

Bumps up the major version of supplied version field.

.. code-block:: bash

    {{version | version_bump_major}}

version_bump_minor
~~~~~~~~~~~~~~~~~~

Bumps up the minor version of supplied version field.

.. code-block:: bash

    {{version | version_bump_minor}}

version_bump_patch
~~~~~~~~~~~~~~~~~~

Bumps up the patch version of supplied version field.

.. code-block:: bash

    {{version | version_bump_patch}}

version_compare
~~~~~~~~~~~~~~~

Compare a semantic version to another value. Returns 1 if LHS is greater or -1 if LHS is smaller or
0 if equal.

.. code-block:: bash

    {{version | version_compare("0.10.1")}}

version_equal
~~~~~~~~~~~~~

Returns True if LHS version is equal to RHS version.

.. code-block:: bash

    {{version | version_equal("0.10.0")}}

version_less_than
~~~~~~~~~~~~~~~~~

Returns True if LHS version is lesser than RHS version. Both inputs have to follow semantic version
syntax.

E.g. ``{{“1.6.0” | version_less_than("1.7.0")}}``.

.. code-block:: bash

    {{version | version_less_than("0.9.2")}}

version_match
~~~~~~~~~~~~~

Returns True if the two provided versions are equivalent (i.e. “2.0.0” and “>=1.0.0” are
equivalent and will return True).

Supports operators ``>``, ``<``, ``==``, ``<=``, and ``>=``.

.. code-block:: bash

    {{version | version_match(">0.10.0")}}

version_more_than
~~~~~~~~~~~~~~~~~

Returns True if LHS version is greater than RHS version. Both inputs have to follow semantic
version syntax.

E.g. ``{{"1.6.0” | version_more_than("1.7.0")}}``.

.. code-block:: bash

    {{version | version_more_than("0.10.1")}}

version_strip_patch
~~~~~~~~~~~~~~~~~~~

Drops patch version of supplied version field.

.. code-block:: bash

    {{version | version_strip_patch}}
