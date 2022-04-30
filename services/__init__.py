from .data_extractors import *

SERVICES = []

values = list(globals().values())

for value in values:
    if callable(value) and value not in SERVICES and value.__module__.startswith('services'):
        SERVICES.append(value)
