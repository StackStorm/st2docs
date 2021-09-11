.. NOTE: This file has been generated automatically, do not manually edit it.
         If you want to update runner parameters, make your changes to the
         runner YAML files in st2/contrib/runners/ and then run

         make docs

         to regenerate the documentation for runners.


* ``debug`` (boolean) - Enable runner debug mode.
* ``content_version`` (string) - Git revision of the pack content to use for this action execution (git commit sha / tag / branch). Only applies to packs which are git repositories.
* ``env`` (object) - Environment variables which will be available to the script.
* ``timeout`` (integer) - Action timeout in seconds. Action will get killed if it doesn't finish in timeout seconds.
* ``log_level`` (string) - Default log level for Python runner actions.