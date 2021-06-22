# coding: utf-8
import argparse
import os
import sys
from typing import Dict

from . import DATA_DIR
from .form import UtokyoHealthManagementReportForm
from .utils import KwargsParamProcessor

here = os.path.abspath(os.path.dirname(__file__))
REMOVE_KEYS = ["params", "quiet"]


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
    tmp_path = os.path.join(DATA_DIR, "UHMRF_tmp.json")
    old2new: Dict[str, str] = {
        "UHMRF_CAMPUS": os.getenv("UHMRF_CAMPUS", "1"),  # 1.Hongo Area Campuses
        "UHMRF_PLACE": os.getenv("UHMRF_PLACE", ""),
        "UTOKYO_ACCOUNT_MAIL_ADDRESS": os.getenv("UTOKYO_ACCOUNT_MAIL_ADDRESS", ""),
        "UTOKYO_ACCOUNT_PASSWORD": os.getenv("UTOKYO_ACCOUNT_PASSWORD", ""),
    }
    old2new.update({k: v for k, v in args.__dict__.items() if k not in REMOVE_KEYS})

    # Rewrite protected content
    with open(path, mode="r") as f:
        origin = "".join(f.readlines())
    for old, new in old2new.items():
        origin = origin.replace(f"<{old}>", new)
    with open(tmp_path, mode="w") as f:
        f.write(origin)

    model = UtokyoHealthManagementReportForm(path=tmp_path, verbose=not args.quiet)
    model.run()

    os.remove(tmp_path)
