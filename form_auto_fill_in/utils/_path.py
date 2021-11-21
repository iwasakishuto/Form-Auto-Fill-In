# coding: utf-8
import os
from pathlib import Path

from ._colorings import toBLUE
from .generic_utils import prepare_example_json

__all__ = ["UTILS_DIR", "MODULE_DIR", "FORM_AUTO_FILL_IN_DIR"]

UTILS_DIR: str = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR: str = os.path.dirname(UTILS_DIR)

FORM_AUTO_FILL_IN_DIR: str = os.path.join(os.path.expanduser("~"), ".FormAutoFillIn")
# Check whether uid/gid has the write access to DATADIR_BASE
if os.path.exists(FORM_AUTO_FILL_IN_DIR) and not os.access(FORM_AUTO_FILL_IN_DIR, os.W_OK):
    FORM_AUTO_FILL_IN_DIR = os.path.join("/tmp", ".FormAutoFillIn")

if not os.path.exists(FORM_AUTO_FILL_IN_DIR):
    os.mkdir(FORM_AUTO_FILL_IN_DIR)
    print(f"{toBLUE(FORM_AUTO_FILL_IN_DIR)} is created. Downloaded data will be stored here.")
    prepare_example_json(to=FORM_AUTO_FILL_IN_DIR)


def canonicalize_path(path: str) -> str:
    if not os.path.exists(path) and path in os.listdir(FORM_AUTO_FILL_IN_DIR):
        path = os.path.join(FORM_AUTO_FILL_IN_DIR, path)
    return path
