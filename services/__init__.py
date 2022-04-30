from .data_extractors import *


SERVICES = []
VALUES = list(globals().values())


for value in VALUES:
    if callable(value) and \
        value not in SERVICES and \
            value.__module__.startswith('services.'):
        SERVICES.append(value)
