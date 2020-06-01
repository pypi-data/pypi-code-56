from datetime import datetime
from sygna_bridge_util.config import EXPIRE_DATE_MIN_OFFSET


def validate_private_key(private_key: str) -> None:
    if type(private_key) is not str:
        raise TypeError('Expect {0} to be {1}, got {2}'.format(
            'private_key',
            str,
            type(private_key))
        )

    if len(private_key) < 1:
        raise ValueError('private_key is too short')


def validate_transfer_id(transfer_id: str) -> None:
    if type(transfer_id) is not str:
        raise TypeError('Expect {0} to be {1}, got {2}'.format(
            'transfer_id',
            str,
            type(transfer_id))
        )

    if len(transfer_id) != 64:
        raise ValueError('transfer_id length should be 64')


def validate_expire_date(expire_date: int) -> None:
    if type(expire_date) is not int:
        raise TypeError('Expect {0} to be {1}, got {2}'.format(
            'expire_date',
            int,
            type(expire_date))
        )

    now = int(datetime.now().timestamp()) * 1000
    if (expire_date - now) < EXPIRE_DATE_MIN_OFFSET:
        raise ValueError('expire_date should be at least {0} seconds away from the current time.'.format(
            EXPIRE_DATE_MIN_OFFSET / 1000
        ))
