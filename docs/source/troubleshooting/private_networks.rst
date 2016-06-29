Troubleshooting WebUI Access on Private Networks
================================================

If you are installing |st2| on a host you don't have 
direct (or VPN) network access to (such as an AWS instance
with only private IP addresses), you may find you have some
level of difficulty connecting to the webui. 

Typically you might try to simply create an SSH tunnel
through a bastion host, and then hit a URL on localhost, such
as https://localhost:8443/. Doing so, though, you will likely
see an error message, such as ``Unable to reach auth service.
[auth:true]``.

Because of the way the webui authentication works, the browser 
will likely be provided with URLs for the auth service that 
don't actually map to your "tunnel URLs".

The easiest solution to bypass this problem, assuming you
don't have the ability to get a proper VPN set up between 
your networks, is to use SSH not to create tunnels, but as an
SSH proxy, such as by doing: ``ssh -N -D 7654 bastion_host``.
This command, using ``-N``, will not yield a command prompt.

Then, configure your browser to use localhost:7654 as a SOCKS5
proxy.  At this point, you should be able to connect to the
|st2| webui using the private IP address, which will be proxied
through your SSH session, and all should just work at that point.
