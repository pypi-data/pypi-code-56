"""
MIT License

Copyright (c) 2020 LidaRandom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import List, Dict

import requests as req

from .abc import Loader


class BadAuth(Exception):
    """Invalid authefication."""

    ...


class RLoader(Loader):
    """Built-in Loader based on requests sessions.

       Args:
        login - dealer profile login
        password - dealer profile password
    """

    __slots__ = ["_login", "_password"]

    def __init__(self, login: str, password: str):
        self._login = str(login)
        self._password = str(password)

    def dump_contracts(self, auth_session: req.Session) -> List[List[str]]:
        contracts = []
        offset = 0
        while True:
            dumped = auth_session.post(
                "http://dealer.uzavtosanoat.uz/b/ap/order_list&table",
                json={
                    "d": None,
                    "p": {
                        "column": [
                            "order_id",
                            "client_kind_name",
                            "client_inn",
                            "client_name",
                            "phone_number",
                            "model_name",
                            "modification_name",
                            "color_name",
                            "option_set",
                            "real_option_set",
                            "vin_code",
                            "dealer_name",
                            "order_date",
                            "state_expired_on",
                            "producing_date",
                            "price",
                            "remain_amount",
                            "paid_amount",
                            "contract_code",
                            "queue_no",
                            "view_state_name",
                            "user_kind",
                        ],
                        "offset": offset,
                        "limit": 5000,
                    },
                },
            ).json()["data"]
            if len(dumped) == 0:
                break
            contracts += dumped
            offset += 5000
        return contracts

    def contracts(self) -> List[Dict[str, str]]:
        session = req.session()
        login_request = session.post(
            "http://dealer.uzavtosanoat.uz/b/core/s$logon",
            {"login": self._login, "password": self._password},
        )
        if login_request.status_code == 400:
            raise BadAuth(f"Incorrect login or password")
        raw_contracts = self.dump_contracts(session)
        fields_names = [
            "ИД",
            "Тип клиента",
            "ИНН",
            "Ф.И.О.",
            "Номер телефона",
            "Модель",
            "Модификация",
            "Цвет",
            "Набор опций",
            "Фактические опции",
            "VIN",
            "Дилер",
            "Дата заказа",
            "Дата истечения заказа",
            "Предполагаемая дата поставки",
            "Цена",
            "К оплате",
            "Сумма оплаты",
            "Код контракта",
            "Очередь",
            "Состояние",
            "Тип оформления",
        ]
        contracts = [
            dict(zip(fields_names, contract_fields))
            for contract_fields in raw_contracts
        ]
        session.close()
        return contracts


__all__ = ["RLoader"]
