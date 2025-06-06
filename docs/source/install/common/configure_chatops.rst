* Review and edit the ``/opt/stackstorm/chatops/st2chatops.env`` configuration file to point it to
  your |st2| installation and the Chat Service you are using. At a minimum, you should generate an
  :ref:`API key <authentication-apikeys>` and set the ``ST2_API_KEY`` variable. By default
  ``st2api`` and ``st2auth`` are expected to be on the same host. If that is not the case, please
  update the ``ST2_API`` and ``ST2_AUTH_URL`` variables or just point to the correct host with
  ``ST2_HOSTNAME``.

  The example configuration uses Slack. To see the full list of supported Chat Services and environmental
  variables to configure see :ref:`chatops-configuration`.