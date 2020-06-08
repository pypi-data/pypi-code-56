"""PhysicalDeviceApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.config_test import PHYSICAL_DEVICE
from ..common.generators import generate_unique_name


@pytest.mark.usefixtures('client_cls')
class PhysicalDeviceApiTest(ApiBase, unittest.TestCase):
    def test_create_physical_device_api(self):
        __unique_name = generate_unique_name('PhysicalDeviceApi')
        physical_device = {
            PHYSICAL_DEVICE: {
                'name': __unique_name,
                'karabo_da': __unique_name,
                'virtual_device_name': __unique_name,
                'device_type_id': -1,
                'detector_id': -1,
                'flg_available': True,
                'description': 'desc 01'
            }
        }

        expect = physical_device[PHYSICAL_DEVICE]

        # Create new entry (should succeed)
        received = self.__create_entry_api(physical_device, expect)

        physical_dev_id = received['id']
        physical_dev_name = received['name']
        physical_dev_det_id = received['detector_id']
        physical_dev_krb_da = received['karabo_da']

        try:
            # Create duplicated entry (should throw an error)
            self.__create_error_entry_uk_api(physical_device)

            # Get entry by name
            self.__get_all_entries_by_name_api(physical_dev_name, expect)

            # Get entry by detector_id
            self.__get_all_entries_by_detector_id_api(physical_dev_det_id,
                                                      expect)

            # Get entry by detector_id
            self.__get_all_entries_by_detector_and_krbda_api(
                physical_dev_det_id, physical_dev_krb_da, expect)

            # Get entry by ID
            self.__get_entry_by_id_api(physical_dev_id, expect)

            # Put entry information (update some fields should succeed)
            self.__update_entry_api(physical_dev_id, expect)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            del_resp = self.cal_client.delete_physical_device_api(
                physical_dev_id
            )

        # Validate the response from deletion if nothing already error-ed
        self.get_and_validate_delete_entry_by_id(del_resp)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['karabo_da'] == expect['karabo_da']
        assert receive['virtual_device_name'] == expect['virtual_device_name']
        assert receive['device_type_id'] == expect['device_type_id']
        assert receive['detector_id'] == expect['detector_id']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']

    def __create_entry_api(self, entry_info, expect):
        response = self.cal_client.create_physical_device_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client.create_physical_device_api(entry_info)
        receive = self.load_response_content(response)

        expect = {'info': {'name': ['has already been taken'],
                           'karabo_da': ['has already been taken']}}
        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = generate_unique_name('PhysicalDevApiUpd')
        physical_dev_upd = {
            PHYSICAL_DEVICE: {
                'name': unique_name_upd,
                'karabo_da': unique_name_upd,
                'virtual_device_name': unique_name_upd,
                # 'device_type_id': '-1',
                # 'detector_id': '-1',
                'flg_available': False,
                'description': 'desc 01 updated!!!'
            }
        }

        resp = self.cal_client.update_physical_device_api(entry_id,
                                                          physical_dev_upd)
        receive = self.load_response_content(resp)

        # Add parameters not send to the update API
        physical_dev_upd[PHYSICAL_DEVICE]['device_type_id'] = -1
        physical_dev_upd[PHYSICAL_DEVICE]['detector_id'] = -1
        expect_upd = physical_dev_upd[PHYSICAL_DEVICE]

        self.fields_validation(receive, expect_upd)
        assert resp.status_code == HTTPStatus.OK

        assert expect['name'] != expect_upd['name']
        assert expect['karabo_da'] != expect_upd['karabo_da']
        assert expect['virtual_device_name'] != expect_upd[
            'virtual_device_name']
        assert expect['flg_available'] != expect_upd['flg_available']
        assert expect['description'] != expect_upd['description']

    def __get_all_entries_by_name_api(self, name, expect):
        response = self.cal_client.get_all_physical_devices_by_name_api(
            name)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_all_entries_by_detector_id_api(self, detector_id, expect):
        response = self.cal_client.get_all_physical_devices_by_detector_id_api(
            detector_id)
        receive = self.get_and_validate_all_entries_by_name(response)

        self.fields_validation(receive, expect)

    def __get_all_entries_by_detector_and_krbda_api(self, detector_id,
                                                    karabo_da, expect):
        resp = self.cal_client.get_all_physical_devices_by_det_and_krbda_api(
            detector_id, karabo_da)
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.cal_client.get_physical_device_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
