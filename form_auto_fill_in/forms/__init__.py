# coding: utf-8
import re
from typing import Union

from ..utils.generic_utils import handleKeyError
from . import base, google, office
from .base import BaseForm
from .google import GoogleForm
from .office import OfficeForm

__all__ = ["GoogleForm", "OfficeForm"]

domain2form = {"forms.gle": "google", "forms.office.com": "office"}


def url2form(url: str) -> str:
    """Estimate the Appropriate Form Model for the URL

    Args:
        url (str) : Form URL.

    Raises:
        ValueError: When ``url`` is not a valid URL.

    Returns:
        str: An identifier for the Form Model.
    """
    match: Union[re.Match, type(None)] = re.match(pattern=r"https?://(.+?)/", string=url)
    if match is None:
        raise ValueError(f"It doesn't seem to be a valid url, got url='{url}'")
    domain = match.group(1)
    handleKeyError(lst=domain2form.keys(), domain=domain)
    return domain2form[domain]


def get(identifier: Union[str, BaseForm], *args, **kwargs) -> BaseForm:
    """Retrieves a Forms instance.

    Args:
        identifier (Union[str, BaseForm]) : An identifier for the Form Model.

    Returns:
        BaseForm: A target Form Model instance.
    """
    if isinstance(identifier, str):
        handleKeyError(lst=all.keys(), identifier=identifier)
        instance = all[identifier](*args, **kwargs)
    else:
        instance = identifier
    return instance


all = {"google": GoogleForm, "office": OfficeForm}
