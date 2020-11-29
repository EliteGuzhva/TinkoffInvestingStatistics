from enum import Enum
from datetime import datetime
from pytz import timezone
from openapi_client import openapi
import time


class AccountType(Enum):
    broker = 0
    iis = 1


class TinkoffApiWrapper(object):

    __BROKER_ACCOUNT_TYPE = 'Tinkoff'
    __IIS_ACCOUNT_TYPE = 'TinkoffIis'

    __OPERATIONS_LIMIT = 120

    def __init__(self, token):
        self.__token = token
        self.__client = openapi.api_client(token)
        self.__broker_account_id = None
        self.__iis_account_id = None
        self.__set_account_ids()

    def get_transactions(self, for_account_type: AccountType):
        date1 = datetime(2019, 6, 1, 0, 0, 0, tzinfo=timezone('Europe/Moscow')).isoformat()
        date2 = datetime.now(tz=timezone('Europe/Moscow')).isoformat()
        account_id = self.__broker_account_id if for_account_type == AccountType.broker else self.__iis_account_id
        ops = self.__client.operations.operations_get(_from=date1, to=date2, broker_account_id=account_id)
        return ops.payload.operations

    def get_ticker_info_by_figi(self, figi):
        instrument = self.__client.market.market_search_by_figi_get(figi)
        name = instrument.payload.name
        ticker = instrument.payload.ticker
        return name, ticker, figi

    def get_ticker_info_by_ticker(self, ticker):
        instruments = self.__client.market.market_search_by_ticker_get(ticker)
        instrument = instruments.payload.instruments[0]
        name = instrument.name
        figi = instrument.figi
        return name, ticker, figi

    def __set_account_ids(self):
        accounts = self.__client.user.user_accounts_get().payload.accounts
        for account in accounts:
            account_type = account.broker_account_type
            account_id = account.broker_account_id
            if account_type == self.__BROKER_ACCOUNT_TYPE:
                self.__broker_account_id = account_id
            else:
                self.__iis_account_id = account_id
