from typing import Optional
from tui.utils import *

class Option:
    def __init__(self, v: str = "",
                 d: str = "",
                 c = None):
        self.value = v
        self.description = d
        self.callback = c


class OptionWidget:
    def __init__(self):
        self._title: Optional[str] = None
        self._quit_message: str = "Quitting..."

        # TODO: use typing
        self._options: list = []

    def add_option(self, value: str, description: str,
                   callback):
        option = Option(value, description, callback)
        self._options.append(option)

    def add_option_quit(self, message: str = None):
        if message:
            self._quit_message = message

        option = Option("q", "quit", self._quit)
        self._options.append(option)

    def set_title(self, title: str):
        self._title = title

    def print_help(self):
        empty_space()

        if self._title:
            print_title(self._title)

        for option in self._options:
            print("[" + option.value + "] " + option.description)

        empty_space()

    def run(self) -> bool:
        inp = input("> ")

        did_select: bool = False
        res: bool = True

        for option in self._options:
            if inp == option.value:
                did_select = True
                res = option.callback()

        if did_select:
            return res
        else:
            self._print_invalid_option_message()
            return True


    def _print_invalid_option_message(self):
        empty_space()
        print("Invalid option. Try again.")
        empty_space()

    def _quit(self) -> bool:
        empty_space()
        print(self._quit_message)
        empty_space()

        return False
