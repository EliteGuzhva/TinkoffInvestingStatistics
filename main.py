import json
from typing import Optional
from TinkofApiWrapper import TinkoffApiWrapper
from TinkofApiWrapper import AccountType
from TinkoffTransaction import TinkoffTransaction
from TransactionsProcessor import TransactionsProcessor

from tui.main_menu import MainMenu

# read token from config
token = ''
with open('settings.json') as f:
    data = json.load(f)
    token = data['tinkoff_open_api_key']

# initialize api
tinkoff_api = TinkoffApiWrapper(token)
transactions_processor: Optional[TransactionsProcessor] = None


# print useful reports
def print_transaction_report(account_type: AccountType):
    account_name = ''
    if account_type == AccountType.broker:
        account_name = 'broker'
    elif account_type == AccountType.iis:
        account_name = 'iis'
    else:
        print('Invalid account type')
        return

    transactions = tinkoff_api.get_transactions(account_type)
    transactions = [TinkoffTransaction(tr) for tr in transactions]

    transactions_processor = TransactionsProcessor(transactions)

    overall_tax_payed_usd = transactions_processor.get_overall_tax_payed_usd()
    overall_tax_payed_rub = transactions_processor.get_overall_tax_payed_rub()

    dividend_received_usd = transactions_processor.get_overall_dividend_received_usd()
    dividend_received_rub = transactions_processor.get_overall_dividend_received_rub()

    broker_commission_usd = transactions_processor.get_overall_commision_payed_usd()
    broker_commission_rub = transactions_processor.get_overall_commision_payed_rub()

    service_commission = transactions_processor.get_service_commission_payed()

    print(f'Overall tax payed on {account_name} account:')
    print(f'{overall_tax_payed_usd:.1f} $')
    print(f'{overall_tax_payed_rub:.1f} ₽')
    print('-' * 50)

    print(f'Overall dividend received on {account_name} account:')
    print(f'{dividend_received_usd:.1f} $')
    print(f'{dividend_received_rub:.1f} ₽')
    print('-' * 50)

    print(f'Overall broker commission payed on {account_name} account:')
    print(f'{broker_commission_usd:.1f} $')
    print(f'{broker_commission_rub:.1f} ₽')
    print('-'*50)

    print(f'Overall service commission payed on {account_name} account:')
    print(f'{service_commission:.1f} ₽')
    print('-'*50)

    """
    надо это говно потом поменять, пока просто для примера оставил с рублями, здесь так то и бачи могут быть
    и тикеры чтоб удобней вводить было, я там написал функцию в TinkofApiWrapper для получения figi по тикеру,
    но она несколько инструментов выдвать может, я это никак не обрабатывал, поэтому пока не пользуюсь ей

    еще надо узнать текущую стоимость этой акции в портфеле, чтобы понимать сколько выйдет прибыль или убыток
    если продать эту акцию прямо сейчас
    """
    ticker = 'NOK'
    name, _, figi = tinkoff_api.get_ticker_info_by_ticker(ticker)
    statistics = transactions_processor.get_statistics_by_figi(figi)
    print(f'Statistics for {name} on {account_name} account:')
    print(f'Total purchase amount: {statistics[0]:.1f} ₽')
    print(f'Total sale amount: {statistics[1]:.1f} ₽')
    print(f'Total commission payed: {statistics[2]:.1f} ₽')
    print(f'Total dividend received: {statistics[3]:.1f} ₽')
    print(f'Total tax payed: {statistics[4]:.1f} ₽')


# print_transaction_report(AccountType.broker)
# print_transaction_report(AccountType.iis)

menu = MainMenu(token)
menu.run()
