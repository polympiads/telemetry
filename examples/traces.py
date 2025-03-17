
# Telemetry example for metrics
# This uses grafana/otel-lgtm, that should be setup
# on port 4318 for HTTP

import os
import random
import sys
import time

# add root folder, just for the example
sys.path.append(
    os.path.dirname(os.path.dirname(__file__)))

from telemetry import configure
from telemetry.config import HttpConfig, Resource, SERVICE_NAME
from telemetry.traces import get_tracer

config = HttpConfig( "http://localhost:4318" )
config.resource = Resource({ SERVICE_NAME: "example_service" })
configure(config)
tracer = get_tracer("example.traces")

with tracer.start_as_current_span( "span_one" ) as span_one:
    time.sleep(1)
    span_one.add_event("some_event", { "some_attribute": "some_value" })
    param = random.randint(1, 6)
    span_one.set_attribute("some_param", param)
    time.sleep(0.1)
    with tracer.start_as_current_span( "save_span" ) as save_span:
        time.sleep(0.1)
        save_span.set_attribute("saving_value", param)
        time.sleep(1)
    time.sleep(0.25)
    span_one.add_event("saving completed")
    time.sleep(0.25)
