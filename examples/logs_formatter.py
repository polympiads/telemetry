
# Telemetry example for logging
# This uses grafana/otel-lgtm, that should be setup
# on port 4318 for HTTP

import os
import sys
import time

# add root folder, just for the example
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from telemetry import configure, HttpConfig, Resource, SERVICE_NAME

import logging

config = HttpConfig( "http://localhost:4318" )
config.resource = Resource({ SERVICE_NAME: "example_service" })
config.formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
configure( config )

logging.error("Some example error message.")
logging.error("Some example error message.", extra={ "extra": "EXTRA" })
