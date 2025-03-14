
.. _telem_traces:

How to write traces
=====================

First of all, we need to define a bit what traces are about as it isn't as usual as logs or metrics.
A trace is a simple representation of the computations and steps taken by the infrastructure to process
a request.

In OpenTelemetry, it involves two types of objects, spans and events. A span is a computation that takes place
during a time interval, and an event is something that happens at a specific time, and that takes place in a space.
A span can have subspans and so the computation will look like a tree structure that can be both in space (in different
services) and in time. Events usually represent status updates such as exceptions or issues.

Each span and event related to the same computation are connected with the trace id.
The root span of a computation automatically creates the trace id for the full computation.

Creating a simple span with an event
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a span, one needs to first acquire the tracer in a similar way as what is done with metrics.
Once a span is acquired, you can add arguments to it or add events. For example, you can do the following :

.. code-block:: python

    from telemetry import traces

    # Configure...

    # Get the tracer for the current file
    tracer = traces.get_tracer(__name__)

    # You need to provide the name of the span when starting it
    with tracer.start_as_current_span("first_span") as span:
        # You can set an attribute
        # Attributes do not depend on the time
        span.set_attribute("key", "value")

        # Do something...

        # You can also add an event with attributes
        # Events are time-dependent, that is adding it at the
        # Start of the span is different than adding it at the end.
        span.add_event(
            "some_event",
            { "event_attribute": "Some reason for the event" }
        )

You can add a subspan by simply doing the following, and the two spans will appear in the dashboard.

.. code-block:: python
    
    with tracer.start_as_current_span("parent_span"):
        # Do something before
        with tracer.start_as_current_span("child_span"):
            # Do something
        # Do something after

Injecting the span in a request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You might want to transfer a span context and a trace to another part of your infrastructure.
To do that, you can either send the span context, but you can easily inject the span id and trace id
into the headers of an HTTP request using the inject method.

.. code-block:: python
    
    from telemetry import traces

    headers = {}
    traces.inject(headers)
    # Do some HTTP request with the headers

The receiving HTTP server needs to be instrumented properly using for example the django instrumentor or
an equivalent instrumentor. You may want to look at the 
`OTEL Python Contrib Documentation <https://opentelemetry-python-contrib.readthedocs.io/en/latest/index.html>`_
to find the instrumentator you need.

.. note::
   If you need to do more advanced context propagation, you can read about the 
   `OpenTelemetry Propagation API <https://opentelemetry.io/docs/specs/otel/context/api-propagators/>`_.
