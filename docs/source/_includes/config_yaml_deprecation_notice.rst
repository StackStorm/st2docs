.. note::

    All the information on this page refers to the config files inside the
    ``/opt/stackstorm/configs/`` directory.

    ``config.yaml`` files inside the pack directory were deprecated in |st2|
    v1.5. In version 2.3, |st2| generated WARNING logs at pack registration if
    the pack contained a ``config.yaml`` file. As of version 2.4, pack
    registration will fail with ERROR logs if the pack contains ``config.yaml``.
    
    If you are still using ``config.yaml``, you **MUST** migrate to the new
    style.
