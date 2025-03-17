
.. _config_test:

How to configure the testing framework
==========================================

.. note::
   This is not the recommended way to use the framework in production,
   it is only usefull when testing on localhost to verify that your code works properly.

   The recommended way to use the framework can be found in :ref:`How to configure the framework using the environment <config_env>`.

To configure the testing framework, you can simply call the ``configure`` method using a ``TestConfig`` object.

.. code-block:: python

    from telemetry import configure, TestConfig

    config = TestConfig()
    configure(config)

Similarly to all other config types, you may modify the opentelemetry ``Resource`` object or the log level in the following way

.. code-block:: python

    from telemetry import configure, TestConfig, Resource, SERVICE_NAME

    config = TestConfig()
    config.resource = Resource({ SERVICE_NAME: "service" })
    configure(config)

If testing your logs involve a different settings for the logger, you may also set the log level used by all the framework (or you may set it test by test using ``logger.setLevel``) :

.. code-block:: python

    from telemetry import configure, TestConfig

    import logging

    config = TestConfig()
    config.loglevel = logging.DEBUG
    configure(config)
