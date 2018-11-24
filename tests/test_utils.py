import unittest

from libpurecool.utils import support_heating, is_heating_device, \
    is_360_eye_device, printable_fields, decrypt_password, \
    is_pure_cool_v2, is_dyson_pure_cool_device, get_field_value


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_support_heating(self):
        self.assertTrue(support_heating("455"))
        self.assertFalse(support_heating("469"))

    def test_is_heating_device(self):
        self.assertTrue(is_heating_device({"ProductType": "455"}))
        self.assertFalse(is_heating_device({"ProductType": "469"}))

    def test_is_360_eye_device(self):
        self.assertTrue(is_360_eye_device({"ProductType": "N223"}))
        self.assertFalse(is_360_eye_device({"ProductType": "455"}))

    def test_is_pure_cool_v2(self):
        self.assertTrue(is_pure_cool_v2("438"))
        self.assertTrue(is_pure_cool_v2("520"))
        self.assertFalse(is_pure_cool_v2("N223"))

    def test_is_dyson_pure_cool_device(self):
        self.assertTrue(is_dyson_pure_cool_device({"ProductType": "438"}))
        self.assertTrue(is_dyson_pure_cool_device({"ProductType": "520"}))
        self.assertFalse(is_dyson_pure_cool_device({"ProductType": "469"}))

    def test_printable_fields(self):
        idx = 0
        fields = ["field1=value1", "field2=value2"]
        for field in printable_fields(
                [("field1", "value1"), ("field2", "value2")]):
            self.assertEqual(field, fields[idx])
            idx += 1

    def test_decrypt_password(self):
        password = decrypt_password("1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70"
                                    "ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2vbCm7"
                                    "uYeTORULKLKQ==")
        self.assertEqual(password, "password1")

    def test_get_field_value(self):
        state = {"field1": ["value1", "value2"], "field2": "value3"}
        self.assertTrue(get_field_value(state, "field1") == "value2")
        self.assertFalse(get_field_value(state, "field1") == "value1")
        self.assertTrue(get_field_value(state, "field2") == "value3")
        self.assertFalse(get_field_value(state, "field2") == "value2")
