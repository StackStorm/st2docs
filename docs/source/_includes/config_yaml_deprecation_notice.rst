.. note::

    All the information on this page refers to the config files inside the
    ``/opt/stackstorm/configs/`` directory.

    config.yaml files inside the pack directory have been deprecated in |st2|
    v1.5. Values from config.yaml file **don't** get saved in the database when
    running ``st2ctl reload --register-configs`` and those configs also don't
    support config schemas.

    For backward compatibility, if a pack doesn't contain a config inside the
    ``/opt/stackstorm/configs/`` directory, values from config.yaml are still
    used when running an action, but support for config.yaml files inside the
    pack directory will be fully removed in the next major release.
