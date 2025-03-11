
import os

from opentelemetry.sdk.resources import *

ENV_CONFIG_TYPE   = "TELEMETRY_CONFIG_TYPE"
ENV_HTTP_ENDPOINT = "TELEMETRY_HTTP_ENDPOINT"

ENV_HTTP_METRICS_SUFFIX = "TELEMETRY_METRICS_SUFFIX"
ENV_HTTP_TRACES_SUFFIX  = "TELEMETRY_TRACES_SUFFIX"
ENV_HTTP_LOGS_SUFFIX    = "TELEMETRY_LOGS_SUFFIX"

class TelemetryConfigException (Exception): pass

class BaseConfig:
    resource: Resource

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
        print(resource_params)

        config = None
        if target_type == "TEST": config = TestConfig.from_env()
        if target_type == "HTTP": config = HttpConfig.from_env()

        if config is None:
            raise TelemetryConfigException(
                f"Environment variable '{ENV_CONFIG_TYPE}' \
                    (with value {target_type}) should be either 'TEST' or 'HTTP'")

        config.resource = Resource(resource_params)

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
        
        config = HttpConfig(endpoint)

        config.suffix_metrics = os.getenv( ENV_HTTP_METRICS_SUFFIX, config.suffix_metrics )
        config.suffix_traces  = os.getenv( ENV_HTTP_TRACES_SUFFIX,  config.suffix_traces  )
        config.suffix_logs    = os.getenv( ENV_HTTP_LOGS_SUFFIX,    config.suffix_logs    )

        return config

    def __init__(self, endpoint: str):
        super().__init__()

        self.endpoint = endpoint

    @property
    def metrics_endpoint (self):
        return self.endpoint + self.suffix_metrics
    @property
    def traces_endpoint (self):
        return self.endpoint + self.suffix_traces