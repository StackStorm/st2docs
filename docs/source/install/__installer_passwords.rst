.. note::

  For security reasons, installer script enables authentication and generates random passwords
  for dependent services such as MongoDB and PostgreSQL.

  If for some reason (e.g. debugging), you need to access those services directly you can find
  passwords in the config files - ``/etc/st2/st2.conf`` for MongoDB and RabbitMQ password and
  ``/etc/mistral/mistral.conf`` for PostgreSQL password.
