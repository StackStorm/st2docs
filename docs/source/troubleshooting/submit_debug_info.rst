.. _submit_debug_info_to_st2:

Submitting debugging information to |st2|
======================================================================

First step when trying to help you debug an issue or a problem you are having
is for us to try to reproduce the problem. To be able to do that, our setup
needs to resemble yours as closely as possible.

To save time and make yours and our life easier, the default distribution of
|st2| includes a utility which allows you to easily and in a secure manner
send us the information we need to help you debug or troubleshoot an issue.

By default, this script sends us the following information:

* All the |st2| services log files from ``/var/log/st2``
* Mistral service log file from ``/var/log/mistral.log``
* |st2| and Mistral config file (``/etc/st2/st2.conf``,
  ``/etc/mistral/mistral.conf``). Prior to sending the config files we strip
  sensitive information such as database and queue access information.
* |st2| content (integration packs) minus the pack configs.

All this information is bundled up in a tarball and encrypted using our
public key via public-key cryptography. Once submitted, this information
is only accessible to Brocade employees and it's used solely for
debugging purposes.

To send debug information to Brocade, simply invoke the command shown
below:

.. sourcecode:: bash

    st2-submit-debug-info

    This will submit the following information to Brocade: logs, configs, content, system_info
    Are you sure you want to proceed? [y/n] y
    2015-02-10 16:43:54,733  INFO - Collecting files...
    2015-02-10 16:43:55,714  INFO - Creating tarball...
    2015-02-10 16:43:55,892  INFO - Encrypting tarball...
    2015-02-10 16:44:02,591  INFO - Debug tarball successfully uploaded to Brocade

By default, the tool will run in an interactive mode. If you want to run it in a
non-interactive mode and assume "yes" as the answer to all the questions you
can use the ``--yes`` flag.

For example:

.. sourcecode:: bash

    st2-submit-debug-info --yes

    2015-02-10 16:45:36,074  INFO - Collecting files...
    2015-02-10 16:45:36,988  INFO - Creating tarball...
    2015-02-10 16:45:37,193  INFO - Encrypting tarball...
    2015-02-10 16:45:43,926  INFO - Debug tarball successfully uploaded to StackStorm

If you want to only send specific information to Brocade or exclude particular information
you can use the ``--exclude-<content>`` flag.

For example, if you want to only send us log files, you would run the command
like this:

.. sourcecode:: bash

    st2-submit-debug-info --exclude-configs --exclude-content --exclude-system-info

Reviewing the debug information
-------------------------------

If you want to review and / or manipulate information (e.g. remove log lines
which you might find sensitive) which is sent to Brocade, you can do that
using ``--review`` flag.

When this flag is used, the archive with debug information won't be encrypted
and uploaded to Brocade.

.. sourcecode:: bash

    st2-submit-debug-info --review

    2015-02-10 17:43:49,016  INFO - Collecting files...
    2015-02-10 17:43:49,770  INFO - Creating tarball...
    2015-02-10 17:43:49,912  INFO - Debug tarball successfully generated and can be reviewed at: /tmp/st2-debug-output-vagrant-ubuntu-trusty-64-2015-02-10-174349.tar.gz

By default, the archive will be written to the /tmp directory. This can be controlled by using
the ``--output`` option to specify the location/filename of the archive.

.. sourcecode:: bash

    st2-submit-debug-info --review --output my-st2-debug-file.tar.gz

    2016-02-24 23:53:25,779  INFO - Collecting files...
    2016-02-24 23:53:26,423  INFO - Creating tarball...
    2016-02-24 23:53:26,526  INFO - Debug tarball successfully generated and can be reviewed at: my-st2-debug-file.tar.gz

After review, the archive can be uploaded to Brocade using the ``--existing-file`` option.

.. sourcecode:: bash

    st2-submit-debug-info --config /etc/st2debug/submit-debug-info.yaml --existing-file my-st2-debug-file.tar.gz

    2016-02-24 23:56:13,019  INFO - Encrypting tarball...
    2016-02-24 23:56:13,814  INFO - Debug tarball successfully uploaded to Brocade (name=my-st2-debug-file.tar.gz.asc)
    2016-02-24 23:56:13,814  INFO - When communicating with support, please let them know the tarball name - my-st2-debug-file.tar.gz.asc


Customizing the debug information gathered
==========================================

st2-submit-debug-info can be customized for specific deployments by loading a set of overrides from
a YAML file. The following config options are supported:

* ``log_file_paths`` - an additional set of log files to gather
* ``st2_config_file_path`` - path to st2.conf
* ``mistral_config_file_path`` - path to mistral.conf
* ``s3_bucket_url`` - the S3 bucket to upload the archive to
* ``gpg_key_fingerprint`` - gpg fingerprint to use when encrypting the archive
* ``gpg_key`` - gpg key to use when encrypting the archive
* ``shell_commands`` - a list of shell commands to execute and capture the output from
* ``company_name`` - the company name to show in the interactive prompts and log messages

Sample config yaml file:

.. literalinclude:: __debug_info_config.yaml

To send debug information to Brocade, simply invoke the command shown below passing it the path to
the YAML config file:

.. sourcecode:: bash

    st2-submit-debug-info --config <path to config file>

    This will submit the following information to BRocade: logs, configs, content, system_info, shell_commands
    Are you sure you want to proceed? [y/n] y
    2016-01-19 06:12:18,587  INFO - Collecting files...
    2016-01-19 06:12:19,602  INFO - Creating tarball...
    2016-01-19 06:12:19,708  INFO - Encrypting tarball...
    2016-01-19 06:12:43,949  INFO - Debug tarball successfully uploaded to Brocade (name=st2-debug-output-70386ae8e4fe-2016-01-19-06:12:18.tar.gz.asc)
    2016-01-19 06:12:43,949  INFO - When communicating with support, please let them know the tarball name - st2-debug-output-70386ae8e4fe-2016-01-19-06:12:18.tar.gz.asc

We can pass through any command line arguments provided to st2-submit-debug-info.

For Example:

* To run it in a non-interactive mode use the '--yes' option.

.. sourcecode:: bash

    st2-submit-debug-info --yes --config <path to config file>

    2016-01-19 06:25:09,024  INFO - Collecting files...
    2016-01-19 06:25:09,617  INFO - Creating tarball...
    2016-01-19 06:25:09,725  INFO - Encrypting tarball...
    2016-01-19 06:25:13,727  INFO - Debug tarball successfully uploaded to Brocade (name=st2-debug-output-70386ae8e4fe-2016-01-19-06:25:09.tar.gz.asc)
    2016-01-19 06:25:13,727  INFO - When communicating with support, please let them know the tarball name - st2-debug-output-70386ae8e4fe-2016-01-19-06:25:09.tar.gz.asc

* To send specific information to Brocade or to exclude particular information use the ``--exclude-<content>`` flag.

.. sourcecode:: bash

    st2-submit-debug-info --exclude-shell-commands --config <path to config file>

    This will submit the following information to Brocade: logs, configs, content, system_info
    Are you sure you want to proceed? [y/n] y
    2016-01-19 06:28:25,533  INFO - Collecting files...
    2016-01-19 06:28:25,895  INFO - Creating tarball...
    2016-01-19 06:28:26,002  INFO - Encrypting tarball...
    2016-01-19 06:28:29,559  INFO - Debug tarball successfully uploaded to Brocade (name=st2-debug-output-70386ae8e4fe-2016-01-19-06:28:25.tar.gz.asc)
    2016-01-19 06:28:29,559  INFO - When communicating with support, please let them know the tarball name - st2-debug-output-70386ae8e4fe-2016-01-19-06:28:25.tar.gz.asc

* To review the debugging information without encrypting and uploading to Brocade.

.. sourcecode:: bash

    st2-submit-debug-info --review --config <path to config file>

    2016-01-19 06:19:04,911  INFO - Collecting files...
    2016-01-19 06:19:05,531  INFO - Creating tarball...
    2016-01-19 06:19:05,637  INFO - Debug tarball successfully generated and can be reviewed at: /tmp/st2-debug-output-70386ae8e4fe-2016-01-19-06:19:04.tar.gz
