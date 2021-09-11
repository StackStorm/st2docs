.. NOTE: This file has been generated automatically, do not manually edit it.
         If you want to update runner parameters, make your changes to the
         runner YAML files in st2/contrib/runners/ and then run

         make docs

         to regenerate the documentation for runners.


* ``allow_redirects`` (boolean) - Set to True if POST/PUT/DELETE redirect following is allowed.
* ``cookies`` (object) - Optional cookies to send with the request.
* ``headers`` (object) - HTTP headers for the request.
* ``http_proxy`` (string) - URL of HTTP proxy to use (e.g. http://10.10.1.10:3128).
* ``https_proxy`` (string) - URL of HTTPS proxy to use (e.g. http://10.10.1.10:3128).
* ``password`` (string) - Password required by basic authentication.
* ``url`` (string) - URL to the HTTP endpoint.
* ``username`` (string) - Username required by basic authentication.
* ``verify_ssl_cert`` (boolean) - Certificate for HTTPS request is verified by default using requests CA bundle which comes from Mozilla. Verification using a custom CA bundle is not yet supported. Set to False to skip verification.
* ``url_hosts_blacklist`` (array) - Optional list of hosts (network locations) to blacklist (e.g. example.com, 127.0.0.1, ::1, etc.). If action will try to access that endpoint, an exception will be thrown and action will be marked as failed.
* ``url_hosts_whitelist`` (array) - Optional list of hosts (network locations) to whitelist (e.g. example.com, 127.0.0.1, ::1, etc.). If specified, actions will only be able to hit hosts on this whitelist.