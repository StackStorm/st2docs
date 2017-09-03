WebUI Access on Private Networks
================================

If you are installing |st2| on a host you don't have direct (or VPN) network access to (such as an
AWS instance with only private IP addresses), you may find you have some difficulty connecting to
the Web UI. 

Simply creating an SSH tunnel through a bastion host, and then using a URL on localhost, such
as https://localhost:8443/ will fail. You will see an error message such as ``Unable to reach auth
service. [auth:true]``.

This is due to the way the Web UI authentication works, where the browser will be provided with
URLs for the authentication service that don't map to your tunnel address.

If you don't have the ability to set up a VPN between your networks, the simplest solution is to
use SSH as a proxy, rather than creating tunnels. Use a command like ``ssh -N -D 7654 bastion_host``.
This command, using ``-N``, will not yield a command prompt.

Then configure your browser to use ``localhost:7654`` as a SOCKS5 proxy. You should then be able to
connect to your |st2| Web UI using the private IP address, which will be proxied through your SSH
session, and it should Just Work.