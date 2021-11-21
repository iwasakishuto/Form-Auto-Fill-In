# coding: utf-8
"""Answering Form using CLI.

.. code-block:: shell
    $ poetry run answer-form ./.github/workflows-json/UHMRF.json \\
                             --secret UHMRF \\
                             -P "UHMRF_PLACE=ABC" \\
                             -P "UTOKYO_ACCOUNT_MAIL_ADDRESS=XXXXXXXXXX@utac.u-tokyo.ac.jp" \\
                             -P "UTOKYO_ACCOUNT_PASSWORD=PASSWORD"
"""
import argparse
import os
import sys
from typing import Dict, List

from ..main import answer_form
from ..utils._path import FORM_AUTO_FILL_IN_DIR
from ..utils._secrets import SECRETS
from ..utils.argparse_utils import KwargsParamProcessor

ARGUMENT_KEYS: List[str] = [
    "path",
    "quiet",
    "browser",
    "secret",
    "params",
]


def answer_form_cli(argv: list = sys.argv[1:]):
    """Answering Form using CLI.

    Args:
        path (str)               : Path to the form data json.
        quiet (bool, optional)   : Whether you want to be quiet or not. Defaults to ``False``.
        browser (bool, optional) : Whether you want to run Chrome with GUI browser. Defaults to ``False``.
        secret (str, optional)   : An identifier for the name of the ``secret_dict``.
        params (dict, optional)  : Key and value combination for Github Secrets. You can specify by ``-P username=USERNAME``, ``-P password=PASSWORD``, etc.

    Examples:
        $ poetry run answer-form ./.github/workflows-json/UHMRF.json \\
                                 --secret UHMRF \\
                                 -P "UHMRF_PLACE=ABC" \\
                                 -P UTOKYO_ACCOUNT_MAIL_ADDRESS="XXXXXXXXXX@utac.u-tokyo.ac.jp" \\
                                 -P UTOKYO_ACCOUNT_PASSWORD="PASSWORD"
    """
    parser = argparse.ArgumentParser(
        description="Auto fill in form about 'UTokyo Health Management Report Form'",
        add_help=True,
    )
    parser.add_argument("path", type=str, help="Path to the form data json")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Whether you want to be quiet or not. Defaults to False",
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Whether you want to run Chrome with GUI browser. Defaults to False",
    )
    parser.add_argument(
        "--secret",
        type=str,
        choices=list(SECRETS.keys()),
        help="An identifier for the name of the secret_dict.",
    )
    parser.add_argument(
        "-P",
        "--secrets",
        action=KwargsParamProcessor,
        help="Key and value combination for Github Secrets. You can specify by -P username=USERNAME -P password=PASSWORD",
    )

    args = parser.parse_args(argv)

    path = args.path
    verbose = not args.quiet
    browser = args.browser

    secrets_dict = SECRETS.get(args.secret, {})
    secrets_dict.update({f"<{k}>": v for k, v in args.__dict__.items() if k not in ARGUMENT_KEYS})

    answer_form(path=path, browser=browser, secrets_dict=secrets_dict, verbose=verbose)
