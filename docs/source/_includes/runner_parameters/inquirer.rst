.. NOTE: This file has been generated automatically, do not manually edit it.
         If you want to update runner parameters, make your changes to the
         runner YAML files in st2/contrib/runners/ and then run

         make docs

         to regenerate the documentation for runners.


* ``schema`` (object) - A JSON schema that will be used to validate the response data
* ``route`` (string) - An arbitrary value for allowing rules to route to proper notification channel
* ``roles`` (array) - A list of roles that are permitted to respond to the action (if nothing provided, all are permitted) - REQUIRES RBAC FEATURES
* ``users`` (array) - A list of usernames that are permitted to respond to the action (if nothing provided, all are permitted)
* ``ttl`` (integer) - Time (in minutes) to wait before timing out the inquiry if no response is received