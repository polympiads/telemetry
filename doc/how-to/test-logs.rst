
.. _test_logs:

How to write unittests for logs
===============================

Writting unittests in telemetry is hard and can take a long time as it is usually something
that you look at, not something that is easily unit tested. To counter that, the telemetry framework
provides a scheme framework. A scheme is the representation of the expected way the logs should look.

For example, you could write the following scheme to check for two logs, one ``CRITICAL`` with message ``"Some
critical message"`` and parameters ``{ "param": "1", "request": "GET /path" }``, and the other one ``ERROR`` with
message ``"Some error message"`` and no parameters.

.. code-block:: 

   CRITICAL "Some critical message" [param:1][request:GET /path]
   ERROR     Some error message

Once you have your scheme, you can call ``VirtualLogRecords.verify_from_scheme`` with the scheme of your string
to verify that the latest logs are the same as the logs you expect (if there are additional parameters in your
logs, they wont fail the result). For example, you could do the following

.. code-block:: python

   assert VirtualLogRecords.verify_from_scheme("""
       CRITICAL "Some critical message" [param:1][request:GET /path]
       ERROR     Some error message
   """)

If you want to simplify debugging in case of a test failure, you can provider a test verbosity to the method,
either ``LogTestVerbosity.ONLY_ERROR`` or ``LogTestVerbosity.FULL``. The ``ONLY_ERROR`` mode will print the
first logs that differ and why they differ, and the ``FULL`` verbosity will print the logs found in scheme format,
the expected logs in scheme format and the error message.

Advanced Testing
~~~~~~~~~~~~~~~~~

.. note::
   This is not the recommended way to do unit testing on logs as it can lead to really long code
   to check that the logs are the same as what you expects.

The test logging is handled by a custom logging handler of type ``TestLoggingHandler``.
You can get the test handler that is used in the configuration using ``telemetry.logging.get_test_handler()``
It provides twos methods, ``get_sent_records`` and ``clear`` to allow you to retrieve the records and clear
them once you don't need them anymore.
