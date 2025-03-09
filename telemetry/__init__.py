
import os
import enum

import telemetry.metrics as metrics

from telemetry.config import *

def configure_from_env ():
    config = BaseConfig.from_env()

    configure(config)

def configure (config: BaseConfig):
    if isinstance(config, TestConfig):
        metrics.configure_test( config )
    
    if isinstance(config, HttpConfig):
        metrics.configure_http( config )
