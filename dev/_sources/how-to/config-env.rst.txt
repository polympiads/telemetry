
.. _config_env:

How to configure the telemetry from the environment
======================================================

.. note::
   This is the recommended way to use this framework for code that runs in production,
   as it allows to modify a lot of parameters using environment variables.

To configure the framework from the environment, you can use the ``configure_from_env`` method.

.. code-block:: python

    from telemetry import configure_from_env

    configure_from_env()

By default, if no environment variable is set, this will result in a crash as the environment does not
provide enough information for the configuration to be generated. The first environment variable you
need to provide is ``TELEMETRY_CONFIG_TYPE``, which tells the telemetry which configuration type to use.

For example, if you want to use the ``TestConfig`` object, you must set the value to ``TEST``. If you want
to use the ``HttpConfig`` object, you must set the value to ``HTTP``. Any other value will result in a crash.
The HTTP configuration requires more environment variables to be properly initialized, and so you need to
set them as described in :ref:`Http-Specific Configuration <config_env_http_specific>`.

.. _config_env_resource:

Setting the parameters of the resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To provide the necessary information about the current container or the current service being run,
one has to provide the necessary arguments in an opentelemetry ``Resource`` object. To do that from
the environment, the telemetry framework provides one environment variable per argument you could pass
to the resource. 

Given the name of the argument, as described by the
`OpenTelemetry Semantic Convention <https://github.com/open-telemetry/opentelemetry-python/blob/main/opentelemetry-semantic-conventions/src/opentelemetry/semconv/resource/__init__.py>`_
in the ``ResourceAttributes`` object, the environment variable will be ``TELEMETRY_RESOURCE_`` followed
by the name. For example, if you want to set ``SERVICE_NAME``, you need to set the environment variable
``TELEMETRY_RESOURCE_SERVICE_NAME``.

.. _config_env_http_specific:

Http-Specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``HttpConfig`` generated when ``TELEMETRY_CONFIG_TYPE`` is set to ``HTTP`` provides a few
environment variables to modify the behaviour of the endpoints in a similar way as what is done
in :ref:`HttpConfig's Advanced Endpoint Guide <config_http_advanced_endpoints>`.

In particular, you can set the base HTTP endpoint using the ``TELEMETRY_HTTP_ENDPOINT`` environment
variable. If this variable is missing, your code wont start. If you need to enforce the slash at the end of
the base endpoint as per :ref:`How to have an ending slash in the endpoint <config_http_force_ending_slash>`,
you can use the ``TELEMETRY_HTTP_FORCE_SLASH`` environment variable and set it to ``TRUE`` or ``FALSE``.
Any other value will result in a ``TelemetryConfigException``.

To modify the suffixes of the HTTP endpoints, you can use one of the ``TELEMETRY_METRICS_SUFFIX``,
``TELEMETRY_TRACES_SUFFIX`` and ``TELEMETRY_LOGS_SUFFIX`` environment variables, that allow you
to change the default suffix. If they are absent, the default value will be the one used by the 
``grafana/otel-lgtm`` docker image, as described in :ref:`How to configure the http exporters <config_http>`.

Example of HTTP Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   
   export TELEMETRY_CONFIG_TYPE="HTTP"
   export TELEMETRY_HTTP_ENDPOINT="http://localhost:4318"

   export TELEMETRY_RESOURCE_SERVICE_NAME="service"
   export TELEMETRY_RESOURCE_HOST_NAME="host_name"

   # Call your python code
