from TinkoffTransaction import TinkoffTransaction


class TransactionsProcessor(object):

    __PAY_IN_OPERATION_TYPE = 'PayIn'  # Пополнение брокерского счета
    __PAY_OUT_OPERATION_TYPE = 'PayOut'  # Вывод денег
    __BUY_CARD_OPERATION_TYPE = 'BuyCard'  # Покупка с карты
    __SELL_OPERATION_TYPE = 'Sell'  # Продажа
    __BROKER_COMMISSION_OPERATION_TYPE = 'BrokerCommission'  # Комиссия брокера
    __DIVIDEND_OPERATION_TYPE = 'Dividend'  # Выплата дивидендов
    __TAX_OPERATION_TYPE = 'Tax'  # Налоги
    __TAX_DIVIDEND_OPERATION_TYPE = 'TaxDividend'  # Налоги c дивидендов
    __SERVICE_COMMISSION_OPERATION_TYPE = 'ServiceCommission'  # Комиссия за обслуживание

    __USD_CURRENCY_TYPE = 'USD'
    __RUB_CURRENCY_TYPE = 'RUB'

    __DONE_STATUS = 'Done'
    __DECLINE_STATUS = 'Decline'

    def __init__(self, transactions: [TinkoffTransaction]):
        self.__transactions = transactions

    def get_overall_tax_payed_usd(self) -> float:
        currency_type = self.__USD_CURRENCY_TYPE
        return self.__get_overall_tax_payed(currency_type)

    def get_overall_tax_payed_rub(self) -> float:
        currency_type = self.__RUB_CURRENCY_TYPE
        return self.__get_overall_tax_payed(currency_type)

    def __get_overall_tax_payed(self, currency_type):
        tax_payed = 0.0
        for tr in self.__transactions:
            operation_type = tr.operation_type
            done = tr.status == self.__DONE_STATUS
            is_tax_type = operation_type == self.__TAX_OPERATION_TYPE or operation_type == self.__TAX_DIVIDEND_OPERATION_TYPE
            is_currency = tr.currency == currency_type
            if is_tax_type and is_currency and done:
                tax_payed += tr.payment
            else:
                continue
        return abs(tax_payed)

    def get_overall_dividend_received_usd(self):
        currency_type = self.__USD_CURRENCY_TYPE
        return self.__get_overall_dividend_received(currency_type)

    def get_overall_dividend_received_rub(self):
        currency_type = self.__RUB_CURRENCY_TYPE
        return self.__get_overall_dividend_received(currency_type)

    def __get_overall_dividend_received(self, currency_type):
        dividend_received = 0.0
        for tr in self.__transactions:
            operation_type = tr.operation_type
            done = tr.status == self.__DONE_STATUS
            is_dividend_type = operation_type == self.__DIVIDEND_OPERATION_TYPE
            is_currency = tr.currency == currency_type
            if is_dividend_type and is_currency and done:
                dividend_received += tr.payment
            else:
                continue
        return abs(dividend_received)

    def get_all_info_by_figi(self, figi):
        pass
