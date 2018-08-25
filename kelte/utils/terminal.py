from colorama import Fore, Style
import typing


def blue(msg: typing.Any):
    msg = Fore.BLUE + str(msg) + Style.RESET_ALL
    return msg


def green(msg: typing.Any):
    msg = Fore.GREEN + str(msg) + Style.RESET_ALL
    return msg


def magenta(msg: typing.Any):
    msg = Fore.MAGENTA + str(msg) + Style.RESET_ALL
    return msg


def red(msg: typing.Any):
    msg = Fore.RED + str(msg) + Style.RESET_ALL
    return msg


def yellow(msg: typing.Any):
    msg = Fore.YELLOW + str(msg) + Style.RESET_ALL
    return msg


def echo(*messages, verbose=None, debug=None, end=None, flush=None):
    verbose = True if verbose is None else verbose
    msg = ' '.join(str(m) for m in messages)
    if verbose or debug:
        print(msg, end=end, flush=flush)
