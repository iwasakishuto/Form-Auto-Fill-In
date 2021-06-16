# coding: utf-8
import os

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(MODULE_DIR, "data")

from . import form, utils
from .__meta__ import *
