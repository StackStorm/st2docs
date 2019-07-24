.. NOTE: This file has been generated automatically, don't manually edit it

* ``schema`` (object) - A JSON schema that will be used to validate the response data
* ``route`` (string) - An arbitrary value for allowing rules to route to proper notification channel
* ``roles`` (array) - A list of roles that are permitted to respond to the action (if nothing provided, all are permitted) - REQUIRES ENTERPRISE FEATURES
* ``users`` (array) - A list of usernames that are permitted to respond to the action (if nothing provided, all are permitted)
* ``ttl`` (integer) - Time (in minutes) to wait before timing out the inquiry if no response is received