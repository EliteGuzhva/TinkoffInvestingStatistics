"""
@brief ANSI escape sequences
"""
class AnsiSeq:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    PURPLE = '\033[95m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    END = '\033[0m'


"""
@brief Spacer
@param[in] n - number of lines for a spacer
"""
def empty_space(n: int = 1):
    for _ in range(n):
        print()


"""
@brief Separator
@param[in] symbol - character used to draw the separator
@param[in] length - number of characters to draw
"""
def separator(symbol: str = '-', length: int = 30):
    print(symbol*length)


"""
@brief Print bold title
@param[in] data - title to print
"""
def print_title(data: str, color: str = AnsiSeq.BLUE):
    print(AnsiSeq.BOLD + color + data + AnsiSeq.END)


"""
@brief Draw a card with a title and some content
@param[in] title - title of the card
@param[in] content - inner content (body)
"""
def draw_card(title: str, content: str, color: str = AnsiSeq.BLUE):
    empty_space()
    separator('=')
    print_title(title, color)
    separator()
    print(content)
    separator('=')
    empty_space()

