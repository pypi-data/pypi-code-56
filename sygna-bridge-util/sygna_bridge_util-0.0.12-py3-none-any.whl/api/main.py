import requests
from sygna_bridge_util.config import (
    SYGNA_BRIDGE_CENTRAL_PUBKEY,
    HTTP_TIMEOUT,
    SYGNA_BRIDGE_CENTRAL_PUBKEY_TEST
)
import sygna_bridge_util.crypto.verify
import json
from sygna_bridge_util.validator import (
    validate_transfer_id,
    validate_post_permission_schema,
    validate_post_permission_request_schema,
    validate_post_transaction_id_schema,
    validate_post_beneficiary_endpoint_url_schema
)
from sygna_bridge_util.utils import (
    sort_post_transaction_id_data,
    sort_post_permission_request_data,
    sort_post_permission_data,
    sort_post_beneficiary_endpoint_url_data
)


class API:
    def __init__(self, api_key: str, sygna_bridge_domain: str):
        self.api_key = api_key
        self.domain = sygna_bridge_domain

    def get_sb(self, url: str) -> dict:
        """HTTP GET request to Sygna Bridge

        Args:
            url: str

        Returns:
            dict
        """
        headers = {'api_key': self.api_key}
        response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
        return response.json()

    def post_sb(self, url: str, body: dict) -> dict:
        """HTTP Post request to Sygna Bridge

        Args:
            url: str
            body: dict

        Returns:
            dict
        """
        headers = {'Content-Type': 'application/json',
                   'api_key': self.api_key}
        response = requests.post(
            url,
            data=json.dumps(body),
            headers=headers,
            timeout=HTTP_TIMEOUT)
        return response.json()

    def get_vasp_list(self, validate: bool = True, is_prod: bool = False) -> [dict]:
        """get list of registered VASP associated with public key

         Args:
            validate: bool. decide whether to validate returned vasp list data.
            is_prod: bool. decide which public key to use

         Returns:
            dict{
                vasp_name: str
                vasp_code: str
                vasp_pubkey: str
            }[]

         Raises:
            Exception('Request VASPs failed')
            Exception('get VASP info error: invalid signature')
         """
        url = self.domain + 'api/v1.1.0/bridge/vasp'
        result = self.get_sb(url)
        if 'vasp_data' not in result:
            raise ValueError(
                'Request VASPs failed: {0}'.format(result['message']))

        if not validate:
            return result['vasp_data']

        pubkey = SYGNA_BRIDGE_CENTRAL_PUBKEY if is_prod is True else SYGNA_BRIDGE_CENTRAL_PUBKEY_TEST

        valid = sygna_bridge_util.crypto.verify.verify_data(result, pubkey)

        if not valid:
            raise ValueError('get VASP info error: invalid signature.')

        return result['vasp_data']

    def get_vasp_public_key(self, vasp_code: str, validate: bool = True, is_prod: bool = False) -> str:
        """A Wrapper function of get_vasp_list to return specific VASP's public key.

         Args:
            vasp_code: str
            validate: bool. decide whether to validate returned vasp list data.
            is_prod: bool. decide which public key to use

         Returns:
            str. uncompressed public key

         Raises:
            Exception('Invalid vasp_code')
         """
        vasps = self.get_vasp_list(validate, is_prod)
        target_vasp = None
        for _, item in enumerate(vasps):
            if item['vasp_code'] == vasp_code:
                target_vasp = item
                break

        if target_vasp is None:
            raise ValueError('Invalid vasp_code')

        return target_vasp['vasp_pubkey']

    def get_status(self, transfer_id: str) -> dict:
        """get detail of particular transaction premission request

         Args:
            transfer_id: str

         Returns:
            dict{
                transferData:dict{
                    transfer_id: str
                    private_info: str
                    transaction: dict{
                        originator_vasp_code: str
                        originator_addrs: str[]
                        Optional originator_addrs_extra: dict
                        beneficiary_vasp_code: str
                        beneficiary_addrs: str[]
                        Optional beneficiary_addrs_extra: dict
                        transaction_currency: str
                        amount: number
                    }
                    data_dt: str
                    permission_request_data_signature: str
                    permission_status: str. ACCEPTED or REJECTED
                    permission_signature: str
                    txid: str
                    txid_signature: str
                    created_at: str
                    transfer_to_originator_time: str
                }
                signature: str
            }
         """
        validate_transfer_id(transfer_id)
        url = self.domain + 'api/v1.1.0/bridge/transaction/status?transfer_id=' + transfer_id
        return self.get_sb(url)

    def post_permission(self, data: dict) -> dict:
        """Notify Sygna Bridge that you have confirmed specific permission Request from other VASP.
        Should be called by Beneficiary Server

         Args:
            data (dict): {
                transfer_id:str,
                permission_status:str,
                Optional expire_date(int)
                Optional reject_code(str) : BVRC001,BVRC002,BVRC003,BVRC004 or BVRC999
                Optional reject_message(str),
                signature:str
            }

         Returns:
            dict{
                status: str
            }

         Raises:
            ValidationError
         """
        validate_post_permission_schema(data)

        sorted_post_permission_data = sort_post_permission_data(data)
        url = self.domain + 'api/v1.1.0/bridge/transaction/permission'
        return self.post_sb(url, sorted_post_permission_data)

    def post_permission_request(self, data: dict) -> dict:
        """Should be called by Originator.

         Args:
             data: dict{
                data: dict{
                    private_info: str
                    transaction: dict{
                        originator_vasp_code: str
                        originator_addrs: str[]
                        Optional originator_addrs_extra: dict
                        beneficiary_vasp_code: str
                        beneficiary_addrs: str[]
                        Optional beneficiary_addrs_extra: dict
                        transaction_currency: str
                        amount: number
                    }
                    data_dt: str
                    Optional expire_date: int
                    signature: str
                }
                callback: dict{
                    callback_url: str
                    signature: str
                }
             }

         Returns:
            dict{
                transfer_id: str
            }

         Raises:
            ValidationError
         """
        validate_post_permission_request_schema(data)

        sorted_post_permission_request_data = sort_post_permission_request_data(data)
        url = self.domain + 'api/v1.1.0/bridge/transaction/permission-request'
        return self.post_sb(url, sorted_post_permission_request_data)

    def post_transaction_id(self, data: dict) -> dict:
        """Send broadcasted transaction id to Sygna Bridge for purpose of storage.

         Args:
            data: dict{
                transfer_id: str
                txid: str
                signature: str
            }

         Returns:
            dict{
                status: str
            }

         Raises:
            ValidationError
         """
        validate_post_transaction_id_schema(data)

        sorted_post_transaction_id_data = sort_post_transaction_id_data(data)
        url = self.domain + 'api/v1.1.0/bridge/transaction/txid'
        return self.post_sb(url, sorted_post_transaction_id_data)

    def post_beneficiary_endpoint_url(self, data: dict) -> dict:
        """This allows VASP to update the Beneficiary's callback URL programmatically.

         Args:
            data: dict{
                vasp_code: str
                Option callback_permission_request_url: str
                Option callback_txid_url: str
                signature: str
            }

         Returns:
            dict{
                status: str
            }

         Raises:
            ValidationError
         """
        validate_post_beneficiary_endpoint_url_schema(data)

        sorted_post_beneficiary_endpoint_url_data = sort_post_beneficiary_endpoint_url_data(data)
        url = self.domain + 'api/v1.1.0/bridge/vasp/beneficiary-endpoint-url'
        return self.post_sb(url, sorted_post_beneficiary_endpoint_url_data)
