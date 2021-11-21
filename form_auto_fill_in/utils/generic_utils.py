# coding: utf-8
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

from ._colorings import _toCOLOR_create, toBLUE, toGREEN, toRED
from ._data import EXAMPLE_JSON_BASE_URL, EXAMPLE_JSON_DATA


def handleKeyError(lst, **kwargs):
    """Check whether all ``kwargs.values()`` in the ``lst``.

    Args:
        lst (list) : candidates.
        kwargs     : ``key`` is the varname that is easy to understand when an error occurs

    Examples:
        >>> from form_auto_fill_in.utils import handleKeyError
        >>> handleKeyError(lst=range(3), val=1)
        >>> handleKeyError(lst=range(3), val=100)
        KeyError: Please choose the argment val from ['0', '1', '2']. you chose 100
        >>> handleKeyError(lst=range(3), val1=1, val2=2)
        >>> handleKeyError(lst=range(3), val1=1, val2=100)
        KeyError: Please choose the argment val2 from ['0', '1', '2']. you chose 100

    Raise:
        KeyError: If ``kwargs.values()`` not in the ``lst``
    """
    for k, v in kwargs.items():
        if v not in lst:
            lst = ", ".join([f"'{toGREEN(e)}'" for e in lst])
            raise KeyError(
                f"Please choose the argment {toBLUE(k)} from [{lst}]. you chose {toRED(v)}"
            )


def load_data(path: Union[str, Path]) -> Dict[str, Any]:
    """Load data from JSON file at ``path``

    Args:
        path (str) : Path to json file.

    Returns:
        Dict[str,Any]: Loaded Data
    """
    if isinstance(path, str):
        with open(path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        with path.open(mode="r", encoding="utf-8") as f:
            data = json.load(f)
    return data


def try_wrapper(
    func: callable,
    *args,
    ret_: Optional[Any] = None,
    msg_: str = "",
    verbose_: bool = True,
    **kwargs,
) -> Any:
    """Wrap ``func(*args, **kwargs)`` with ``try`` and ``except`` blocks.

    Args:
        func (callable)                : functions.
        ret_ (Optional[Any], optional) : default ret val. Defaults to ``None``.
        msg_ (str, optional)           : message to print. Defaults to ``""``.
        verbose_ (bool, optional)      : Whether to print message or not. Defaults to ``True``.

    Examples:
        >>> from form_auto_fill_in.utils import try_wrapper
        >>> ret = try_wrapper(lambda x,y: x/y, 1, 2, msg_="divide")
        Succeeded to divide
        >>> ret
        0.5
        >>> ret = try_wrapper(lambda x,y: x/y, 1, 0, msg_="divide")
        [division by zero] Failed to divide
        >>> ret is None
        True
        >>> ret = try_wrapper(lambda x,y: x/y, 1, 0, ret_=1, msg_="divide")
        >>> ret is None
        False
        >>> ret
        1
    """
    try:
        ret_ = func(*args, **kwargs)
        prefix = toGREEN("Succeeded to ")
    except Exception as e:
        prefix = toRED(f"[{e.__class__.__name__}] Failed to ")
    if verbose_:
        print(prefix + msg_)
    return ret_


def openf(file_path: str, timeout: Optional[int] = None) -> None:
    """Open a file in Finder.

    Args:
        file_path (str)                   : Path to the file to be opened.
        timeout (Optional[int], optional) : Timeout. Defaults to ``None``.
    """
    subprocess.call(f"open '{file_path}'", timeout=timeout, shell=True)


def prepare_example_json(to: str, timeout: Optional[int] = None) -> None:
    for fn in EXAMPLE_JSON_DATA:
        subprocess.call(
            ["wget", EXAMPLE_JSON_BASE_URL + fn, "-O", os.path.join(to, fn)],
            timeout=timeout,
            shell=False,
        )
        print(f"Downloaded {toGREEN(fn)}")


def wrap_start(string: str, color: str = "GREEN", indent: int = 0) -> str:
    return " " * indent + _toCOLOR_create(color=color.upper())(f"<--- {string} ---")


def wrap_end(string: str, color: str = "GREEN", indent: int = 0) -> str:
    return " " * indent + _toCOLOR_create(color=color.upper())(f"--- {string} --->")
