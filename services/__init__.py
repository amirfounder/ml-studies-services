from typing import Callable

from .data_extractors import *

SERVICES = []

values = globals().values()

for value in values:
    if callable(value) and value not in SERVICES:
        SERVICES.append(value)
