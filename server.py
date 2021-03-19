from app import create_app
from settings import REDIS_HOST, REDIS_PORT, REDIS_DB, DEBUG, PORT


app = create_app({
    'REDIS': {
        'address': (REDIS_HOST, REDIS_PORT),
        'db': REDIS_DB
    }
})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
