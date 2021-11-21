# coding: utf-8
from typing import Any, Dict

from . import forms
from .utils.generic_utils import load_data


def answer_form(
    path: str,
    browser: bool = False,
    secrets_dict: Dict[str, str] = {},
    verbose: bool = True,
    **kwargs
) -> None:
    """Answer Form Using Respective Form Model.

    Args:
        path (str)                              : [description].
        browser (bool, optional)                : [description]. Defaults to ``False``.
        secrets_dict (Dict[str, str], optional) : [description]. Defaults to ``{}``.
        verbose (bool, optional)                : [description]. Defaults to ``True``.
    """
    data: Dict[str, Any] = load_data(path)
    form: str = data.get("form")
    if form is None:
        form = forms.url2form(url=data.get("url"))
    model = forms.get(
        identifier=form, path=path, secrets_dict=secrets_dict, verbose=verbose, **kwargs
    )
    model.run(browser=browser)
