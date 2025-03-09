
# Telemetry example for metrics
# This uses grafana/otel-lgtm, that should be setup
# on port 4318 for HTTP

import os
import sys
import time

# add root folder, just for the example
sys.path.append(
    os.path.dirname(os.path.dirname(__file__)))

from telemetry import configure
from telemetry.config import HttpConfig
from telemetry.metrics import get_meter

config = HttpConfig( "http://localhost:4318" )
configure(config)

meter = get_meter( "example.metrics" )

# should be visible at grafana under 'example_gauge'
gauge = meter.create_gauge( "example_gauge" )

for i in range(10):
    print("Setting gauge for time", i)
    gauge.set(i, { "time": i })
    time.sleep(1)
