from sygna_bridge_util.config import PermissionStatus


def sort_permission_request_transaction(transaction: dict) -> dict:
    """sort transaction

     Args:
        transaction : dict{
            originator_vasp_code: str
            originator_addrs: str[]
            Optional originator_addrs_extra: dict
            beneficiary_vasp_code: str
            beneficiary_addrs: str[]
            Optional beneficiary_addrs_extra: dict
            transaction_currency: str
            amount: number
        }

     Returns:
        sorted dict{
            originator_vasp_code: str
            originator_addrs: str[]
            Optional originator_addrs_extra: dict
            beneficiary_vasp_code: str
            beneficiary_addrs: str[]
            Optional beneficiary_addrs_extra: dict
            transaction_currency: str
            amount: number
        }
     """
    sorted_data = {
        'originator_vasp_code': transaction['originator_vasp_code'],
        'originator_addrs': transaction['originator_addrs']
    }

    if 'originator_addrs_extra' in transaction:
        sorted_data['originator_addrs_extra'] = transaction['originator_addrs_extra']

    sorted_data['beneficiary_vasp_code'] = transaction['beneficiary_vasp_code']
    sorted_data['beneficiary_addrs'] = transaction['beneficiary_addrs']

    if 'beneficiary_addrs_extra' in transaction:
        sorted_data['beneficiary_addrs_extra'] = transaction['beneficiary_addrs_extra']

    sorted_data['transaction_currency'] = transaction['transaction_currency']
    sorted_data['amount'] = transaction['amount']
    return sorted_data


def sort_permission_request_data(permission_request_data: dict) -> dict:
    """sort permission_request_data

     Args:
        permission_request_data : dict{
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
        }

     Returns:
        sorted dict{
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
        }
     """
    sorted_transaction = sort_permission_request_transaction(permission_request_data['transaction'])

    sorted_permission_request_data = {
        'private_info': permission_request_data['private_info'],
        'transaction': sorted_transaction,
        'data_dt': permission_request_data['data_dt']
    }
    if 'expire_date' in permission_request_data:
        sorted_permission_request_data['expire_date'] = permission_request_data['expire_date']
    return sorted_permission_request_data


def sort_permission_data(permission_data: dict) -> dict:
    """sort permission_data
    if permission_status is REJECTED, reject_code is required.
    if permission_status is REJECTED and reject_code is BVRC999, reject_message is required.

     Args:
        permission_data : dict{
            transfer_id: str
            permission_status: str. ACCEPTED or REJECTED
            Optional expire_date: int
            Optional reject_code: str. BVRC001,BVRC002,BVRC003,BVRC004 or BVRC999
            Optional reject_message: str
        }

     Returns:
        sorted dict{
            transfer_id: str
            permission_status: str
            Optional expire_date: int
            Optional reject_code: str
            Optional reject_message: str
        }
     """
    sorted_permission_data = {
        'transfer_id': permission_data['transfer_id'],
        'permission_status': permission_data['permission_status'],
    }

    if 'expire_date' in permission_data:
        sorted_permission_data['expire_date'] = permission_data['expire_date']

    if permission_data['permission_status'] == PermissionStatus.REJECTED.value:
        if 'reject_code' in permission_data:
            sorted_permission_data['reject_code'] = permission_data['reject_code']
        if 'reject_message' in permission_data:
            sorted_permission_data['reject_message'] = permission_data['reject_message']

    return sorted_permission_data


def sort_callback_data(callback_data: dict) -> dict:
    """sort callback_data

     Args:
        callback_data : dict{
            callback_url: str
        }

     Returns:
        sorted dict{
            callback_url: str
        }
     """
    sorted_callback_data = {
        'callback_url': callback_data['callback_url']
    }
    return sorted_callback_data


def sort_transaction_id_data(transaction_id_data: dict) -> dict:
    """sort transaction_id_data

     Args:
        transaction_id_data : dict{
            transfer_id: str
            txid: str
        }

     Returns:
        sorted dict{
            transfer_id: str
            txid: str
        }
     """
    sorted_transaction_id_data = {
        'transfer_id': transaction_id_data['transfer_id'],
        'txid': transaction_id_data['txid']
    }
    return sorted_transaction_id_data


def sort_post_permission_data(post_permission_data: dict) -> dict:
    """sort post_permission_data
    if permission_status is REJECTED, reject_code is required.
    if permission_status is REJECTED and reject_code is BVRC999, reject_message is required.

     Args:
        post_permission_data : dict{
            transfer_id: str
            permission_status: str. ACCEPTED or REJECTED
            Optional expire_date: int
            Optional reject_code: str. BVRC001,BVRC002,BVRC003,BVRC004 or BVRC999
            Optional reject_message: str
            signature: str
        }

     Returns:
        sorted dict{
            transfer_id: str
            permission_status: str
            Optional expire_date: int
            Optional reject_code: str
            Optional reject_message: str
            signature: str
        }
     """
    sorted_post_permission_data = sort_permission_data(post_permission_data)
    sorted_post_permission_data['signature'] = post_permission_data['signature']
    return sorted_post_permission_data


def sort_post_permission_request_data(post_permission_request_data: dict) -> dict:
    """sort permission_request_data

     Args:
        post_permission_request_data : dict{
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
        sorted dict{
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
     """
    sorted_post_permission_request_data_data = sort_permission_request_data(post_permission_request_data['data'])
    sorted_post_permission_request_data_data['signature'] = post_permission_request_data['data']['signature']
    sorted_post_permission_request_data_callback = sort_callback_data(post_permission_request_data['callback'])
    sorted_post_permission_request_data_callback['signature'] = post_permission_request_data['callback']['signature']

    sorted_post_permission_request_data = {
        'data': sorted_post_permission_request_data_data,
        'callback': sorted_post_permission_request_data_callback
    }
    return sorted_post_permission_request_data


def sort_post_transaction_id_data(post_transaction_id_data: dict) -> dict:
    """sort transaction_id_data

     Args:
        post_transaction_id_data : dict{
            transfer_id: str
            txid: str
            signature: str
        }

     Returns:
        sorted dict{
            transfer_id: str
            txid: str
            signature: str
        }
     """
    sorted_post_transaction_id_data = sort_transaction_id_data(post_transaction_id_data)
    sorted_post_transaction_id_data['signature'] = post_transaction_id_data['signature']
    return sorted_post_transaction_id_data


def sort_beneficiary_endpoint_url_data(beneficiary_endpoint_url_data: dict) -> dict:
    """sort beneficiary_endpoint_url_data

     Args:
        beneficiary_endpoint_url_data : dict{
            vasp_code: str
            Optional callback_permission_request_url: str
            Optional callback_txid_url: str
        }

     Returns:
        sorted dict{
            vasp_code: str
            Optional callback_permission_request_url: str
            Optional callback_txid_url: str
        }
     """
    sorted_beneficiary_endpoint_url_data = {
        'vasp_code': beneficiary_endpoint_url_data['vasp_code']
    }
    if 'callback_permission_request_url' in beneficiary_endpoint_url_data:
        sorted_beneficiary_endpoint_url_data['callback_permission_request_url'] = beneficiary_endpoint_url_data[
            'callback_permission_request_url']

    if 'callback_txid_url' in beneficiary_endpoint_url_data:
        sorted_beneficiary_endpoint_url_data['callback_txid_url'] = beneficiary_endpoint_url_data[
            'callback_txid_url']

    return sorted_beneficiary_endpoint_url_data


def sort_post_beneficiary_endpoint_url_data(post_beneficiary_endpoint_url_data: dict) -> dict:
    """sort post_beneficiary_endpoint_url_data

     Args:
        post_beneficiary_endpoint_url_data : dict{
            vasp_code: str
            Optional callback_permission_request_url: str
            Optional callback_txid_url: str
            signature: str
        }

     Returns:
        sorted dict{
            vasp_code: str
            Optional callback_permission_request_url: str
            Optional callback_txid_url: str
            signature:str
        }
     """
    sorted_post_beneficiary_endpoint_url_data = sort_beneficiary_endpoint_url_data(post_beneficiary_endpoint_url_data)
    sorted_post_beneficiary_endpoint_url_data['signature'] = post_beneficiary_endpoint_url_data['signature']
    return sorted_post_beneficiary_endpoint_url_data
