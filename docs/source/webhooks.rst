Webhooks
========

Webhooks allow you to integrate external systems with |st2| using HTTP webhooks. Unlike sensors,
which use a "pull" approach, webhooks use a "push" approach. They push triggers directly to the
|st2| API using HTTP POST requests.

## Sensors vs Webhooks

Sensors integrate with external systems using either a polling approach (sensors periodically
connect to an external system to retrieve data) or a passive approach, where they listen on some
port, receiving data using a custom protocol.

Webhooks, in contrast, provide a built-in passive approach for receiving JSON or URL-encoded form
data via HTTP POST. This data must be "pushed" from an external system to |st2| when an event
occurs.

Sensors are the preferred integration method as they offer a more robust and customizable
approach.

However, webhooks are useful when:

- You have an existing script or software that can easily send a webhook to the |st2| API.
- You want to consume events from a third-party service that already supports webhook
  integrations, such as GitHub or Stripe.

## Authentication

All requests to ``/api/v1/webhooks`` must be authenticated, similar to other API requests. You
can use either API keys or tokens:

| **Authentication Method** | **Usage** |
|--------------------------|---------------------------|
| **API Key (Recommended)** | ``St2-Api-Key`` header or ``?st2-api-key`` query parameter |
| **Token-Based** | ``X-Auth-Token`` header or ``?x-auth-token`` query parameter |

API keys are preferred for webhooks as they do not expire, unlike tokens that have a fixed expiry.

Headers are recommended for authentication when using scripts, whereas query parameters are often
used when integrating with third-party services that allow only URL-based authentication.

## Request Body

Webhooks support two types of payload formats:

| **Content-Type** | **Format** |
|-----------------|-------------------------------|
| ``application/json`` | JSON payload |
| ``application/x-www-form-urlencoded`` | URL-encoded form data |

All examples in this documentation assume JSON input.

## Registering a Webhook

To register a webhook in |st2|, you must specify the ``core.st2.webhook`` trigger in a rule
definition.

Example rule registering a webhook named ``sample``:

.. sourcecode:: yaml

    trigger:
        type: "core.st2.webhook"
        parameters:
            url: "sample"

Once registered, you can send data to this webhook by making a POST request to:
``https://{$ST2_IP}/api/v1/webhooks/sample``

### Example: Sending a Webhook Request

.. sourcecode:: bash

    curl -X POST https://localhost/api/v1/webhooks/sample \
         -H "X-Auth-Token: matoken" \
         -H "Content-Type: application/json" \
         --data '{"key1": "value1"}'

### Rule to Match Webhook Data

.. sourcecode:: yaml

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

## Using a Generic Webhook

A built-in webhook named ``st2`` allows triggering rules without explicitly registering a new webhook.
This is useful when you need to trigger rules dynamically.

The request payload must contain:

| **Field** | **Description** |
|----------|----------------|
| ``trigger`` | Name of the trigger (e.g., ``mypack.mytrigger``) |
| ``payload`` | JSON object containing trigger payload |

### Example: Sending a Generic Webhook

.. sourcecode:: bash

    curl -X POST https://localhost/api/v1/webhooks/st2 \
         -H "X-Auth-Token: matoken" \
         -H "Content-Type: application/json" \
         --data '{"trigger": "mypack.mytrigger", "payload": {"attribute1": "value1"}}'

### Rule to Match Data

.. sourcecode:: yaml

    trigger:
        type: "mypack.mytrigger"

    criteria:
        trigger.attribute1:
            type: "equals"
            pattern: "value1"

    action:
        ref: "mypack.myaction"

## Listing Registered Webhooks

To list all registered webhooks:

.. code-block:: bash

    st2 webhook list

## Debugging Webhook Issues

If your webhook isn't triggering expected actions, check the logs and troubleshoot using the
``--debug`` flag.

## Alternative Tools for Webhook Testing

To test webhooks locally before integrating with |st2|, you can use:

- **Beeceptor** (https://beeceptor.com) - Mock and inspect webhook requests.
- **Webhook.site** (https://webhook.site/) - Capture and debug webhooks.

These tools allow you to validate webhook payloads before sending them to |st2|.

## When Not to Use Webhooks

Consider using the ``/v1/executions`` API instead of webhooks if:

- You need a bidirectional response (webhooks only push data into |st2|).
- You require guaranteed execution (webhooks may not always trigger an action).

You can invoke an action synchronously using:

.. sourcecode:: bash

    curl -X POST https://[ST2_IP]/api/v1/executions \
         -H "X-Auth-Token: matoken" \
         -H "Content-Type: application/json" \
         --data '{"action": "core.local", "parameters": {"cmd": "date"}}'
