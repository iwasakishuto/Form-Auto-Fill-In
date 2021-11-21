# coding: utf-8
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List

from ..utils._colorings import toBLUE, toGREEN
from ..utils._path import FORM_AUTO_FILL_IN_DIR
from ..utils.generic_utils import load_data, openf


def show_forms(argv: list = sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Show All Forms Data",
        add_help=True,
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Whether you want to open the target directory.",
    )
    args = parser.parse_args(argv)

    print(f"Show ALL JSON files at {toGREEN(FORM_AUTO_FILL_IN_DIR)}")
    p = Path(FORM_AUTO_FILL_IN_DIR)
    for fp in p.glob("**/*.json"):
        data = load_data(fp)
        print(f"{toBLUE(fp.name)} : {data.get('name', 'NO NAME')}")

    if args.open:
        openf(FORM_AUTO_FILL_IN_DIR)
