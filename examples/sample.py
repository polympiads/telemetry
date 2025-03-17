import os
import sys
import time

# add root folder, just so the example has access to the telemetry framework
sys.path.append(
    os.path.dirname(os.path.dirname(__file__)))

# sample example, as in the documentation

# content of example-telemetry.py
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