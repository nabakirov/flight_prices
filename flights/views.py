import json as _json

from sanic.blueprints import Blueprint
from sanic.response import json
from sanic.exceptions import InvalidUsage

from app import redis


blueprint = Blueprint('flights')


@blueprint.get('/flights')
async def get_flights(request):
    fly_from = request.args.get('fly_from')
    fly_to = request.args.get('fly_to')
    if not fly_to or not fly_from:
        raise InvalidUsage('query params fly_from and fly_to required')
    response = {}
    with await redis.conn as r:
        flight_keys = await r.get(f'{fly_from}-{fly_to}')
        if not flight_keys:
            return json({'message': 'waiting for pull'})
        flight_keys = _json.loads(flight_keys)
        for date, key in flight_keys.items():
            flight = _json.loads(await r.get(key))
            flight.pop('dump')
            if 'checked' in flight:
                flight['checked'].pop('dump')
            response[date] = flight
    return json(response)
