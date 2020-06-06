from unittest.mock import MagicMock

from tests import XS1TestBase


class TestXS1(XS1TestBase):

    def test_device_id_stable(self):
        api_response = TestXS1.get_api_response("get_list_sensors")
        # self._underTest._send_request = MagicMock(return_value=api_response)

        sensor64 = self._underTest.get_sensor(64)
        self.assertIsNotNone(sensor64)
        sensor_id = sensor64.id()
        sensor_name = sensor64.name()
        sensor64.update()
        self.assertEqual(sensor64.id(), sensor_id)
        self.assertEqual(sensor64.name(), sensor_name)
        config = self._underTest.get_config_sensor(sensor64.number())
        print()
