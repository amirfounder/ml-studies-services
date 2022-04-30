from .data_extractors import *

SERVICES = []

for name, variable in globals().items():
    if isinstance(variable, callable) and variable not in SERVICES:
        SERVICES.append(variable)
