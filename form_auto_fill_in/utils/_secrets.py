# coding: utf-8
import os
from typing import Dict

__all__ = ["SECRETS"]

SECRETS: Dict[str, Dict[str, str]] = {
    "UHMRF": {
        "<UHMRF_PLACE>": os.getenv("UHMRF_PLACE", ""),
        "<UTOKYO_ACCOUNT_MAIL_ADDRESS>": os.getenv("UTOKYO_ACCOUNT_MAIL_ADDRESS", ""),
        "<UTOKYO_ACCOUNT_PASSWORD>": os.getenv("UTOKYO_ACCOUNT_PASSWORD", ""),
    }
}
