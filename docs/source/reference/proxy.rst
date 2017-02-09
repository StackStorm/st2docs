|st2| behind an HTTP proxy
==========================

If your |st2| installation is running behind a proxy, you will need to configure
``git`` and ``pip`` to utilize your proxy otherwise some CLI commands such as
``packs.install`` won't work.

Note About Pack Install
-----------------------
Currently, the instructions for modifying ``git`` and ``pip`` configurations still
don't allow ``st2 pack install`` to work via proxy. This is a `known issue
<https://github.com/StackStorm/st2/issues/3137>`_ and will be addressed fully in
a future release.

In the meantime, to allow pack installation to work with the new ``st2 pack install``
command that was released in v2.1, you need to modify the following files so that
they contain the three environment variables "HTTP_PROXY", "HTTPS_PROXY", and
"no_proxy" as shown below (specifically, the "env" section of each):

.. sourcecode:: yaml

	vagrant@st2vagrant:~$ cat /opt/stackstorm/packs/packs/actions/setup_virtualenv.yaml
	---
	  name: "setup_virtualenv"
	  runner_type: "python-script"
	  description: "Set up virtual environment for the provided packs"
	  enabled: true
	  entry_point: "pack_mgmt/setup_virtualenv.py"
	  parameters:
	    packs:
	      type: "array"
	      items:
	        type: "string"
	    update:
	      type: "boolean"
	      default: false
	      description: "Check this option if the virtual environment already exists and if you only want to perform an update and installation of new dependencies. If you don't check this option, the virtual environment will be destroyed then re-created. If you check this and the virtual environment doesn't exist, it will create it."
	    env:
	      type: "object"
	      description: "Optional environment variables"
	      required: false
	      default:
	        HTTP_PROXY: http://< Proxy IP >:< Proxy Port >
	        HTTPS_PROXY: http://< Proxy IP >:< Proxy Port >
	        no_proxy: 127.0.0.1

	vagrant@st2vagrant:~$ cat /opt/stackstorm/packs/packs/actions/download.yaml
	---
	  name: "download"
	  runner_type: "python-script"
	  description: "Downloads packs and places it in the local content repository."
	  enabled: true
	  entry_point: "pack_mgmt/download.py"
	  parameters:
	    packs:
	      type: "array"
	      items:
	        type: "string"
	      required: true
	    abs_repo_base:
	      type: "string"
	      default: "/opt/stackstorm/packs/"
	      immutable: true
	    verifyssl:
	      type: "boolean"
	      default: true
	    force:
	      type: "boolean"
	      description: "Set to True to force install the pack and skip StackStorm version compatibility check"
	      required: false
	      default: false
	    env:
	      default:
	        HTTP_PROXY: http://< Proxy IP >:< Proxy Port >
	        HTTPS_PROXY: http://< Proxy IP >:< Proxy Port >
	        no_proxy: 127.0.0.1

Make sure to fill in < Proxy IP > and < Proxy Port > with the IP address/hostname and
port for your proxy, and run ``st2ctl reload`` to allow these to take effect. This should allow
``st2 pack install`` to work via the configured proxy.


Configuring git
---------------

To configure git you need to set global git ``http.proxy`` option in the
.gitconfig file for the user under which |st2| action runner component is
running.

git config is stored at ``~/.gitconfig``. To configure it, you need to put
the following lines in the config:

.. sourcecode:: ini

    [http]
    proxy = http://user:passwd@proxy.server.com:port

You can achieve the same this by running ``git config`` command which will
write into the config for you.

.. sourcecode:: bash

    git config --global http.proxy http://user:passwd@proxy.server.com:port

Configuring pip
---------------

To configure pip you need to edit pip config for the user under which |st2|
action runner component is running.

pip config is stored at ``$HOME/.config/pip/pip.conf``. To configure it, you
need to put the following lines in the config:

.. sourcecode:: ini

    [global]
    proxy = [user:passwd@]proxy.server.com:port
