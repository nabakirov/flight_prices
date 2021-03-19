

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
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')
DEBUG = os.getenv('DEBUG')
PORT = os.getenv('PORT')

