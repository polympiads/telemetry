
from unittest.mock import patch, Mock

from telemetry import using_test_config
from telemetry.config import HttpConfig
from telemetry.config import TestConfig as _TestConfig
from telemetry.traces import configure_test, configure_http, get_test_exporter, get_tracer

@patch("telemetry.traces.TracerProvider")
@patch("telemetry.traces.BatchSpanProcessor")
@patch("telemetry.traces.HTTPExporter")
@patch("opentelemetry.trace.set_tracer_provider")
def test_configure_http (
        set_tracer_provider: Mock, http_exporter: Mock,
        batch_processor : Mock, tracer_provider : Mock):
    tracer_provider.return_value = Mock()
    tracer_provider.return_value.add_span_processor = Mock()

    http_exporter  .return_value = Mock()
    batch_processor.return_value = Mock()

    http_config = HttpConfig( "http://localhost:4318" )
    configure_http(http_config)

    set_tracer_provider.assert_called_once_with( tracer_provider.return_value )
    tracer_provider.return_value.add_span_processor \
        .assert_called_once_with( batch_processor.return_value )
    batch_processor.assert_called_once_with( http_exporter.return_value )
    http_exporter.assert_called_once_with( http_config.traces_endpoint )
    tracer_provider.assert_called_once_with( resource=http_config.resource )

@patch("telemetry.traces.TracerProvider")
@patch("telemetry.traces.SimpleSpanProcessor")
@patch("opentelemetry.trace.set_tracer_provider")
def test_configure_test (set_tracer_provider: Mock, simple_processor: Mock, tracer_provider: Mock):
    tracer_provider.return_value = Mock()
    tracer_provider.return_value.add_span_processor = Mock()
    simple_processor.return_value = Mock()
    set_tracer_provider.return_value = Mock()

    test_config = _TestConfig()
    configure_test(test_config)

    set_tracer_provider.assert_called_once_with( tracer_provider.return_value )
    tracer_provider.return_value.add_span_processor \
        .assert_called_once_with( simple_processor.return_value )
    simple_processor.assert_called_once_with( get_test_exporter() )
    tracer_provider.assert_called_once_with(resource=test_config.resource)

@using_test_config
def test_traces ():
    tracer = get_tracer("tests")

    with tracer.start_as_current_span("some_span") as some_span:
        some_span.add_event("e1")
        with tracer.start_as_current_span("other_span") as other_span:
            other_span.add_event("e2")
            other_span.set_attribute("one_attr", 42)
        some_span.add_event("e3", { "eattr": "R" })
        some_span.set_attribute("some_attr", 1)
        some_span.set_attribute("other_attr", "abcd")

    exporter = get_test_exporter()
    spans = exporter.get_finished_spans()
    if spans[0].parent is None:
        a, b = spans
        spans = a, b

    assert len(spans) == 2
    assert spans[0].parent == spans[1].context

    child = spans[0]
    root  = spans[1]

    assert child.name == "other_span"
    assert len(child.events) == 1

    event2 = child.events[0]
    assert event2.name == "e2"
    assert child.attributes == { "one_attr": 42 }

    assert root.name == "some_span"
    assert len(root.events) == 2

    event1, event3 = root.events
    assert event1.name == "e1"
    assert event3.name == "e3"
    assert event3.attributes == { "eattr": "R" }

    assert root.attributes == { "some_attr": 1, "other_attr": "abcd" }
