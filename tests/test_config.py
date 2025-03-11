
import os

from unittest.mock import patch, Mock

from telemetry import configure, configure_from_env
from telemetry.config import TestConfig as _TestConfig
from telemetry.config import BaseConfig, HttpConfig, \
    ENV_CONFIG_TYPE, ENV_HTTP_ENDPOINT, ENV_HTTP_LOGS_SUFFIX, \
    ENV_HTTP_METRICS_SUFFIX, ENV_HTTP_TRACES_SUFFIX, \
    Resource, SERVICE_NAME

@patch("telemetry.metrics.configure_test")
def test_configure_test_config (configure_test: Mock):
    config = _TestConfig()
    configure( config )

    configure_test.assert_called_once_with(config)

@patch("telemetry.metrics.configure_http")
def test_configure_http_config (configure_http: Mock):
    config = HttpConfig("http://localhost:4318")
    configure( config )

    configure_http.assert_called_once_with( config )

def create_obj (cls, args = [], kwargs = {}, fields = {}):
    obj = cls(*args, **kwargs)

    for key in fields:
        setattr(obj, key, fields[key])
def check_obj (a, b):
    assert dir(a) == dir(b)

    for x in dir(a):
        if "__" in x: continue
        assert getattr(a, x) == getattr(b, x)

@patch("telemetry.configure")
def test_from_env (configure: Mock):
    TESTS = []

    TESTS.append((
        None,
        {  }
    ))
    TESTS.append((
        _TestConfig(),
        { ENV_CONFIG_TYPE: "TEST" }
    ))
    tconfig = _TestConfig()
    tconfig.resource = Resource({ SERVICE_NAME: "some_service" })
    TESTS.append((
        tconfig,
        { ENV_CONFIG_TYPE: "TEST", "TELEMETRY_RESOURCE_SERVICE_NAME": "some_service" }
    ))
    TESTS.append((
        None,
        { ENV_CONFIG_TYPE: "HTTP" }
    ))
    TESTS.append((
        HttpConfig( "http://localhost:4318" ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318" }
    ))
    TESTS.append((
        create_obj( HttpConfig, [ "http://localhost:4318" ], {}, { "suffix_traces": "/v2/traces" } ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318", ENV_HTTP_TRACES_SUFFIX: "/v2/traces" }
    ))
    TESTS.append((
        create_obj( HttpConfig, [ "http://localhost:4318" ], {}, { "suffix_metrics": "/v2/traces" } ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318", ENV_HTTP_METRICS_SUFFIX: "/v2/traces" }
    ))
    TESTS.append((
        create_obj( HttpConfig, [ "http://localhost:4318" ], {}, { "suffix_logs": "/v2/traces" } ),
        { ENV_CONFIG_TYPE: "HTTP", ENV_HTTP_ENDPOINT: "http://localhost:4318", ENV_HTTP_LOGS_SUFFIX: "/v2/traces" }
    ))

    for expects, envs in TESTS:
        try:
            for key in envs.keys():
                os.environ.update([ (key, envs[key]) ])
            
            result = BaseConfig.from_env()

            check_obj(expects, result)
        except Exception as e:
            assert expects is None
        finally:
            for key in envs.keys():
                os.environ.pop(key)
        
        try:
            for key in envs.keys():
                os.environ.update([ (key, envs[key]) ])
            
            configure.reset_mock()
            configure_from_env()
            configure.assert_called_once()
            objs = configure.call_args_list[0]
            assert len(objs.args) == 1

            check_obj(expects, objs.args[0])
        except Exception as e:
            assert expects is None
        finally:
            for key in envs.keys():
                os.environ.pop(key)
