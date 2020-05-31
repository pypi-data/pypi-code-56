from typing import Tuple, Union, List
from ..connectors.xAPIConnector import APIClient
from ..interfaces.IBroker import IBroker
from ..types import TradeTransaction, TimeStamp, AccountBalance, User, Symbol, Commission, Credentials


class XTBClient(IBroker):

    def __init__(self):
        self.client = APIClient()
        self.streamSessionId = None

    def verify_response(self, response: dict) -> dict:
        """Verifies that the response received from XTB is successful, else raises error.

        Validates the response received from the XTB API Connector and extracts the data portion from it.

        Args:
            response: A XTB client response object.

        Returns:
            A dict mapping containing the extracted response data from the passed response object. For example:
            {
                "balance": 995800269.43,
                "credit": 1000.00,
                "currency": "PLN",
                "equity": 995985397.56,
                "margin": 572634.43,
                "margin_free": 995227635.00,
                "margin_level": 173930.41
            }

        Raises:
            AssertionError: The response code received indicated that the operation was not successful.
        """
        if not response.get("status", False):
            raise AssertionError("Operation was not successful.")

        return response['returnData']

    def connect(self, user: Union[int, str] = None, password: str = None) -> bool:
        login_response = self.client.commandExecute('login', dict(userId=user, password=password))
        if login_response['status'] is False:
            print(
                f"Authentication error. Error code: {login_response['errorCode']}\nError message: {login_response['errorDescr']}")
            return self.authenticated

        self.streamSessionId = login_response['streamSessionId']
        self.authenticated = login_response['status']
        return self.authenticated

    def connect_with_credentials(self, credentials: Credentials) -> bool:
        if credentials.is_token:
            raise TypeError("XTB cannot accept a token credentials.")
        return self.connect(credentials.username, credentials.password)

    def disconnect(self) -> None:
        self.client.commandExecute('logout')
        self.client.disconnect()

    def get_symbol(self, symbol: Union[str, Symbol]) -> Symbol:
        if type(symbol) == str:
            symbol_command = self.client.commandExecute("getSymbol", dict(symbol=symbol))
        elif type(symbol) == Symbol:
            symbol_command = self.client.commandExecute("getSymbol", dict(symbol=symbol.ticker))
        else:
            raise TypeError("Passed parameter is not of type Symbol or str.")

        # Return result
        symbol = self.verify_response(symbol_command)
        return Symbol(ticker=symbol['symbol'],
                      ask=symbol['ask'],
                      bid=symbol['bid'],
                      category=symbol['categoryName'],
                      contract_size=symbol['contractSize'],
                      currency=symbol['currency'],
                      currency_pair=symbol['currencyPair'],
                      currency_profit=symbol['currencyProfit'],
                      description=symbol['description'],
                      expiration=symbol['expiration'],
                      high=symbol['high'],
                      initial_margin=symbol['initialMargin'],
                      leverage=symbol['leverage'],
                      long_only=symbol['longOnly'],
                      min_lot=symbol['lotMin'],
                      max_lot=symbol['lotMax'],
                      lot_step=symbol['lotStep'],
                      low=symbol['low'],
                      pip_precision=symbol['pipsPrecision'],
                      price_precision=symbol['precision'],
                      shortable=symbol['shortSelling'],
                      time=TimeStamp(symbol['time'], unix=True, milliseconds=True)
                      )

    def get_available_symbols(self) -> List[Symbol]:
        response = self.client.commandExecute('getAllSymbols')
        symbols = self.verify_response(response)
        available_symbols = []
        for symbol in symbols:
            s = Symbol(ticker=symbol['symbol'],
                       ask=symbol['ask'],
                       bid=symbol['bid'],
                       category=symbol['categoryName'],
                       contract_size=symbol['contractSize'],
                       currency=symbol['currency'],
                       currency_pair=symbol['currencyPair'],
                       currency_profit=symbol['currencyProfit'],
                       description=symbol['description'],
                       expiration=symbol['expiration'],
                       high=symbol['high'],
                       initial_margin=symbol['initialMargin'],
                       leverage=symbol['leverage'],
                       long_only=symbol['longOnly'],
                       min_lot=symbol['lotMin'],
                       max_lot=symbol['lotMax'],
                       lot_step=symbol['lotStep'],
                       low=symbol['low'],
                       pip_precision=symbol['pipsPrecision'],
                       price_precision=symbol['precision'],
                       shortable=symbol['shortSelling'],
                       time=TimeStamp(symbol['time'], unix=True, milliseconds=True)
                       )
            available_symbols.append(s)

        return available_symbols

    def get_commission(self, volume: float, symbol: Union[str, Symbol]) -> Commission:
        if type(symbol) == str:
            res = self.client.commandExecute("getCommissionDef", dict(symbol=symbol, volume=volume))
        elif type(symbol) == Symbol:
            res = self.client.commandExecute("getCommissionDef", dict(symbol=symbol.ticker, volume=volume))
        else:
            raise TypeError("Passed parameter is not of type Symbol or str.")

        commission = self.verify_response(res)

        return Commission(commission=commission['commission'],
                          exchange_rate=commission['rateOfExchange'])

    def get_current_user_data(self) -> User:
        raise NotImplementedError("This feature is still under development.")

    def get_account_balance(self) -> AccountBalance:
        res = self.client.commandExecute("getMarginLevel")
        data = self.verify_response(res)
        return AccountBalance(
            balance=data["balance"],
            credit=data['credit'],
            currency=data['currency'],
            equity=data['equity'],
            margin=data['margin'],
            free_margin=data['margin_free']
        )

    def get_server_time(self) -> TimeStamp:
        res = self.client.commandExecute("getServerTime")

        data = self.verify_response(res)
        return TimeStamp(time_value=data['time'], unix=True, milliseconds=True)

    def get_version(self) -> str:
        res = self.client.commandExecute("getVersion")

        return self.verify_response(res)['version']

    def connection_status(self) -> bool:
        res = self.client.commandExecute("ping")
        return res.get("status", False)

    def check_transaction_status(self, transaction: TradeTransaction) -> bool:
        res = self.client.commandExecute("tradeTransactionStatus", dict(order=transaction.order_number))
        return self.verify_response(res)['requestStatus']

    def open_position(self, transaction: TradeTransaction) -> TradeTransaction:
        tt_info = {
            'cmd': transaction.operation,
            'customComment': transaction.comment,
            'expiration': transaction.expiration,
            'offset': transaction.trailing_offset,
            'order': transaction.order_number,
            'price': transaction.price,
            'sl': transaction.stop_loss_price,
            'symbol': transaction.symbol.ticker,
            'tp': transaction.take_profit_price,
            'type': transaction.transaction_type,
            'volume': transaction.volume
        }

        res = self.client.commandExecute("tradeTransaction", dict(tradeTransInfo=tt_info))
        transaction.order_number = self.verify_response(res)['order']
        return transaction
