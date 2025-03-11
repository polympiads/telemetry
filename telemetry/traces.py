
from opentelemetry import trace
from opentelemetry.trace import get_tracer
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as HTTPExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as GRPCExporter
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor

from telemetry.config import TestConfig, HttpConfig

#################
# CONFIGURATION #
#################

_TEST_EXPORTER = InMemorySpanExporter()

def configure_http (config: HttpConfig):
    provider = TracerProvider(resource=config.resource)
    provider.add_span_processor(BatchSpanProcessor(HTTPExporter( config.traces_endpoint )))

    trace.set_tracer_provider(provider)

def get_test_exporter ():
    return _TEST_EXPORTER
def configure_test (config: TestConfig):
    provider = TracerProvider(resource=config.resource)
    provider.add_span_processor(SimpleSpanProcessor(_TEST_EXPORTER))

    trace.set_tracer_provider(provider)
