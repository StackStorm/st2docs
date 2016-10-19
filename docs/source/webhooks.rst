Webhooks
========

Webhooks allow you to integrate external systems with |st2| using HTTP
webhooks. Unlike sensors which use a "pull" approach, webhooks use a "push"
approach. This means they work by you pushing triggers directly to the |st2|
API using HTTP POST requests.

Sensors vs Webhooks
-------------------

Sensors integrate with external systems and services using a poll approach
(sensors periodically reach out to an external system to retrieve data you are
interested in) and webhooks use a push approach (your systems push data to the
|st2| API when an event you are interested in occurs).

Sensors are the preferred integration method since they offer a more granular and
tighter integration.

On the other hand, webhooks come in handy when you have an existing script or
software which you can easily modify to send a webhook to the |st2| API when an
event you are interested in occurs.

Another example where webhooks come handy is when you want to consume events
from a 3rd party service which already offer webhooks integration - e.g. GitHub

Authentication
--------------

All the requests to the /webhooks endpoints needs to be authenticated in the
same way as other API requests. There are two possible authentication approaches - API
keys and tokens. API keys are recommended for webhooks, as they do not expire. Tokens
have a fixed expiry.

API key-based
~~~~~~~~~~~~~

* `Header` : ``St2-Api-Key``
* `Query parameter` : ``?st2-api-key``

Token-based
~~~~~~~~~~~

* `Header` : ``X-Auth-Token``
* `Query parameter` : ``?x-auth-token``


Both methods above support providing the authentication material as a header or query parameter.
A header is usually used with your scripts where you can control request headers while query
parameters are used with 3rd party services such as GitHub where you can only specify a URL.

Request Body
------------

The request body or so called trigger payload can be either JSON or URL encoded form data. The body type
is determined based on the value of the ``Content-Type`` header (``application/json`` for JSON and
``application/x-www-form-urlencoded`` for URL encoded form data).

All the examples below assume JSON and as such, provide ``application/json`` for the
``Content-Type`` header value.

Registering a Webhook
---------------------

You can register a webhook in |st2| by specifying ``core.st2.webhook``
trigger inside a rule definition.

Here is an excerpt from a rule which registers a new webhook named ``sample``:

.. sourcecode:: yaml

    ...
    trigger:
            type: "core.st2.webhook"
            parameters:
                url: "sample"
    ...

Once this rule is created, you can use this webhook by POST-ing data to
``/v1/webhooks/sample``. The request body needs to be JSON and can contain
arbitrary data which you can match against in the rule criteria.

Note that all trailing and leading ``/`` of the ``url`` parameter are ignored by
|st2|. e.g. a value of ``/sample``, ``sample/``, ``/sample/`` and ``sample`` are
all treated the same i.e. considered identical.

POST-ing data to a custom webhook will cause a trigger with the following
attributes to be dispatched:

* ``trigger`` - Trigger name.
* ``trigger.headers`` - Dictionary containing the request headers.
* ``trigger.body`` - Dictionary containing the request body.

This example shows how to send data to a custom webhook using
cURL and how to match on this data using rule criteria:

.. sourcecode:: bash

    curl -X POST https://localhost/api/v1/webhooks/sample -H "X-Auth-Token: matoken" -H "Content-Type: application/json" --data '{"key1": "value1"}'

Rule:

.. sourcecode:: yaml

    ...
    trigger:
            type: "core.st2.webhook"
            parameters:
                url: "sample"

    criteria:
        trigger.body.key1:
            type: "equals"
            pattern: "value1"

    action:
        ref: "mypack.myaction"
        parameters:
    ...

Using a Generic Webhook
-----------------------

By default, a special-purpose webhook with the name ``st2`` is already registered. Instead
of using ``st2.core.webhook``, it allows you to specify any trigger that is known to |st2|
(either by default or from custom sensors and triggers in packs), so you can use it to
trigger rules that aren’t explicitly set up to be triggered by webhooks.

The body of this request needs to be JSON and must contain the following attributes:

* ``trigger`` - Name of the trigger (e.g. ``mypack.mytrigger``)
* ``payload`` - Object with a trigger payload.

This example shows how to send data to the generic webhook using
cURL, and how to match this data using rule criteria (replace ``localhost`` with your st2 host if call remotely):

.. sourcecode:: bash

    curl -X POST https://localhost/api/v1/webhooks/st2 -H "X-Auth-Token: matoken" -H "Content-Type: application/json" --data '{"trigger": "mypack.mytrigger", "payload": {"attribute1": "value1"}}'

Rule:

.. sourcecode:: yaml

    ...
    trigger:
        type: "mypack.mytrigger"

    criteria:
        trigger.attribute1:
            type: "equals"
            pattern: "value1"

    action:
        ref: "mypack.myaction"
        parameters:
    ...

Keep in mind that the ``trigger.type`` attribute inside the rule definition
needs to be the same as the trigger name defined in the webhook payload body.

Listing Registered Webhooks
---------------------------

To list all registered webhooks, run:

::

    st2 webhook list
