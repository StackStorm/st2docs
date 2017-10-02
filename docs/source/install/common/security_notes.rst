By default, when MongoDB, RabbitMQ and PostgreSQL are installed, they have authentication disabled
or use a default static password. As such, after you install those services you should configure
them and enable authentication with strong randomly generated passwords.

**NB:** If you use the |st2| installation script, this is done automatically for you.

Configuring authorization and passwords for those services is out of the scope for this
documentation. For more information refer to the links below:

* MongoDB - https://docs.mongodb.com/manual/tutorial/enable-authentication/, https://docs.mongodb.com/manual/core/authorization/
* RabbitMQ - https://www.rabbitmq.com/authentication.html
* PostgreSQL - https://www.postgresql.org/docs/9.4/static/auth-methods.html

After you enable authentication for those components, you will also need to update |st2|
services to use the new settings.

This means editing the following configuration options:

1. |st2| - ``/etc/st2/st2.conf``

  * ``database.username`` - MongoDB database username.
  * ``database.password`` - MongoDB database password.
  * ``messaging.url`` - RabbitMQ transport url (``amqp://<username>:<password>@<hostname>:5672``)

2. Mistral - ``/etc/mistral/mistral.conf``

  * ``database.connection`` - PostgreSQL database connection string (``postgresql+psycopg2://<username>:<password>@<hostname>/mistral``)
  * ``transport_url`` - RabbitMQ transport url (``rabbit://<username>:<password>@<hostname>:5672``)

In addition, you are strongly encouraged to follow these best practices for running network
services:

* Ensure communication between services is encrypted. Enable SSL/TLS for MongoDB, RabbitMQ,
  and PostgreSQL.
* Configure services to only listen on localhost, and where needed, internal IP addresses. There
  is usually no need for most services which are used by |st2| (MongoDB, RabbitMQ, PostgreSQL) to
  be available on a public IP address.
* Configure a firewall and set up a whitelist. The firewall should only allow access by those
  users and systems which need access to those services. API and auth services usually need to be
  accessible to your users, but other dependent services such as MongoDB, RabbitMQ and PostgreSQL
  don't. These should not be directly accessible by users, and only |st2| components should be
  allowed to talk to them.
* Where possible, you should also utilize additional network-based isolation and security features
  such as DMZs.

The steps mentioned above are especially important for distributed production deployments where
|st2| components are running on multiple servers.