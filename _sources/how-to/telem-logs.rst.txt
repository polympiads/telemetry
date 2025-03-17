
.. _telem_logs:

How to write logs
==================

The logging system uses the classical Python ``logging`` library so
all the features that are available in the library are mostly available.
For certain features, you might need to set the value of the ``loglevel``
or the ``formatter`` value of the config as described in
:ref:`How to configure HTTP <config_http>`.

If you need to use advanced features of logging, you can check the 
`Python Logging Library <https://docs.python.org/3/library/logging.html>`_,
which should contain the informations you need.

When logging using one of the standard logging functions such as ``debug``, ``info``, ``warn``,
``warning``, ``error`` and ``critical``, you can pass extra arguments that will be displayed
in the final dashboard if correctly configured. For example, you can do the following :

.. code-block:: python
    
    logging.critical( "Some critical message", extra = { "arg": 42 } )
