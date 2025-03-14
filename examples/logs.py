
# Telemetry example for logging
# This uses grafana/otel-lgtm, that should be setup
# on port 4318 for HTTP

import os
import sys
import time

# add root folder, just for the example
sys.path.append(
    os.path.dirname(os.path.dirname(__file__)))

from telemetry import configure, HttpConfig, Resource, SERVICE_NAME

import logging

config = HttpConfig( "http://localhost:4318" )
config.resource = Resource({ SERVICE_NAME: "example_service" })
# Uncomment the following line if you want to see all the logs
# Otherwise, you will only see the 3 first messages and not info / debug
# config.loglevel = logging.DEBUG
configure( config )

logging.critical( "Some critical message", extra = { "arg": 42 } )
logging.error( "Some error message" )
logging.warning( "Some warning message" )
logging.info("Some info message")
logging.debug("Some debug message")
