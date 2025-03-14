
import os
import logging

from opentelemetry.sdk.resources import *

ENV_CONFIG_TYPE      = "TELEMETRY_CONFIG_TYPE"
ENV_CONFIG_LOGLEVEL  = "TELEMETRY_LOG_LEVEL"
ENV_HTTP_ENDPOINT    = "TELEMETRY_HTTP_ENDPOINT"
ENV_HTTP_FORCE_SLASH = "TELEMETRY_HTTP_FORCE_SLASH"

ENV_HTTP_METRICS_SUFFIX = "TELEMETRY_METRICS_SUFFIX"
ENV_HTTP_TRACES_SUFFIX  = "TELEMETRY_TRACES_SUFFIX"
ENV_HTTP_LOGS_SUFFIX    = "TELEMETRY_LOGS_SUFFIX"

class TelemetryConfigException (Exception): pass

def get_loglevel_from_name (name: str):
    if name == "CRITICAL":
        return logging.CRITICAL
    if name == "ERROR":
        return logging.ERROR
    if name == "WARNING":
        return logging.WARNING
    if name == "INFO":
        return logging.INFO
    if name == "DEBUG":
        return logging.DEBUG

    raise TelemetryConfigException(
        f"Could not find log level for name '{name}' "
        + "(expecting 'CRITICAL', 'ERROR', 'WARNING', 'INFO' or 'DEBUG')"
    )

class BaseConfig:
    resource: Resource

    # Log Parameters
    loglevel  = logging.NOTSET
    formatter: "logging.Formatter | None" = None

    def __init__ (self):
        self.resource = Resource({})
    @staticmethod
    def from_env () -> "BaseConfig":
        target_type = os.environ.get( ENV_CONFIG_TYPE )

        resource_params = {}

        for key in dir(ResourceAttributes):
            if "__" in key: continue

            val = os.getenv(f"TELEMETRY_RESOURCE_{key}")
            if val is None: continue

            resource_params[getattr(ResourceAttributes, key)] = val

        config = None
        if target_type == "TEST": config = TestConfig.from_env()
        if target_type == "HTTP": config = HttpConfig.from_env()

        if config is None:
            raise TelemetryConfigException(
                f"Environment variable '{ENV_CONFIG_TYPE}' \
                    (with value {target_type}) should be either 'TEST' or 'HTTP'")

        config.resource = Resource(resource_params)
        
        loglevel_target = os.environ.get(ENV_CONFIG_LOGLEVEL, None)
        if loglevel_target is not None:
            config.loglevel = get_loglevel_from_name( loglevel_target )

        return config

class TestConfig(BaseConfig):
    @staticmethod
    def from_env ():
        return TestConfig()

class HttpConfig(BaseConfig):
    endpoint: str

    suffix_metrics: str = "/v1/metrics"
    suffix_traces : str = "/v1/traces"
    suffix_logs   : str = "/v1/logs"

    @staticmethod
    def from_env():
        endpoint = os.getenv( ENV_HTTP_ENDPOINT )
        if endpoint is None:
            raise TelemetryConfigException(f"Environment variable '{ENV_HTTP_ENDPOINT}' should be set in 'HTTP' mode.")
        
        force_slash = False
        force_slash_env = os.getenv( ENV_HTTP_FORCE_SLASH )
        if force_slash_env is not None:
            force_slash = force_slash_env == 'TRUE'
            if not force_slash and force_slash_env != 'FALSE':
                raise TelemetryConfigException(f"Environment variable '{ENV_HTTP_FORCE_SLASH}' should be set to 'TRUE', 'FALSE' or shouldn't be set at all.")
        
        config = HttpConfig(endpoint, force_slash)

        config.suffix_metrics = os.getenv( ENV_HTTP_METRICS_SUFFIX, config.suffix_metrics )
        config.suffix_traces  = os.getenv( ENV_HTTP_TRACES_SUFFIX,  config.suffix_traces  )
        config.suffix_logs    = os.getenv( ENV_HTTP_LOGS_SUFFIX,    config.suffix_logs    )

        return config

    def __init__(self, endpoint: str, force_ending_slash: bool = False):
        super().__init__()

        if endpoint.endswith("/") and not force_ending_slash:
            print("WARNING, the ending '/' will be removed by default.")
            endpoint = endpoint[:-1]

        self.endpoint = endpoint

    @property
    def metrics_endpoint (self):
        return self.endpoint + self.suffix_metrics
    @property
    def traces_endpoint (self):
        return self.endpoint + self.suffix_traces
    @property
    def logs_endpoint (self):
        return self.endpoint + self.suffix_logs