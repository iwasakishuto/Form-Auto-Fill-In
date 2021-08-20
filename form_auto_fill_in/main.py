# coding: utf-8
import argparse
import os
import sys
from typing import Dict

from . import DATA_DIR
from .form import UtokyoHealthManagementReportForm
from .utils import KwargsParamProcessor

here = os.path.abspath(os.path.dirname(__file__))
ARGUMENT_KEYS = ["params", "quiet"]


def UHMRF(argv: list = sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="Answer UHMRF",
        description="Auto fill in form about 'UTokyo Health Management Report Form'",
        add_help=True,
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Whether you want to be quiet or not. (default=False)",
    )
    parser.add_argument(
        "-P",
        "--params",
        action=KwargsParamProcessor,
        help="Specify the kwargs. You can specify by -P username=USERNAME -P password=PASSWORD",
    )
    args = parser.parse_args(argv)

    path = os.path.join(DATA_DIR, "UHMRF.json")
    secrets_dict: Dict[str, str] = {
        "<UHMRF_PLACE>": os.getenv("UHMRF_PLACE", ""),
        "<UTOKYO_ACCOUNT_MAIL_ADDRESS>": os.getenv("UTOKYO_ACCOUNT_MAIL_ADDRESS", ""),
        "<UTOKYO_ACCOUNT_PASSWORD>": os.getenv("UTOKYO_ACCOUNT_PASSWORD", ""),
    }
    secrets_dict.update(
        {k: v for k, v in args.__dict__.items() if k not in ARGUMENT_KEYS}
    )

    model = UtokyoHealthManagementReportForm(
        path=path, secrets_dict=secrets_dict, verbose=not args.quiet
    )
    model.run()
