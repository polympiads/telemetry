
.. _telem_metrics:

How to write metrics
=====================

.. note::
   The metric system uses the ``OpenTelemetry`` metric instruments. You can read more about the
   full list of instruments that you may use in `OpenTelemetry Metrics <https://opentelemetry.io/docs/concepts/signals/metrics/#metric-instruments>`_.

The first step to create good metrics is to first create the metric instruments.
A metric instrument is an object that allows you to set the value of a metric.
For example, a Gauge metric instrument is the simplest object, for which you can simply set the value.
On the other hand, a Counter is an object on which you can increment the value.

If you want to create a Gauge, you first need to get the meter (that is, the factory of
metric instruments for the current file, similarly to the name of ``getLogger`` in the Python ``logging`` library),
and then you can instantiate the gauge from the meter.

.. code-block:: python

    from telemetry import metrics

    # Configure the framework...

    # Get metrics and create the gauge
    meter = metrics.get_meter(__name__)
    gauge = meter.create_gauge(
        "example_gauge", unit="...", description="..."
    )

    gauge.set(1)
    # Do something...
    gauge.set(2)

You can choose the unit as you wish, but you can find a non-exhaustive list of
the usual units used in metrics in the `Prometheus Documentation <https://prometheus.io/docs/practices/naming/#base-units>`_.

There are certain conventions on how to properly name your metrics. These are
described in the `Prometheus Documentaton <https://prometheus.io/docs/practices/naming/#metric-names>`_

.. note::
   You need to avoid creating metric instruments multiple times.
   Usually one instantiates the instrument only once per metric.

Understanding labels
~~~~~~~~~~~~~~~~~~~~~

Labels are core to metrics as you don't want to create too many metrics,
as each one of these needs one global variable. Labels are used to
infer some properties on the metrics, such as error status, or special
parameters. For example, we can extend the previous code so the gauge
has a status.

.. code-block:: python

    gauge.set(1, { "status": "BEFORE" })
    # Do something...
    gauge.set(2, { "status": "AFTER" })

.. warning::
   To avoid flooding the databases with unnecessary data, the labels have to be general data not user-specific data.
   For example, you don't want to have a "username" label on your login page, but you could have a
   "auth-method" label to differentiate between two authentication methods (for example email vs oauth).
