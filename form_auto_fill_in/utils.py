# coding: utf-8
import argparse
import json
from typing import Any, Dict, Optional

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


def load_data(path: str) -> Dict[str, Any]:
    """Load data from JSON file at ``path``

    Args:
        path (str) : Path to json file.

    Returns:
        Dict[str,Any]: [description]
    """
    with open(path, mode="r", encoding="utf-8") as fr:
        data = json.load(fr)
    return data


def get_chrome_driver() -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)


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
        prefix = "Succeeded to "
    except Exception as e:
        prefix = f"[{e.__class__.__name__}] Failed to "
    if verbose_:
        print(prefix + msg_)
    return ret_


def try_find_element(
    driver: WebDriver, by: str, identifier: str, timeout: int = 3, verbose: bool = True
) -> None:
    """Find an element given a By strategy and locator.

    Args:
        driver (WebDriver) : Selenium WebDriver.
        by (str)           : Locator strategies. See `4. Locating Elements — Selenium Python Bindings 2 documentation <https://selenium-python.readthedocs.io/locating-elements.html>`_
        identifier (str)   : Identifier to find the element
        timeout (int)      : Number of seconds before timing out (default= ``3``)
        verbose (bool)     : Whether you want to print output or not. (default= ``True`` )

    Examples:
        >>> from form_auto_fill_in.utils import get_driver, try_find_element
        >>> with get_driver() as driver:
        ...     driver.get("https://www.google.com/")
        ...     e = try_find_element(driver=driver, by="tag name", identifier="img")
        Succeeded to locate element with tag name=img
    """
    return try_wrapper(
        func=WebDriverWait(driver=driver, timeout=timeout).until,
        msg_=f"locate element with {by}={identifier}",
        method=lambda x: x.find_element(by=by, value=identifier),
        verbose_=verbose,
    )


def try_find_element_send_keys(
    driver: WebDriver,
    by: Optional[str] = None,
    identifier: Optional[str] = None,
    values: tuple = (),
    target: Optional[WebElement] = None,
    timeout: int = 3,
    verbose: bool = True,
) -> None:
    """Find an element given a By strategy and locator, and Simulates typing into the element.

    Args:
        driver (WebDriver)  : Selenium WebDriver.
        by (str)            : Locator strategies. See `4. Locating Elements — Selenium Python Bindings 2 documentation <https://selenium-python.readthedocs.io/locating-elements.html>`_
        identifier (str)    : Identifier to find the element
        values (tuple)      : A string for typing, or setting form fields. For setting file inputs, this could be a local file path.
        target (WebElement) : Represents a DOM element. (If you already find element)
        timeout (int)       : Number of seconds before timing out (default= ``3``)
        verbose (bool)      : Whether you want to print output or not. (default= ``True`` )
    """
    if target is None:
        target = try_find_element(
            driver=driver,
            identifier=identifier,
            by=by,
            timeout=timeout,
            verbose=verbose,
        )
    if target is not None:
        try_wrapper(
            target.send_keys,
            *tuple(values),
            msg_=f"fill {values} in element with {by}={identifier}",
            verbose_=verbose,
        )


def try_find_element_click(
    driver: WebDriver,
    by: Optional[str] = None,
    identifier: Optional[str] = None,
    target: Optional[WebElement] = None,
    timeout: int = 3,
    verbose: bool = True,
) -> None:
    """Find an element given a By strategy and locator, and Clicks the element.

    Args:
        driver (WebDriver)  : Selenium WebDriver.
        by (str)            : Locator strategies. See `4. Locating Elements — Selenium Python Bindings 2 documentation <https://selenium-python.readthedocs.io/locating-elements.html>`_
        identifier (str)    : Identifier to find the element
        target (WebElement) : Represents a DOM element. (If you already find element)
        timeout (int)       : Number of seconds before timing out (default= ``3``)
        verbose (bool)      : Whether you want to print output or not. (default= ``True`` )
    """
    if target is None:
        target = try_find_element(
            driver=driver,
            identifier=identifier,
            by=by,
            timeout=timeout,
            verbose=verbose,
        )
    if target is not None:

        def element_click(driver, target):
            try:
                driver.execute_script("arguments[0].click();", target)
            except StaleElementReferenceException:
                target.click()

        try_wrapper(
            func=element_click,
            msg_=f"click the element with {by}={identifier}",
            verbose_=verbose,
            driver=driver,
            target=target,
        )


class KwargsParamProcessor(argparse.Action):
    """Set a new argument.

    Examples:
        >>> import argparse
        >>> from form_auto_fill_in.utils import KwargsParamProcessor
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument("--kwargs", action=KwargsParamProcessor)
        >>> args = parser.parse_args(args=["--kwargs", "foo=a", "--kwargs", "bar=b"])
        >>> (args.kwargs, args.foo, args.bar)
        (None, 'a', 'b')

    Note:
        If you run from the command line, execute as follows::

        $ python app.py --kwargs foo=a --kwargs bar=b
    """

    def __call__(self, parser, namespace, values, option_strings=None):
        k, v = values.split("=")
        setattr(namespace, k, v)
