
.. _config_http:

How to configure the http exporters
==========================================

.. warning::
   This is not the recommended way to use the framework in production,
   it is only usefull when testing on localhost to verify that your code works properly.

   The recommended way to use the framework can be found in :ref:`How to configure the framework using the environment <config_env>`

To configure the http exporters, you can simply call the ``configure`` method using a ``HttpConfig`` object.

.. code-block:: python

    from telemetry import configure, TestConfig

    config = HttpConfig("http://localhost:4318")
    configure(config)

Here, we have assumed that you are using the ``grafana/otel-lgtm`` docker image, so it will automatically choose the endpoints as ``http://localhost:4318/v1/traces``, ``http://localhost:4318/v1/metrics`` and ``http://localhost:4318/v1/logs``.

.. _config_http_force_ending_slash:
.. note::
    By default, if a ``'/'`` is found at the end of the base endpoint, it will be removed as the endpoints is computed
    as a direct concatenation of the base endpoint and the suffix, so you would get two ``'/'`` adjacent in your
    target path. As this might be an issue, the program issues a warning and removes the occurrence in the base.
    If you want to force this behaviour, there is the optional parameter ``force_ending_slash`` to remove this behaviour.

Configuration parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

You may need to modify the opentelemetry ``Resource`` object to signal what service or cluster your code is running in,
to do that, you may set the ``resource`` field to a new object of your choice.

.. code-block:: python

    from telemetry import configure, HttpConfig, Resource, SERVICE_NAME

    config = HttpConfig("http://localhost:4318")
    config.resource = Resource({ SERVICE_NAME: "service" })
    configure(config)

To set the log level of your telemetry, you can set the ``loglevel`` property of your config.

.. code-block:: python

    from telemetry import configure, HttpConfig

    import logging

    config = HttpConfig("http://localhost:4318")
    # Only send ERROR and CRITICAL logs
    config.loglevel = logging.ERROR
    configure(config)

.. _config_http_advanced_endpoints:

Advanced endpoints
~~~~~~~~~~~~~~~~~~~

By default, the config assumes you are using the docker image of ``grafana/otel-lgtm``, but it might not be the case. To modify this behaviour, you can therefore change the variables ``suffix_metrics``, ``suffix_traces`` and ``suffix_logs`` to something else that suits your configuration better.

.. code-block:: python

    from telemetry import configure, TestConfig

    config = HttpConfig("http://localhost:4318")
    config.suffix_metrics = "/v2/metrics"
    # the endpoint will now be http://localhost:4318/v2/metrics
    configure(config)

If you need to have something more advanced than just adding a suffix to the base endpoint, you might need to create a new config that inherints from ``HttpConfig`` and in particular that overrides the properties ``metrics_endpoint``, ``traces_endpoint`` and ``logs_endpoint``.

.. code-block:: python

    from telemetry import configure, HttpConfig

    # An example of a custom Http Config
    #  - Metrics are on port 4319
    #  - Logs and traces are as usual on port 4318
    class MyHttpConfig (HttpConfig):
        def __init__ (self):
            super().__init__("http://localhost:4318/")
        
        @property
        def metrics_endpoint (self):
            return "http://localhost:4319/"

    config = MyHttpConfig()
    configure(config)
