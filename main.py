import json
from TinkofApiWrapper import TinkoffApiWrapper
from TinkofApiWrapper import AccountType
from TinkoffTransaction import TinkoffTransaction
from TransactionsProcessor import TransactionsProcessor

# read token from config
token = ''
with open('settings.json') as f:
    data = json.load(f)
    token = data['tinkoff_open_api_key']

# initialize api
tinkoff_api = TinkoffApiWrapper(token)


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
    print('-'*50)

    print(f'Overall dividend received on {account_name} account:')
    print(f'{dividend_received_usd:.1f} $')
    print(f'{dividend_received_rub:.1f} ₽')
    print('-'*50)

    print(f'Overall broker commission payed on {account_name} account:')
    print(f'{broker_commission_usd:.1f} $')
    print(f'{broker_commission_rub:.1f} ₽')
    print('-' * 50)

    print(f'Overall service commission payed on {account_name} account:')
    print(f'{service_commission:.1f} ₽')
    print('-' * 50)


print_transaction_report(AccountType.broker)
print_transaction_report(AccountType.iis)

