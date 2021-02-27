import unittest

from unittest import mock

from libpurecool.dyson_pure_cool import DysonPureCool
from libpurecool.dyson_pure_hotcool import DysonPureHotCool
from libpurecool.dyson import DysonAccount, DysonPureCoolLink, \
    DysonPureHotCoolLink, Dyson360Eye, DysonNotLoggedException, \
    DYSON_API_USER_AGENT

API_HOST = 'appapi.cp.dyson.com'
API_CN_HOST = 'appapi.cp.dyson.cn'


class MockResponse:
    def __init__(self, json, status_code=200):
        self._json = json
        self.status_code = status_code

    def json(self, **kwargs):
        return self._json


def _mocked_login_post_failed(*args, **kwargs):
    url = 'https://{0}{1}?{2}={3}'.format(API_HOST,
                                          '/v1/userregistration/authenticate',
                                          'country',
                                          'language')
    payload = {'Password': 'password', 'Email': 'email'}
    if args[0] == url and kwargs['data'] == payload and \
            kwargs['headers'] == {'User-Agent': DYSON_API_USER_AGENT}:
        return MockResponse({
            'Account': 'account',
            'Password': 'password'
        }, 401)
    else:
        raise Exception("Unknown call")

def _mock_gets(*args, **kwargs):
    if "provisioningservice" in args[0]:
        return _mocked_list_devices(*args, **kwargs)
    else:
        return _mocked_status_get(*args, **kwargs)

def _mocked_status_get(*args, **kwargs):
    url = 'https://{0}{1}'.format(API_HOST,
                                          '/v1/userregistration/userstatus')
    params = {"country": "language", "email": "email"}
    if args[0] == url and kwargs['params'] == params:
        return MockResponse({
            'accountStatus': 'ACTIVE'
        })
    else:
        raise Exception("Unknown call")

def _mocked_status_get_cn(*args, **kwargs):
    url = 'https://{0}{1}'.format(API_CN_HOST,
                                          '/v1/userregistration/userstatus')
    params = {"country": "CN", "email": "email"}
    if args[0] == url and kwargs['params'] == params:
        return MockResponse({
            'accountStatus': 'ACTIVE'
        })
    else:
        raise Exception("Unknown call")

def _mocked_status_get_failed(*args, **kwargs):
    url = 'https://{0}{1}'.format(API_HOST,
                                          '/v1/userregistration/userstatus')
    params = {"country": "language", "email": "email"}
    if args[0] == url and kwargs['params'] == params:
        return MockResponse({
            'accountStatus': 'INACTIVE'
        })
    else:
        raise Exception("Unknown call")

def _mocked_login_post(*args, **kwargs):
    url = 'https://{0}{1}?{2}={3}'.format(API_HOST,
                                          '/v1/userregistration/authenticate',
                                          'country',
                                          'language')
    payload = {'Password': 'password', 'Email': 'email'}
    if args[0] == url and kwargs['json'] == payload and \
            kwargs['headers'] == {'User-Agent': DYSON_API_USER_AGENT}:
        return MockResponse({
            'Account': 'account',
            'Password': 'password'
        })
    else:
        raise Exception("Unknown call")


def _mocked_login_post_cn(*args, **kwargs):
    url = 'https://{0}{1}?{2}={3}'.format(API_CN_HOST,
                                          '/v1/userregistration/authenticate',
                                          'country',
                                          'CN')
    payload = {'Password': 'password', 'Email': 'email'}
    if args[0] == url and kwargs['json'] == payload and \
            kwargs['headers'] == {'User-Agent': DYSON_API_USER_AGENT}:
        return MockResponse({
            'Account': 'account',
            'Password': 'password'
        })
    else:
        raise Exception("Unknown call")


def _mocked_list_devices(*args, **kwargs):
    url = 'https://{0}{1}'.format(API_HOST,
                                  '/v1/provisioningservice/manifest')
    url_v2 = 'https://{0}{1}'.format(API_HOST,
                                     '/v2/provisioningservice/manifest')

    if args[0] == url:
        return MockResponse(
            [
                {
                    "Active": True,
                    "Serial": "device-id-1",
                    "Name": "device-1",
                    "ScaleUnit": "SU01",
                    "Version": "21.03.08",
                    "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                        "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                        "bCm7uYeTORULKLKQ==",
                    "AutoUpdate": True,
                    "NewVersionAvailable": False,
                    "ProductType": "475"
                },
                {
                    "Active": False,
                    "Serial": "device-id-2",
                    "Name": "device-2",
                    "ScaleUnit": "SU02",
                    "Version": "21.02.04",
                    "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuebkH6aWl2H5Q1vCq"
                                        "CQSjJfENzMefozxWaDoW1yDluPsi09SGT5nW"
                                        "MxqxtrfkxnUtRQ==",
                    "AutoUpdate": False,
                    "NewVersionAvailable": True,
                    "ProductType": "455"
                },
                {
                    "Active": True,
                    "Serial": "device-id-3",
                    "Name": "device-3",
                    "ScaleUnit": "SU01",
                    "Version": "21.03.08",
                    "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                        "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                        "bCm7uYeTORULKLKQ==",
                    "AutoUpdate": True,
                    "NewVersionAvailable": False,
                    "ProductType": "N223"
                }
            ]
        )

    if args[0] == url_v2:
        return MockResponse(
            [
                {
                    "Serial": "AB1-EU-DBD1231B",
                    "Name": "device-1",
                    "Version": "02.05.001.0006",
                    "AutoUpdate": True,
                    "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                        "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                        "bCm7uYeTORULKLKQ==",
                    "NewVersionAvailable": False,
                    "ProductType": "438"
                },
                {
                    "Serial": "DB1-US-DBD1231D",
                    "Name": "device-3",
                    "Version": "02.05.001.0006",
                    "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuebkH6aWl2H5Q1vCq"
                                        "CQSjJfENzMefozxWaDoW1yDluPsi09SGT5nW"
                                        "MxqxtrfkxnUtRQ==",
                    "AutoUpdate": True,
                    "NewVersionAvailable": False,
                    "ProductType": "520"
                },
                {
                    "Serial": "CB1-US-DBD1231C",
                    "Name": "device-4",
                    "Version": "02.05.001.0006",
                    "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuebkH6aWl2H5Q1vCq"
                                        "CQSjJfENzMefozxWaDoW1yDluPsi09SGT5nW"
                                        "MxqxtrfkxnUtRQ==",
                    "AutoUpdate": True,
                    "NewVersionAvailable": False,
                    "ProductType": "527"
                }
            ]
        )


class TestDysonAccount(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('requests.get', side_effect=_mock_gets)
    @mock.patch('requests.post', side_effect=_mocked_login_post)
    def test_connect_account(self, mocked_login, mocked_status):
        dyson_account = DysonAccount("email", "password", "language")
        logged = dyson_account.login()
        self.assertEqual(mocked_status.call_count, 1)
        self.assertEqual(mocked_login.call_count, 1)
        self.assertTrue(logged)

    @mock.patch('requests.get', side_effect=_mocked_status_get_cn)
    @mock.patch('requests.post', side_effect=_mocked_login_post_cn)
    def test_connect_account_cn(self, mocked_login, mocked_status):
        dyson_account = DysonAccount("email", "password", "CN")
        logged = dyson_account.login()
        self.assertEqual(mocked_status.call_count, 1)
        self.assertEqual(mocked_login.call_count, 1)
        self.assertTrue(logged)

    @mock.patch('requests.get', side_effect=_mocked_status_get_failed)
    @mock.patch('requests.post', side_effect=_mocked_login_post_failed)
    def test_connect_account_failed(self, mocked_login, mocked_status):
        dyson_account = DysonAccount("email", "password", "language")
        logged = dyson_account.login()
        self.assertEqual(mocked_status.call_count, 1)
        self.assertEqual(mocked_login.call_count, 0)
        self.assertFalse(logged)

    def test_not_logged(self):
        dyson_account = DysonAccount("email", "password", "language")
        self.assertRaises(DysonNotLoggedException, dyson_account.devices)

    @mock.patch('requests.get', side_effect=_mock_gets)
    @mock.patch('requests.post', side_effect=_mocked_login_post)
    def test_list_devices(self, mocked_login, mocked_list_devices):
        dyson_account = DysonAccount("email", "password", "language")
        dyson_account.login()
        self.assertEqual(mocked_login.call_count, 1)
        self.assertTrue(dyson_account.logged)
        devices = dyson_account.devices()
        self.assertEqual(mocked_list_devices.call_count, 3)
        self.assertEqual(len(devices), 6)
        self.assertTrue(isinstance(devices[0], DysonPureCoolLink))
        self.assertTrue(isinstance(devices[1], DysonPureHotCoolLink))
        self.assertTrue(isinstance(devices[2], Dyson360Eye))
        self.assertTrue(isinstance(devices[3], DysonPureCool))
        self.assertTrue(isinstance(devices[4], DysonPureCool))
        self.assertTrue(isinstance(devices[5], DysonPureHotCool))
        self.assertTrue(devices[0].active)
        self.assertTrue(devices[0].auto_update)
        self.assertFalse(devices[0].new_version_available)
        self.assertEqual(devices[0].serial, 'device-id-1')
        self.assertEqual(devices[0].name, 'device-1')
        self.assertEqual(devices[0].version, '21.03.08')
        self.assertEqual(devices[0].product_type, '475')
        self.assertEqual(devices[0].credentials, 'password1')
