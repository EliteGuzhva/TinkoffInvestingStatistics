import json
from TinkofApiWrapper import TinkoffApiWrapper
from TinkofApiWrapper import AccountType
from TinkoffTransaction import TinkoffTransaction
from TransactionsProcessor import TransactionsProcessor

token = ''
with open('settings.json') as f:
    data = json.load(f)
    token = data['tinkoff_open_api_key']

tinkoff_api = TinkoffApiWrapper(token)


broker_transactions = tinkoff_api.get_transactions(AccountType.broker)
iis_transactions = tinkoff_api.get_transactions(AccountType.iis)


def initialize_transaction(transactions):
    tinkoff_transactions = [TinkoffTransaction(tr) for tr in transactions]
    return tinkoff_transactions


broker_tinkoff_transactions = initialize_transaction(broker_transactions)
iis_tinkoff_transactions = initialize_transaction(iis_transactions)

transactions_processor = TransactionsProcessor(broker_tinkoff_transactions)
overall_tax_payed_usd = transactions_processor.get_overall_tax_payed_usd()
overall_tax_payed_rub = transactions_processor.get_overall_tax_payed_rub()
dividend_received_usd = transactions_processor.get_overall_dividend_received_usd()
dividend_received_rub = transactions_processor.get_overall_dividend_received_rub()
print('Overall tax payed on broker account:')
print(round(overall_tax_payed_usd, 2), '$')
print(round(overall_tax_payed_rub, 2), '₽')
print('------------------')
print('Overall dividend received on broker account:')
print(round(dividend_received_usd, 2), '$')
print(round(dividend_received_rub, 2), '₽')
print('------------------')

transactions_processor = TransactionsProcessor(iis_tinkoff_transactions)
overall_tax_payed_usd = transactions_processor.get_overall_tax_payed_usd()
overall_tax_payed_rub = transactions_processor.get_overall_tax_payed_rub()
dividend_received_usd = transactions_processor.get_overall_dividend_received_usd()
dividend_received_rub = transactions_processor.get_overall_dividend_received_rub()
print('Overall tax payed on iis account:')
print(round(overall_tax_payed_usd, 2), '$')
print(round(overall_tax_payed_rub, 2), '₽')
print('------------------')
print('Overall dividend received on iis account:')
print(round(dividend_received_usd, 2), '$')
print(round(dividend_received_rub, 2), '₽')
print('------------------')
