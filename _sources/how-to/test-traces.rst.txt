
.. _test_traces:

How to write unittests for traces
=================================

Writting unittests in telemetry is hard and can take a long time as it is usually something
that you look at, not something that is easily unit tested. To counter that, the telemetry framework
provides a scheme framework. A scheme is the representation of the expected way the trace should look.

For example, you could write the following scheme to represent a complex computation involving multiple
events and subspans :

.. code-block::

   +    Span  "some_span" [some_attr:1][other_attr:abcd]
   |    Event "e1"    
   | +  Span  "other_span" [one_attr:42]
   | |  Event "e2"
   | +
   |    Event "e3" [eattr:R]
   +

Here, the scheme described a root span named ``"some_span"``, with attributes ``{ "some_attr": 1, "other_attr": "abcd" }``.
Containing first in order an event named ``"e1"`` with no attributes, a subspan named ``"other_span"``
with attributes ``{ "one_attr": 42 }`` and an event named ``"e2"`` inside of it, and finally in the root
span an event named ``"e3"`` with attributes ``{ "eattr": "R" }``.

You can verify that the scheme is equivalent to the latest spans by calling ``VirtualContext.verify_scheme``
with your scheme string. You can also provider a verbosity (either ``FULL`` or ``NONE``, where ``FULL`` prints
only the expected and found schemes). You could do something like this :

.. code-block:: python

   assert VirtualContext.verify_scheme("""
       +    Span  "some_span" [some_attr:1][other_attr:abcd]
       |    Event "e1"    
       | +  Span  "other_span" [one_attr:42]
       | |  Event "e2"
       | +
       |    Event "e3" [eattr:R]
       +
   """)

.. warning::
   Please note that the expected and found schemes might differ if some timings overlap (for example two
   spans last less than a microsecond and they get swapped in the display).

   Theoretically, the verifier should still be able to verify the schemes as it checks greedily
   all valid equivalent spans and events, but you should be careful as wrong configuration can lead
   to increasingly slow checks.

   To avoid that, try to avoid spans that last less than a microsecond or if there are some, try
   avoiding them lasting having both the same name and the same attributes.

Advanced testing
~~~~~~~~~~~~~~~~~

.. note::
   This is not the recommended way to do unit testing on traces as it can lead to really long code
   to check that the traces are the same as what you expects.

If you want to access directly the underlying spans, you can get the ``InMemorySpanExporter`` by
calling ``telemetry.traces.get_test_exporter()``. It provides the methods ``get_finished_spans`` and ``clear``.
