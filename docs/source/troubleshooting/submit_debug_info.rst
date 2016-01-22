.. _submit_debug_info_to_st2:

Submitting debugging information to StackStorm
==============================================

First step when trying to help you debug an issue or a problem you are having
is for us to try to reproduce the problem. To be able to do that, our setup
needs to resemble yours as closely as possible.

To save time and make yours and our life easier, the default distribution of
StackStorm includes a utility which allows you to easily and in a secure manner
send us the information we need to help you debug or troubleshoot an issue.

By default, this script sends us the following information:

* All the StackStorm services log files from ``/var/log/st2``
* Mistral service log file from ``/var/log/mistral.log``
* StackStorm and Mistral config file (``/etc/st2/st2.conf``,
  ``/etc/mistral/mistral.conf``). Prior to sending the config files we strip
  sensitive information such as database and queue access information.
* StackStorm content (integration packs) minus the pack configs.

All this information is bundled up in a tarball and encrypted using our
public key via public-key cryptography. Once submitted, this information
is only accessible to the StackStorm employees and it's used solely for
debugging purposes.

To send debug information to StackStorm, simply invoke the command shown
below:

.. sourcecode:: bash

    st2-submit-debug-info

    This will submit the following information to StackStorm: logs, configs, content, system_info
    Are you sure you want to proceed? [y/n] y
    2015-02-10 16:43:54,733  INFO - Collecting files...
    2015-02-10 16:43:55,714  INFO - Creating tarball...
    2015-02-10 16:43:55,892  INFO - Encrypting tarball...
    2015-02-10 16:44:02,591  INFO - Debug tarball successfully uploaded to StackStorm

By default, tool run in an interactive mode. If you want to run it an
non-interactive mode and assume "yes" as the answer to all the questions you
can use the ``--yes`` flag.

For example:

.. sourcecode:: bash

    st2-submit-debug-info --yes

    2015-02-10 16:45:36,074  INFO - Collecting files...
    2015-02-10 16:45:36,988  INFO - Creating tarball...
    2015-02-10 16:45:37,193  INFO - Encrypting tarball...
    2015-02-10 16:45:43,926  INFO - Debug tarball successfully uploaded to StackStorm

If you want to only send a specific information to StackStorm or exclude a
particular information you can use the ``--exclude-<content>`` flag.

For example, if you want to only send us log files, you would run the command
like this:

.. sourcecode:: bash

    st2-submit-debug-info --exclude-configs --exclude-content --exclude-system-info

Reviewing the debug information
-------------------------------

If you want to review and / or manipulate information (e.g. remove log lines
which you might find sensitive) which is sent to StackStorm, you can do that
using ``--review`` flag.

When this flag is used, the archive with debug information won't be encrypted
and uploaded to StackStorm.

.. sourcecode:: bash

    st2-submit-debug-info --review

    2015-02-10 17:43:49,016  INFO - Collecting files...
    2015-02-10 17:43:49,770  INFO - Creating tarball...
    2015-02-10 17:43:49,912  INFO - Debug tarball successfully generated and can be reviewed at: /tmp/st2-debug-output-vagrant-ubuntu-trusty-64-2015-02-10-17:43:49.tar.gz


Submitting debugging information to Plexxi
===============================

The enhancement work will allow submit_debug_info.py to be customized for specific deployments (Plexxi's as an example :-) by loading a set of overrides from a YAML file. The following config options can now be specified:

* log_file_paths - an additional set of log files to gather
* conf_file_paths - an additional set of config files to gather
* s3_bucket - the S3 bucket to upload the archive to
* gpg - gpg key and fingerprint to use when encrypting the archive
* shell_commands - a list of shell commands to execute and capture the output from
* company_name - the company name to show in the interactive prompts and log messages

Sample Config yaml file:

log_file_paths:
    st2_log_files_path: /var/log/st2/*.log
    mistral_log_files_path: /var/log/mistral*.log
    rabbitmq_log_files_path: /var/log/rabbitmq/*
    message_files_path: /var/log/messages*
    salt_log_files_path: /var/log/*salt.log
    mongodb_log_files_path: /var/log/mongod/*
    nginx_log_files_path: /var/log/nginx/*
    yum_log_files_path: /var/log/yum.log
conf_file_paths:
    st2_config_file_path: /etc/st2/st2.conf
    mistral_config_file_path: /etc/mistral/mistral.conf
s3_bucket:
    url: https://plexxi-support.s3.amazonaws.com/
gpg:
    gpg_key_fingerprint: 61765A448C8115A958CB01DE747C61F1FF67E6B8
    gpg_key: |
          -----BEGIN PGP PUBLIC KEY BLOCK-----
          Version: GnuPG v2.0.14 (GNU/Linux)

          mQENBFZ7zZkBCACrSqIElndvQfog9TyzkG0p399+t+JSZ8CQBs0PvOXro4UGlgsz
          7dUfVPu/yOgtuByTQ6HR+F2zHtZVZIYANE+42fncz8aDIKwesGLtbglyOcon80sn
          XYon7KUBTy39x1hDZE5idghMw6uDhEbxCFW8WFkRxZtNhKmKLxmVQRF6F31St/LK
          ddaw2jszI/ekpEcGRSaPuxOfptUPkfqN+ItbIqcOJQpLi6GkyNVBX9USkIUl5UpP
          q+jTczCJYs5vMhxKHktoElRbcEwA+LOZXEuMCzoqfqIsppv+nYCTdQBpL0dRW692
          zzWwRSRVlnW6lNrJWo3V9fM6NttteVBQ4/rlABEBAAG0MnBsZXh4aSAodG8gc3Vi
          bWl0IGRlYnVnIGluZm8pIDxzdXBwb3J0QHBsZXh4aS5jb20+iQE4BBMBAgAiBQJW
          e82ZAhsDBgsJCAcDAgYVCAIJCgsEFgIDAQIeAQIXgAAKCRB0fGHx/2fmuLAzB/9o
          olpnnPgkIqwSeBvdb1Elo3hiBu1/xJBqL0n0M0eevwlo2udDWvWbPAi5m9NDqYOy
          BMoweqW6yP6OmaZmuysN2L3lTAabjDGZCPynfazPYErRYD4N9scDRgAR6Hb2P3Cj
          42to9JEQlTw7LGYDEvKBnGqRqIjv8UfYj6nHH7tW6XBJo3Me1CFsOC+dQkDbG3w7
          Gatv0JAOYVkZcHEzLQutbCO2EdVi8RU/H5/F1obbjz1ZOuMxLwt5rDrY4SQpFwBM
          VJchI8HYogqwaitzR1alsVQ5IKdIS0Dw24gv4oRkZCpe/AFrp4LHQ7tnu/6iD06i
          vHuwdSZ38Al5xrEvCMz/uQENBFZ7zZkBCADqTPUuVN4JcD26GLMMGEhiXaMeY03j
          qJBUXEoZRfgE9+/BCQzYLkOci1BjISlTMfrFob7Gi9gC/rrrI5ZE9TLTjKeiDjv8
          xVDUuxqUDtBchJCJXoSvXlEi1ZfI4UQ1qk+m/2eRyicPuRz7Gg+JhR5hzM7g3YKS
          wbJ2cX+TyBYLtPijpbGiAcs/vdYu7TZRfeOFGdcirtiByRGKh7WXB9qaqrsH+y05
          8J6YMvVZi1u3fZemPl01UedRP412Bbzym89ozkuhCexPU2cB1uf3SREpzj4kEWPd
          IrgqCGZCzpPS9CDAt5KIZzyjdCrVuF26C+bMn4r91mPag3m7ecC4p5lzABEBAAGJ
          AR8EGAECAAkFAlZ7zZkCGwwACgkQdHxh8f9n5rgTzgf+PunMeCZyYmm2HRi4R8D/
          mtx8FXjZc3/IvJ5AZAUPNGhqRInHRRRuIi/Ff8yKFwIBoYvPwQ2HFovIb14oVgeN
          dvfSlndY1GtgbbYjeKHydNI7r41oW2vO+3AAs9sUrY2BotTGYciXaPmFcFW5aozI
          hEEHYx/KajN0vCpQkKa3lWzviszak0nLs1TO8ppNPHgv3otNVFhLWZiIzv/A4LTY
          WwShxYmHXZfu8p4wVeYNhT/g0ThFz8QpnzpZBO8PfROTS/5/v7aJrmkUTY/tTDhb
          VDEaUjnGCtgflosRXd/uUK+VP0FibjJnP+W93PThnkpTJmFCuy5WPJlBYPHAMmZF
          Tg==
          =qDpc
          -----END PGP PUBLIC KEY BLOCK-----
shell_commands:
    cmd1: rpm -qa
company_name:
    name: Plexxi

To send debug information to Plexxi, simply invoke the command shown below:

.. sourcecode:: bash

    submit-debug-info.sh

    This will submit the following information to Plexxi: logs, configs, content, system_info, shell_commands
    Are you sure you want to proceed? [y/n] y
    2016-01-19 06:12:18,587  INFO - Collecting files...
    2016-01-19 06:12:19,602  INFO - Creating tarball...
    2016-01-19 06:12:19,708  INFO - Encrypting tarball...
    2016-01-19 06:12:43,949  INFO - Debug tarball successfully uploaded to Plexxi (name=st2-debug-output-70386ae8e4fe-2016-01-19-06:12:18.tar.gz.asc)
    2016-01-19 06:12:43,949  INFO - When communicating with support, please let them know the tarball name - st2-debug-output-70386ae8e4fe-2016-01-19-06:12:18.tar.gz.asc

We can pass through any command line arguments provided to st2-submit-debug-info

Sample examples:

* To run it an non-interactive mode using '--yes' option.

.. sourcecode:: bash

    submit-debug-info.sh --yes

    2016-01-19 06:25:09,024  INFO - Collecting files...
    2016-01-19 06:25:09,617  INFO - Creating tarball...
    2016-01-19 06:25:09,725  INFO - Encrypting tarball...
    2016-01-19 06:25:13,727  INFO - Debug tarball successfully uploaded to Plexxi (name=st2-debug-output-70386ae8e4fe-2016-01-19-06:25:09.tar.gz.asc)
    2016-01-19 06:25:13,727  INFO - When communicating with support, please let them know the tarball name - st2-debug-output-70386ae8e4fe-2016-01-19-06:25:09.tar.gz.asc

* To send a specific information to Plexxi or exclude a particular information using ``--exclude-<content>`` flag.

.. sourcecode:: bash

    submit-debug-info.sh --exclude-shell-commands

    This will submit the following information to Plexxi: logs, configs, content, system_info
    Are you sure you want to proceed? [y/n] y
    2016-01-19 06:28:25,533  INFO - Collecting files...
    2016-01-19 06:28:25,895  INFO - Creating tarball...
    2016-01-19 06:28:26,002  INFO - Encrypting tarball...
    2016-01-19 06:28:29,559  INFO - Debug tarball successfully uploaded to Plexxi (name=st2-debug-output-70386ae8e4fe-2016-01-19-06:28:25.tar.gz.asc)
    2016-01-19 06:28:29,559  INFO - When communicating with support, please let them know the tarball name - st2-debug-output-70386ae8e4fe-2016-01-19-06:28:25.tar.gz.asc

* To review the debugging information without encrypted and uploaded to Plexxi

.. sourcecode:: bash

    submit-debug-info.sh --review

    2016-01-19 06:19:04,911  INFO - Collecting files...
    2016-01-19 06:19:05,531  INFO - Creating tarball...
    2016-01-19 06:19:05,637  INFO - Debug tarball successfully generated and can be reviewed at: /tmp/st2-debug-output-70386ae8e4fe-2016-01-19-06:19:04.tar.gz  
