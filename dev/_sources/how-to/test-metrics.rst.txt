
.. _test_metrics:

How to write unittests for metrics
===================================

Writting unittests in telemetry is hard and can take a long time as it is usually something
that you look at, not something that is easily unit tested. To counter that, the telemetry framework
provides a scheme framework. A scheme is the representation of the expected way the metrics should look.

For example, you could write the following scheme to check for a gauge called ``some_gauge`` that is ``1``
without arguments, and ``1.5`` with arguments ``{ "f1": "hello" }``.

.. code-block:: 

   some_gauge = 1
   some_gauge[f1:hello] = 1.5

Once you have described your scheme as a string, you can call ``CollectedMetrics.verify_scheme`` with the scheme.
For example, you could do the following :

.. code-block:: python

   assert CollectedMetrics.verify_scheme("""
       some_gauge = 1
       some_gauge[f1:hello] = 1.5
   """)

If you want to simplify debugging in case of a test failure, you can provide a test verbosity to the method,
either ``MetricsTestVerbosity.SIMPLE_ERROR`` or ``MetricsTestVerbosity.FULL_LOG``. The ``SIMPLE_ERROR`` will
only show a simple error message such as ``Wrong value for metric 'gauge', with expected value 1, found 2 (distance 1 > 0)``.
In case you provide the ``FULL_LOG``, the framework will print both the expected and found metrics in the scheme
format, as well as the error message.

You may also provide a ``tolerance`` parameters, that allows you to set the tolerance on floating point numbers.

Advanced Testing
~~~~~~~~~~~~~~~~~

.. note::
   This is not the recommended way to do unit testing on metrics as it can lead to really long code
   to check that the metrics are the same as what you expects.

If you need some advanced unit testing, you can call the ``telemetry.metrics.get_test_reader()`` method
that returns an ``InMemoryMetricsReader``. It provides a ``get_metrics_data()`` method that returns and clears
the latest metrics data. 
