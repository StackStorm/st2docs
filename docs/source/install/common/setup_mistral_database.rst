Run these commands to set up the Mistral PostgreSQL database:

.. code-block:: bash

  # Create Mistral DB in PostgreSQL
  cat << EHD | sudo -u postgres psql
  CREATE ROLE mistral WITH CREATEDB LOGIN ENCRYPTED PASSWORD 'StackStorm';
  CREATE DATABASE mistral OWNER mistral;
  EHD

  # Setup Mistral DB tables, etc.
  /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head
  # Register mistral actions
  /opt/stackstorm/mistral/bin/mistral-db-manage --config-file /etc/mistral/mistral.conf populate | grep -v -e openstack -e keystone -e ironicclient
