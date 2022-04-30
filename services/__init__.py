from typing import Callable

from .data_extractors import *

SERVICES = []

for value in globals().values():
    if callable(value) and value not in SERVICES:
        SERVICES.append(value)
