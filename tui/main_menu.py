from typing import Optional
from TinkofApiWrapper import TinkoffApiWrapper
from TinkofApiWrapper import AccountType
from TinkoffTransaction import TinkoffTransaction
from TransactionsProcessor import TransactionsProcessor

from tui.utils import *
from tui.option import OptionWidget


class MainMenu:
    def __init__(self, token: str):
        self.api = TinkoffApiWrapper(token)
        self.tp: Optional[TransactionsProcessor] = None


        self._accounts = OptionWidget()
        self._accounts.set_title("Select account:")
        self._accounts.add_option("1", "broker",
                                  self._select_broker)
        self._accounts.add_option("2", "iis",
                                  self._select_iis)
        self._accounts.add_option_quit()


        self._actions = OptionWidget()
        self._actions.set_title("Select action:")
        self._actions.add_option("t", "tax", self._show_tax)
        self._actions.add_option("d", "dividend", self._show_dividend)
        self._actions.add_option("bc", "broker commission",
                                 self._show_broker_commission)
        self._actions.add_option("sc", "service commission",
                                 self._show_service_commission)
        self._actions.add_option("a", "all statistics",
                                 self._show_all_statistics)
        self._actions.add_option("c", "change accout",
                                 self._show_account_selection)
        self._actions.add_option("h", "show available actions",
                                 self._show_help)
        self._actions.add_option_quit()

    def run(self):
        self._choose_account_type()

    def _choose_account_type(self):
        self._accounts.print_help()

        should_continue: bool = self._accounts.run()

        if not should_continue:
            return

        self._choose_account_type()

    def _init_processor(self, account_type: AccountType):
        transactions = self.api.get_transactions(account_type)
        transactions = [TinkoffTransaction(tr) for tr in transactions]

        self.tp = TransactionsProcessor(transactions)

        self._info_options(show_info = True)

    def _info_options(self, show_info: bool = False):
        if show_info:
            self._actions.print_help()

        should_continue: bool = self._actions.run()
        if not should_continue:
            return

        self._info_options()

    def _select_broker(self) -> bool:
        self._init_processor(AccountType.broker)

        return False

    def _select_iis(self) -> bool:
        self._init_processor(AccountType.iis)

        return False

    def _show_tax(self) -> bool:
        overall_tax_payed_usd = self.tp.get_overall_tax_payed_usd()
        overall_tax_payed_rub = self.tp.get_overall_tax_payed_rub()

        self._print_info("Tax",
                         overall_tax_payed_usd,
                         overall_tax_payed_rub,
                         AnsiSeq.RED)

        return True

    def _show_dividend(self) -> bool:
        dividend_received_usd = self.tp.get_overall_dividend_received_usd()
        dividend_received_rub = self.tp.get_overall_dividend_received_rub()

        self._print_info("Dividend",
                         dividend_received_usd,
                         dividend_received_rub,
                         AnsiSeq.GREEN)

        return True

    def _show_broker_commission(self) -> bool:
        broker_commission_usd = self.tp.get_overall_commision_payed_usd()
        broker_commission_rub = self.tp.get_overall_commision_payed_rub()

        self._print_info("Broker commission",
                         broker_commission_usd,
                         broker_commission_rub,
                         AnsiSeq.YELLOW)

        return True

    def _show_service_commission(self) -> bool:
        service_commission = self.tp.get_service_commission_payed()

        self._print_info("Service commission",
                         0,
                         service_commission,
                         AnsiSeq.PURPLE)

        return True

    def _show_all_statistics(self) -> bool:
        draw_card("All statistics", "Not implemented yet...",
                  AnsiSeq.DARKCYAN)

        return True

    def _show_account_selection(self) -> bool:
        self._choose_account_type()

        return False

    def _show_help(self) -> bool:
        self._actions.print_help()

        return True

    @staticmethod
    def _print_info(label: str, usd: float, rub: float,
                    color: str = AnsiSeq.BLUE):
        content = f'{usd:.2f} $\n{rub:.2f} ₽'

        draw_card(label, content, color)

