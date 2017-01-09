By default when dependent services such as MongoDB, RabbitMQ and PostgreSQL are installed, they
have authentication disabled or use a default static password. As such, after you install those
services you should configure them and enable authentication with a strong randomly generated
passwords.

Configuring authorization and passwords for those services is out of the scope of this documents,
but for more information you can refer to the links below.

* MongoDB - https://docs.mongodb.com/manual/tutorial/enable-authentication/, https://docs.mongodb.com/manual/core/authorization/
* RabbitMQ - https://www.rabbitmq.com/authentication.html
* PostgreSQL - https://www.postgresql.org/docs/9.4/static/auth-methods.html

After you enable authentication for those components, you will also need to configure StackStorm
services so they can talk to them.

This means editing editing the following configuration file options:

1. StackStorm config - ``/etc/st2/st2.conf``

  * ``database.username`` - MongoDB database username.
  * ``database.password`` - MongoDB database password.
  * ``messaging.url`` - RabbitMQ transport url (``amqp://<username>:<password>@<hostname>:5672``)

2. Mistral config - ``/etc/mistral/mistral.conf``

  * ``database.connection`` - PostgreSQL database connection string (``postgresql://<username>:<password>@<hostname>/mistral``)
  * ``transport_url`` - RabbitMQ transport url (``rabbit://<username>:<password>@<hostname>:5672``)

In addition to that, you are strongly encouraged to follow other best practices for running network
services:

* Ensure communication between services is encrypted an enable SSL / TLS for all the services -
  MongoDB, RabbitMQ, PostgreSQL.
* Configure services to only listen on localhost and where needed, also internal IP address. There
  is usually no need for most services which are used by |st2| (MongoDB, RabbitMQ, PostgreSQL) to
  be available to the public and listen on an external (public) IP address.
* Configure firewall and set up a whitelist. You should set up a firewall and only allow services
  and users which need access to the services to be able to access them. API and auth service
  usually need to be accessible to your users, but other dependent services such as MongoDB,
  RabbitMQ and PostgreSQL aren't and shouldn't be directly accessible to the users should be
  locked down and only StackStorm components should be allowed to talk to them.
* Where possible and available, you should also utilize additional network based isolation and
  security features such as VLANs.

Steps mentioned above are especially important for distributed production deployments where |st2|
components are running on multiple servers.
