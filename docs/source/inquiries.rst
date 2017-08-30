Inquiries
===============================

StackStorm 2.4 introduced a new feature that allows you to pause a workflow
to wait for additional information. This is done by using a new action:
``core.ask``. We call these "Inquiries", and the basic premise is to allow you
to "ask a question" in the middle of a workflow. This could be a question like
"do I have approval to continue?" or "what is the second factor I should provide
to this authentication service?"

These use cases (and others) require the ability to pause a workflow mid-execution
and wait for additional information. Inquiries make this possible, and will
be explained in this document. 


New ``core.ask`` Action
----------------------------------------

The primary usage of Inquiries is by referencing a new action - ``core.ask`` - in
your workflows. This action is built on a new runner type: ``inquirer``, which performs
the bulk of the logic required to pause workflows and wait for a response.

.. note::

   NOTE

Using ``core.ask`` in a Workflow
----------------------------------------

.. code-block:: python

    code

Notifying users of Inquiries using Rules
----------------------------------------

    TODO

