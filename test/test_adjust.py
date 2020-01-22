import pytest

import sys
import json
import io
import importlib

from adjust_driver import Ec2S3Driver, DESC, HAS_CANCEL, VERSION

adjust_settings = {
    "application": {
        "components": {
            "web": {
                "settings": {
                    "UriEnableCache": {"value": 1},
                    "UriScavengerPeriod": {"value": 260},
                    "WebConfigCacheEnabled": {"value": 0},
                    "WebConfigEnableKernelCache": {"value": 1},
                    "inst_type": {"value": "t2.micro"}
                }
            }
        }
    }
}

def test_version(monkeypatch):
    with monkeypatch.context() as m:
        # replicate command line arguments fed in by servo
        m.setattr(sys, 'argv', ['', '--version', '1234'])
        driver = Ec2S3Driver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION)
        with pytest.raises(SystemExit) as exit_exception:
            driver.run()
        assert exit_exception.type == SystemExit
        assert exit_exception.value.code == 0

def test_info(monkeypatch):
    with monkeypatch.context() as m:
        # replicate command line arguments fed in by servo
        m.setattr(sys, 'argv', ['', '--info', '1234'])
        driver = Ec2S3Driver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION)
        with pytest.raises(SystemExit) as exit_exception:
            driver.run()
        assert exit_exception.type == SystemExit
        assert exit_exception.value.code == 0

def test_query(monkeypatch):
    with monkeypatch.context() as m:
        # replicate command line arguments fed in by servo
        m.setattr(sys, 'argv', ['', '--query', '1234'])
        driver = Ec2S3Driver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION)
        with pytest.raises(SystemExit) as exit_exception:
            driver.run()
        assert exit_exception.type == SystemExit
        assert exit_exception.value.code == 0

def test_adjust(monkeypatch):
    with monkeypatch.context() as m:
        # replicate command line arguments fed in by servo
        m.setattr(sys, 'argv', ['', '1234'])
        m.setattr(sys, 'stdin', io.StringIO(json.dumps(adjust_settings)))
        driver = Ec2S3Driver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION)
        driver.run()
        assert True

# Load static utf-16-le textfile containing content that would be returned by describe endpoint
describe_endpoint_resp_text_bytes = open('describe.json', 'rb').read()
test_insts_described = [ 
    { "PublicIpAddress": '192.168.1.1', "InstanceId": 1 },
    { "PublicIpAddress": '192.168.1.2', "InstanceId": 2 }
]

def test_validate(monkeypatch, requests_mock):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['', '1234']) # override argv so pytest args are not parsed by driver
        # Requests mock
        for ti in test_insts_described:
            requests_mock.register_uri(
                'GET',
                'http://{}:8080/describe.json'.format(ti["PublicIpAddress"]),
                content=describe_endpoint_resp_text_bytes
            )

        validator = importlib.import_module('adjust_driver').get_validator.__func__()

        result = validator(
            component_key='web',
            described_instances=test_insts_described,
            settings_to_verify=adjust_settings['application']['components']['web']['settings']
        )
        
        assert result == []
