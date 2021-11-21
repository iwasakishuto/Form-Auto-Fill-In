# coding: utf-8
import os
from typing import Callable, Dict, Tuple

__all__ = [
    "toACCENT",
    "toBLACK",
    "toRED",
    "toGREEN",
    "toYELLOW",
    "toBLUE",
    "toMAGENTA",
    "toCYAN",
    "toWHITE",
    "toDEFAULT",
    "toGRAY",
    "toBRIGHT_RED",
    "toBRIGHT_GREEN",
    "toBRIGHT_YELLOW",
    "toBRIGHT_BLUE",
    "toBRIGHT_MAGENTA",
    "toBRIGHT_CYAN",
    "toBRIGHT_WHITE",
    "check_all_toCOLOR",
]


def _enable_vts() -> bool:
    """Enable Virtual Terminal Sequences (ANSI escape sequences) in Windows10."""
    INVALID_HANDLE_VALUE = -1
    # STD_INPUT_HANDLE     = -10
    STD_OUTPUT_HANDLE = -11
    # STD_ERROR_HANDLE     = -12
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    # ENABLE_LVB_GRID_WORLDWIDE = 0x0010
    try:
        from ctypes import byref, windll, wintypes
        from functools import reduce

        hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        if hOut == INVALID_HANDLE_VALUE:
            return False
        dwMode = wintypes.DWORD()
        if windll.kernel32.GetConsoleMode(hOut, byref(dwMode)) == 0:
            return False
        dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING  # ENABLE_LVB_GRID_WORLDWIDE
        if windll.kernel32.SetConsoleMode(hOut, dwMode) == 0:
            return False
    except:
        return False
    return True


try:
    __WINDOWS_VTS_SETUP__
except NameError:
    if os.name == "nt":
        __WINDOWS_VTS_SETUP__ = _enable_vts()
    else:
        __WINDOWS_VTS_SETUP__ = True

SUPPORTED_COLORINGS: Dict[str, Tuple[str, str]] = {
    "ACCENT": ("\x1b[01m", "\x1b[01m"),
    "BLACK": ("\x1b[30m", "\x1b[40m"),
    "RED": ("\x1b[31m", "\x1b[41m"),
    "GREEN": ("\x1b[32m", "\x1b[42m"),
    "YELLOW": ("\x1b[33m", "\x1b[43m"),
    "BLUE": ("\x1b[34m", "\x1b[44m"),
    "MAGENTA": ("\x1b[35m", "\x1b[45m"),
    "CYAN": ("\x1b[36m", "\x1b[46m"),
    "WHITE": ("\x1b[37m", "\x1b[47m"),
    "DEFAULT": ("\x1b[39m", "\x1b[49m"),
    "GRAY": ("\x1b[90m", "\x1b[100m"),
    "BRIGHT_RED": ("\x1b[91m", "\x1b[101m"),
    "BRIGHT_GREEN": ("\x1b[92m", "\x1b[102m"),
    "BRIGHT_YELLOW": ("\x1b[93m", "\x1b[103m"),
    "BRIGHT_BLUE": ("\x1b[94m", "\x1b[104m"),
    "BRIGHT_MAGENTA": ("\x1b[95m", "\x1b[105m"),
    "BRIGHT_CYAN": ("\x1b[96m", "\x1b[106m"),
    "BRIGHT_WHITE": ("\x1b[97m", "\x1b[107m"),
    # "END"           : ('\x1b[0m',  '\x1b[0m'),
}


def _toCOLOR_create(color: str = "") -> Callable[[str, bool], str]:
    color = color.upper()
    if __WINDOWS_VTS_SETUP__ and (color in SUPPORTED_COLORINGS.keys()):
        charcode = SUPPORTED_COLORINGS[color]
        func = lambda x, is_bg=False: f"{charcode[is_bg]}{str(x)}\x1b[0m"
        func.__doc__ = f"""Convert the output color to {color}

        Args:
            x (str)      : string
            is_bg (bool) : Whether to change the background color or not.

        Examples:
            >>> from pycharmers.utils import to{color}
            >>> print(to{color}("hoge"), is_bg=False)
            {func('hoge', is_bg=False)}
            >>> print(to{color}("hoge"), is_bg=True)
            {func('hoge', is_bg=True)}
        """
    else:
        func = lambda x, is_bg=False: str(x)
        func.__doc__ = "Convert to string."
    return func


toACCENT = _toCOLOR_create(color="ACCENT")
toBLACK = _toCOLOR_create(color="BLACK")
toRED = _toCOLOR_create(color="RED")
toGREEN = _toCOLOR_create(color="GREEN")
toYELLOW = _toCOLOR_create(color="YELLOW")
toBLUE = _toCOLOR_create(color="BLUE")
toMAGENTA = _toCOLOR_create(color="MAGENTA")
toCYAN = _toCOLOR_create(color="CYAN")
toWHITE = _toCOLOR_create(color="WHITE")
toDEFAULT = _toCOLOR_create(color="DEFAULT")
toGRAY = _toCOLOR_create(color="GRAY")
toBRIGHT_RED = _toCOLOR_create(color="BRIGHT_RED")
toBRIGHT_GREEN = _toCOLOR_create(color="BRIGHT_GREEN")
toBRIGHT_YELLOW = _toCOLOR_create(color="BRIGHT_YELLOW")
toBRIGHT_BLUE = _toCOLOR_create(color="BRIGHT_BLUE")
toBRIGHT_MAGENTA = _toCOLOR_create(color="BRIGHT_MAGENTA")
toBRIGHT_CYAN = _toCOLOR_create(color="BRIGHT_CYAN")
toBRIGHT_WHITE = _toCOLOR_create(color="BRIGHT_WHITE")


def check_all_toCOLOR(word="Hello, World!"):
    func_names = [f for f in __all__ if f.startswith("to")]
    digit = max([len(f) for f in func_names])
    for func_name in func_names:
        func = globals().get(func_name)
        print(f"{func_name:<{digit}}: {func(word, is_bg=False)}\t{func(word, is_bg=True)}")
