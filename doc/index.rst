.. telemetry auth documentation master file, created by
   sphinx-quickstart on Mon Sep 30 11:58:09 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

telemetry : Polympiads telemetry utils
======================================

This tool is a wrapper for opentelemetry that makes it easy to configure the ``opentelemetry`` exporters and to unit test telemetry with simple visual schemes.

A quick example
~~~~~~~~~~~~~~~

.. code-block:: python

   # content of examples/sample.py
   from telemetry import configure, HttpConfig, Resource, SERVICE_NAME

   from telemetry.traces  import get_tracer
   from telemetry.metrics import get_meter

   import logging

   # Configure with grafana/otel-lgtm
   config = HttpConfig("http://localhost:4318")
   config.resource = Resource({ SERVICE_NAME: "example_service" })
   configure(config)

   meter  = get_meter("example")
   tracer = get_tracer("example")
   logger = logging.getLogger("example")

   gauge = meter.create_gauge( "example_gauge" )

   with tracer.start_as_current_span("some_span"):
      logger.warning("Setting gauge to 1")
      gauge.set(1)
      logger.warning("Setting gauge[x:1] to 2")
      gauge.set(2, { "x": 1 })

In this example, you should see a span appearing in grafana that is linked directly to the two logs, and with the gauge appearing in prometheus.

.. toctree::
   :maxdepth: 10
   :hidden:

   how-to/index
   api