class TinkoffTransaction(object):

    def __str__(self):
        print('FIGI:', self.figi)
        print('Date:', self.date)
        print('Type:', self.operation_type)
        print('Status:', self.status)
        print('Currency:', self.currency)
        if self.commission is not None:
            print('Commission:', self.commission.value, self.commission.currency)
        print('Payment:', round(self.payment, 2))
        return ''

    def __init__(self, transaction):
        self.date = None
        self.operation_type = None
        self.status = None
        self.currency = None
        self.commission = None
        self.figi = None
        self.payment = None
        self.__process_transaction(transaction)

    def __process_transaction(self, transaction):
        self.date = transaction.date
        self.operation_type = transaction.operation_type
        self.status = transaction.status
        self.currency = transaction.currency
        self.commission = transaction.commission
        self.figi = transaction.figi
        if transaction.trades is None:
            self.payment = transaction.payment
        else:
            payment = 0.0
            for trade in transaction.trades:
                price = trade.price
                quantity = trade.quantity
                if price is not None and quantity is not None:
                    payment += price * quantity
            self.payment = payment