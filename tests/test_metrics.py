
from unittest.mock import patch, Mock

from telemetry.config import HttpConfig, TestConfig
from telemetry.metrics import configure_http, configure_test, get_test_reader

from opentelemetry.sdk.metrics import MeterProvider

@patch("opentelemetry.metrics.set_meter_provider")
def test_configure_test (set_meter_provider: Mock):
    MeterProvider._all_metric_readers.clear()

    configure_test(TestConfig())

    set_meter_provider.assert_called_once()    

    provider_call = set_meter_provider.call_args_list[0]
    assert len(provider_call.args) == 1
    provider: MeterProvider = provider_call.args[0]
    readers = list(provider._all_metric_readers)
    assert len(readers) == 1
    assert readers[0] is get_test_reader()
    
    MeterProvider._all_metric_readers.clear()

@patch("telemetry.metrics.MeterProvider")
@patch("telemetry.metrics.PeriodicExportingMetricReader")
@patch("telemetry.metrics.HTTPExporter")
@patch("opentelemetry.metrics.set_meter_provider")
def test_configure_http (set_meter_provider: Mock, otlp_exporter: Mock, periodic_reader: Mock, meter_provider: Mock):
    otlp_exporter.return_value   = Mock()
    periodic_reader.return_value = Mock()
    meter_provider.return_value  = Mock()

    configure_http( HttpConfig("http://localhost:4318") )
    set_meter_provider.assert_called_once_with( meter_provider.return_value )
    meter_provider    .assert_called_once_with( metric_readers=[ periodic_reader.return_value ] )
    periodic_reader   .assert_called_once_with( otlp_exporter.return_value )
    otlp_exporter     .assert_called_once_with( "http://localhost:4318/v1/metrics" )
