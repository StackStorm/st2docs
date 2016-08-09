Jinja
==============

|st2| uses `Jinja <http://jinja.pocoo.org/>`_ extensively for templating.
By now, you would have seen how to use jinja templates in YAML files for rules,
actions, action chains and workflows. Jinja allows you to manipulate parameter
values in |st2| by allowing you to refer to other parameters, applying filters
or refer to system specific constructs (like datastore access). This document is here to help you with Jinja in the context of |st2|. Please refer to `Jinja docs <http://jinja.pocoo.org/docs/>`_
for Jinja specific documentation.

For brevity, the jinja patterns are only documented. Usage of these patterns inside YAML is subject to understanding the YAML for each content type (sensors, triggers, rules, action and workflows) and their syntax.

Accessing datastore items with Jinja
------------------------------------

You can use ``{{system.foo}}`` to access key ``foo`` from datastore.

Applying filters with Jinja
----------------------------

Aside from `standard filters <http://jinja.pocoo.org/docs/dev/
templates/#builtin-filters>`_ available in Jinja, |st2| supports custom filters
as well. To use a filter ``my_filter`` on ``foo``, simply do
``{{foo | my_filter}}``. Please pay attention to data type and available filters
for each data type. Since Jinja is a text templating language, all your input is
converted to text and then manipulations happen on them. The necessary casting at
the end is done by |st2| based on information you provide in YAML (for example,
``type`` field in action parameters). The casting is a best effort casting.

The current supported filters are grouped into following categories.

.. note::

    **For Developers:** The filters are defined in
    :github_st2:`st2/st2common/st2common/jinja/filters/ </st2common/st2common/jinja/filters/>`.


+--------------------------------+----------------------------------------------------------------+
|      Operator                  |   Description                                                  |
+================================+================================================================+
| ``to_json_string``             | Convert data to JSON string.                                   |
+--------------------------------+----------------------------------------------------------------+
| ``to_yaml_string``             | Convert data to YAML string.                                   |
+--------------------------------+----------------------------------------------------------------+
| ``to_human_time_from_seconds`` | Given time elapsed in seconds, this filter                     |
|                                | converts it to human readable form like                        |
|                                | 3d5h6s.                                                        |
+--------------------------------+----------------------------------------------------------------+
|``version_compare``             | Compare a semantic version to another value.                   |
|                                | Returns 1 if LHS is greater or -1 if LHS is                    |
|                                | smaller or 0 if equal.                                         |
+--------------------------------+----------------------------------------------------------------+
| ``version_more_than``          | Returns if LHS version is greater than RHS                     |
|                                | version. Both input has to follow semantic                     |
|                                | version syntax. E.g. {{"1.6.0" | version_more_than("1.7.0")}}. |
+--------------------------------+----------------------------------------------------------------+
| ``version_less_than``          | Returns if LHS version is lesser than RHS                      |
|                                | version. Both input has to follow semantic                     |
|                                | version syntax. E.g. {{"1.6.0" | version_less_than("1.7.0")}}. |
+--------------------------------+----------------------------------------------------------------+
| ``version_equal_than``         | Returns if LHS version is equal to RHS version.                |
+--------------------------------+----------------------------------------------------------------+
| ``version_bump_major``         | Bumps the major version and returns new                        |
|                                | version.                                                       |
+--------------------------------+----------------------------------------------------------------+
| ``version_bump_minor``         | Bumps the minor version and returns new                        |
|                                | version.                                                       |
+--------------------------------+----------------------------------------------------------------+

Examples of how to use filters are available in
:github_st2:`st2/contrib/examples/actions/chains/data_jinja_filter.yaml </contrib/examples/actions/chains/data_jinja_filter.yaml>`,
:github_st2:`st2/contrib/examples/actions/chains/time_jinja_filter.yaml </contrib/examples/actions/chains/time_jinja_filter.yaml>`
and :github_st2:`st2/contrib/examples/actions/chains/version_jinja_filter.yaml </contrib/examples/actions/chains/version_jinja_filter.yaml>`.
