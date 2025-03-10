
from typing import Type

from opentelemetry import metrics
from opentelemetry.metrics import get_meter
from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter as GRPCExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as HTTPExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, InMemoryMetricReader

from telemetry.config import TestConfig, HttpConfig

_TEST_READER = InMemoryMetricReader()

def _configure (endpoint: str, exporter: "Type[GRPCExporter] | Type[HTTPExporter]"):
    exporter = exporter( endpoint )
    reader   = PeriodicExportingMetricReader( exporter )

    provider = MeterProvider(metric_readers=[reader])

    metrics.set_meter_provider(provider)

def configure_http (config: "HttpConfig"):
    print(HTTPExporter)
    _configure(config.metrics_endpoint, HTTPExporter)

def get_test_reader ():
    return _TEST_READER
def configure_test (config: "TestConfig"):
    provider = MeterProvider(metric_readers=[_TEST_READER])

    metrics.set_meter_provider(provider)
