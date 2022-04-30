from typing import Callable

from .data_extractors import *

SERVICES = []

for name, variable in globals().items():
    if isinstance(variable, Callable) and variable not in SERVICES:
        SERVICES.append(variable)
