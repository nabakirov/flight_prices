import os

DIRECTIONS = (
    ('ALA', 'TSE'),
    ('TSE', 'ALA'),
    ('ALA', 'MOW'),
    ('MOW', 'ALA'),
    ('ALA', 'CIT'),
    ('CIT', 'ALA'),
    ('TSE', 'MOW'),
    ('MOW', 'TSE'),
    ('TSE', 'LED'),
    ('LED', 'TSE'),
)



REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_DB = int(os.getenv('REDIS_DB'))
DEBUG = os.getenv('DEBUG')
if DEBUG:
    if DEBUG in {'True', 'true'}:
        DEBUG = True
    else:
        DEBUG = False
else:
    DEBUG = False
PORT = int(os.getenv('PORT'))

